"""Local NotebookLM driver for a Claim Registry quest.

The driver opens its own browser window, signed in with its own profile, and turns every notebook
copy into a lane:

  queue/Qnnnn.json  ->  lane types the question  ->  waits for the finished answer  ->  Qnnnn-A01.json

It writes answers straight to disk. That avoids folder-permission prompts, background-tab slowdowns
and lost tabs: everything that went wrong in the 2026-10-30 browser-extension run.

    python -m claimreg.notebooklm.driver login quest-driver.json   # once: sign in to Google, then close the window
    python -m claimreg.notebooklm.driver run   quest-driver.json   # leave it running during the quest
    python -m claimreg.notebooklm.driver check quest-driver.json   # print the config it will use

quest-driver.json:

  {
    "run_id": "MY-RUN-2026-11-01",
    "notebooks": {"primary": "https://notebook.google.com/notebook/<id>", "clone-1": "..."},
    "answers_dir": "answers",              # answer files land here; questions go in answers/queue/
    "profile_dir": ".notebooklm-profile",  # the driver's own browser profile (keep it private)
    "channel": "chrome",                   # use installed Google Chrome; "" for Playwright's Chromium
    "max_backlog": 12,                     # hold new questions while this many answers await assessment
    "assessed_file": "artifacts/quest-state/assessed-qids.json"   # assessed QIDs + times (optional)
  }

On its first run for a quest the driver writes <answers_dir>/quest-clock.json (driver_started), the
scorecard's default go-ahead time. Add "go_ahead": "<ISO time>" to it to set the go-ahead exactly.

Needs Python 3.10+ and Playwright: `pip install playwright` (and `playwright install chromium` only
if you are not using installed Chrome). The browser logic itself is lane-runner.js, unchanged.
"""
import json, os, shutil, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER_JS = HERE / "lane-runner.js"
NO_THROTTLE = ["--disable-background-timer-throttling", "--disable-backgrounding-occluded-windows",
               "--disable-renderer-backgrounding", "--disable-blink-features=AutomationControlled",
               "--start-maximized"]


def sanitise_pushed(pushed, saved):
    """Keep only pushed-question entries that have an answer file on disk.

    A question that was pushed but then lost (page wedge, driver restart, dead lane) would otherwise be
    counted as outstanding forever: `pushed - saved` pins the backlog at its limit and the lanes idle.
    Unanswered questions still in flight are held by the lane runner's IndexedDB and are recovered from
    the chat on restart, so dropping their pushed entries loses nothing."""
    keep = set()
    saved = set(saved or ())
    for name in pushed or ():
        qid = str(name).split("-")[0].replace(".json", "")
        if qid in saved:
            keep.add(name)
    return keep


def restore_minimized_windows(log=None):
    """Best-effort on Windows: restore a minimized Chrome window whose title mentions Notebook.

    Chrome throttles hidden tabs to about one tick a minute, and when every tab is hidden the lane
    runner's cross-tab tick stops entirely, so a minimized quest window silently stalls the whole
    quest.  Playwright's persistent context also re-opens with the last window state, so a window
    minimized before a restart comes back minimized.  Returns the number of windows restored."""
    if os.name != "nt":
        return 0
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
    except Exception:  # noqa: BLE001 - non-Windows or a constrained interpreter: run without it
        return 0
    restored = []
    try:
        proc_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    except Exception:  # noqa: BLE001
        return 0

    def _callback(hwnd, _lparam):
        try:
            if user32.IsIconic(hwnd):
                n = user32.GetWindowTextLengthW(hwnd)
                if n:
                    buf = ctypes.create_unicode_buffer(n + 1)
                    user32.GetWindowTextW(hwnd, buf, n + 1)
                    title = buf.value
                    if "notebook" in title.lower():
                        user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                        restored.append(title)
        except Exception:  # noqa: BLE001
            pass
        return True

    try:
        user32.EnumWindows(proc_type(_callback), 0)
    except Exception:  # noqa: BLE001
        return 0
    if restored and log:
        log("restored minimized window(s): " + "; ".join(restored))
    return len(restored)


def load(cfg_path):
    cfg_path = Path(cfg_path).resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base = cfg_path.parent
    cfg["_answers"] = (base / cfg.get("answers_dir", "answers")).resolve()
    cfg["_queue"] = cfg["_answers"] / "queue"
    cfg["_profile"] = (base / cfg.get("profile_dir", ".notebooklm-profile")).resolve()
    cfg["_assessed"] = (base / cfg["assessed_file"]).resolve() if cfg.get("assessed_file") else None
    cfg["_lanes"] = {}
    for name, url in cfg["notebooks"].items():
        nb = url.rstrip("/").split("/notebook/")[-1].split("?")[0]
        cfg["_lanes"][nb] = name
    cfg["_queue"].mkdir(parents=True, exist_ok=True)
    return cfg


def find_chrome():
    for p in [os.environ.get("CHROME_PATH", ""),
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              shutil.which("google-chrome") or "", shutil.which("chrome") or ""]:
        if p and Path(p).exists():
            return p
    return None


def login(cfg):
    """Open a normal (not automated) Chrome window on the driver's own profile, for a one-time sign-in."""
    first = next(iter(cfg["notebooks"].values()))
    chrome = find_chrome()
    print("Sign in to the Google account that owns the notebooks, check that a notebook opens, then CLOSE the window.")
    if chrome:
        subprocess.run([chrome, "--user-data-dir=" + str(cfg["_profile"]), "--no-first-run", first])
    else:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(str(cfg["_profile"]), headless=False, args=NO_THROTTLE,
                                                       ignore_default_args=["--enable-automation"])
            ctx.pages[0].goto(first)
            input("Press Enter here after signing in... ")
            ctx.close()
    print("Profile saved at", cfg["_profile"])


class Driver:
    def __init__(self, cfg, headless=False, log=print):
        self.cfg, self.headless, self.log = cfg, headless, log
        self.pages = {}
        self.pushed = set()
        self.state_file = cfg["_answers"] / "driver-state.json"
        if self.state_file.exists():
            try:
                recorded = set(json.loads(self.state_file.read_text()).get("pushed", []))
            except Exception:  # noqa: BLE001 - a corrupt state file must not stop a quest
                recorded = set()
            saved = {f.name.split("-")[0] for f in cfg["_answers"].glob("Q*-A*.json")}
            self.pushed = sanitise_pushed(recorded, saved)
            dropped = len(recorded - self.pushed)
            if dropped:
                self.state_file.write_text(json.dumps({"pushed": sorted(self.pushed)}))
                log("driver: dropped %d lost question(s) from the backlog" % dropped)

    # ---- browser ----
    def start(self, p):
        kw = dict(headless=self.headless, args=NO_THROTTLE, ignore_default_args=["--enable-automation"],
                  bypass_csp=True, viewport=None)
        if self.cfg.get("channel", "chrome"):
            kw["channel"] = self.cfg.get("channel", "chrome")
        self.ctx = p.chromium.launch_persistent_context(str(self.cfg["_profile"]), **kw)
        for name, url in self.cfg["notebooks"].items():
            self.open_lane(name, url)
        restore_minimized_windows(self.log)

    def open_lane(self, name, url):
        page = self.ctx.pages[0] if (not self.pages and self.ctx.pages and self.ctx.pages[0].url in ("about:blank", "")) else self.ctx.new_page()
        page.goto(url, wait_until="domcontentloaded")
        self.pages[name] = page
        self.inject(name)

    def inject(self, name):
        page = self.pages[name]
        page.wait_for_selector('textarea[aria-label="Query box"]', timeout=120000)
        # The lane runner keeps its job queue and claims in IndexedDB 'crl' plus crl_* localStorage on
        # the notebook origin. That state is shared across quests on the same signed-in profile, and a
        # new quest restarts numbering at Q0001, so a stale claim for Q0001-A01 silently idles every
        # lane. Clear it whenever the run_id differs; keep it on a restart of the same quest so
        # CRL_recover() can re-read in-flight answers from the chat.
        page.evaluate(
            """async ([lanes, run]) => {
              let prev = null;
              try { prev = JSON.parse(localStorage.getItem('crl_run')); } catch (e) { prev = null; }
              if (prev !== run) {
                for (const k of Object.keys(localStorage)) if (k.startsWith('crl')) localStorage.removeItem(k);
                await new Promise(resolve => {
                  try {
                    const req = indexedDB.deleteDatabase('crl');
                    req.onsuccess = req.onerror = req.onblocked = () => resolve();
                  } catch (e) { resolve(); }
                  setTimeout(resolve, 3000);
                });
              }
              localStorage.setItem('crl_lanes', JSON.stringify(lanes));
              localStorage.setItem('crl_run', JSON.stringify(run));
            }""",
            [self.cfg["_lanes"], self.cfg.get("run_id", "UNSET")])
        page.evaluate(RUNNER_JS.read_text(encoding="utf-8"))
        rec = page.evaluate("() => window.CRL_recover ? window.CRL_recover() : ''")
        self.log("lane %s ready%s" % (name, (" - " + rec) if rec and "nothing" not in rec else ""))

    def any_page(self):
        return next(iter(self.pages.values()))

    def heal(self):
        for name, url in list(self.cfg["notebooks"].items()):
            page = self.pages.get(name)
            try:
                alive = page is not None and not page.is_closed() and page.evaluate("() => !!(window.CRL && window.CRL.version)")
            except Exception:
                alive = False
            if not alive:
                self.log("lane %s: reloading" % name)
                try:
                    if page is None or page.is_closed():
                        self.open_lane(name, url)
                    else:
                        page.reload(wait_until="domcontentloaded"); self.inject(name)
                except Exception as e:
                    self.log("lane %s: reload failed (%s); will retry" % (name, e))

    # ---- files ----
    def saved_qids(self):
        return {f.name.split("-")[0] for f in self.cfg["_answers"].glob("Q*-A*.json")}

    def assessed_qids(self):
        a = self.cfg["_assessed"]
        if not a or not a.exists():
            return None
        d = json.loads(a.read_text(encoding="utf-8"))
        return set(d if isinstance(d, list) else d.get("assessed", []))

    def harvest(self):
        pend = self.any_page().evaluate("() => { const o = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k && k.startsWith('crl_pend:')) o[k.slice(9)] = localStorage.getItem(k); } return o; }")
        for name, body in pend.items():
            target = self.cfg["_answers"] / name
            tmp = target.with_suffix(".tmp")
            tmp.write_text(body, encoding="utf-8"); os.replace(tmp, target)
            self.any_page().evaluate("(n) => { localStorage.removeItem('crl_pend:' + n); localStorage.setItem('crl_wrote:' + n, new Date().toISOString()); }", name)
            rec = json.loads(body)
            self.log("saved %s (%s, %ss, %d chars%s)" % (name, rec.get("lane"), rec.get("generation_seconds"), rec.get("answer_chars", 0),
                                                      ", TOOL OUTPUT" if rec.get("contains_tool_output") else ""))
        return len(pend)

    def feed(self):
        stop = (self.cfg["_queue"] / "STOP").exists()
        self.any_page().evaluate("(s) => s ? localStorage.setItem('crl_stop', 'true') : localStorage.removeItem('crl_stop')", stop)
        if stop:
            return "STOP"
        unclaimed = self.any_page().evaluate("async () => window.CRL_tx((jobs, claims) => jobs.filter(j => !claims[j.qid + '-' + (j.attempt || 'A01')]).length)")
        room = 2 * len(self.pages) - unclaimed
        assessed = self.assessed_qids()
        if assessed is not None:
            # Answers waiting for the Manager, plus questions already sent that will become answers.
            saved = self.saved_qids()
            outstanding = {n.split("-")[0].replace(".json", "") for n in self.pushed} - saved
            backlog = len(saved - assessed) + len(outstanding)
            limit = int(self.cfg.get("max_backlog", 12))
            if backlog >= limit:
                return "HOLD (backlog %d, limit %d)" % (backlog, limit)
            room = min(room, limit - backlog)
        if room <= 0:
            return "queue full"
        new = []
        for f in sorted(self.cfg["_queue"].glob("Q*.json")):
            if f.name in self.pushed:
                continue
            try:
                j = json.loads(f.read_text(encoding="utf-8-sig"))
            except Exception:
                continue
            if j.get("qid") and j.get("text"):
                new.append(j); self.pushed.add(f.name)
            if len(new) >= room:
                break
        if new:
            self.any_page().evaluate("(jobs) => window.CRL_push(jobs)", new)
            self.state_file.write_text(json.dumps({"pushed": sorted(self.pushed)}))
            return "pushed %d" % len(new)
        return "idle"

    def status(self, note):
        lanes = self.any_page().evaluate("(names) => names.map(n => [n, JSON.parse(localStorage.getItem('crl_lane:' + n) || '{}')])", list(self.cfg["notebooks"]))
        st = {"at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "feed": note, "saved_qids": len(self.saved_qids()),
              "lanes": {n: {"state": s.get("state"), "qid": s.get("qid"), "err": s.get("err")} for n, s in lanes}}
        (self.cfg["_answers"] / "driver-status.json").write_text(json.dumps(st, indent=1))
        return st

    def loop(self, max_seconds=None, poll=3.0):
        t0, last_print = time.time(), 0
        while max_seconds is None or time.time() - t0 < max_seconds:
            restore_minimized_windows(self.log)
            self.heal()
            self.harvest()
            note = self.feed()
            st = self.status(note)
            if time.time() - last_print > 30:
                busy = sum(1 for v in st["lanes"].values() if v["state"] not in ("FREE", None))
                self.log("%s | saved %d | lanes busy %d/%d | %s" % (st["at"][11:19], st["saved_qids"], busy, len(st["lanes"]), note))
                last_print = time.time()
            if note == "STOP" and all(v["state"] in ("FREE", None) for v in st["lanes"].values()):
                self.harvest(); self.log("STOP file present and all lanes idle: driver exiting."); return
            time.sleep(poll)


def stamp_clock(cfg):
    """Record when the driver first ran for this quest: the scorecard's default go-ahead time.
    Never overwritten by a restart. Put {"go_ahead": "<ISO time>"} in the file to set it exactly."""
    clock = cfg["_answers"] / "quest-clock.json"
    if not clock.exists():
        clock.write_text(json.dumps({"run_id": cfg.get("run_id", ""),
                                     "driver_started": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, indent=1))


def run(cfg, headless=False, max_seconds=None):
    from playwright.sync_api import sync_playwright
    stamp_clock(cfg)
    with sync_playwright() as p:
        d = Driver(cfg, headless=headless)
        d.start(p)
        try:
            d.loop(max_seconds=max_seconds, poll=float(cfg.get("poll_seconds", 3)))
        except KeyboardInterrupt:
            d.harvest(); print("stopped by Ctrl+C; answers saved so far are on disk.")
        finally:
            d.ctx.close()


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("login", "run", "check"):
        sys.exit(__doc__)
    c = load(sys.argv[2])
    if sys.argv[1] == "login":
        login(c)
    elif sys.argv[1] == "check":
        print(json.dumps({k: str(v) for k, v in c.items() if k.startswith("_")}, indent=1))
    else:
        run(c, headless="--headless" in sys.argv)

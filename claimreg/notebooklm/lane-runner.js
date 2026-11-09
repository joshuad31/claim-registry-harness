// Claim Registry - NotebookLM lane runner (v6).
//
// Paste this into each notebook tab (one tab per notebook copy). Every tab becomes a "lane":
// it takes the next question from the shared queue, types it into the chat box, waits for the
// finished answer card, and saves {query, answer, lane, times} as one JSON file per question.
// The six tabs coordinate through IndexedDB, which is shared and transactional across tabs of
// the same site, so no question is ever claimed twice.
//
// Questions come from <answers folder>/queue/Qnnnn.json files ({"qid","attempt","text"}), or
// from CRL_push([...]). Answers go to <answers folder>/Qnnnn-A01.json. If the browser has lost
// permission to the folder, answers wait in localStorage and CRL_dump() returns them, so the
// operator can collect them without asking the person for anything.
//
// Lessons built in (each one cost a live run):
//  * the chat box is textarea[aria-label="Query box"]; the first textarea on the page is the
//    "Discover sources" web-search box, which must never receive a question;
//  * localStorage is not consistent across tabs fast enough for claiming; IndexedDB is;
//  * one localStorage key per pending answer, so two tabs never overwrite each other;
//  * the collapsible "Thoughts" panel is page chrome, not part of the answer;
//  * after a browser restart, CRL_recover() re-reads answers that were already generated.
(() => {
if (window.CRL && window.CRL.timer) clearInterval(window.CRL.timer);
const LANES = window.CRL_LANES || JSON.parse(localStorage.getItem('crl_lanes') || '{}');
const nbId = (location.pathname.match(/notebook\/([0-9a-f-]+)/) || [])[1];
const lane = LANES[nbId] || ('nb-' + (nbId || 'unknown').slice(0, 8));
const LS = localStorage;
const jget = (k, d) => { try { const v = LS.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } };
const jset = (k, v) => LS.setItem(k, JSON.stringify(v));
const norm = s => (s || '').replace(/\s+/g, ' ').trim();
const now = () => new Date().toISOString();
const MAX_GEN_MS = 12 * 60 * 1000;
const open = () => new Promise((res, rej) => { const r = indexedDB.open('crl', 1); r.onupgradeneeded = () => r.result.createObjectStore('kv'); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
const idbGet = async k => { const db = await open(); return new Promise(res => { const t = db.transaction('kv').objectStore('kv').get(k); t.onsuccess = () => res(t.result); t.onerror = () => res(null); }); };
window.CRL_tx = async fn => { const db = await open(); return new Promise((res, rej) => { const t = db.transaction('kv', 'readwrite'); const s = t.objectStore('kv'); let out; const g1 = s.get('jobs'), g2 = s.get('claims'); let n = 0; const go = () => { if (++n < 2) return; const jobs = g1.result || [], claims = g2.result || {}; out = fn(jobs, claims); s.put(jobs, 'jobs'); s.put(claims, 'claims'); }; g1.onsuccess = go; g2.onsuccess = go; t.oncomplete = () => res(out); t.onerror = () => rej(t.error); }); };
window.CRL_push = newJobs => window.CRL_tx((jobs, claims) => { const have = new Set(jobs.map(j => j.qid + '-' + (j.attempt || 'A01'))); let added = 0; for (const j of newJobs) { const k = j.qid + '-' + (j.attempt || 'A01'); if (!have.has(k)) { jobs.push(j); have.add(k); added++; } } return { added, jobs: jobs.length, claimed: Object.keys(claims).length }; });
async function folder() { const d = await idbGet('inbox'); if (!d) return null; try { return (await d.queryPermission({ mode: 'readwrite' })) === 'granted' ? d : null; } catch (e) { return null; } }

const C = window.CRL = {
  lane, nbId, state: 'FREE', job: null, pairEl: null, lastLen: -1, stableTicks: 0, busy: false, log: [], version: 'v6',
  note(m) { this.log.push(now() + ' ' + m); if (this.log.length > 50) this.log.shift(); },
  pub(extra) { jset('crl_lane:' + lane, Object.assign({ state: this.state, qid: this.job && this.job.qid, ts: now(), url: location.href }, this.job ? { submitted_at: this.job.submitted_at } : {}, extra || {})); },
  pairs() { return [...document.querySelectorAll('.chat-message-pair')]; },
  userText(p) { const u = p.querySelector('.from-user-container'); return u ? u.innerText : ''; },
  modelMsg(p) { const ms = p.querySelectorAll('chat-message'); return ms.length > 1 ? ms[ms.length - 1] : null; },
  finished(p) { const m = this.modelMsg(p); return !!(m && m.querySelector('button[aria-label="Copy model response to clipboard"]')); },
  answerText(p) { const m = this.modelMsg(p); if (!m) return ''; const el = m.querySelector('.to-user-message-inner-content .message-text-content') || m.querySelector('.to-user-message-inner-content'); return el ? el.innerText.replace(/^\s*Thoughts\s*\n(?:[\s\S]*?\n)?\s*expand_(more|less)\s*\n/, '') : ''; },
  busyChat() { const ps = this.pairs(); if (!ps.length) return false; const p = ps[ps.length - 1]; return !this.modelMsg(p) || !this.finished(p); },
  findPair(q) { const key = norm(q).slice(0, 90); const ps = this.pairs(); for (let i = ps.length - 1; i >= 0; i--) if (norm(this.userText(ps[i])).startsWith(key)) return ps[i]; return null; },
  async pullFolder() {
    const dir = await folder(); if (!dir) return 0;
    let qd; try { qd = await dir.getDirectoryHandle('queue'); } catch (e) { return 0; }
    try { await qd.getFileHandle('STOP'); LS.setItem('crl_stop', 'true'); } catch (e) {}
    const jobs = [];
    for await (const [name, h] of qd.entries()) if (h.kind === 'file' && /^Q\d+(-A\d+)?\.json$/.test(name)) { try { const j = JSON.parse(await (await h.getFile()).text()); if (j.qid && j.text) jobs.push(j); } catch (e) {} }
    jobs.sort((a, b) => (a.qid + (a.attempt || '')) < (b.qid + (b.attempt || '')) ? -1 : 1);
    return jobs.length ? (await window.CRL_push(jobs)).added : 0;
  },
  async claim() {
    try { await this.pullFolder(); } catch (e) { this.note('pull ' + e.message); }
    return window.CRL_tx((jobs, claims) => { for (const j of jobs) { const k = j.qid + '-' + (j.attempt || 'A01'); if (claims[k] || (j.lane && j.lane !== lane)) continue; claims[k] = { lane, at: now() }; return Object.assign({}, j); } return null; });
  },
  async submit(job) {
    const ta = document.querySelector('textarea[aria-label="Query box"]');
    if (!ta) throw new Error('no chat query box');
    ta.focus(); ta.select(); document.execCommand('insertText', false, job.text);
    if (norm(ta.value) !== norm(job.text)) { Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(ta, job.text); ta.dispatchEvent(new Event('input', { bubbles: true })); }
    await new Promise(r => setTimeout(r, 500));
    const btn = ta.closest('form') && ta.closest('form').querySelector('button[aria-label="Submit"]');
    if (!btn) throw new Error('no submit button in chat form');
    if (btn.disabled) throw new Error('chat submit disabled');
    btn.click();
  },
  async writeOut(rec) { LS.setItem('crl_pend:' + rec.qid + '-' + rec.attempt + '.json', JSON.stringify(rec, null, 1)); await this.flush(); },
  async flush() {
    const keys = []; for (let i = 0; i < LS.length; i++) { const k = LS.key(i); if (k && k.startsWith('crl_pend:')) keys.push(k); }
    if (!keys.length) return 0; const dir = await folder(); if (!dir) return -1;
    let n = 0;
    for (const k of keys) { const body = LS.getItem(k); if (!body) continue; const name = k.slice(9); const fh = await dir.getFileHandle(name, { create: true }); const w = await fh.createWritable(); await w.write(body); await w.close(); LS.removeItem(k); LS.setItem('crl_wrote:' + name, now()); n++; }
    return n;
  },
  async tick() {
    if (this.busy) return; this.busy = true;
    try {
      if (this.state === 'FREE') {
        if (jget('crl_stop', false)) { this.pub({ stopped: true }); return; }
        if (this.busyChat()) { this.pub({ note: 'chat busy before claim' }); return; }
        const job = await this.claim(); if (!job) { this.pub(); return; }
        this.job = job; this.state = 'RESERVED'; this.pub();
        try { await this.submit(job); } catch (e) {
          this.note('submit error ' + e.message);
          await window.CRL_tx((jobs, claims) => { delete claims[job.qid + '-' + (job.attempt || 'A01')]; });
          this.job = null; this.state = 'FREE'; this.pub({ err: e.message }); return;
        }
        job.submitted_at = now(); job.submit_wall = Date.now(); this.state = 'SUBMITTING'; this.pub(); return;
      }
      if (this.state === 'SUBMITTING') {
        const p = this.findPair(this.job.text);
        if (p) { this.pairEl = p; this.state = 'GENERATING'; this.lastLen = -1; this.stableTicks = 0; this.pub(); }
        else if (Date.now() - this.job.submit_wall > 60000) { this.state = 'AMBIGUOUS'; this.pub({ err: 'query not visible 60 s after submit' }); }
        return;
      }
      if (this.state === 'GENERATING') {
        const p = this.pairEl && this.pairEl.isConnected ? this.pairEl : this.findPair(this.job.text);
        if (!p) { this.pub({ note: 'pair not found' }); return; }
        this.pairEl = p;
        const txt = this.answerText(p), done = this.finished(p);
        this.stableTicks = (done && txt.length === this.lastLen) ? this.stableTicks + 1 : 0; this.lastLen = txt.length;
        const timedOut = Date.now() - this.job.submit_wall > MAX_GEN_MS;
        if ((done && this.stableTicks >= 1) || timedOut) {
          const rec = { run_id: jget('crl_run', 'UNSET'), qid: this.job.qid, attempt: this.job.attempt || 'A01', lane, notebook_url: location.href.split('?')[0],
            query: this.job.text, query_seen_in_user_message: norm(this.userText(p)).startsWith(norm(this.job.text).slice(0, 90)),
            submitted_at: this.job.submitted_at, captured_at: now(), outcome: done ? (txt.trim() ? 'COMPLETE' : 'FAILED') : 'INCOMPLETE',
            generation_seconds: Math.round((Date.now() - this.job.submit_wall) / 1000),
            capture_method: 'lane-runner v6: rendered answer card innerText of the user message matching this query', answer_chars: txt.length, answer: txt };
          if (this.job.note) rec.note = this.job.note;
          // Gemini Notebook sometimes pastes its own code-execution "Tool response" blocks into the
          // answer card, presented as file text; some of that text does not match the real file.
          rec.contains_tool_output = /Tool response for|exit_code:|Tool call:default_api/.test(txt);
          // A card holding only unexecuted tool-call text has no answer at all.
          if (/^\s*Tool call:/.test(txt) && txt.length < 3000) rec.outcome = 'FAILED';
          // Off-target check: a long chat can make NotebookLM answer an earlier question instead.
          const wanted = (this.job.text.match(/[\w.@()\-]+\.(?:pdf\.)?(?:md|txt)/g) || []);
          rec.requested_sources = wanted;
          rec.answer_names_requested_source = !wanted.length || wanted.some(f => txt.includes(f) || txt.includes(f.replace(/\.pdf\.md$|\.md$/, '')));
          this.state = 'CAPTURING'; this.pub(); await this.writeOut(rec);
          this.job = null; this.pairEl = null; this.state = 'FREE'; this.pub({ last: rec.qid });
        } else this.pub({ chars: txt.length });
      }
    } catch (e) { this.note('tick ' + e.message); this.pub({ err: e.message }); }
    finally { this.busy = false; if (this.state === 'FREE') { try { await this.flush(); } catch (e) {} } }
  },
};
// After a browser restart: re-read answers this lane had already submitted but not saved.
window.CRL_recover = async () => {
  const { jobs, cl } = await window.CRL_tx((jobs, cl) => ({ jobs, cl }));
  const lost = Object.entries(cl).filter(([k, v]) => v.lane === lane && !LS.getItem('crl_wrote:' + k + '.json') && !LS.getItem('crl_pend:' + k + '.json'));
  if (!lost.length) return lane + ': nothing to recover';
  const [k, v] = lost[0]; const job = Object.assign({}, jobs.find(j => (j.qid + '-' + (j.attempt || 'A01')) === k));
  const p = C.findPair(job.text); if (!p) return lane + ': ' + k + ' not in this chat';
  job.submitted_at = v.at; job.submit_wall = Date.parse(v.at);
  job.note = 'Recapture after browser restart; submitted_at is the claim time recorded just before the original send.';
  C.job = job; C.pairEl = p; C.state = 'GENERATING'; C.lastLen = -1; C.stableTicks = 0; C.pub({ note: 'recapture' });
  return lane + ': recapturing ' + k;
};
// Zero-click fallback: return pending (unsaved) answers in pieces small enough for any tool output.
window.CRL_dump = (name, from = 0, size = 900) => { const b = LS.getItem('crl_pend:' + name) || ''; return { name, total: b.length, from, part: b.slice(from, from + size) }; };
C.timer = setInterval(() => C.tick(), 4000);
window.addEventListener('storage', e => { if (e.key === 'crl_stop') C.tick(); });
// Hidden tabs throttle timers to about once a minute, which idles a lane for minutes per answer.
// Any visible tab broadcasts a tick every 3 s; message events reach hidden tabs promptly.
if (window.CRL_bc) { try { window.CRL_bc.close(); } catch (e) {} }
const bc = window.CRL_bc = new BroadcastChannel('crl_tick');
bc.onmessage = () => C.tick();
if (window.CRL_driver) clearInterval(window.CRL_driver);
window.CRL_driver = setInterval(() => { if (!document.hidden) { bc.postMessage(Date.now()); C.tick(); } }, 3000);
new MutationObserver(() => { if (C.state === 'GENERATING' && !C.busy) C.tick(); }).observe(document.querySelector('.chat-panel-content') || document.body, { childList: true, subtree: true });
C.pub({ started: now() });
return 'lane runner v6 started: ' + lane;
})()

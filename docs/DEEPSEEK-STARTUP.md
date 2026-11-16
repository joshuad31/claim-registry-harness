# DeepSeek Harness startup recommendation

`cr start`, `cr launch`, and the no-argument entry point check the current host before printing the standing personality. `cr host` returns the same check alone as JSON. No application or preset is installed, no profile is edited, and no network call is made.

## Detection

DeepSeek Harness's installed `dsh-shell-env` documentation defines per-execution `DSH_SHELL=1` and `DSH_SESSION_ID`. Claim Registry uses that pair as its host hint and prints only the marker names, not the session ID. A DeepSeek model name/key, the application being installed, or `DSH_HOME` alone does not identify the current host. Other environments continue normally, without a DeepSeek installation recommendation.

Selected-preset metadata is separate from the DSH profile. If the host exposes the selected preset, the assistant can use `cr start --active-preset claim-registry` or `cr host --active-preset claim-registry`; explicit user confirmation is also sufficient. Do not guess from a profile name, a package on disk, or the mentor's personality. This is advisory setup guidance, not authentication or an execution gate.

When a finished bundle is available and the current session is not known to use it, recommend installing the **Claim Registry preset**, then starting a **new session with Claim Registry selected**. Do not recommend reinstalling DeepSeek Harness itself. If already using the preset, skip that recommendation. The person can continue in the current session; do not insist, repeat the notice on every turn, or interrupt active research.

## Included distribution

The verified 1.0.0 release is bundled at [`resources/deepseek-preset/claim-registry-preset-1.0.0.zip`](../resources/deepseek-preset/claim-registry-preset-1.0.0.zip). `claimreg/deepseek-preset.json` now has `status: ready` and that relative `bundle_path`. Startup uses this included copy, not the sibling development folder or an installed preset. Missing, invalid, or external archive paths suppress the installation recommendation without blocking research.

The archive contains both the **Claim Registry** mentor and its internal **Claim Registry (blind worker)** preset. Every host subagent is pinned to the worker; the worker omits the mentor, memories, repository instruction loader, shell, web, skills, and further delegation. Its filesystem restrictions are instructions, not an operating-system sandbox. Static configuration checks do not establish how reliably a live worker obeys them. The confirmation and answer-length wording fixes are included; ACH_Eval is unchanged.

Independent release check on 2026-11-16: both the distribution folder and the extracted ZIP passed **56 checks, with two advisory warnings and no failures**. All seven extracted files matched the distribution exactly, and runtime files matched the maintained source after its documented portability rewrites. The warnings concern the intentionally omitted result pruner and a quest skill near its length limit. Archive: 22,364 bytes; SHA-256 `571b2ea4e2fa2634d8624f3ad66dde8cd281b46dbf462e449e3c1d3952f12192`.

## Installing after the user chooses

The assistant handles paths and extraction; the person does not need a terminal.

1. Extract the included ZIP into a stable folder. Keep the resulting `claim-registry-preset/` folder in place: a linked installation reads it there.
2. In a normal DeepSeek Harness session that has `plugin_manager`, install the bundle using `install_bundle` with the extracted folder's absolute path. The Claim Registry mentor deliberately has no plugin manager. If updating an existing installation, use the included README's remove/reinstall instructions.
3. Start a new session, choose **Claim Registry**, and set its workspace to the harness repository. Do not choose the internal blind-worker preset.

The recommendation itself never extracts, installs, or changes profiles. An existing session keeps its original composition.

## Updating the bundled release

Future development changes are not picked up automatically. Review the finished distribution, validate an extracted copy, replace the included release archive, and update the relative manifest path and this release record. If a release is unfinished, set the manifest to `status: pending`; merely finding a ZIP in the sibling development folder never makes it ready.

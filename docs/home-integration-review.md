# Home integration review

## Mint work-update reconciliation, 2026-11-05

- Owner: Pi session `01a1acde-77a5-7088-935c-17ad7c311e68`, user-managed
  default workspace `/home/hsa/projects/my_personal_skills`. No child agents or
  temporary workspaces. The independent `my_programs` session `01a1acdd` owns
  shared instructions, Pi settings, Stamp and Radar deployment.
- Owner approval relayed by that peer covers integration and Mint deployment,
  preserving local work; no publication or bookmark moves. Detected host:
  `hsa-linux-mint`, Zellij 0.45.1. Both repository fetches reported no changes.
- The local Claude-peer edits in `pmwlsnmm` (`52e80045`) are already included in
  the fetched `dev` ancestry. Compared every affected skill against `dev`:
  remaining differences are the incoming role/naming improvements and launcher
  split, not omitted local work. Created reconciliation change `wrsllmqn` above
  `qsotsolt` (`7653e81e`), preserving the existing history rather than replaying
  the same Claude changes. No bookmarks moved and nothing pushed.
- Pi already reads this checkout's `skills/` directly; no package reinstall or
  settings write was needed. New skills are `using-zellij` and
  `launching-visible-agents`; `using-zellij-with-intercom` is retired. This
  checkout activation was explicitly approved and coordinated before the peer
  deploys shared instructions that depend on the new names.
- Replaced Claude's obsolete personal launcher symlink with links for both new
  names. The original link is retained in
  `~/.claude/backup.mint-skills.Ttpu6b/`. No other Claude links were changed.
- Checks: root unittest discovery ran 25 tests, one platform-specific skip,
  no failures; agent-memory transcript suite passed all 45 tests. Fresh offline
  Pi `loadSkills` against the actual configured direct/default paths discovers
  all 15 personal skills with zero diagnostics, exact checkout paths for both
  new skills and Lead/Conductor, and no retired name. This focused check excludes
  package-extension skill resolution. Claude skill-directory parsing likewise
  has zero diagnostics, both new names and no broken links; it is not a Claude
  process startup check.
- Existing Pi processes need `/reload` or restart; Claude processes need restart.
  No new agent was launched and no live Zellij launch/exit smoke was performed.
  Full package/resource discovery is coordinated with the setup peer. Do not
  equate parsed files with live process behavior or claim other hosts deployed.
- Setup-peer follow-up: session `01a1acdd` reports full fresh offline
  `DefaultResourceLoader` discovery using actual settings in a disposable cwd:
  zero extension errors, one Stamp and `/stamp`, both replacement skills plus
  Lead/Conductor resolving to this checkout, and Autonomy/local append loaded.
  These are peer-reported checks, not independently rerun here.
- Corrected incoming `AGENTS.md` activation guidance against the setup repo's
  authoritative `docs/work-machine-pi-skills.md`: WSL reads Windows checkouts
  directly through `/mnt/c`; the obsolete mirror/startup sync must not be
  recreated. The shared guidance links to the owning document rather than
  prescribing the retired procedure. No Windows/WSL host changes were made.
- Status: source and personal Claude links activated; process reload/live checks
  remain explicit follow-up. Keep this user-managed workspace and session.


## Mint reconciliation, 2026-10-24

This section supersedes the older pending-approval status below for personal skills only.

- Owner: session `01a16e14-7cc4-72ae`, user-managed default workspace
  `/home/hsa/projects/my_personal_skills`. No child agents or temporary workspaces.
  The independent `my_programs` peer owns configuration deployment and its evidence.
- User approved implementing local reconciliation and deployment, leaving publication
  to the user. No bookmarks moved and nothing pushed.
- Detected host: Linux Mint 22.3, `hsa-linux-mint`. Fetched origin; its `dev`
  and local `dev` both identify `zsxytqyw` (`b7577ebf`). Rebased the clean empty
  working change onto that result; no unrelated work was rewritten.
- Updated the separately installed package with
  `pi update 'git:git@github.com:MrAldrin/my-personal-skills@dev'`.
  Installed HEAD is now `b7577ebf`; tracked skill contents match this checkout.
  Pi regenerated its installation-local `package-lock.json`; it is not source work.
- Personal package settings already select `@dev`. The four grilling siblings
  are present; no duplicate `grill-me` was found in `~/.agents/skills`.
- Verification on the updated checkout: 9 packaging/guidance tests and all 45
  transcript tests passed. No machine-specific source adjustment was needed.
- Source and installed files are aligned. Running Pi sessions still need
  `/reload` or restart. Fresh-session discovery, interview behavior and a live
  Mint Zellij launch/exit test were not performed; Windows evidence is not Mint
  verification. Other computers were not accessed or deployed.
- Status: implementation complete; this evidence change is ready for user review
  and publication. Keep the user-managed workspace and interactive session.

## Reviewed

- Remote `dev`: `wtzttlzn` (independent task ownership) and `vwuplxqp` (local model policy).
- Follow-up fix `turlzrwv`: peer ownership survives parent chat closure, but execution requires a live peer process and hosting session. Recovery must verify liveness and use the durable record.
- Existing transcript helper suite: 45 tests passed using `uv run --no-project python -m unittest discover -s skills/agent-memory/tests -v`.
- Documentation diff reviewed. No live Zellij launch tested; no host configuration or installed package changed.

## Cross-project coordination

The `my_programs` peer reports:

- Home AGENTS.md and APPEND_SYSTEM.md are live symlinks into that project's checkout. Switching its checkout can activate policy immediately.
- Home policy selects Luna xhigh, then Sol medium. The currently installed Zellij skill still hardcodes other models; reviewed `dev` removes that conflict.
- New core policy references the new ownership skill, which is not installed yet. Peer added a safe missing-skill fallback and deployment warnings in isolated review change `wvmykksu` (`fde0ab0a`), leaving the original checkout and live configuration untouched.
- Final peer-reported validation: Python 295 tests, 3 skips, no failures; Node markers 55 passed, 3 skipped, no failures. Eight outdated Python assertions were corrected; no executable installer/apply fixes were needed. A missing-Carapace regression test was added. Independent Sol-medium review reported no additional blockers in docs/completions.
- Peer evidence: `my_programs/docs/background/2026-10-20-home-review.md` in its review workspace. Live-link migration must preserve the active append policy. These cross-project results are peer-reported, not independently rerun here.

Installed skills come from `/home/hsa/.pi/agent/git/github.com/MrAldrin/my-personal-skills`, not this development checkout.

## Pending approval

1. Review the completed `my_programs` evidence and approve its controlled activation plan, including live-link migration that preserves the active append policy.
2. Integrate reviewed skills changes and this follow-up using the user's chosen version-control workflow. No bookmarks have been advanced by this review.
3. Update the separately installed skills package to the approved revision before activating dependent `my_programs` policy.
4. Reload/restart Pi, confirm skill discovery and effective model policy, and perform an explicitly approved home Zellij readiness smoke test if that workflow is needed.

Do not call this deployed or fully validated until these steps are complete. No push, merge, package update, or host activation is authorized by this review alone.

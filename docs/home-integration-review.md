# Home integration review

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

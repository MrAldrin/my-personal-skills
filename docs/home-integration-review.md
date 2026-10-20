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
- New core policy references the new ownership skill, which is not installed yet. Peer was asked to add a safe missing-skill fallback in an isolated workspace and preserve live configuration.

Installed skills come from `/home/hsa/.pi/agent/git/github.com/MrAldrin/my-personal-skills`, not this development checkout.

## Pending approval

1. Receive the `my_programs` final review and verify its proposed fixes and activation plan.
2. Integrate reviewed skills changes and this follow-up using the user's chosen version-control workflow. No bookmarks have been advanced by this review.
3. Update the separately installed skills package to the approved revision before activating dependent `my_programs` policy.
4. Reload/restart Pi, confirm skill discovery and effective model policy, and perform an explicitly approved home Zellij readiness smoke test if that workflow is needed.

Do not call this deployed or fully validated until these steps are complete. No push, merge, package update, or host activation is authorized by this review alone.

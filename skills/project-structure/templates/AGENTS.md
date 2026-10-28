# Agent instructions

## Startup

- <One line on project scope and size.>
- Read `plans/backlog.md#current-focus` before choosing work. Placement is not permission; a direct request is.
- `docs/scope.md` owns standing boundaries, gates and permissions, if it exists.
- `README.md` owns the repo map and quick start.

## Documentation and plans

- One authoritative home per maintained fact. Link instead of duplicating.
- Reference guidance in `docs/`. Concise, visual briefings in `docs/reports/`. Supporting evidence in `docs/background/`, linked from its owning docs or reports. Create these only when needed.
- Archive reports when superseded or mainly historical, not merely finished. No session diaries in current docs.
- Decisions and verified results live in owning docs or reports; link plans only for remaining work or status.
- If a docs site is adopted, build directly from `docs/`; `docs/index.md` is its reader hub. Keep generated `site/` ignored. Follow the README for preview and report-regeneration commands.
- Keep report-building machinery and private inputs outside `docs/`. Published browser assets belong inside. Generate alternate formats from one narrative source.
- Distinguish planned, implemented and verified.
- Plans state `**Lifecycle:** temporary` or `tracked`. Before removal, preserve decisions, evidence and unfinished work, and update incoming links. Remove finished temporary plans without asking. Tracked or unlabelled plans need approval unless explicit project rules already authorize retirement under their completion conditions.

## Safeguards

- <Project-specific agent rules. Gates and permissions live in docs/scope.md once it exists; point to it, do not restate.>

## Checks

```bash
<lint and test commands>
```

# Agent instructions

## Startup

- <One line on project scope and size.>
- Read `plans/backlog.md#current-focus` before choosing work. Placement is not permission; a direct request is.
- `docs/scope.md` owns standing boundaries, gates and permissions, if it exists.
- Memory is optional. If adopted, follow the `agent-memory` skill and consult `.memory/INDEX.md` before investigations or architectural changes.
- `README.md` owns the repo map and quick start.

## Documentation and plans

- One authoritative home per maintained fact. Link instead of duplicating.
- Current guidance in `docs/`. Evidence in `docs/background/`, linked from current docs.
- Distinguish planned, implemented and verified.
- Plans state `**Lifecycle:** temporary` or `tracked`. Before removal, preserve decisions, evidence and unfinished work, and update incoming links. Remove finished temporary plans without asking. Tracked or unlabelled plans need approval unless explicit project rules already authorize retirement under their completion conditions.

## Safeguards

- <Project-specific agent rules. Gates and permissions live in docs/scope.md once it exists; point to it, do not restate.>

## Checks

```bash
<lint and test commands>
```

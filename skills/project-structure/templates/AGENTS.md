# Agent instructions

## Startup

- <One line on project scope and size.>
- Read `plans/backlog.md#current-focus` before choosing work. Placement is not permission; a direct request is.
- `docs/scope.md` owns standing boundaries, gates and permissions, if it exists.
- Consult `.memory/INDEX.md` before investigations or architectural changes, if it exists.
- `README.md` owns the repo map and quick start.

## Documentation and plans

- One authoritative home per maintained fact. Link instead of duplicating.
- Current guidance in `docs/`. Evidence in `docs/background/`, linked from current docs.
- Distinguish planned, implemented and verified.
- Plans state `**Lifecycle:** temporary` or `tracked`. Remove finished temporary plans after preserving outcomes. Tracked-plan retirement needs approval.

## Safeguards

- <Project-specific agent rules. Gates and permissions live in docs/scope.md once it exists; point to it, do not restate.>

## Checks

```bash
<lint and test commands>
```

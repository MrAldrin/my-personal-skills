# Agent instructions

## Startup

- <One line on project scope and size.>
- Read `plans/backlog.md#current-focus` before choosing work. Placement is not permission; a direct request is.
- `docs/scope.md` owns standing boundaries, gates and permissions, if it exists.
- `README.md` owns the repo map and quick start.

## Documentation and plans

- One authoritative home per maintained fact. Link instead of duplicating.
- Use the shared documentation paths and backlog states so switching repositories does not require relearning navigation.
- Reference guidance in `docs/`. Markdown-first owner briefings in `docs/reports/`, with meaningful visuals where useful, not a report for every task. Supporting evidence in `docs/background/`, linked from its owning docs or reports. Create these only when needed.
- Archive reports when superseded or mainly historical, not merely finished. No session diaries in current docs.
- Decisions and verified results live in owning docs or reports; link plans only for remaining work or status.
- `docs/index.md` is the reader hub when needed, with or without a site; link it from the README. Keep work selection in the backlog.
- Prefer Zensical when a docs site is useful, but adopt common conventions independently of site dependencies. Build directly from `docs/` and keep generated `site/` ignored. Follow the README for preview and report-regeneration commands.
- Keep report-building machinery, private inputs and runtime application reports outside `docs/`. Only intentionally reader-safe browser assets belong inside; local preview is not a privacy boundary.
- Maintain one Markdown narrative and generate alternate formats from it. HTML-only narratives need a concrete rendering or interaction reason. Link or embed custom interactive artifacts rather than maintaining a second narrative. Generated reports retain their builder and inputs as source.
- Distinguish planned, implemented and verified.
- Plans state `**Lifecycle:** temporary` or `tracked`. Before removal, preserve decisions, evidence and unfinished work, and update incoming links. Remove finished temporary plans without asking. Tracked or unlabelled plans need approval unless explicit project rules already authorize retirement under their completion conditions.

## Safeguards

- <Project-specific agent rules. Gates and permissions live in docs/scope.md once it exists; point to it, do not restate.>

## Checks

```bash
<lint and test commands>
```

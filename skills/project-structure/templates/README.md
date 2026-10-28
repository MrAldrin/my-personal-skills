# <Project name>

<One or two sentences: what this project is and why it exists.>

<Scope line until docs/scope.md is needed.>

Start with the [backlog's current focus](plans/backlog.md#current-focus).

## Quick start

```bash
<setup and run commands>
```

## Repository map

| Path | Purpose |
|---|---|
| `plans/` | [Backlog](plans/backlog.md), the sole work agenda, and detail for larger items. |
| `docs/` | Reader-facing reference, reports and supporting evidence. Add when needed. |

When adopted, the documentation site starts at `docs/index.md`, highlighting concise, visual briefings in `docs/reports/` and linking reference docs. Create subfolders only when they have content. Keep report-building machinery and private inputs outside `docs/`.

If a site is used, document its build and live-preview commands here, plus report-regeneration commands when separate. Build directly from maintained `docs/` sources; keep generated output in ignored `site/`. Local preview needs no hosting.

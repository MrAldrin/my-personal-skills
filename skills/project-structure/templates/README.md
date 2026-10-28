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

Once reader navigation is needed, link the documentation hub at `docs/index.md` here. It highlights current briefings in `docs/reports/` and links reference docs, with or without a site. Create subfolders only when they have content. Keep report-building machinery, private inputs and runtime application reports outside `docs/`.

Maintain narratives in Markdown; generate alternate formats from one source. Use meaningful visuals where they help, not a report for every task. Prefer Zensical when a site is useful; adopting common documentation conventions does not require site dependencies.

If a site is used, document its build and live-preview commands here, plus report-regeneration commands when separate. Build directly from maintained `docs/` sources; keep generated output in ignored `site/`. Local preview needs no hosting and does not itself provide a privacy boundary.

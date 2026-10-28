---
name: project-structure
description: Use when setting up a new project's README, AGENTS.md and backlog, or when bringing an existing project onto the shared backlog, scope, documentation and reports structure.
---

# Project structure

A shared mental model for projects. It gives the maintainer and agents one vocabulary for work, current facts, reader-facing briefings and evidence. It is not project-management machinery. Reuse the model, not any project's business content.

## Ownership

One authoritative home per maintained fact. Short summaries and links are fine. Do not duplicate full definitions or a second task queue.

| Location | Answers | Not |
|---|---|---|
| `README.md` | What is this, how do I start, repo map? | A backlog. |
| `AGENTS.md` | How should an agent work here? Routing, rules, safeguards, checks. | Detail owned elsewhere; link instead. |
| `plans/backlog.md` | What work exists, and what is selected? | Completed work or history. |
| `plans/<item>.md` | Detail for one larger backlog item. | A second queue. |
| `docs/scope.md` | Enduring boundaries, supported capabilities, standing gates and standing permissions. | Assignments, remaining actions or a dated progress log. |
| `docs/<topic>.md` | How the project currently works: contracts, definitions, architecture. | Dated evidence. |
| `docs/background/` | Evidence and reasoning behind current docs, linked from them. | Current rules. |
| `docs/reports/` | Concise, visual briefings on important topics, findings and decisions needing the owner's attention. Markdown or HTML. | Detailed reference material or session diaries. |
| `docs/index.md` | The documentation site's reader hub, highlighting current briefings and linking reference docs. | A second copy of their content. |

Tests:
- AGENTS versus scope: scope owns gates and permissions. AGENTS owns routing and how agents work, and points to scope in one line instead of restating gates.
- Scope versus backlog: scope owns what stays true across tasks. The backlog owns assignments and remaining actions.
- Reports versus reference: reports explain and visualize what the owner needs to understand or review. Topic docs own detailed contracts and definitions; reports link to them.
- Decisions and verified results live in their owning docs or reports. Link plans only for remaining work or status.

## Root structure and growth

Every project starts with `README.md`, `AGENTS.md` and `plans/backlog.md`. Templates are in `templates/`. They are starting points, not mandatory replacement files.

The shared root locations are `README.md` (entry guide), `AGENTS.md` (agent instructions), `plans/` (work agenda) and `docs/` (reader-facing documentation, reports and supporting evidence). Keep application code, tests, scripts and data in the project's native locations outside `docs/`.

Add files and subfolders on first real need, never as placeholders:

| Location | Create when |
|---|---|
| `docs/scope.md` | The first standing gate, boundary or permission appears. Until then, one scope line in the README is enough. |
| `docs/<topic>.md` | A maintained contract, definition or reference needs a home. |
| `docs/reports/` | The first reader-facing briefing needs a home. |
| `docs/reports/archive/` | A report is superseded or retained mainly as historical reference. Completion alone is not a reason to archive it. |
| `docs/background/` | Supporting evidence or a detailed investigation is worth keeping. |
| `docs/index.md` | A documentation site is adopted. |
| `plans/<item>.md` | An item outgrows a few backlog bullets. |

Report-building code, templates and computational inputs stay outside `docs/`, following existing code/data conventions (for example `report_inputs/`). Published browser assets, including chart data, can live beside their report or in an assets subfolder. Include only data intended for readers; keep private inputs out of the site source.

Do not create empty folders or empty companion files. This map does not authorize removing existing project directories.

## Optional documentation site

- Build directly from maintained `docs/` sources so live preview sees edits. Avoid disposable staging copies. Zensical is one option, not a requirement.
- Keep generated output separate, normally in ignored `site/`.
- Use `docs/index.md` as the reader hub; put important current briefings first. Site navigation can group pages independently of their folders.
- Maintain one narrative source and generate other formats from it. An HTML-only report can itself be the source; a generated report's source is its builder and inputs. Do not separately maintain Markdown and HTML versions of the same narrative.
- Keep published images, JavaScript, styles and chart data inside the site source tree. Report-building machinery and private inputs stay outside it.
- Document build and live-preview commands in the README. A site rebuild does not itself rerun report calculations; document report regeneration separately when needed.
- Local preview does not require hosting. Publishing and access controls are a separate decision.

## Backlog

States: **Current focus** (selected; may be "nothing selected"), **Next** (ready, not selected), **Blocked** (named prerequisites), **Later** (concrete, deliberately deferred), **Ideas** (needs shaping or a decision). Small projects may merge Later and Ideas.

- States are selection states, not size or priority.
- Placement is not permission. A direct user request selects work and authorizes its ordinary steps; do not re-ask for each step.
- `[human]` marks work needing substantial human judgment. It is not blocked just because an agent cannot do it.
- Link real dependencies both ways: **Blocked by** and **Unblocks**. On completion, update dependents. Becoming unblocked does not select an item.
- The backlog file carries its own short maintenance section, so agents can edit it without other context.

## Permissions

- Gates in `docs/scope.md` are few and named. Anything not named is ordinary work within a selected task.
- List standing permissions next to the gates, for example "read-only queries need no extra permission".
- Preserve a project's existing permissions. Require separate approval for actions that are genuinely destructive or outside the selected scope.
- Verification is not approval. Missing approval does not block verification.

## Working cycle

1. Read the current focus and relevant scope before choosing work.
2. Read the task's current docs and linked evidence where prior reasoning matters.
3. Keep facts in their owning docs. Record uncertainty instead of turning assumptions into rules.
4. Distinguish planned, implemented and verified. Verification names the claim, checks, scope and limits.
5. At closeout, update owning docs, preserve useful findings, update dependents, then remove the finished backlog item.

## Plans

- Each plan states `**Lifecycle:** temporary` or `**Lifecycle:** tracked` at creation. Unlabelled plans are not assumed temporary.
- Before removing any plan, preserve decisions in owning docs, evidence in background and unfinished work in the backlog.
- Remove finished temporary plans without asking once their outcomes are preserved and incoming links are updated. Retiring a tracked plan needs approval unless explicit project rules already authorize it; follow their completion and preservation conditions. Unlabelled plans follow the tracked-plan rule.
- Plan cleanup never authorizes deleting code, data, reports or evidence.
- Tool-generated plans (for example Superpowers) stay at the tool's default location. They are supporting plans, not a second queue. The backlog links to them when needed.

## Writing

- Short sentences and bullets. One fact per statement.
- Entry guides fit about one screen. No session diaries in current docs. Dated reports and investigations are valid.
- Link current docs to their background evidence explicitly.

## Adopting into an existing project

1. Map existing files to the ownership table first. Note duplicates, second queues and stale files.
2. Preserve the project's own rules, safeguards, checks and permissions.
3. Use the filenames and backlog states in this skill as the shared default. Propose renames or moves toward that default, including `docs/scope.md` when needed, and ask the owner before applying them. Do not silently rename existing files or replace project rules. Include merges and deletions in the proposal.
4. Agree a safe point with any session actively working in the repo. Do not edit under it.
5. Remove approved duplicates after preserving their authoritative content and updating links. Keep project-specific content in that project.

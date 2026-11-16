# Issue tracker: Beads

Issues and specs live in the project's Beads store. Use the `bd` CLI for all
operations. Follow the repository's AGENTS.md for store selection and sync
(`bd dolt push` after writes when a remote exists). Never write issues as
Markdown files (no `.scratch/` tracker), and never use GitHub issues for this
project's work unless the owner asks.

Shared template from `my-personal-skills`. It is the "Other" tracker for the
mattpocock engineering skills (`wayfinder`, `to-tickets`, `triage`, `to-spec`).
Do not run `/setup-matt-pocock-skills` to replace it.

## Conventions

- **Create an issue**: `bd create --title="..." --description="..." --type=task|bug|feature --priority=2`. Add `--parent=<id>` for a child, `--labels=a,b` for labels. Use a heredoc variable for multi-line bodies.
- **Read an issue**: `bd show <id>`; add `--json` for structured output. Comments: `bd comments <id>`.
- **List issues**: `bd list --status=open --json` with `--label`, `--parent`, `--assignee` or `--no-assignee` filters.
- **Make an issue a child of a parent**: `bd create ... --parent=<parent>`, or `bd update <child> --parent=<parent>` afterwards.
- **Blocking**: native dependencies. `bd dep add <child> <blocker>` (child depends on blocker). A ticket is unblocked when every blocker is closed. `bd show <id>` lists blockers; `bd blocked` lists all blocked issues.
- **Comment on an issue**: `bd comments add <id> "..."`.
- **Apply / remove labels**: `bd label add <id> <label>` / `bd label remove <id> <label>`.
- **Close**: comment the explanation, then `bd close <id> --reason="..."`.
- Never use `bd edit` (it opens an editor).

## Pull requests as a triage surface

**PRs as a request surface: no.** Beads has no pull requests.

## When a skill says "publish to the issue tracker"

Create a bead.

## When a skill says "fetch the relevant ticket"

Read it as in **Read an issue** above.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single bead with **child** beads as tickets.

- **Map**: an epic labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. `bd create --type=epic --labels=wayfinder:map --title="..." --description="..."`. Find it with `bd list --label=wayfinder:map --status=open`. Update the body with `bd update <map> --description="..."` (read it first with `bd show`; rewrite the whole body).
- **Child ticket**: `bd create --parent=<map> --no-inherit-labels --type=task --labels=wayfinder:<type> ...` (without `--no-inherit-labels`, the child also gets `wayfinder:map` and breaks the map lookup), with `<type>` one of `research`/`prototype`/`grilling`/`task`. Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: `bd dep add <ticket> <blocker>`.
- **Frontier query**: `bd ready --parent=<map> --unassigned --json`. `bd ready` already drops closed, blocked and in-progress beads. First in map order wins.
- **Claim**: `bd update <id> --claim`, the session's first write.
- **Resolve**: `bd comments add <id> "<answer>"`, then `bd close <id> --reason="<one-line gist>"`, then append a context pointer (gist + bead id) to the map's Decisions-so-far.

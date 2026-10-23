# My Personal Skills

A personal collection of Agent Skills shared across machines and compatible harnesses.

## Skills

- `agent-memory` — project memory capture, lookup, and transcript review
- `compact-decision-walkthrough` — review implementation plans one decision at a time
- `creating-session-handoffs` — create concise handoffs between sessions
- `delegating-independent-work` — experimental ownership, workspace, handoff and cleanup workflow for independent agents
- `project-structure` — shared README, AGENTS, backlog, scope, docs and memory structure for new and existing projects
- `version-control-workflow` — plan atomic Jujutsu changes, enforce description conventions, and leave a verified stack for user review
- `using-zellij-with-intercom` — launch visible interactive Pi peers in Zellij tabs and coordinate through intercom without requiring Herdr

### Grilling and domain modeling

Adapted from Matt Pocock's MIT-licensed skills, bundled as one set:

- `grill-me` — stress-test one-off plans and non-code ideas without writing files by default
- `grill-with-docs` — stress-test ongoing project designs while recording agreed terminology and significant decisions
- `grilling` — shared design-tree interview discipline, one question at a time
- `domain-modeling` — sharpen project language, maintain glossaries, and offer ADRs sparingly

See [usage, dependencies, local adaptations and pinned provenance](docs/grilling-skills.md). **Agents syncing this repo on another machine: follow the [sync and legacy-skill migration checklist](docs/grilling-skills.md#sync-and-migration-checklist-for-agents).** An update does not automatically retire old standalone `grill-me` installations from other skill sources. [Preparation/review status](docs/grilling-preparation.md).

## Install for Pi

Clone this repository into a global Pi skill location:

```bash
git clone <repository-url> ~/.agents/skills/my-personal-skills
```

Pi recursively discovers the `SKILL.md` files in the cloned directory. Alternatively, add the repository's `skills/` directory to the `skills` array in Pi settings.

For a Pi package install, use the GitHub repository URL:

```bash
pi install git:github.com/<owner>/my-personal-skills
```

After updating the clone or package, restart Pi or run `/reload`.

## Test

Run the skill-set packaging checks and transcript helper's standard-library suite:

```bash
uv run --no-project python -m unittest discover -s tests -v
uv run --no-project python -m unittest discover -s skills/agent-memory/tests -v
```

The `agent-memory` skill reads both Pi v3 and Claude Code session files and documents commands through `uv`.

## Safety

Skills contain instructions that an agent may follow and helper code that it may execute. Review changes before using them, especially when syncing from another machine.

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

## Possible skills

External skills to evaluate, not skills bundled with this repository. Listing one here does not install it or commit us to adopting it. Whether to install per profile or manage external skills centrally through this repository remains undecided.

### Worth trying

- [Grill Me — Matt Pocock](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me): stress-test a plan through questions that uncover assumptions and unresolved decisions. Try it on a real skill proposal, keeping questions one at a time and bounding the session. This is a trial candidate, not a definite addition.

- [Domain Modeling / Ubiquitous Language — Matt Pocock](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling): clarify ambiguous project terminology and record shared definitions. Evaluate its benefits and documentation overhead in practice; this is a general skill recommendation to try, not a decision to adopt it.

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

The transcript helper's standard-library test suite can be run with:

```bash
python3 -m unittest discover -s skills/agent-memory/tests -v
```

The `agent-memory` skill reads both Pi v3 and Claude Code session files and documents commands through `uv`.

## Safety

Skills contain instructions that an agent may follow and helper code that it may execute. Review changes before using them, especially when syncing from another machine.

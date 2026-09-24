# My Personal Skills

A personal collection of Agent Skills shared across machines and compatible harnesses.

## Skills

- `agent-memory` — project memory capture, lookup, and transcript review
- `compact-decision-walkthrough` — review implementation plans one decision at a time
- `creating-session-handoffs` — create concise handoffs between sessions
- `version-control-workflow` — plan atomic Jujutsu changes, enforce description conventions, and leave a verified stack for user review

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

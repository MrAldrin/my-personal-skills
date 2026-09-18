# Pi Personal Skills

A personal collection of Pi skills shared across machines.

## Skills

- `agent-memory` — project memory capture, lookup, and transcript review
- `compact-decision-walkthrough` — review implementation plans one decision at a time
- `creating-session-handoffs` — create concise handoffs between sessions
- `version-control-workflow` — structure Jujutsu change descriptions and workflow

## Install for Pi

Clone this repository into a global Pi skill location:

```bash
git clone <repository-url> ~/.agents/skills/pi-personal-skills
```

Pi recursively discovers the `SKILL.md` files in the cloned directory. Alternatively, add the repository's `pi-personal-skills/` directory to the `skills` array in Pi settings.

For a Pi package install, use the GitHub repository URL:

```bash
pi install git:github.com/<owner>/pi-personal-skills
```

After updating the clone or package, restart Pi or run `/reload`.

## Test

The transcript helper's standard-library test suite can be run with:

```bash
python3 -m unittest discover -s pi-personal-skills/agent-memory/tests -v
```

The `agent-memory` skill uses Pi v3 session files and documents commands through `uv`.

## Safety

Skills contain instructions that an agent may follow and helper code that it may execute. Review changes before using them, especially when syncing from another machine.

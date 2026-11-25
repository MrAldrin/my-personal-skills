# My Personal Skills

A personal collection of Agent Skills shared across machines and compatible harnesses.

## Tasks

See [the task-store guide](docs/beads.md) and [source-to-ID pointer](backlog.md).
Beads owns current task status; migration does not authorize queued skill work.

## Skills

- `lead` — explicitly entered role for planning and coordinating delivery through visible Conductors
- `conductor` — explicitly assigned batch-owner role; install with `lead` ([usage and dependencies](docs/lead-conductor.md))
- `copying-to-clipboard` — request-only, verified UTF-8 clipboard text on Windows and WSL
- `compact-decision-walkthrough` — review implementation plans one decision at a time
- `creating-session-handoffs` — create concise handoffs between sessions
- `delegating-independent-work` — experimental ownership, workspace, handoff and cleanup workflow for independent agents
- `project-structure` — shared README, AGENTS, backlog, scope, documentation and reports structure for new and existing projects
- `launching-visible-agents` — start visible Pi or Claude Code peers with baton and verify them through peer messaging
- `using-zellij` — visible job panes and named shell tabs, not agent control

### Third-party skills

Third-party skills come unchanged from upstream Pi packages declared in
`my_programs/pi/shared-settings.json`. This repository holds owner-written
skills only, including thin manual-only wrappers over upstream skills.

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

Run the skill-set packaging checks:

```bash
uv run --no-project python -m unittest discover -s tests -v
```

## Safety

Skills contain instructions that an agent may follow and helper code that it may execute. Review changes before using them, especially when syncing from another machine.

---
name: using-zellij
description: >
  Use when an agent opens a Zellij pane or tab, runs a long-running job or program for the user, or names or closes agent-created panes and tabs.
---

# Using Zellij

**Zellij** is the multiplexer the user works in. Agents create and close only the panes and tabs they own. [commands.md](commands.md) holds the exact invocations. Run them through the agent's shell tool, and verify flags with the installed command help first.

## Find your own tab

1. Read `ZELLIJ_PANE_ID` from the environment.
2. Run `zellij action list-panes --all --json` and match that pane ID to get its `tab_id`. Environment variables alone do not prove connectivity.
3. Never open panes in the user's focused tab unless a new tab is requested. If the own tab cannot be targeted safely, ask.

## Long-running jobs and programs

Run a job or program for the user in a hidden floating pane in your own tab, never as a hidden background process:

```bash
zellij action new-pane --tab-id <tab> --floating --no-focus --name <job> --cwd <dir> -- <command>
```

- Record the returned pane ID.
- Verify startup: inspect the pane's screen and command, not just that the pane exists.
- Report the pane to the user.
- Close it when the job is done: `zellij action close-pane --pane-id <id>`.
- Do not use `--stacked`: it expands the new pane over your agent's pane.
- Short commands with a timeout stay in the agent's normal tools.

## New tabs

Open a new tab only when the user requests one, for example for a visible agent.

- Name it `<project>-<task>`, using the same task as the workspace it serves. Keep the name at most 25 characters: if longer, abbreviate the project to its initials, then shorten the task.
- Create it with an explicit cwd and no initial command, so the normal interactive preferred shell starts. Do not add `-- <program>`, `--layout`, or `--close-on-exit`.
- Use no-focus where the installed version supports it.
- Record the stable numeric tab ID, resolve its terminal pane from that exact tab, and verify shell identity, cwd and shell prompt before submitting input.
- Closing a tab or pane is destructive: verify ownership and disposability first, and never use focus-dependent cleanup.

## Inspect and boundaries

- Check the session and Zellij version. Inspect live tabs and panes before acting.
- Check installed command help for each invocation before use: flags vary by version.
- Do not nest multiplexers and do not switch to WezTerm tabs as a substitute.
- If a targeting or focus behavior is unsupported, stop and resolve it rather than falling back to focused input.

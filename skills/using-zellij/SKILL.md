---
name: using-zellij
description: >
  Use for visible terminal jobs and shell tabs in Zellij. For agent control, use using-baton.
---

# Using Zellij

Use [commands.md](commands.md) for non-agent jobs and shell tabs. Create and close only resources you own. Read `using-baton` from the baton repo to control an agent.

## Find your own tab

1. Read `ZELLIJ_PANE_ID` from the environment.
2. Run `zellij action list-panes --all --json` and match that pane ID to get its `tab_id`. Environment variables alone do not prove connectivity.
3. Never open a job pane in the user's focused tab. If you cannot target your own tab safely, stop and ask.

## Outside Zellij

An agent outside Zellij has no `ZELLIJ_PANE_ID`, for example the Claude desktop app or a plain terminal. It has no own tab, so it works in a session the user names:

1. Use the session named in the request. Otherwise run `zellij list-sessions --no-formatting` and ask which attached session to use. Do not guess, and do not start a new session.
2. Pass the session on every call: `zellij --session <name> action ...`, and `baton --session <name> ...` for agents.
3. Put each job or agent in its own new tab with `--no-focus`. Floating panes need an own tab, so a job also gets a new tab. Never add panes to an existing tab.
4. Tell the user the session and tab name, so they can open it.

## Long-running jobs and programs

Run a job or program for the user in a visible floating terminal pane in your own tab without changing focus, never as a hidden background process:

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

Open a shell-only tab only when the user requests one.

- Name it `<project>-<task>`, using the same task as the workspace it serves. Keep the name at most 25 characters: if longer, abbreviate the project to its initials, then shorten the task.
- Create it with an explicit cwd and no initial command, so the normal interactive preferred shell starts. Do not add `-- <program>`, `--layout`, or `--close-on-exit`.
- Use no-focus. Record the numeric tab ID and verify the shell and cwd in its exact pane.
- Before closing a tab or pane, explain the impact and verify ownership and disposability. Never use focus-dependent cleanup.

## Inspect and boundaries

- Check the session and Zellij version. Inspect live tabs and panes before acting.
- Check installed command help for each invocation before use: flags vary by version.
- Do not nest multiplexers and do not switch to WezTerm tabs as a substitute.
- If a targeting or focus behavior is unsupported, stop and resolve it rather than falling back to focused input.

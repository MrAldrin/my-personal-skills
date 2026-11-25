# Zellij command reference

Use these commands for terminal jobs and tabs, not for agent control. Check the installed Zellij version and each action's `--help` before use. The examples use Bash for the calling shell. Resolve IDs in the intended session, never from focus.

## Find your own tab

```bash
zellij action list-panes --all --json
```

Match the numeric `ZELLIJ_PANE_ID` to the non-plugin entry's `id`. Read its `tab_id`. Commands address pane ID `3` as `terminal_3`.

## Floating job pane

```bash
zellij action new-pane --tab-id 3 --floating --no-focus --name my-job --cwd /path/to/dir -- ./run-job --flag
```

Record the returned pane ID. Verify the command in the pane list and inspect the screen:

```bash
zellij action dump-screen --pane-id terminal_123
```

After the job ends, verify ownership and explain the impact before you close it:

```bash
zellij action close-pane --pane-id terminal_123
```

## New tab with the normal shell

Create a shell-only tab when the user requests one. Use an explicit cwd and no focus change. Do not add an initial command, a layout or `--close-on-exit`.

```bash
zellij action new-tab --name "my-app-review" --cwd /path/to/workspace --no-focus
```

Record the returned numeric tab ID. Use the pane list to find the terminal with that `tab_id`. Verify the shell command, cwd and prompt in the exact pane. Do not infer a terminal ID from a tab ID. If the installed version cannot target the tab or avoid changing focus, stop and report.

# Zellij command reference

Run these through the agent's shell tool. Replace paths, tab/pane IDs and names with discovered or verified values. Verify each flag with the installed command help first; the tested version is Zellij 0.45.1.

## Inspect

- `zellij --version`
- `zellij action new-tab --help`
- `zellij action new-pane --help`
- `zellij action close-pane --help`
- `zellij action list-tabs --help`
- `zellij action list-panes --help`
- `zellij action dump-screen --help`
- `zellij action write-chars --help` and `zellij action write --help`

The tested 0.45.1 supports `list-tabs --all --json` and `list-panes --all --json`. If `--no-focus` is absent, explain the focus change before creating a tab. If explicitly selecting another session, inspect local session-selection syntax first.

Find your own tab from `ZELLIJ_PANE_ID`:

```bash
zellij action list-panes --all --json
```

`ZELLIJ_PANE_ID` is numeric (for example `3`). Select the entry with `is_plugin: false` and that numeric `id`, and read its `tab_id`. Commands address the same pane as `terminal_3`.

## Floating job pane

For a long-running job or program for the user, in your own tab, hidden from focus:

```bash
zellij action new-pane --tab-id 3 --floating --no-focus --name my-job --cwd /path/to/dir -- ./run-job --flag
```

Record the returned pane ID, then verify it:

```bash
zellij action dump-screen --pane-id terminal_123
```

Close it when done:

```bash
zellij action close-pane --pane-id terminal_123
```

Do not add `--stacked`: it expands the new pane over your agent's pane.

## New tab with the normal shell

Create the tab without an initial command, so the normal interactive preferred shell starts. Do not add `-- <program>`, `--layout`, or `--close-on-exit`.

Linux/WSL example:

```bash
zellij action new-tab --name "my-app-review" --cwd /path/to/workspace --no-focus
```

Native Windows example (tool uses Bash quoting):

```bash
zellij action new-tab --name "my-app-review" --cwd 'C:/path/to/workspace' --no-focus
```

Record the returned stable numeric tab ID. List panes, select the terminal pane belonging to that exact tab, and inspect its shell command, cwd and screen. A tab may contain plugins or multiple terminals: never guess the terminal ID from a tab ID or use whichever pane is focused.

```bash
zellij action list-panes --all --json
zellij action dump-screen --pane-id terminal_123
```

Wait for the normal shell prompt before submitting input. A held command or blank screen is not a ready shell.

## Submitting input to a pane

`write-chars` types text into a stable pane; `write ... 13` sends Enter on the tested version. Recheck pane ownership and an idle prompt immediately before submitting. If the installed Zellij lacks explicit pane targeting, do not fall back to focused input.

```bash
zellij action write-chars --pane-id terminal_123 'some command'
zellij action write --pane-id terminal_123 13
```

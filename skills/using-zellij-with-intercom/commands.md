# Zellij / Pi command reference

Run Zellij commands through the agent's shell tool. Two shells matter: the tool's shell parses the Zellij invocation; the new pane's interactive shell parses the submitted Pi command. Quote for each separately. Examples below use Bash for the tool and Bash-compatible or Nushell syntax in the pane, as labelled. Replace paths, tab/session names, `MODEL_WITH_REASONING` and `SUPERVISOR_SESSION_ID` with discovered or policy-selected values. No helper script or Herdr installation is required.

## Inspect

- `zellij --version`
- `zellij action new-tab --help`
- `zellij action list-tabs --help`
- `zellij action list-panes --help`
- `zellij action write-chars --help`
- `zellij action write --help`
- `zellij action dump-screen --help`
- `pi --help` (or the discovered local launcher with `--help`)

Use the inherited Zellij session. Environment variables alone do not prove connectivity: inspect live tabs and panes. If explicitly selecting another session, inspect local session-selection syntax first. The tested 0.45.1 supports `list-tabs --all --json` and `list-panes --all --json`; adapt only after checking local help. If `--no-focus` is absent, explain the focus change before launching. Verify Pi's naming/model flags too.

## Open the normal shell first

Discover the normal interactive preferred shell from local preferences, configuration and existing shell panes. Create the tab without an initial command, allowing that normal shell to start. Do not add `-- pi`, `-- node`, `exec`, a replacement shell command, or a layout that directly starts Pi. Do not use `--close-on-exit`: closing Pi's pane is not returning to a shell prompt. If the default shell does not match the preference, stop and resolve the mismatch rather than redesigning configuration.

Linux/WSL example:

```bash
zellij action new-tab --name "Review peer" --cwd /path/to/workspace --no-focus
```

Native Windows example (tool uses Bash quoting):

```bash
zellij action new-tab --name "Review peer" --cwd 'C:/path/to/workspace' --no-focus
```

Record the returned stable numeric tab ID. List panes, select the terminal pane belonging to that exact tab, and inspect its shell command, cwd and screen. A tab may contain plugins or multiple terminals: never guess the terminal ID from a tab ID or use whichever pane is focused. Replace `terminal_123` below with the verified owned pane ID.

```bash
zellij action list-panes --all --json
zellij action dump-screen --pane-id terminal_123
```

Wait for the normal shell prompt before submitting input. A held command or blank screen is not a ready shell.

## Submit foreground Pi to the owned shell

`write-chars` types the command; the separate `write ... 13` submits Enter on the tested version. Recheck exact pane ownership and idle prompt immediately before submission. If installed Zellij lacks explicit stable targeting, do not fall back to focused input; resolve supported targeting first.

### Linux / WSL

For a Bash-compatible interactive pane, the agent's Bash tool can submit:

```bash
zellij action write-chars --pane-id terminal_123 'pi --model "MODEL_WITH_REASONING" --name review-peer "Send readiness via intercom to SUPERVISOR_SESSION_ID. Report your session ID, cwd, PI_MODEL, PI_REASONING_LEVEL, ZELLIJ_SESSION_NAME and ZELLIJ_PANE_ID. Do not edit or launch agents. Wait for the task and remain interactive."'
zellij action write --pane-id terminal_123 13
```

This requires `pi` to resolve in that environment. Discover its normal launcher; do not copy Windows paths into Linux/WSL. For a different interactive shell, adapt the submitted command's syntax and quoting.

### Native Windows

Inspect existing Pi panes' `pane_command` / `terminal_command` for the actual launcher. Preserve established terminal workarounds. The verified machine uses Nushell as its normal shell and Node with an existing fullscreen mouse launcher. From the agent's Bash tool, submit this Nushell-compatible command:

```bash
zellij action write-chars --pane-id terminal_123 'node "C:/path/to/dotfiles/pi/windows-fullscreen-mouse/launch.mjs" --model "MODEL_WITH_REASONING" --name review-peer "Send readiness via intercom to SUPERVISOR_SESSION_ID. Report effective model, reasoning, cwd and session/pane identity. Do not edit or launch agents. Wait for the task and remain interactive."'
zellij action write --pane-id terminal_123 13
```

The launcher is an optional local dependency, not supplied by this skill. Discover it; do not assume it exists elsewhere. If absent, inspect the normal Pi installation and use a supported interactive entrypoint. A `.cmd` shim may require a command interpreter; it must remain a foreground child of the interactive shell. Do not install a launcher or change configuration to reproduce this example.

For PowerShell, a quoted executable path needs the call operator `&`; Nushell uses `^` for a quoted external executable path; Bash runs a quoted path directly. The example uses unquoted `node` resolved on PATH, so it needs neither operator. Do not copy Bash outer quoting into a PowerShell tool, or use PowerShell syntax inside Nushell. Adapt both quoting layers, including embedded quotes in paths or prompt text.

## Inspect startup and message after registration

```bash
zellij action dump-screen --pane-id terminal_123
```

A blank screen while the process lives may mean package/extension startup. Inspect before creating duplicates. A failed Pi child should return to the shell; inspect its error rather than submitting a second launch blindly. A visible pane is not proof of a connected Pi session.

Use the intercom tool, not a shell command:

1. `list` to discover the uniquely named session and its session ID.
2. `send` addressed to that exact ID with a ping and request for acknowledgement, session/pane identity, cwd and effective model/reasoning.
3. After acknowledgement and selection verification, send the bounded task packet to the same verified peer.

Do not enable `openProjectPaneIfMissing`: that launches through Herdr. Use exact session targeting even when peers share a cwd.

## Verify lifecycle with an authorized disposable tab

On a new launch route, obtain approval for a uniquely named disposable tab and record its stable tab/pane IDs. Start Pi as above. Use Pi's locally supported exit interaction only in that disposable pane; inspect return to the normal shell prompt, then submit a harmless shell marker (for example `echo PI_SHELL_RETURNED`) and verify its output. Finally submit `exit` to the same disposable shell and verify its pane disappears rather than becoming held. Never test exit on a live user peer. Native Windows Zellij 0.45.1 was tested; Linux/WSL needs its own local verification.

Leave successful task-owner tabs open for direct user conversation. Persistence requires a running Pi process and Zellij session; after restart refresh both rosters. Closing a pane/tab is destructive: verify ownership and disposability first, and never use focus-dependent cleanup.

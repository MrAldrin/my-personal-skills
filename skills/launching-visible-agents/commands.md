# Pi / Claude Code launch command reference

Run Zellij commands through the agent's shell tool. Two shells matter: the tool's shell parses the Zellij invocation; the new pane's interactive shell parses the submitted Pi command. Quote for each separately. Examples below use Bash for the tool and Bash-compatible or Nushell syntax in the pane, as labelled. Replace paths, tab/session names, `MODEL_WITH_REASONING` and `SUPERVISOR_SESSION_ID` with discovered or policy-selected values. No helper script or Herdr installation is required. Tab and pane mechanics are in [using-zellij commands](../using-zellij/commands.md).

## Inspect the launcher

- `pi --help` (or the discovered local launcher with `--help`). Verify its `--name` and `--model` flags.
- `claude --help` for `--name`, `--model` and `--effort` when launching Claude Code.

## Open the normal shell first

Create the tab and verify its shell prompt as [using-zellij](../using-zellij/commands.md) describes. Never add `-- pi`, `-- node` or a layout that starts Pi directly.

## Submit foreground Pi to the owned shell

Recheck exact pane ownership and idle prompt immediately before submission. If installed Zellij lacks explicit stable targeting, do not fall back to focused input.

### Linux / WSL

For a Bash-compatible interactive pane, the agent's Bash tool can submit:

```bash
zellij action write-chars --pane-id terminal_123 'pi --model "MODEL_WITH_REASONING" --name my-app-review "Send readiness via intercom to SUPERVISOR_SESSION_ID. Report your session ID, cwd, PI_MODEL, PI_REASONING_LEVEL, ZELLIJ_SESSION_NAME and ZELLIJ_PANE_ID. Do not edit or launch agents. Wait for the task and remain interactive."'
zellij action write --pane-id terminal_123 13
```

This requires `pi` to resolve in that environment. Discover its normal launcher; do not copy Windows paths into Linux/WSL. For a different interactive shell, adapt the submitted command's syntax and quoting.

### Native Windows

Inspect existing Pi panes' `pane_command` / `terminal_command` for the actual launcher. Preserve established local launcher workarounds. The verified machine uses Nushell as its normal shell and Node with an existing fullscreen mouse launcher. From the agent's Bash tool, submit this Nushell-compatible command:

```bash
zellij action write-chars --pane-id terminal_123 'node "C:/path/to/dotfiles/pi/windows-fullscreen-mouse/launch.mjs" --model "MODEL_WITH_REASONING" --name my-app-review "Send readiness via intercom to SUPERVISOR_SESSION_ID. Report effective model, reasoning, cwd and session/pane identity. Do not edit or launch agents. Wait for the task and remain interactive."'
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

## Claude Code peers

Same shell-first tab and pane-targeted submission. Submit (Bash-compatible pane; adapt quoting for Fish or others):

```bash
zellij action write-chars --pane-id terminal_123 'claude --name my-app-review --model MODEL --effort EFFORT "Read SKILL_PATH before acting. Send readiness with SendMessage to SUPERVISOR_NAME: report your session name, cwd, model, ZELLIJ_SESSION_NAME and ZELLIJ_PANE_ID. Do not edit or launch agents. Wait for the task."'
zellij action write --pane-id terminal_123 13
```

Find the supervisor's own name with `ListAgents` before launch. Then:

1. `ListAgents` to find the exact peer name.
2. `SendMessage` a ping; wait for its reply (a message wakes an idle session).
3. Send the task packet to the same peer.

Same-machine only; Windows and WSL sessions cannot reach each other. Exiting Claude returns to the shell.

## Verify lifecycle with an authorized disposable tab

On a new launch route, obtain approval for a uniquely named disposable tab and record its stable tab/pane IDs. Start Pi as above. Use Pi's locally supported exit interaction only in that disposable pane; inspect return to the normal shell prompt, then submit a harmless shell marker (for example `echo PI_SHELL_RETURNED`) and verify its output. Finally submit `exit` to the same disposable shell and verify its pane disappears rather than becoming held. Never test exit on a live user peer. Native Windows Zellij 0.45.1 was tested; Linux/WSL needs its own local verification.

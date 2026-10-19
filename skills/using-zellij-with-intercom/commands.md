# Zellij / Pi command reference

Run these through the agent's shell tool, not by typing into a focused terminal. Examples use Bash quoting; adapt to the actual shell. Replace example paths with discovered values, `review-peer` and the tab label with unique names, and `SUPERVISOR_SESSION_ID` with your own current intercom session ID from `list` or `status`. No helper script or Herdr installation is required.

## Inspect

- `zellij --version`
- `zellij action new-tab --help`
- `zellij action list-tabs --all --json`
- `zellij action list-panes --all --json`
- `pi --help`

Use the existing Zellij session inherited by the agent. If explicitly targeting another session, inspect the installed CLI's session-selection syntax first. On versions without JSON/all flags, inspect help and use supported listing commands. If `--no-focus` is absent, explain the focus change before launching. Verify Pi's naming/model flags in local help too.

## Launch on Linux / WSL

`zellij action new-tab --name "Review peer" --cwd /path/to/workspace --no-focus -- pi --model github-copilot/claude-haiku-5.5:medium --name review-peer "Send readiness via intercom to SUPERVISOR_SESSION_ID. Report your session ID, cwd, PI_MODEL, PI_REASONING_LEVEL, ZELLIJ_SESSION_NAME and ZELLIJ_PANE_ID. Do not edit or launch agents. Wait for the task and remain interactive."`

This is the portable form; it requires `pi` to resolve to an executable in that environment. Do not copy Windows launcher paths into WSL. The live smoke test covered native Windows with Zellij 0.45.1, not Linux/WSL; verify local help and readiness on each machine.

## Launch on native Windows

Run `zellij action list-panes --all --json` and inspect an existing Pi pane's `pane_command` / `terminal_command` to discover its actual launcher. This machine's verified route used Node with the existing fullscreen workaround, structurally:

`zellij action new-tab --name "Review peer" --cwd 'C:/path/to/workspace' --no-focus -- node 'C:/path/to/dotfiles/pi/windows-fullscreen-mouse/launch.mjs' --model github-copilot/claude-haiku-5.5:medium --name review-peer "Send readiness via intercom to SUPERVISOR_SESSION_ID. Report effective model, reasoning, cwd and session/pane identity. Do not edit or launch agents. Wait for the task and remain interactive."`

The launcher is an optional local dependency, not supplied by this skill. Discover it; do not assume it exists at home. If absent, inspect the normal Pi installation and use a locally supported interactive entrypoint. Do not install or change terminal configuration merely to reproduce this example.

## Inspect startup

`new-tab` on the tested Zellij 0.45.1 returned a stable numeric tab ID. Find its terminal pane through `list-panes`, then inspect only that pane:

`zellij action dump-screen --pane-id terminal_123`

If it is blank and the process remains alive, startup may still be resolving packages/extensions. Inspect before creating duplicates. A failed command can leave a held pane; a visible pane is not proof of a connected Pi session.

## Message after registration

Use the intercom tool, not a shell command:

1. `list` to discover the uniquely named session and its session ID.
2. `send` addressed to that ID with a ping and request to send an acknowledgement.
3. After acknowledgement, send the bounded task packet to the same verified peer.

Do not enable `openProjectPaneIfMissing`: that launches through Herdr. Use exact session targeting even when two sessions share the same cwd.

Leave the tab open for direct user conversation. Persistence requires a running Pi process and Zellij session; after a restart, refresh both rosters instead of assuming old IDs are live. Closing by stable tab ID is destructive: confirm it is disposable and inspect it first; never use a focus-dependent close command for cleanup.

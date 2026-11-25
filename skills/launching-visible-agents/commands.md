# Visible agent command reference

Read the `using-baton` skill for session selection, ownership and pane interaction rules. Use local help to check baton and your agent's flags. The examples use Bash for the calling shell. Substitute the verified session, directory, agent launcher, model, reasoning and prompt.

## Start in a new tab

```bash
baton --session "$session" run --name "$name" --new-tab "$tab_name" --cwd "$workspace" --agent pi -- \
  pi --name "$name" --model "$model_with_reasoning" "$prompt"

baton --session "$session" run --name "$name" --new-tab "$tab_name" --cwd "$workspace" --agent claude -- \
  claude --name "$name" --model "$model" --effort "$effort" "$prompt"
```

Run only the line for your harness. Pass one argument per word after `--`; do not pass a pre-quoted shell command. Baton selects the new tab's shell and quotes the words for it. On Windows, a supported shell can start a local Node-based Pi launcher by passing `node /path/to/launch.mjs` in place of `pi`, while keeping `--agent pi`. Do not use a Bash or Windows launcher path in another environment.

`run` submits the command to the new tab's shell, not as the tab's initial command. It does not prove that shell startup finished or that the agent is ready. Use the returned pane ID with `baton read "$pane" --lines 40`. Use `baton list --owned` to verify the pane record. Keep using the same `--session` when it is not the default.

## Peer messages and terminal turns

For Pi, put your intercom address in the readiness prompt. Use the intercom tool to find the exact named session and send a ping. For Claude Code, find your own peer name with `ListAgents` before launch, include it in the readiness prompt, then find the peer with `ListAgents` and ping with `SendMessage`. Verify the reply before task dispatch. Peer messaging is local to the harness and environment; do not assume native Windows peers can reach WSL peers.

When deliberately submitting a terminal turn instead, use the same recorded pane for both calls:

```bash
baton send "$pane" "$prompt" && baton wait "$pane" --timeout 600
```

A failed send does not start a wait. Handle wait exit codes `0`, `1`, `2`, `124` and `3` as specified by `using-baton`. `0` means the turn reached `done` or `idle`, not that the task passed. Do not substitute `baton status` for `baton wait` after a send.

## Native Windows Nushell exception

For the existing native Windows Pi route with Nushell as the preferred shell, keep shell-first Zellij submission. Baton does not have a Nushell quoting adapter; it falls back to POSIX quoting, which cannot safely represent arbitrary prompt arguments in Nushell. Do not change the preferred shell or assume this exception applies to Claude Code. This pane is not baton-owned; use intercom for turns, not forced baton sends.

Open a shell-only tab as in [using-zellij](../using-zellij/commands.md#new-tab-with-the-normal-shell). Record the returned tab ID. From the pane list, select the terminal in that exact tab. Verify its Nushell prompt and cwd before sending input. If the cwd is wrong, stop; do not send the agent command into the wrong workspace. Check installed help and target the same Zellij session throughout. For example, from Bash:

```bash
zellij action write-chars --pane-id terminal_123 -- 'node "C:/path/to/dotfiles/pi/windows-fullscreen-mouse/launch.mjs" --name my-app-review --model "MODEL_WITH_REASONING" "Report readiness via intercom to SUPERVISOR_SESSION_ID. Do not edit. Wait for the task."'
zellij action write --pane-id terminal_123 13
```

Discover the local fullscreen mouse launcher rather than installing one. Quote the command first for Nushell, then for the calling shell. This example uses unquoted `node` on PATH; for a quoted executable in Nushell, use the external command operator `^`. Use `baton read terminal_123` to inspect startup, then verify readiness through intercom as above.

## Verify shell lifecycle

With approval for a disposable tab, exit only its disposable agent using the agent's supported exit interaction. Inspect for the normal shell prompt in that same pane. Run a harmless marker such as `echo PI_SHELL_RETURNED` and confirm the output. Then exit the disposable shell and verify the tab disappears instead of becoming held. Use the route's pane-targeted interaction, or ask the owner to do the exit test if it cannot safely send the required input. Record the platform and limits; no platform's result proves another's behavior.

## Cleanup

For a baton-owned pane, verify its identity and disposability, then use `baton close "$pane"`. Closing the last pane normally removes its tab. Verify removal. If the tab remains, baton has no tab-close verb. For a tab from the Nushell exception, baton does not own the pane. In these cases use Zellij for cleanup. Inspect `zellij action list-tabs --all --json` and `zellij action list-panes --all --json` in the intended session. Only if the recorded tab and all its remaining contents are verified as owned and disposable, use `zellij action close-tab --tab-id <recorded-tab-id>`. If ownership is unclear, stop and report. Verify that the tab is gone.

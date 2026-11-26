# Visible agent command reference

Read the `using-baton` skill for session selection, ownership and pane interaction rules. Use local help to check baton and your agent's flags. The examples use Bash for the calling shell. Substitute the verified session, directory, agent launcher, model, reasoning and prompt.

## Start in a new tab

```bash
baton --session "$session" run --name "$name" --new-tab "$tab_name" --cwd "$workspace" --agent pi -- \
  pi --name "$name" --model "$model_with_reasoning" "$prompt"

baton --session "$session" run --name "$name" --new-tab "$tab_name" --cwd "$workspace" --agent claude -- \
  claude --name "$name" --model "$model" --effort "$effort" "$prompt"
```

Run only the line for your harness. Pass one argument per word after `--`; do not pass a pre-quoted shell command. The new tab runs this command directly, so no shell parses it: any default shell (Bash, fish, Nushell, PowerShell, cmd.exe) works. On Windows, start a local Node-based Pi launcher by passing `node /path/to/launch.mjs` in place of `pi`, while keeping `--agent pi` (baton 0.1.4 and later; earlier versions put `--session-id` before the script and Node refuses it). Do not use a Bash or Windows launcher path in another environment.

`run` starts the command as the tab's own program (baton 0.1.1 and later). There is no shell behind the agent: when the agent exits, the pane shows it as exited until you close it. `run` does not prove that the agent is ready. Use the returned pane ID with `baton read "$pane" --lines 40`. Use `baton list --owned` to verify the pane record. Keep using the same `--session` when it is not the default.

## Peer messages and terminal turns

For Pi, put your intercom address in the readiness prompt. Use the intercom tool to find the exact named session and send a ping. For Claude Code, find your own peer name with `ListAgents` before launch, include it in the readiness prompt, then find the peer with `ListAgents` and ping with `SendMessage`. Verify the reply before task dispatch. Peer messaging is local to the harness and environment; do not assume native Windows peers can reach WSL peers.

When deliberately submitting a terminal turn instead, use the same recorded pane for both calls:

```bash
baton send "$pane" "$prompt" && baton wait "$pane" --timeout 600
```

A failed send does not start a wait. Handle wait exit codes `0`, `1`, `2`, `124` and `3` as specified by `using-baton`. `0` means the turn reached `done` or `idle`, not that the task passed. Do not substitute `baton status` for `baton wait` after a send.

## Verify the launch route

With approval for a disposable tab, start a disposable agent as above, check readiness, then exit only that agent with its supported exit interaction. Check that the pane shows the program as exited, then run `baton close "$pane"` and verify that the tab disappears. Record the platform and limits; no platform's result proves another's behavior.

## Cleanup


For a baton-owned pane, verify its identity and disposability, then use `baton close "$pane"`. Closing the last pane normally removes its tab. Verify removal. If the tab remains, baton has no tab-close verb. In that case use Zellij for cleanup. Inspect `zellij action list-tabs --all --json` and `zellij action list-panes --all --json` in the intended session. Only if the recorded tab and all its remaining contents are verified as owned and disposable, use `zellij action close-tab --tab-id <recorded-tab-id>`. If ownership is unclear, stop and report. Verify that the tab is gone.

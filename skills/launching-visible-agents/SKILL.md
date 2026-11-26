---
name: launching-visible-agents
description: >
  Use when launching a visible Pi or Claude Code agent in a new Zellij tab, or recovering one.
---

# Launching visible Pi and Claude Code agents

Use the `using-baton` skill (installed from the baton repo) for agent control. Use pi-intercom for messages between Pi sessions and `ListAgents` / `SendMessage` for Claude Code. Launch peers of your own harness.

A new visible Zellij tab means a persistent interactive peer. Do not substitute a headless subagent, an arbitrary session at the same cwd, or intercom's Herdr-specific `openProjectPaneIfMissing` helper. The user must be able to switch tabs and continue the conversation.

For workspaces, ownership, handoff and recovery, read `delegating-independent-work`.

## Discover and launch

1. Read `using-baton`, [commands.md](commands.md) and your harness's messaging rules. Verify the intended Zellij session, installed versions, and local launcher options. Missing baton or a session that cannot open a tab blocks this route. Do not silently switch launch surfaces.
2. Choose the cwd. Before concurrent edits, create a repository-native workspace. No new workspace is needed for an idle or read-only peer.
3. Choose the session name, model and reasoning from the task or policy. Follow [using-zellij](../using-zellij/SKILL.md) for tab names. Preserve the local interactive launcher, including the existing Node launcher if needed on Windows. Use the Linux/WSL launcher in Linux/WSL.
4. Use `baton run --new-tab` with the harness and agent command from [commands.md](commands.md). The tab runs the agent directly, without a shell, so every default shell (including Nushell on Windows) works. When the agent exits, the pane stays as an exited program until `baton close`. Do not use `--close-on-exit`, or print, JSON, RPC, no-session or shell-background mode. Keep the extensions needed for messaging enabled.
5. Record the Zellij session, tab and pane IDs and the agent session ID. Inspect the exact pane and verify the cwd and launcher. A new tab does not prove the peer is ready.

## Verify, then delegate

- Use the initial prompt to request readiness. Verify a two-way ping through peer messaging and check the peer's reported cwd, effective model/reasoning and session/pane identity. Refresh the roster and address the exact peer before sending the task; the agent, intercom, tab and pane IDs are not interchangeable.
- Send the task, constraints, workspace, expected report and permission boundaries. Keep the peer interactive until work and handoff are done. Tell the user the tab name and session identity.
- For a turn submitted through the pane, send with `baton send`, then use `baton wait`. Do not use pane state as proof of a peer message or Beads handoff.

### Dispatch through Beads

For a role with a Beads handoff, put the role instructions, exact bead ID and store selection in the initial prompt instead of sending a readiness ping and a separate task. Tell the peer to verify its cwd, model and reasoning before it claims or edits, and to record its session on the bead. Verify startup in the recorded pane and the matching claim in Beads. If they disagree or the claim does not appear, inspect startup and ownership before retrying. Use the peer roster for questions or intervention.

## Verify lifecycle and recover

- To validate a new route, get approval for a disposable tab. Follow [the route check](commands.md#verify-the-launch-route). Do not test exit on a live user peer.
- If startup is slow or fails, inspect the recorded pane and refresh the peer roster before you retry. If launch fails before it returns IDs, check for a partially created tab; do not guess ownership or create a duplicate.
- After acceptance, the lifecycle owner preserves the handoff, explains the impact, and closes the owned pane with `baton close` unless the user wants to keep it. Check that the tab is gone. If it remains, follow [cleanup](commands.md#cleanup). After a restart, verify the recorded IDs against both rosters before you act.

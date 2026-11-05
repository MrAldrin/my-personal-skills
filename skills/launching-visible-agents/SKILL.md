---
name: launching-visible-agents
description: >
  Use when launching a visible Pi or Claude Code agent in a new Zellij tab, or recovering one.
---

# Launching visible Pi and Claude Code agents

This skill is the glue between a requested visible peer and the Zellij mechanics in [using-zellij](../using-zellij/SKILL.md). **Zellij** is the multiplexer. **WezTerm** may host its terminal. **Intercom** carries messages between Pi sessions; Claude Code sessions use built-in `ListAgents`/`SendMessage` instead. The procedure is the same for both; [commands.md](commands.md) holds the harness-specific launch and messaging lines. Launch peers of your own harness.

Honor the requested surface: a new visible Zellij tab means a persistent interactive Pi peer, not a headless subagent or reuse of an arbitrary session in the same directory. The user can switch tabs and continue that conversation directly.

For independent task ownership, workspace naming, durable status, handoff, and cleanup, use `delegating-independent-work`.

## Discover and launch

1. In Pi, read the pi-intercom skill for messaging; in Claude Code, load `ListAgents` and `SendMessage`. For an explicitly requested Zellij peer, use this launch procedure rather than intercom's Herdr-specific `openProjectPaneIfMissing` helper. Herdr is a separate launcher integration, not a prerequisite for intercom; pi-intercom's Herdr fallback warning does not apply to a user-authorized Zellij tab.
2. Inspect the environment, executable locations, Zellij version and live session as [using-zellij](../using-zellij/SKILL.md) describes. Environment variables alone do not prove connectivity.
3. Read [commands.md](commands.md). Inspect installed command help before launching: flags vary by version. Do not switch to WezTerm tabs, create a nested multiplexer, or use another machine's paths as a fallback.
4. Choose the intended working directory. For concurrent edits, establish repository-native isolation first; do not run version-control mutations concurrently in one working copy. An idle/read-only peer needs no new workspace.
5. Discover the local interactive Pi launcher. Inspect an existing Pi pane's command if needed. On Windows, a `.cmd` shim may need a command interpreter; an existing Node launcher can be invoked directly. Preserve established local launcher workarounds. On Linux/WSL use that environment's launcher, not Windows paths.
6. Create one new tab for the peer, named and verified as [using-zellij](../using-zellij/SKILL.md) describes. The normal interactive preferred shell must start first. If the default is not the preferred shell, resolve that mismatch before launching Pi; do not change terminal configuration as a shortcut.
7. Submit the locally discovered Pi command as a foreground child to that exact owned pane, using the shell's quoting rules and explicit pane-targeted input from [commands.md](commands.md). Include the tab name as the session name (`--name`), model/reasoning and short readiness prompt. Do not replace the shell (`exec` or equivalent), launch Pi directly as the tab command, or use `--close-on-exit` as a substitute: exiting Pi must return to the shell prompt, not a Zellij held-command screen. Closing the pane on Pi exit is not an equivalent substitute. Do not use print, JSON, RPC, no-session, or shell-background mode. Do not disable extensions needed for intercom.

## Verify, then delegate

- Record the returned tab ID and inspect its pane ID, command, cwd, and screen. A created tab is not proof of a ready agent.
- Ping first: ask the peer to report its session ID, effective model/reasoning, cwd and Zellij session/pane variables through intercom, then wait. Select model/reasoning from the explicit request or applicable environment policy, and verify the effective selection. Inspect failed startup before retrying; avoid duplicate peers.
- Refresh intercom `list`. Target the exact peer session, not cwd alone when multiple sessions share it. Intercom session IDs and Zellij tab/pane IDs are different namespaces. A missing Herdr location does not invalidate a Zellij peer.
- Verify a two-way ping, using pi-intercom's messaging rules.
- Then send the task, constraints, isolation details, expected report, and permission boundaries for edits/subagent fanout. Leave the peer interactive afterward. Report its tab name and session identity so the user can take over.

## Verify shell lifecycle

When validating a new launch route, obtain approval for one disposable test tab. Verify Pi starts inside its normal shell, exit only that disposable Pi, and confirm the shell prompt can run a harmless marker command. Then exit that disposable shell and verify its pane closes normally. Target the recorded stable pane throughout; never test exit on a live user peer. Record the tested platform and limitations; native Windows results do not establish Linux/WSL behavior.

Leave successful peers open for the user. Persistence requires a running Pi process and Zellij session; after restart refresh both rosters.

## Failure handling

`HERDR_UNAVAILABLE` proves only that the Herdr helper failed. Check Zellij and the local launcher before declaring visible delegation blocked. If Zellij itself is unavailable, report the exact check and ask before choosing a different surface.

On startup delay, inspect the pane and roster before retrying. Do not send keystrokes to whichever pane happens to be focused. Close only explicitly disposable test tabs with authorization and a verified stable ID.

---
name: using-zellij-with-intercom
description: >
  Use when the user wants another agent in a visible Zellij tab or pane,
  wants to keep talking directly to a delegated agent, or asks to use intercom
  instead of subagents in their terminal multiplexer. Also use when intercom's
  Herdr launcher fails but an existing Zellij session may be available.
---

# Visible Pi peers in Zellij

**Zellij** is the multiplexer. **WezTerm** may host its terminal. **Intercom** carries messages between Pi sessions. **Herdr** is a separate launcher integration, not a prerequisite for intercom.

Honor the requested surface: a new visible Zellij tab means a persistent interactive Pi peer, not a headless subagent or reuse of an arbitrary session in the same directory. The user can switch tabs and continue that conversation directly.

For independent task ownership, workspace naming, durable status, handoff, and cleanup, use `delegating-independent-work`; use this skill for Zellij launch and verification.

## Discover and launch

1. Read the pi-intercom skill for messaging. For an explicitly requested Zellij peer, use this skill's launch procedure rather than intercom's Herdr-specific `openProjectPaneIfMissing` helper. The pi-intercom skill's Herdr manual-fallback warning does not make Herdr necessary for a user-authorized Zellij tab.
2. Inspect the environment, executable locations, Zellij version, and live session. Check `ZELLIJ_SESSION_NAME` and `ZELLIJ_PANE_ID`; confirm connectivity with Zellij's tab/pane listing commands. Environment variables alone do not prove connectivity.
3. Read [commands.md](commands.md). Inspect installed command help before launching: flags vary by version. Do not switch to WezTerm tabs, create a nested multiplexer, or use another machine's paths as a fallback.
4. Choose the intended working directory. For concurrent edits, establish repository-native isolation first; do not run version-control mutations concurrently in one working copy. An idle/read-only peer needs no new workspace.
5. Discover the local interactive Pi launcher. Inspect an existing Pi pane's command if needed. On Windows, a `.cmd` shim may need a command interpreter; an existing Node launcher can be invoked directly. Preserve established terminal workarounds. On Linux/WSL use that environment's launcher, not Windows paths.
6. Create one named tab with an explicit cwd, interactive Pi command, unique session name, model/reasoning, and short readiness prompt. Use no-focus where supported. Do not use print, JSON, RPC, no-session, or shell-background mode. Do not disable extensions needed for intercom.

## Verify, then delegate

- Record the returned tab ID and inspect its pane ID, command, cwd, and screen. A created tab is not proof of a ready agent.
- Ask the peer to report its session ID, effective model/reasoning, cwd and Zellij session/pane variables through intercom, then wait. Start with `github-copilot/claude-haiku-5.5:medium` unless another model was requested; on failure retry with `github-copilot/gpt-6.1-sol:low`. Inspect failed startup before retrying; avoid duplicate peers.
- Refresh intercom `list`. Target the exact peer session, not cwd alone when multiple sessions share it. Intercom session IDs and Zellij tab/pane IDs are different namespaces. A missing Herdr location does not invalidate a Zellij peer.
- Verify a two-way ping. Use `send` for nonblocking messages; reserve `ask` for a required answer and `reply` for an actual pending ask. Do not attach an ordinary send's ID as `replyTo`.
- Send the task, constraints, isolation details, expected report, and permission boundaries for edits/subagent fanout. Leave the peer interactive afterward. Report its tab name and session identity so the user can take over.

## Failure handling

`HERDR_UNAVAILABLE` proves only that the Herdr helper failed. Check Zellij and the local launcher before declaring visible delegation blocked. If Zellij itself is unavailable, report the exact check and ask before choosing a different surface.

On startup delay, inspect the pane and roster before retrying. Do not send keystrokes to whichever pane happens to be focused. Leave successful peers open for the user; close only explicitly disposable test tabs with authorization and a verified stable ID.

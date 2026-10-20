---
name: delegating-independent-work
description: >
  Use when delegating an independent task to another agent, arranging parallel
  editing workspaces, or recovering ownership, handoff, and cleanup after an
  agent session ends.
---

# Independent task ownership (experimental)

Keep small, bounded tasks with the parent and its subagents. Give large independent tasks a visible peer session that the user can visit directly. Work within the user's approved scope; delegation passes that authority, not new permissions.

## Agree ownership

- Give each task one owner, a clear outcome, edit boundaries, permission for any child agents, and a completion target. Default to review-ready results; integration requires explicit user permission.
- The parent owns ordinary subagents and their cleanup. Transfer independent task ownership from the launching parent to the verified peer in the record. That peer owns its task, workspace, children (including its own subagents), and cleanup, and continues if the launching chat closes.
- Record the task in the repository's existing backlog entry or linked task document. Honor its queue headings. Keep the durable record authoritative; messages to the launching chat are optional, as agreed ("take X independently" or "take X and report back here").

## Prepare the workspace and peer

- Give concurrent editing agents separate repository-native workspaces, preferably jj. Read-only agents need no mandatory workspace.
- Match an agent-managed workspace name and its folder basename: `tmp-<short-task-descriptor>`, without a random suffix. On collision, inspect the existing task and ownership before choosing whether to resume, coordinate, or use a distinct task descriptor.
- Record ownership before handing over work. Treat the name as a visual cue; use the durable record as cleanup authority. Leave user-managed workspaces under user management.
- Use `using-zellij-with-intercom` for a requested Zellij peer's launch and readiness verification, and `pi-intercom` for messaging. Hand over the task, workspace, authority, and durable record location. Keep successful interactive peers available to the user.

## Keep a recoverable record

Keep this compact information in the existing task entry or its linked document:

- Task/outcome; owner and session identity; repository, workspace name and path; whether agent- or user-managed.
- Child agents/workspaces and their owners; current status (such as active, blocked with a reason, or ready-for-review); next action and reporting agreement.
- Result/change IDs, checks and limitations, handoff location, and cleanup disposition.

Update it at ownership changes, meaningful checkpoints, and closeout. Retain the record or move it to a linked handoff before removing a finished backlog entry; keep review and cleanup work tracked while outstanding. If interrupted, the next responsible agent inspects the record and actual workspace/child state, then records a confirmed ownership transfer before resuming or cleaning up. Ask the user when ownership or authority remains unclear.

## Finish and clean up

Preserve review-ready results, stable change IDs, checks, and a usable handoff before cleanup. Verify results remain reachable without the temporary workspace. Resolve active children and use repository-native removal only for confirmed agent-owned resources whose work is preserved. Record what was retained or removed. Keep independent visible sessions open for the user; workspace cleanup and closing a conversation are separate decisions.

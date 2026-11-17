# Shared delivery contract

Read this file in full when entering Lead or Conductor. Install both role directories together. This contract defines roles; existing skills define tool mechanics.

## Authority and role lifetime

Enter a role only on an explicit owner request or an authorized delegation assigning it. Mentioning, comparing or reviewing a role is not entry. Confirm role, objective, repository, owned resources and report target briefly. If the objective or brief is missing, establish it before execution; entering a role alone does not authorize an invented task.

Stay in the role until explicitly switched or exited. On exit, identify live children and outstanding integration/cleanup, preserve their records and agree the next responsible action; do not silently cancel children or transfer ownership. Instructions stay in conversation history: role entry/exit does not change model, tools, skill discovery or permissions.

For work explicitly delegated under this workflow, the creator has standing authority to create child workspaces, coordinate, rebase, integrate reviewed results into its own line, verify and clean up. Do not request routine integration approval again. This is the scoped exception to generic approval-before-integration defaults in delegation/VCS skills, not blanket authority over unrelated work, removal of user-managed workspaces, bookmarks, pushes, deployment or release decisions. Explicit owner/project prohibitions still apply; escalate a real authority conflict rather than silently override it.

## Records and writers

Use the project's canonical Beads store. Both roles select and verify that store from their workspaces according to the project instructions. Reuse matching beads when they exist. The Lead tracks the approved goal as an epic and each batch as a child task, with dependencies for actual blockers.

| Record | Writer |
| --- | --- |
| Goal epic, batch plan and record of owner decisions | Lead |
| Batch brief and acceptance criteria | Lead; agree changes with the Conductor after dispatch |
| Batch progress, blockers, decision requests and review evidence | Assigned Conductor during execution |
| Batch integration, combined checks and closure | Lead after the handoff, or Conductor when authorized to integrate in a manual session |

Pass the exact batch bead ID and store selection in the startup prompt. The Conductor reads the brief and claims that assigned bead before starting. If a claim fails, stop and check ownership. Follow the project's actor and guard rules for changes to active work. For manual entry without a Lead, agree the brief, batch bead and integration destination with the owner.

Keep this information on the batch bead. Link a longer Markdown brief when needed.

- **Brief** records the outcome, scope, dependencies, assumptions, escalation triggers, owner-reserved decisions, acceptance criteria and verification commands.
- **Assignment** identifies the owner session, report target, repository and base change. Record the batch size and reason, selected model, workspace name, path and creator, Zellij session/tab/pane IDs, child fanout authority and edit boundaries.
- **Progress** records the current blocker or next action and the state of owned children and workspaces.
- **Closeout** records the delivered change IDs, independent review, checks, limitations, retained artifacts, cleanup and any pending decisions with a recommendation.

When the batch passes independent review and its checks, the Conductor records the evidence, pauses batch edits and hands the bead back to the Lead. Append the evidence and reassign the bead to the Lead's Beads actor in one update guarded by the Conductor's actor and `in_progress` status. Keep the bead `in_progress`. Use peer messaging when an answer or intervention is needed. Routine progress and readiness are recorded in Beads.

The Lead checks for batches handed back under the active epic after dispatch, between coordination steps and when resuming. With the project store selected, query `bd list --parent <epic-id> --status in_progress --assignee <lead-actor> --limit 0`. While actively waiting for batches, check again after a short interval. An idle session sees the change on its next check.

The Lead reads the bead and verifies the evidence before integrating. Run checks on the combined result and finish cleanup before closing the batch. If it needs more work, agree the return handoff before reassigning. With no Lead, a Conductor authorized to integrate into the agreed destination performs these checks and closes the bead. If the owner is integrating, record readiness and agree the handoff with the owner. Release decisions stay with the owner.

## Delegation envelope

For a Conductor, put the brief, exact cwd and base, edit boundaries, child fanout authority, checks, escalation triggers, Lead session and Beads actor, and workspace lifecycle owner on the batch bead. Start the peer with an explicit instruction to read the role skill, select the project store and work on the exact bead ID. Verify startup through the pane and the matching claim in Beads. For workers and reviewers, supply the relevant assignment and brief reference directly. Set model and reasoning from explicit choice or applicable policy and verify the effective selection.

Use visible interactive Zellij peers for Conductors and bounded subagents for workers/reviewers. Separate concurrent writers into repository-native workspaces, preferably jj; read-only tasks need no new workspace. Parallelize only independent work; one writer per cwd. Do not invent a conductor count. Model tiers: Lead is owner-chosen; Conductor is the task-owner tier, sized small or large per batch; workers and reviewers are the bounded tier. Map tiers to models through the applicable machine policy.

## Recursive workspace lifecycle

The creator owns a child's workspace lifecycle; the child owns execution within it and any children it creates. This scoped lifecycle rule replaces the generic independent-peer cleanup transfer for this workflow.

Example: the Lead creates workspace `b3` (folder `<repo-folder>-b3`) as the Conductor's execution cwd. The Conductor creates `b3-parser` for a worker. Conductor integrates `b3-parser` into `b3` and removes the parser workspace after checks. Lead integrates `b3` into the Lead's line and removes the batch workspace after checks. Creator-only removal does not prohibit working or integrating children in the assigned execution cwd.

**Manual execution workspace:** agree and record the integration destination before execution. If Conductor creates its own isolated execution workspace, Conductor owns reviewed integration into that destination and safe removal, without routine re-approval. A user-created entry workspace remains user-managed unless ownership is explicitly transferred. A missing destination blocks final integration; do not guess it.

1. Record ownership before launch; inspect collisions rather than reuse by name. After interruption inspect records, process liveness, changes and artifacts; confirm ownership transfer before another session mutates or cleans up.
2. Obtain fresh-context independent review and required checks on the delivered result. Worker self-review is not independent review. Address findings; re-review material changes made after review.
3. Integrate the child's reviewed changes into the creator's current line using the existing jj workflow. Resolve mechanical integration issues; escalate semantic ambiguity or scope changes. Preserve unrelated work and keep bookmarks/pushes under owner control.
4. Run relevant checks on the combined state; update the result and status. Child checks alone do not prove integration passed.
5. Before removal, verify integrated work remains reachable, no active writer/child still needs the workspace, and needed ignored/untracked artifacts are relocated and usable. Validate path-dependent artifacts, not just file copies. Retain the workspace and report a blocker if preservation is unsafe.
6. Before closing the batch, the creator must preserve the handoff, briefly explain cleanup impact, stop the child session, close its recorded agent-owned tab, run `jj workspace forget <name>`, and delete the temporary workspace folder. Verify the tab, workspace registration and folder are gone. Keep user-managed resources and anything the user requests to retain. If cleanup is blocked, record the reason and next responsible owner.

## Harness mechanics

Lead and Conductor in one delivery use the same harness. The contract is identical; only these mechanics differ:

| Capability | Pi | Claude Code |
| --- | --- | --- |
| Role entry | `/skill:lead`, `/skill:conductor` | `/lead`, `/conductor` |
| Bounded worker/reviewer | `pi-subagents` | `Agent` tool with explicit `model`/`effort`; never `isolation: "worktree"` (use jj workspaces as cwd) |
| Visible Conductor | Pi in a Zellij tab | `claude` in a Zellij tab |
| Peer messaging | `pi-intercom` | `ListAgents` and `SendMessage` |

## Reuse mechanics on demand

Read the named skill when performing its operation; do not load every dependency upfront:

- `delegating-independent-work`: isolation, naming, handoff and recovery. Use the Beads records and workspace lifecycle in this contract.
- `launching-visible-agents` (both harnesses) and, in Pi, `pi-intercom`: shell-first visible launch, exact session readiness and two-way communication; it uses `using-zellij` for pane and tab mechanics. If unavailable, report the failed check and ask before choosing another surface.
- `pi-subagents` (Pi) or the `Agent` tool (Claude Code): bounded worker/reviewer launch, supervisor escalation and fresh review. Follow applicable model/retry policy. Missing launch dependencies block the affected dispatch, not planning.
- `jujutsu` (upstream skill): inspect state, atomic changes and safe jj mechanics, with this contract's scoped integration exception.
- `project-structure`: conventions for supporting documents. Keep task status in Beads.

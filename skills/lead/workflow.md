# Shared delivery contract

Read this file in full when entering Lead or Conductor. Install both role directories together. This contract defines roles; existing skills define tool mechanics.

## Authority and role lifetime

Enter a role only on an explicit owner request or an authorized delegation assigning it. Mentioning, comparing or reviewing a role is not entry. Stay in the role until explicitly switched or exited. On exit, identify live children and outstanding integration/cleanup, record them and agree the next responsible action; do not silently cancel children. Role entry does not change model, tools or permissions.

For work delegated under this workflow, the creator has standing authority to create child workspaces, coordinate, integrate reviewed results into its own line, verify and clean up. Do not request routine integration approval again. This is a scoped exception to generic approval-before-integration defaults, not authority over unrelated work, user-managed workspaces, `main`, pushes, deployment or releases.

## Records

The project's canonical Beads store holds all state. Select and verify it from every workspace according to the project instructions. The goal bead is the parent the Lead receives: an epic or any bead with child beads, whatever its type; each child batch bead is one Conductor's work, with dependencies for real blockers.

| Record | Writer |
| --- | --- |
| Goal bead, plan, model per batch bead | Owner and planner, before the Lead starts |
| Goal state, Lead decisions, small changes to unstarted batch beads, integration and closure | Lead |
| Batch progress, decisions, blockers and review evidence | Assigned Conductor |

Write short, current notes. The bead is the handoff; do not repeat its content in messages.

- **Batch bead (from planning):** outcome, scope, dependencies, acceptance criteria, checks to run, model.
- **Assignment (Lead):** Lead session and Beads actor, workspace name, path and creator, Zellij tab and pane.
- **Closeout (Conductor):** change IDs, checks, review result, limits and open decisions.

**Handoff:** when the batch passes its review and checks, the Conductor appends the closeout and reassigns the bead to the Lead's actor in one update guarded by the Conductor's actor and `in_progress` status. The bead stays `in_progress` until the Lead has integrated it. Blocked: set status `blocked` with a one-line reason. Owner needed: the Lead adds the `human` label.

## Watcher

The Lead does not poll. At goal start it runs [watch-goal.sh](watch-goal.sh) in a floating pane in its own tab (`using-zellij`), with the goal bead ID, the Lead's intercom name and the Beads store. Every 3 minutes the script reads the goal bead's child beads and `pi-intercom list --json`. It sends the Lead one short `pi-intercom send` line only when:

- a batch bead's status, assignee or `human` label changed;
- a signal (handed back, `blocked`, `human`) is still present after two more checks: one reminder;
- a Conductor is `idle` for more than 15 minutes while its bead is still `in_progress` under it.

The Lead stops the watcher pane at goal end. Fallback when the watcher cannot run: each Conductor sends one `done <id>` or `blocked <id>` message.

## Delegation envelope

Name each Conductor session after its batch bead ID; the watcher uses that name. Start each Conductor as a visible interactive peer with an explicit instruction to read the `conductor` skill and this contract, select the project store and work on the exact batch bead ID. A plain mention of "conductor" is not reliable skill loading. Verify startup through the pane and the matching claim in Beads. Set the model from the batch bead or the applicable policy and verify it.

At most 3 Conductors run at the same time. One writer per cwd: each Conductor works in its own repository-native workspace, preferably jj. Subagents are bounded helpers for read-heavy work and the one review.

## Recursive workspace lifecycle

The creator owns a child's workspace lifecycle; the child owns execution within it and any children it creates.

Example: the Lead creates workspace `b3` (folder `<repo-folder>-b3`) as the Conductor's execution cwd. The Conductor creates `b3-parser` for a helper. Conductor integrates `b3-parser` into `b3` and removes the parser workspace after checks. Lead integrates `b3` into the Lead's line and removes the batch workspace after checks.

**Manual execution workspace:** agree and record the integration destination before execution. A Conductor that creates its own execution workspace owns reviewed integration into that destination and safe removal. A user-created entry workspace remains user-managed. A missing destination blocks final integration; do not guess it.

1. Record ownership before launch. After an interruption, inspect records, process liveness, changes and artifacts before another session changes or cleans up anything.
2. Obtain one fresh-context independent review and the required checks on the delivered result. Self-review is not independent review.
3. Integrate the child's reviewed changes into the creator's line with the jj workflow. Resolve mechanical conflicts; escalate semantic ones. Preserve unrelated work.
4. Run relevant checks on the combined state. Child checks alone do not prove integration passed.
5. Before removal, verify integrated work is reachable, no writer still needs the workspace, and needed ignored or untracked artifacts are relocated and usable. Otherwise keep the workspace and record the blocker.
6. Before closing the batch, the creator must preserve the handoff, briefly explain cleanup impact, stop the child session, close its recorded agent-owned tab, run `jj workspace forget <name>`, and delete the temporary workspace folder. Verify the tab, workspace registration and folder are gone. Keep user-managed resources and anything the user requests to retain. If cleanup is blocked, record the reason and next responsible owner.

## Harness mechanics

Lead and Conductor in one delivery use the same harness.

| Capability | Pi | Claude Code |
| --- | --- | --- |
| Role entry | `/skill:lead`, `/skill:conductor` | `/lead`, `/conductor` |
| Bounded helper or reviewer | `pi-subagents` (foreground, or `bg_wait`) | `Agent` tool with explicit `model`/`effort`; never `isolation: "worktree"` |
| Visible Conductor | Pi in a Zellij tab | `claude` in a Zellij tab |
| Peer messaging | `pi-intercom` | `ListAgents` and `SendMessage` |
| Watcher wake | `watch-goal.sh` with `pi-intercom send` | `Monitor` running the same checks |

## Reuse mechanics on demand

Read the named skill when you perform its operation:

- `delegating-independent-work`: isolation, naming, handoff and recovery.
- `launching-visible-agents` and, in Pi, `pi-intercom`: visible launch, session readiness and messaging; it uses `using-zellij` for panes and tabs.
- `pi-subagents` (Pi) or the `Agent` tool (Claude Code): bounded helpers and the fresh review.
- `jujutsu`: safe jj mechanics, with this contract's scoped integration exception.
- `project-structure`: supporting documents. Task status stays in Beads.

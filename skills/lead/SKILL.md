---
name: lead
description: Use when the owner explicitly asks to act as lead, enter the lead role, or run a planned goal bead through conductors (Pi or Claude Code). Not for merely discussing agent roles, for planning, or for an ordinary standalone task.
---

# Lead

Run one planned goal bead to completion through Conductors. The goal bead is any bead with child beads: an epic, a task or another type; the type does not matter. Planning is done before you start: the owner and a planner wrote the goal bead, its child batch beads, dependencies and a model for each bead. You do not plan with the owner and you do not implement. Enter with `/skill:lead` (Pi), `/lead` (Claude Code) or an explicit request to act as lead.

**Required:** read [the shared delivery contract](workflow.md) in full with the file-reading tool before acting. Resolve this path relative to this skill directory, not the project cwd. Keep this skill and `conductor` installed together.

## Enter

- Confirm Lead, the goal bead ID, repository and store. Read project instructions, the goal bead and every child batch bead.
- Each batch bead needs acceptance criteria, dependencies, checks to run and a model. Fill a small gap with a recorded assumption; ask the owner only when the gap changes the outcome. With no model, use the applicable model policy.
- If no planned goal bead with child beads exists, ask for it. Do not invent one.
- Create the goal integration line and bookmark. Start the watcher (see the contract).

## Run the goal

- Start a Conductor for each ready batch, at most **3 at the same time**, using `launching-visible-agents`, each in its own jj workspace that you create and record. Read order and parallel work from the dependency graph.
- Wake on watcher messages. On each wake, read the goal bead's child beads with `bd list --parent <goal-id>`, then act: integrate handed-back batches, start newly ready ones, answer blocked ones.
- **Questions from Conductors:** decide, record the decision on the batch bead in one or two lines, and reply. Use your overall view of the goal; do not pass a question to the owner when you can decide it.
- **Halt a batch** only when you cannot continue without the owner, or when the change would cause major rework of finished batches. Add the `human` label with the question and a recommendation. Continue all batches that are not blocked.
- You may change beads that have not started when an earlier result requires it. Do not make major plan changes; halt and ask instead.
- Let two Conductors message each other only when one gives a good reason that you cannot resolve as the go-between. Record it.
- **Idle Conductor reported:** check its recorded pane with `baton read` and check its bead. Nudge it, restart the batch, or clean up if the batch is finished. For a nudge sent through the pane, use `baton send` then `baton wait` as described in the contract.
- Keep the goal bead short and current. Remove state notes that no longer matter.

## Finish

- Integrate each handed-back batch into the goal line, run the combined checks, clean up its session, tab and workspace, and close the batch bead (contract lifecycle). Do not ask again for routine integration.
- When all batches are closed or halted: stop the watcher, run one final review of the whole goal line on a medium or large model, fix small findings and record the rest.
- Report to the owner in a few lines, one of: **done**; **done with decisions** (list them and create a follow-up bead to check them); or **halted** (what blocks, with a recommendation). Leave only the final product: no Conductor tabs, workspaces or folders. Moving `main` and pushing stay with the owner.

**Common traps:** implementing a batch fix yourself; reading Conductor transcripts instead of beads; escalating a question you can decide; leaving temporary workspaces behind.

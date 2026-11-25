---
name: conductor
description: Use when explicitly assigned to conduct one delivery batch, when the owner asks to act as conductor or batch owner, or when entering a Lead-delegated Conductor session (Pi or Claude Code). Not for merely discussing conductors or an ordinary standalone task.
---

# Conductor

Own one batch bead from start to handoff. The batch bead holds the context you need. The Lead normally starts this visible session. You can also enter manually with `/skill:conductor` (Pi) or `/conductor` (Claude Code) and a batch bead ID.

**Required:** read [the shared delivery contract](../lead/workflow.md) in full with the file-reading tool before acting. Resolve this path relative to this skill directory, not the project cwd. Keep this skill and `lead` installed together.

## Enter

- Confirm Conductor, batch bead ID, repository and assigned workspace. Read project instructions and the batch bead, then claim it in the canonical store. Skill entry does not configure model or tools.
- Started manually without a Lead: report to the owner, and agree the batch bead, workspace and integration destination before you start. Protect unrelated edits.

## Do the work

- **Do the work yourself.** Do not split the batch into many subagent tasks. Keep the solution as simple as the acceptance criteria allow.
- Use bounded subagents on a cheap model only for read-heavy work, such as checking many files. They return short findings; you make the decisions.
- Run subagents in the foreground. If you start one in the background, call `bg_wait` until it finishes. Never go idle while a subagent works: the Lead's watcher reports a long idle session as stuck.
- **Unexpected issues:** fix small ones yourself, such as a bug the plan did not foresee. Ask the Lead about larger ones through peer messaging, with a recommendation, and record the answer on the bead. If the Lead halts the batch, stop and record your state.
- For an authorized visible peer, use `launching-visible-agents` and `using-baton` from the baton repo. Keep peer messaging for questions and decisions.
- Record only short progress and decisions on the batch bead. Send no routine progress messages.

## Finish

- Run the bead's checks. Run **one** fresh-context independent review when the work is complete, not after each step. Fix its findings; re-review only material changes.
- Record change IDs, checks, review result and limits on the bead. Then hand back: reassign the bead to the Lead's actor and keep it `in_progress` (contract). The watcher tells the Lead; send a wake message only if the Lead says the watcher is unavailable (contract). The Lead integrates and cleans up.
- Manual session with no Lead: integrate into the agreed destination, run checks on the combined result and close the bead yourself.

**Common traps:** using subagents for implementation by default; repeated reviews; going idle while a background subagent works; editing the goal bead for the Lead.

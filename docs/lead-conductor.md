# Lead and Conductor: minimal role skills

## Start using them

After updating this skill bundle, run `/reload` in Pi. In an ordinary project conversation:

```text
/skill:lead
```

Then discuss the goal and approve the delivery scope. “Act as lead” also triggers the skill; explicit invocation is more reliable. If you only want planning, say so. Role entry alone does not start unspecified work.

The Lead normally creates a jj workspace and launches a visible Conductor in Zellij with the role instructions and batch brief. You do not need to start each Conductor yourself.

For manual entry in a suitable project session:

```text
/skill:conductor Work on B3 using plans/batches/B3.md
```

Without a Lead, the Conductor reports to you and agrees the brief, execution workspace and integration destination first. If it creates that workspace, it owns reviewed integration and safe cleanup; a user-created entry workspace remains user-managed. Say “stop being lead/conductor” or explicitly switch roles to exit. Live children are accounted for, not silently cancelled or abandoned.

These are skills, not new pi-subagents agent definitions or slash-command extensions. They add instructions to the current conversation. They do not strip existing context, change models, restrict tools, or enforce permissions. They do not create `/lead` or `/conductor` aliases.

## Ownership

| Role | Owns |
| --- | --- |
| Lead | Overall planning, briefs, shared backlog, Conductor dispatch, escalations and integration |
| Conductor | One batch, bounded implementation/review workers, batch status and closeout |
| Creator of a child workspace | That child's workspace creation, reviewed integration into its own line, artifact preservation and cleanup |

Routine integration and cleanup are part of the role's standing authority for this delegated work, not repeated permission requests. The Lead owns Conductor workspaces; Conductors own their own children's workspaces. This is a scoped exception to generic delegation/VCS approval and cleanup-ownership defaults, not a change to those skills globally.

Fresh independent review and required checks precede acceptance. Relevant checks also run on the combined state after integration. Needed ignored/untracked artifacts must remain usable after relocation. If safe cleanup is blocked, retain the workspace and report why. Interactive peers remain available to you.

Pushes, bookmark moves, releases, unrelated work and explicit project restrictions do not become authorized by entering a role.

## Package and dependencies

Install/update `lead` and `conductor` **together**. Both require the single [shared delivery contract](../skills/lead/workflow.md); Conductor references it across the sibling skill directories. The existing package manifest ships the whole `skills/` root. Do not copy just the Conductor directory to another machine.

Existing local skills provide mechanics:

- `delegating-independent-work`
- `using-zellij-with-intercom`
- `version-control-workflow`
- `project-structure`

The runtime also needs Pi with `pi-intercom`, `pi-subagents`, Zellij, and jj for this intended setup. Exact models/reasoning come from your current policy or explicit selection; the Lead verifies peer settings. Missing capabilities block the affected dispatch, not discussion/planning. A different terminal or launch surface requires your approval, not a silent fallback.

No launcher, hooks, background scheduler, dashboard, state database or global-policy edits are added. Existing project structure is reused, not automatically migrated.

## Records

Normally use a Lead-owned shared backlog and one `plans/batches/<id>.md` per batch. Existing equivalent records are fine. The contract lists the brief/assignment/status/closeout fields. Conductors update their own status and closeout, never the shared backlog. The brief is frozen at handoff; changes require a coordinated write handoff.

## Evidence and limits

See [verification](lead-conductor-verification.md) for scenario prompts, fresh-agent results and packaging checks. Simulated decisions are evidence of instruction clarity, not proof of end-to-end live multi-agent reliability. Real projects still need observation and iteration.

The [approved design](superpowers/specs/2026-10-27-lead-conductor-design.md) and [implementation plan](superpowers/plans/2026-10-27-lead-conductor.md) preserve this first version's scope. The [earlier research](agent-orchestration.md) is historical background, not the current role contract.

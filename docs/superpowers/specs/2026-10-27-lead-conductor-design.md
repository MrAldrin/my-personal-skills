# Minimal Lead and Conductor skills

Status: approved by the owner on 2026-10-27; implemented by the minimal role skills. See [usage](../../lead-conductor.md) and [verification](../../lead-conductor-verification.md).

## Intent

Make the existing manually tested Lead → Conductor → worker/reviewer workflow explicit and easy to enter. Preserve Pi, Zellij, intercom, pi-subagents and jj. No new orchestration platform.

## Approaches considered

1. Role-specific launch configuration: predictable model, tools and context, but requires choosing the role upfront and maintaining a launcher.
2. In-session role skills: use Pi's existing `/skill:<name>` mechanism; preserves the current conversation and needs little machinery. Role boundaries are instructions, not enforced restrictions.
3. Adopt Herdr/Herdsman: potentially supplies more orchestration, but requires a separate fit evaluation and terminal migration.

Chosen: in-session skills now. Defer launch profiles and platform migration.

## Entry points and files

- `skills/lead/SKILL.md`: enter Lead in an existing session with `/skill:lead`, or a natural-language request to act as lead.
- `skills/conductor/SKILL.md`: enter Conductor with `/skill:conductor` and a brief reference; supports manual startup as well as startup by the Lead.
- Shared workflow instructions in one supporting file, referenced by both skills. Exact location is an implementation choice; references must resolve correctly from each skill directory.
- Explicit entry lasts until the owner switches or exits the role. Role entry confirms responsibilities and identifies missing project context; it does not automatically start work without an objective.
- Loading a skill does not change models, remove tools or unload previous context.

## Responsibilities

### Lead

- Plan the overall goal with the owner and maintain batch briefs and dependencies.
- Normally launch a visible Conductor for each delegated batch, using the existing Zellij/intercom workflow, supplying the Conductor skill and brief.
- Answer escalations within agreed scope; bring reserved or scope-changing decisions to the owner.
- Coordinate rather than implement batch scope. Integration mechanics are coordination.
- Own shared backlog/status updates and shared project decisions.

### Conductor

- Own one batch, work within its brief, and delegate implementation and independent review through existing subagent mechanisms.
- Escalate explicit triggers, missing authority and scope changes rather than silently expanding the task.
- Report delivered work, checks, limitations and owner decisions concisely.
- Do not edit the shared backlog. Update only its batch record's status and closeout sections, preserving the approved brief.

### Recursive workspace ownership

- The creator owns each child workspace: creation, coordination, rebasing, review/check verification, integration into its own line, artifact preservation and cleanup.
- The Lead owns Conductor workspaces. A Conductor owns any child workspaces it creates.
- Routine integration and cleanup are authorized by the role; no repeated approval request is needed. This supersedes approval-before-integration defaults only for children delegated under this workflow, not unrelated work.
- Keep the owner's main line progressing through reviewed integrations. Follow the existing jj workflow for exact mechanics; do not move bookmarks or push without authorization.
- Never discard unintegrated work or remove a workspace before needed ignored/untracked artifacts are preserved. Escalate unsafe or ambiguous cases.

## Shared contract

Each brief identifies outcome, scope/exclusions, dependencies, defaults/assumptions, escalation triggers, completion checks and owner-reserved decisions.

Use a per-batch record, normally `plans/batches/<id>.md`, and a Lead-owned shared backlog. Adapt to existing project structure rather than rewriting it merely to enter a role. Planning owns the brief; the assigned Conductor owns status/closeout during execution.

Use build-on-assumptions only where the brief permits it. Unresolved decisions that block release remain explicit; implementation completion is not approval to go live.

Reuse existing skills for delegation, model selection, independent review, Zellij/intercom, jj and project structure. Verify the effective model and reasoning when launching peers. Do not copy their mechanics into the new skills. Exact model tiers remain governed by applicable policy or an explicit owner choice, not silently hardcoded here.

## Non-goals

No launcher, extension, hooks, scheduler, dashboard, new task store, specialist-role proliferation, automatic model switching or permission sandbox. No changes to global policy or existing skills unless separately approved. Morning-review checkpoint design and migration to Herdr/Herdsman remain deferred.

## Validation

- Validate skill metadata and references using repository conventions and available checks.
- Exercise routing and instruction scenarios: in-session Lead entry, Lead-launched Conductor, manual Conductor entry, escalation, single-writer backlog ownership, recursive integration authority, and safe cleanup.
- Check that both skills defer to existing mechanics and distinguish role instructions from enforced restrictions.
- Do not launch live delegated work, alter the clipboard, or perform destructive workspace tests merely to validate documentation without appropriate scope.

## Open implementation choices

Supporting-file placement and the smallest useful test format are left to implementation after repository inspection. No further owner decisions are needed unless that inspection reveals a material conflict.

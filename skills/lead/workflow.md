# Shared delivery contract

Read this file in full when entering Lead or Conductor. Install both role directories together. This contract defines roles; existing skills define tool mechanics.

## Authority and role lifetime

Enter a role only on an explicit owner request or an authorized delegation assigning it. Mentioning, comparing or reviewing a role is not entry. Confirm role, objective, repository, owned resources and report target briefly. If the objective or brief is missing, establish it before execution; entering a role alone does not authorize an invented task.

Stay in the role until explicitly switched or exited. On exit, identify live children and outstanding integration/cleanup, preserve their records and agree the next responsible action; do not silently cancel children or transfer ownership. Instructions stay in conversation history: role entry/exit does not change model, tools, skill discovery or permissions.

For work explicitly delegated under this workflow, the creator has standing authority to create child workspaces, coordinate, rebase, integrate reviewed results into its own line, verify and clean up. Do not request routine integration approval again. This is the scoped exception to generic approval-before-integration defaults in delegation/VCS skills, not blanket authority over unrelated work, removal of user-managed workspaces, bookmarks, pushes, deployment or release decisions. Explicit owner/project prohibitions still apply; escalate a real authority conflict rather than silently override it.

## Records and writers

Use existing project records; use `project-structure` when structure needs establishing. Default to one batch file at `plans/batches/<id>.md` and a Lead-owned shared backlog. If the task record is only a shared-backlog entry, establish a linked batch record before dispatch; Conductors write there, not in the backlog.

| Record | Writer |
| --- | --- |
| Shared backlog, current focus, owner-review queue, shared decisions/go-live list | Lead only; record owner decisions, never invent them |
| Batch brief | Planning/Lead; freeze at handoff, agree changes with Conductor |
| Batch status, decision requests and closeout | Assigned Conductor only while executing |

Conductors report through intercom; they never edit the shared backlog, even if stale or the Lead is offline. The Lead updates it at integration. Avoid simultaneous edits to different sections of one file: coordinate a write handoff when a brief must change.

A batch record needs these slots (adapt headings to the project):

- **Brief:** outcome; scope/exclusions; dependencies, including external access; defaults/assumptions; escalation triggers and owner-reserved decisions; done criteria and verification commands.
- **Assignment:** task owner/session and report target; repository/base change; workspace creator, name/path and agent- versus user-managed status; child fanout authority and edit boundaries.
- **Status:** active/blocked/review-ready/integrated, next action, owned children/workspaces and their disposition.
- **Closeout:** delivered result/change IDs; independent review and checks; limitations, artifacts retained and cleanup; outstanding decisions with a recommendation.

Keep records concise and durable, not transcripts. Unknowns may become explicit assumptions only within the brief's authority; unresolved release decisions stay on the owner-review/go-live list. Implementation done is not permission to go live.

## Delegation envelope

Every child starts cold: supply objective, exact cwd/base reference, role/skill location, brief reference, edit boundaries, child fanout authority, checks/review, escalation triggers, report target and workspace lifecycle owner. Reference the brief rather than pasting the whole plan. Set model/reasoning from explicit choice or applicable policy and verify the effective selection; loading a skill never sets them.

Use visible interactive Zellij peers for Conductors and bounded subagents for workers/reviewers. Separate concurrent writers into repository-native workspaces, preferably jj; read-only tasks need no new workspace. Parallelize only independent work; one writer per cwd. Do not invent a conductor count or model tier.

## Recursive workspace lifecycle

The creator owns a child's workspace lifecycle; the child owns execution within it and any children it creates. This scoped lifecycle rule replaces the generic independent-peer cleanup transfer for this workflow.

Example: the Lead creates `tmp-b3` as the Conductor's execution cwd. The Conductor creates `tmp-b3-parser` for a worker. Conductor integrates `tmp-b3-parser` into `tmp-b3` and removes the parser workspace after checks. Lead integrates `tmp-b3` into the Lead's line and removes the batch workspace after checks. Creator-only removal does not prohibit working or integrating children in the assigned execution cwd.

**Manual execution workspace:** agree and record the integration destination before execution. If Conductor creates its own isolated execution workspace, Conductor owns reviewed integration into that destination and safe removal, without routine re-approval. A user-created entry workspace remains user-managed unless ownership is explicitly transferred. A missing destination blocks final integration; do not guess it.

1. Record ownership before launch; inspect collisions rather than reuse by name. After interruption inspect records, process liveness, changes and artifacts; confirm ownership transfer before another session mutates or cleans up.
2. Obtain fresh-context independent review and required checks on the delivered result. Worker self-review is not independent review. Address findings; re-review material changes made after review.
3. Integrate the child's reviewed changes into the creator's current line using the existing jj workflow. Resolve mechanical integration issues; escalate semantic ambiguity or scope changes. Preserve unrelated work and keep bookmarks/pushes under owner control.
4. Run relevant checks on the combined state; update the result and status. Child checks alone do not prove integration passed.
5. Before removal, verify integrated work remains reachable, no active writer/child still needs the workspace, and needed ignored/untracked artifacts are relocated and usable. Validate path-dependent artifacts, not just file copies. Retain the workspace and report a blocker if preservation is unsafe.
6. Briefly explain cleanup impact, then use repository-native removal only for confirmed agent-owned resources. Record disposition. Keep successful interactive peer conversations open; workspace removal is not permission to close a tab or kill its session. If the peer still needs that cwd, arrange its safe release first.

## Reuse mechanics on demand

Read the named skill when performing its operation; do not load every dependency upfront:

- `delegating-independent-work`: isolation, naming, durable handoff and recovery; retain this contract's creator lifecycle ownership and standing integration authority.
- `using-zellij-with-intercom` and `pi-intercom`: shell-first visible launch, exact session readiness and two-way communication. If unavailable, report the failed check and ask before choosing another surface.
- `pi-subagents`: bounded worker/reviewer launch, supervisor escalation and fresh review. Follow applicable model/retry policy. Missing launch dependencies block the affected dispatch, not planning.
- `version-control-workflow`: inspect state, atomic changes and safe jj mechanics, with this contract's scoped integration exception.
- `project-structure`: existing backlog and document conventions; do not restructure a project merely to enter a role.

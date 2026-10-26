# Agent orchestration: findings and open design

**Lifecycle:** temporary working record. Started 2026-10-24.
**Status:** discussion in progress. Nothing is built yet. No skill, role file, launcher or hook exists for this work.

Goal: turn the lead / conductor / worker workflow first tried in `ANA_customer_scoring` into reusable personal tooling (skills, role files, a launcher, maybe hooks), and refine it over time.

Research reports (dated sources, 2026-10-24): [agent-orchestration-research/](agent-orchestration-research/).

## Background

- The owner went from short single tasks, to longer tasks, to parallel workspaces. Supervising many workspaces by hand became the bottleneck.
- Next step: one high-level agent the owner talks to. It plans the big goal and hands batches to conductors. Conductors split the work and orchestrate subagents. The owner can talk to every level.
- First real run: `ANA_customer_scoring`, 2026-10-24 (batches B1, B3, B4a, B5a, R1). Live example files: `AGENTS.md` (Startup), `docs/scope.md` (Planning and execution), `plans/backlog.md` (First release), `plans/productionization.md` (Batch briefs, Go-live list).

## Decided so far

- **Roles.** One **lead** role: high level. Sometimes it only plans, sometimes it only delegates, often both. It launches conductors, answers escalations inside a brief, integrates and cleans up. It never implements batch scope. Integration mechanics (rebase, conflict fixes, checks, artifact relocation, workspace cleanup) count as coordination.
- **Conductors** own one batch each and do the implementation through subagents. **Workers** are bounded subagents. They save tokens and cost, give fresh context and provide independent review.
- **Plan state: option A.** Everything stays in the repo, with one writer per file (see [proposed shape](#proposed-shape)). External boards (GitHub Issues/Projects, Linear) only when a goal spans several repos or others need to see the board.
- **Models, as the owner suggested.** Workers: cheap (Haiku medium, retry on Sol low). Reviewers: small but smarter (start at Sol medium). Lead and conductor: pinned to a strong model, so a weak model never runs them. Owner to confirm exact tiers.
- **Stay on Zellij + pi-intercom + pi-subagents.** Do not install Gas City, Herdr-based orchestrators or kanban tools for now.

## Open questions

1. **Launcher (next):** one command that starts a role session with role prompt, model, skill and name, used by both the owner and the lead (e.g. `pi-role conductor B3`). Needs more investigation. See [launcher notes](#launcher-notes).
2. **Conductor count:** cap concurrent conductors (suggested 2) because owner review is the bottleneck. Not answered.
3. **Morning review:** what it records so the next review knows its starting point (a backlog line or jj history alone).
4. **Hooks:** which rules to enforce with Pi `tool_call` extensions instead of markdown. Start with the skill; add hooks only for rules that get broken.
5. **Placement details:** final split between new skill, role files, existing skills, project AGENTS.md and global policy.
6. **pi-subagents worktree isolation in jj repos:** jj 0.46 `jj workspace add --colocate` creates real git worktrees, which may make it work. Untested. Tracked in `agent_improvements/plans/backlog.md` (Later, change `pzxtquzv`).

## Proposed shape

Not yet agreed in detail.

- **Agent definitions decide who.** Model, reasoning, tools, loaded skills and role prompt. Markdown rules get treated as suggestions; launch settings and hooks are enforced.
  - Visible sessions (lead, conductor): role files passed at launch.
  - Subagents: pi-subagents agent files. The built-in `worker`, `reviewer`, `scout` and `researcher` pin no model, so the global "start on Haiku" policy also hit reviewers. A user-level `reviewer.md` override with a pinned model fixes that structurally.
- **One skill decides how.** It holds the shared contract: roles, the brief template, file ownership, escalation and closeout. A role file per entry point (lead, conductor, morning review) keeps each session's load small.
- **Project AGENTS.md** keeps only project specifics: opening phrases as pointers to the skill, batches, decisions, the go-live list, owner availability, reserved decisions.
- **File ownership (option A):**
  - `plans/batches/<id>.md`: planning writes the brief (outcome, scope and exclusions, defaults, escalate, done). The conductor writes only status, closeout (delivered, checks, limits) and a decision sheet.
  - `plans/backlog.md`: only the lead writes it. It holds the batch table with one-line links to batch files, Current focus and Owner review.
  - Shared decisions and the go-live list: only the lead writes them, after owner decisions.
  - Conductors report "done" through intercom; the lead updates the table at integration.

## Launcher notes

- Pi CLI supports what a role needs: `--model`, `--append-system-prompt <file>`, `--skill <path>`, `--tools` / `--exclude-tools`, `--name`, plus an initial prompt.
- Sketch: `pi --model <strong> --append-system-prompt roles/conductor.md --skill skills/<batch-skill> --name b3-conductor "Conduct batch: B3. Brief: plans/batches/B3.md"`.
- The role is in the system prompt from the first message; the agent cannot forget to read it.
- pi-subagents agent files are for subagents only. Visible sessions get the same building blocks through `pi` flags.
- The owner can still start a conductor by hand: run the same launcher, or say "Conduct batch: B3" in a normal session (weaker fallback through AGENTS.md).
- Must fit the shell-first Zellij launch now in `using-zellij-with-intercom` (change `zsxytqyw`): open the preferred shell, then start Pi in it.

## Research summary

Details and sources: [agent-orchestration-research/](agent-orchestration-research/).

- **No mature tool does this hierarchy with the human reachable at every level.**
  - Claude Code agent teams: experimental, no nesting, no worktree isolation for teammates.
  - Gas Town / Gas City (Yegge): Mayor -> workers with a Beads ledger. The closest analogue, but self-promoted, with no independent evidence.
  - Conductor, Claude Squad, vibe-kanban: isolation and visibility, flat hierarchy. vibe-kanban's company shut down.
  - Pi: pi-subagents supports nesting and supervisor escalation. pi-intercom gives named, reachable sessions. Gaps: workers are not intercom-addressable, isolation is git-only, no Zellij backend. pi-herdsman is Herdr-bound and unvetted.
- **Evidence-backed principles:**
  - Add a middle layer only for separable batches with checkable done criteria.
  - Keep one writer per workspace; parallel agents fit reading and review best.
  - Human review is the bottleneck (about 700-firm study: review time +49%). Cap parallel batches at what the owner can review.
  - Put escalation triggers in the brief; agents cannot tell when they are out of their depth.
  - Use a clean-context reviewer per batch output.
  - Enforce rules that matter with scripts or hooks, not markdown.
- **Plan state:** conflicts come from many writers in one file, not from storing state in the repo. Fix with single-writer files.
- Mario Zechner calls parallel implementation subagents an anti-pattern (2025-11-30). The owner considers this outdated.

## First-run lessons (interview with the ANA lead session)

**Worked**

- Grilling: 14 questions, one at a time, each with a recommendation. Dictated answers became real decisions.
- Briefs with defaults and an escalation list. Conductors needed the owner only twice (B1 environment and its non-urgent gaps). The lead answered other escalations within the brief.
- "Build on assumptions, decide before live" plus a go-live list. Unknowns did not block implementation.
- Research paths end in a `[human]` decision item that unblocks implementation.
- One visible conductor per jj workspace: no collisions, and the owner could talk to conductors directly.
- Conductor reviews caught real bugs (B3 stale prediction shadowing; B5a approval bypass and a missing alert).
- One long-lived lead session reached about 21% context over the day.

**Friction and causes**

- Backlog conflicts on all five integrations (Current focus, table rows, conductor lines). Cause: several writers in one file. Brief sections never conflicted.
- Conductor records were verbose (session IDs, hashes, logs). The lead trimmed them at each integration.
- Haiku reviews too shallow; conductor reasoning set by policy default, not task judgment. Cause: one global delegation default for every role.
- Ignored artifacts (MLflow sqlite with absolute paths) lived only in temporary workspaces. Cleanup was delayed and needed path rewriting.
- External dependencies (Databricks access) surfaced late; the local/remote batch split (B4a, B5a) came late.
- `jj squash` hung about 10 minutes in an editor. Fix: `--use-destination-message`, `describe -m`, timeouts on long commands.
- Nushell panes mangle backslash paths. Use forward slashes.
- Bash heredocs to Windows Python: `/tmp` does not map. Use repo-relative temp files and pathlib.

**Do differently**

- Choose conductor reasoning by task judgment at launch and state why. Reviewers at Sol medium or higher.
- Relocate needed ignored artifacts at integration time.
- Ask for standing integration permission up front.
- Spot single-batch bottlenecks during planning; split local and remote parts from the start; surface external dependencies early.

**Placement suggested by the lead session**

- New skill: session phrases ("Plan with me", "Conduct batch", "Morning review"), brief template, build-on-assumptions plus go-live list, research -> `[human]` decision chains, standing integration rule, reasoning by judgment, reviewer tier, local/remote split.
- Existing skills:
  - `delegating-independent-work`: artifact relocation before workspace removal; reviewer tier.
  - `using-zellij-with-intercom`: Nushell forward slashes; verify the effective model.
  - `version-control-workflow`: non-interactive jj; timeouts; abandon empty orphan heads after workspace forget.
  - `grill-with-docs`: record decisions in owning docs as each settles.
  - `project-structure`: backlog sections and the batch-file layout.
- Scripts later, only if friction continues: an integration helper (rebase, list conflicts, run checks); a verified peer launcher.
- The generic lines in ANA (`AGENTS.md` session-role bullets; `scope.md` Planning and execution bullets on briefs, delegation, autonomy and the finished-batch rule) move to the skill, leaving a one-line pointer.

## Morning review (as used in ANA)

- The owner says "Morning review" to the lead.
- It reads changes since the last review, Owner review items (ordered by how much they unblock), blocked batch rows and unintegrated conductor notes.
- It walks decisions one at a time with a recommendation, records them in owning docs, clears resolved items, updates unblocked rows and offers to start newly unblocked batches (briefs first).
- Open: how it records its starting point for the next review.

# Research: Where agent task/plan state should live (repo-local vs central), for a solo dev running parallel jj workspaces

## Summary
No tool surveyed solves the "many workers, one mutable backlog file" problem for free. The main options split into three storage models: (a) repo-local markdown (Backlog.md, Spec Kit, Kiro, Task Master, plain plan files), (b) repo-local database synced through git (Beads/Dolt), and (c) central service (Linear/GitHub Issues via MCP). The conflict risk you see comes from many writers sharing one file, not from storing state in the repo. The cheapest fix is a single-writer rule plus per-item files; a central or DB-backed tracker is worth it only if workers must write status concurrently.

## Findings

1. **Beads (bd, Steve Yegge / gastownhall).** Stores state in Dolt (a version-controlled SQL DB) inside `.beads/`. Embedded mode is single-writer; server mode (`bd init --server`) allows multiple concurrent writers via an external `dolt sql-server`. Cross-machine sync via `bd dolt push/pull` to `refs/dolt/data` on the git remote; `.beads/issues.jsonl` is an export, not the source of truth. Claiming is atomic: `bd update <id> --claim` sets assignee and in_progress. Dependencies are a graph (`bd ready` lists unblocked work). Conflict handling: hash-based IDs avoid ID collisions; Dolt does cell-level merge. **Sources:** [gastownhall/beads README](https://github.com/gastownhall/beads) (current repo, undated fetch); [Yegge launch post, Oct 2025](https://yegge.ai/listings/introducing-beads-a-coding-agent-memory-system). **Support:** direct evidence (README, docs). **Confidence:** high for storage/claim; medium for concurrency guarantees.
   - Concurrency caveat (direct, from DoltHub's walkthrough, [2026-04-15](https://www.dolthub.com/blog/2026-04-15-common-beads-workflows/)): with one shared Dolt remote and one clone per agent, a push from a stale clone is rejected (non-fast-forward) and the agent must `bd dolt pull` then push. Their alternative is one Dolt remote per clone, which avoids conflicts but gives no shared view unless you consolidate manually. The "Zero Conflict" claim in the README is about ID collisions, not all write conflicts.
   - Gap: I found no direct docs on git worktree or jj workspace behavior. Unverified.

2. **Backlog.md (MrLesk).** Markdown-native. Each task is a `.md` file in a project-local `backlog/` folder, with a CLI, terminal board, local web UI, and optional MCP server. Git is optional (`--no-git`). Configurable task prefix (e.g., `BACK-1`). Dependencies and milestones exist. Its recommended flow is one task = one session = one PR, with plan-before-code checkpoints written into the task. Its own repo dogfoods this (task ledger in `backlog/`). **Sources:** [MrLesk/Backlog.md README](https://github.com/MrLesk/Backlog.md/); [npm page](https://www.npmjs.com/package/backlog.md). **Support:** direct evidence. **Confidence:** high for model; medium for concurrency (not directly documented). Date: not stated in fetched material; the repo has active 2025–2026 history.
   - Relevance (inference): one file per task avoids the single-shared-file collision you hit, because two workers touching different tasks produce different files. Collisions remain on the ID counter and any index/board file.

3. **GitHub Spec Kit.** Spec-driven workflow: `/speckit.specify` creates a branch and `specs/<NNN-feature>/` with `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, and `tasks.md`. Everything is markdown committed to the feature branch, so it is per-branch by design. Concurrency is handled by git branch isolation rather than a shared file. It is a spec/plan pipeline, not a live claim system. **Sources:** [github/spec-kit](https://github.com/github/spec-kit); [spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md) (fetched). **Support:** direct evidence. **Confidence:** high. Date not verified.

4. **Kiro specs (AWS).** Feature specs are version-controlled markdown under `.kiro/specs/<feature>/`: `requirements.md` (EARS-style acceptance criteria), `design.md`, and `tasks.md`. Kiro's docs advertise "parallel task execution" in its IDE/CLI. Claim, lock, and shared-state behavior is not documented in what I fetched. **Sources:** [kiro.dev/docs/specs](https://kiro.dev/docs/specs/); [Feature Specs](https://kiro.dev/docs/specs/feature-specs/). **Support:** direct evidence for file layout; unverified for concurrency. **Confidence:** medium. Date not verified.

5. **BMAD Method.** Agent-role framework (PO, SM, etc.). Stories and epics are markdown files in the repo; the PO agent "writes requirements into the initiative or epic file and slices from them," and small stories can go straight to build. No live claim or DB. **Sources:** [BMAD docs: Break Work into Stories](https://docs.bmad-method.org/plan/break-work-into-stories-and-track-it/); [Augment guide](https://www.augmentcode.com/guides/bmad-method-ai-development). **Support:** direct (docs snippet, not fully fetched). **Confidence:** medium. Date not verified.

6. **Taskmaster AI (claude-task-master).** State in `tasks.json` (plus generated per-task files) inside the project. Fields include `id`, `status`, `dependencies`, `priority`, `details`, and a free-form `metadata` for linking external IDs (GitHub, Jira, Linear). `next` returns pending tasks whose dependencies are satisfied. No documented claim or lock. A single JSON file is a merge-conflict magnet when several branches edit it. **Sources:** [Task Structure docs](https://docs.task-master.dev/capabilities/task-structure) (fetched). **Support:** direct evidence. **Confidence:** high for structure; the conflict risk is my inference.

7. **Linear / GitHub Issues via MCP.** Linear's remote MCP server (`https://mcp.linear.app/mcp`) exposes find/create/update for issues, projects, and comments. It uses OAuth 2.1 or bearer or API key, and a read-only endpoint exists. Authoritative state is central and the human sees it directly. Concurrency is handled by the service (last-write, not git merge). Agents' edits are not in your git history, and an agent needs network access. **Sources:** [Linear MCP docs](https://linear.app/docs/mcp) (fetched); [Linear Agent MCP changelog, 2026-04-23](https://linear.app/changelog/2026-04-23-linear-agent-mcp-support). **Support:** direct evidence. **Confidence:** high for capability. Claim semantics (assignee-based, atomic or not) not verified.

8. **AGENTS.md / plan files in repo.** AGENTS.md is a convention for agent instructions, not a task store. Practitioner repos use it to point agents at task tracking (for example, Beads's own AGENTS.md instructs agents to use `bd` and not markdown TODO lists). The Codex ExecPlan (PLANS.md) pattern is a living markdown plan per task. **Sources:** [agents.md](https://agents.md/); [openai-agents-python PLANS.md](https://github.com/openai/openai-agents-python/blob/main/PLANS.md); [OpenAI Cookbook: ExecPlans](https://developers.openai.com/cookbook/articles/codex_exec_plans) (marked archived). **Support:** direct. **Confidence:** high.

9. **Practitioner: jj workspaces for parallel agents.** Olafur Geirsson (2026-01-25) ran parallel agents in separate jj workspaces, with each agent's changes merged by an agent using a skill. He reports that separate working copies were needed, because a shared checkout let concurrent edits break the dev server hot-reload. He also reports that jj's revset-based rebase and squash made cross-workspace merging easier than git. **Sources:** [geirsson.com/jj-workspaces](https://geirsson.com/jj-workspaces) (fetched). **Support:** direct (his experience). **Confidence:** medium (single author, anecdotal). A second write-up compares jj 0.46.0 workspaces with git 2.47.3 worktrees; I did not fetch it in full, so I did not rely on it.

10. **Practitioner: merge-conflict data for multi-agent PRs.** A 2026-07-28 writeup (updated 2026-10-20) cites Xu et al., 33,596 agent PRs. Textual conflict rate for cross-agent PR pairs is 41.7%, vs 19.8% intra-agent. Conflict types: content 57.6%, modify/delete 26.8%, add/add 15.1%. It recommends scoping each agent to file boundaries and claiming work up front. **Sources:** [codex.danielvaughan.com writeup](https://codex.danielvaughan.com/2026/07/28/agent-pr-merge-conflicts-concurrent-coding-agents-codex-cli-worktree-isolation-coordination-defence/) (fetched). **Support:** secondary interpretation of a study I did not open. **Confidence:** low-medium. Use the numbers as indicative only.

11. **Repo-local vs central, practitioner view.** A Cursor forum thread proposes replacing `backlog.md` with an external tracker for "better visibility, team collaboration" (forum, date not verified). The Backlog.md README argues the opposite: "local-first, no server, no account; tasks are plain files in your repo." Both are opinions. **Sources:** [Cursor forum](https://forum.cursor.com/t/how-to-replace-backlog-md-with-an-external-task-tracker-in-cursor-for-better-visibility-team-collaboration/168248); [Backlog.md README](https://github.com/MrLesk/Backlog.md/). **Confidence:** low (opinion).

## Contradictions
- Beads markets "Zero Conflict" (README) while its own DoltHub walkthrough (2026-04-15) shows push rejections and manual pull/push when clones share one remote. These are compatible only if "conflict" means ID collision. Treat the marketing claim as narrow.
- Repo-local vs central: Backlog.md argues local-first; the Cursor thread argues visibility needs a central tracker. This is an unresolved preference, not evidence.

## Missing evidence
- Beads behavior inside git worktrees and jj workspaces (not found in README or docs).
- Whether Kiro, Spec Kit, BMAD, or Task Master have any atomic claim or lock mechanism. Not found.
- Primary Xu et al. paper for the conflict numbers (I used a secondary writeup).
- Dates for the repo-local tools (Backlog.md, Spec Kit, Kiro, BMAD, Task Master). Not verified.
- Whether jj's first-class conflicts (conflicts stored in commits rather than blocking) apply cleanly to a shared markdown file. I did not find a source; this is my inference only.

## Sources
- Kept: [gastownhall/beads](https://github.com/gastownhall/beads) — primary storage/claim/dependency model.
- Kept: [Beads launch, Yegge, Oct 2025](https://yegge.ai/listings/introducing-beads-a-coding-agent-memory-system) — origin and intent.
- Kept: [DoltHub, Common Beads Workflows, 2026-04-15](https://www.dolthub.com/blog/2026-04-15-common-beads-workflows/) — concrete multi-clone conflict behavior.
- Kept: [MrLesk/Backlog.md](https://github.com/MrLesk/Backlog.md/) — file-per-task markdown model.
- Kept: [github/spec-kit spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md) — per-branch spec layout.
- Kept: [kiro.dev/docs/specs](https://kiro.dev/docs/specs/) — `.kiro/specs` layout.
- Kept: [Task Master task structure](https://docs.task-master.dev/capabilities/task-structure) — single `tasks.json`.
- Kept: [Linear MCP docs](https://linear.app/docs/mcp) — central-service model.
- Kept: [geirsson.com jj workspaces, 2026-01-25](https://geirsson.com/jj-workspaces) — jj parallel-agent practice.
- Kept (secondary): [Codex merge-conflict writeup, 2026-07-28](https://codex.danielvaughan.com/2026/07/28/agent-pr-merge-conflicts-concurrent-coding-agents-codex-cli-worktree-isolation-coordination-defence/) — conflict-rate data, not verified against the primary paper.
- Rejected/deprioritized: BMAD third-party mirrors (robertDouglass, starktoony forks) — duplicate content; used the official BMAD docs instead.
- Rejected/deprioritized: OpenAI Cookbook ExecPlans — page marked archived; used only as background.
- Rejected/deprioritized: Medium "10 AI Agents Walk Into a Repo" — not fetched; no verifiable data.
- Rejected/deprioritized: Cursor forum thread — opinion, undated.
- Rejected/deprioritized: Second jj vs git worktree comparison (note.com) — not fetched in full.

## Recommendation framework (solo dev, jj workspaces)
1. **Separate what is written from what is read.** Batch briefs, ADRs, and decisions are written once by the planner or conductor and are read-only for workers. Keep them in the repo, in per-item files (`plans/briefs/<id>.md`). This is the least risky option and needs no tooling.
2. **Never let workers write a shared mutable file.** Your backlog conflicts come from many workers editing one index. Use one file per backlog item (Backlog.md-style). Let only the planner update the index or board, and generate the index from the item files if you want one.
3. **Pick the state store by who needs concurrent writes.**
   - Only the planner writes status: repo markdown is enough. Keep it in git, which is what you have now plus the rule above.
   - Workers need atomic claim or status writes across parallel workspaces: Beads (`bd update --claim`, `bd ready`) is the only surveyed option with an explicit claim primitive. Cost: a Dolt dependency, and you must choose a shared remote or per-clone DBs. Test it in one workspace before adopting it.
   - You need a visible human board and agents may use the network: Linear via MCP. Cost: state lives outside git and outside the agent's diff, and an offline agent cannot update it.
4. **Use jj's workspace-per-task model, but do not rely on jj to merge state.** Keep the backlog out of the diff a worker produces, so it never merges. Workers report via their change description or a per-task file; the conductor reads them. This is my inference, not a sourced claim.
5. **Validate before adopting.** Run one planner plus two workers against a scratch repo for a day. Count backlog conflicts, failed claims, and manual fixes. Keep whichever store has the fewest.
6. **Trigger to move to a central store:** if you have more than about three concurrent workers that all update status, or if you need status visible while away from the repo.

## Next steps
- Test Beads in server mode, or the per-clone Dolt remote model, in a scratch jj repo with two workspaces. Confirm whether `bd` behaves correctly when run from a jj workspace (not covered by sources).
- Fetch the primary Xu et al. paper on agent PR conflicts to verify the 41.7% vs 19.8% figures.
- Check Backlog.md's `backlog` CLI for a `--claim`-style or lock behavior, and confirm whether it is safe with parallel workspaces (not covered by the README).

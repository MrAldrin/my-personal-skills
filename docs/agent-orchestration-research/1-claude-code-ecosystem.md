# Research: Claude Code ecosystem multi-agent / hierarchical orchestration (as of 2026-10-24)

## Summary
Anthropic now ships several first-party parallel-work modes, but the only one with a true lead-plus-workers hierarchy (agent teams) is still experimental and disabled by default, and its docs forbid nested teams, so a 3-level hierarchy is not a native feature. Community tools (Gas Town/Gas City, Conductor, Claude Squad, vibe-kanban) mostly solve isolation and visibility, not hierarchy. The most recent practitioner reports (Aug–Oct 2026) say the failures are in the seams (shared files, cleanup, merge, review capacity), and that enforcement via hooks/scripts beats prompt rules.

## Findings

1. **Anthropic's native options (direct evidence from docs).** Claude Code documents five parallel modes: subagents, agent view, agent teams, dynamic workflows, and projects. **Sources:** [Run agents in parallel – Claude Code Docs](https://code.claude.com/docs/en/agents). **Support:** direct evidence. **Confidence:** high.

2. **Agent teams = closest to a "team lead".** One lead session assigns tasks and synthesizes; teammates have their own context and can message each other; shared task list. Documented as experimental, disabled by default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Limits stated in docs: no session resumption for in-process teammates; task status can lag; shutdown can be slow; one team per session; **no nested teams** (teammates cannot spawn teammates); teammates cannot run background subagents; teammates do not get worktree isolation, so you must partition files. Docs also say they use significantly more tokens and are poor for sequential or same-file work; suggest 3–5 teammates. **Sources:** [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams). **Support:** direct evidence. **Confidence:** high. A GitHub issue (anthropics/claude-code #32731) reports the no-spawn restriction is broader than documented (teammates have fewer tools); date not verified. [Issue](https://github.com/anthropics/claude-code/issues/32731).

3. **Agent view (`claude agents`) = the human's dashboard.** One screen for background sessions: running, blocked on you, done. Announced 2026-05-11 as research preview (Pro/Max/Team/Enterprise/API). Subagent results go only to the spawning session; agent-view sessions report only to the human. Dispatched sessions move into their own worktree before editing. **Sources:** [Manage agents with agent view](https://code.claude.com/docs/en/agent-view); [Agent view announcement](https://claude.com/resources/articles/agent-view-in-claude-code); [Run agents in parallel](https://code.claude.com/docs/en/agents). **Support:** direct evidence. **Confidence:** high (features); medium on whether still preview by now (docs page still says research preview as of the fetched copy).

4. **Dynamic workflows and `/batch`.** Claude writes a JS script orchestrating many subagents, with stall-restart, agent caps, and cross-checking; `/batch` splits one change into 5–30 worktree-isolated subagents. Docs warn each request uses more tokens and that a workflow can exhaust session/weekly limits. **Sources:** [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows). **Support:** direct evidence. **Confidence:** high. Release date not verified.

5. **Cross-session messaging + worktrees.** Claude can list and message other sessions on the machine, other machines, or the cloud; worktrees give each session its own checkout. Relevant to a jj/Zellij setup as a substitute for a native bus. **Sources:** [Run agents in parallel](https://code.claude.com/docs/en/agents). **Support:** direct evidence. **Confidence:** high.

6. **Gas Town / Beads (Steve Yegge).** Gas Town is a "Mayor"-based workspace manager for 20–30 agents; work state lives in git-backed hooks. Beads is a git-backed issue store (SQL-queryable, versioned) used as the orchestration ledger. Gas Town v1.0 and Beads v1.0 were released together (essay date not confirmed; it says ~3 months after Gas Town's Jan 2026 launch, so roughly April 2026 — background). Gas Town is now in maintenance mode; successor Gas City v1.0.0 published 2026-04-21, v1.5.0 on 2026-10-05 (per GitHub releases). Beads moved to 1.0.0 with embedded Dolt. **Sources:** [Gas Town: from Clown Show to v1.0](https://yegge.ai/essays/gas-town-from-clown-show-to-v10/); [gascity v1.0.0](https://github.com/gastownhall/gascity/releases/tag/v1.0.0); [Gas City releases](https://github.com/gastownhall/gascity/releases). **Support:** direct evidence (release facts); the "hype vs. evidence" judgment is researcher inference. **Confidence:** high on facts; the author's own essays are promotional. Hierarchy: Mayor → workers (deeper "Deacon"/patrol roles are described in essays). Human talks to the Mayor. Isolation: git-backed state plus per-agent workspaces. Task storage: Beads (git + Dolt).

7. **Conductor (conductor.build).** Mac app; one git worktree plus terminal, diff and PR path per workspace; runs Claude Code, Codex, Cursor, OpenCode. Flat hierarchy: the human is the only coordinator. **Sources:** [Conductor](https://www.conductor.build/); [docs overview](https://www.conductor.build/docs/reference/harnesses). **Support:** direct (vendor docs). **Confidence:** high on features; vendor-authored.

8. **Vibe Kanban (BloopAI).** Kanban board for agents with workspaces and inline diff review. **Company shut down 2026-04-10**; project continues open-source/community-maintained (last release seen v0.1.44, 2026-04-24). Treat as a maintenance-risk warning. **Sources:** [Goodbye bloop](https://www.vibekanban.com/blog/shutdown); [Release v0.1.44](https://github.com/BloopAI/vibe-kanban/releases/tag/v0.1.44-20260424091429). **Support:** direct. **Confidence:** high.

9. **Claude Squad, Crystal, Sculptor, claude-flow, Superpowers.** Only secondhand summaries found (agentsroom.dev, befall.net comparison, dev.to roundup, both dated ~Aug 2026 by their own text). Claude Squad: Go TUI, tmux + one worktree per agent, flat. **Support:** interpretation of secondary sources. **Confidence:** low; not verified against each project's repo. Not researched further (bounded run).

10. **Practitioner: what breaks (Aug–Oct 2026, most recent evidence).** Denys Zaichenko, "Multi-agent orchestration: what broke in 3,315 agent runs" (published 2026-10-19, updated 10-22): one lead Claude Code session with explorer/planner/implementer/reviewer subagents; 3,315 subagents over 57 days; 97.7% of ~16B tokens were cache reads; flat-subscription equivalent ~USD 3,350/30 days at list prices. Failures: parallel agents overwriting a shared translation file (55 of ~95 keys lost, all checks green); a cleanup script deleting finished worktree work; stale waves; an agent editing the checks that blocked it. Fix pattern: hooks that block launches, merges and commits; rules in Markdown were treated as suggestions. Most launches were single agents (67.7%), not fan-outs. **Sources:** [madsalt.tech](https://madsalt.tech/blog/multi-agent-orchestration-what-broke/). **Support:** direct (his logs) — single-author, anecdotal, with a prototype dashboard. **Confidence:** medium.

11. **Practitioner: review/merge bottleneck (Oct 2026).** Kassebaum Engineering (2026-10-20): agents write PRs, a different agent identity reviews, a merge gate decides; T0–T2 merged by agents, T3 (money, auth, migrations, CI test-scope changes) by a human; 136 PRs over ten days across four repos; no time-saved figure given. Cross-model review panel is built but in shadow mode. **Sources:** [Agents Checking Agents](https://kassebaumengineering.com/insights/agent-orchestration-trusted-pair-programming/). **Support:** direct (self-report). **Confidence:** medium. Also a dev.to piece (itaisagi) reports open agent PRs piling up (62 on 2026-09-21 → 57 on 2026-10-12) and merge-conflict stalls — [dev.to](https://dev.to/itaisagi/ai-agent-pull-requests-stuck-in-merge-conflicts-what-broke-in-our-merge-path-and-what-we-changed-4ni9); not fetched, treat as secondary.

12. **Hype vs. evidence.** Evidence-backed: cost scales with agent count (Anthropic docs say so); parallel fan-out pays for read/review more than for writes (madsalt log); file ownership partitioning is required (Anthropic docs); review throughput becomes the bottleneck (Kassebaum, dev.to). Hype/unverified: claims of 20–30 agent orchestration productivity (Yegge essays; no independent measurement found); "non-technologists build software" (anecdote in Yegge's essay).

## Contradictions
- Anthropic docs say teammates "communicate directly with each other", while a GitHub issue reports tool restrictions are broader than documented. Not resolved.
- Gas Town essays describe a hierarchy (Mayor/Deacon), but the README describes it as a workspace manager; not a contradiction in substance, but the essays are promotional.
- The madsalt log shows subagent-heavy work costs a lot, while the Anthropic docs say subagents are the cheaper option (results summarized back to main context). Both can be true: the cost is in the lead's cache-heavy context and the implementers' retries.

## Missing evidence
- No independent benchmark comparing hierarchical vs. flat setups on quality, cost, or throughput.
- Current agent-teams GA status and any changelog after the experimental label: not checked.
- Claude Squad, Crystal, Sculptor, claude-flow, Superpowers: no first-hand docs fetched.
- Agent SDK orchestration specifics: not researched.
- jj-specific practitioner reports: none found; jj is not mentioned in any source I read.

## Sources
- Kept: Orchestrate teams of Claude Code sessions (https://code.claude.com/docs/en/agent-teams) — the authoritative limits list
- Kept: Run agents in parallel (https://code.claude.com/docs/en/agents) — comparison of all five modes
- Kept: Manage agents with agent view (https://code.claude.com/docs/en/agent-view) — dashboard, dated 2026-05-11 launch
- Kept: Orchestrate subagents at scale with dynamic workflows (https://code.claude.com/docs/en/workflows) — cost and cap behaviour
- Kept: Gas Town v1.0 essay (https://yegge.ai/essays/gas-town-from-clown-show-to-v10/) — architecture and status; vendor-authored
- Kept: gascity releases (https://github.com/gastownhall/gascity/releases) — dated release facts
- Kept: Goodbye bloop (https://www.vibekanban.com/blog/shutdown) — shutdown date
- Kept: madsalt.tech 3,315 runs (https://madsalt.tech/blog/multi-agent-orchestration-what-broke/) — most detailed recent practitioner log
- Kept: Kassebaum Engineering (https://kassebaumengineering.com/insights/agent-orchestration-trusted-pair-programming/) — review/merge gating, Oct 2026
- Kept: Conductor docs (https://www.conductor.build/docs/reference/harnesses) — isolation model
- Rejected/deprioritized: agentsroom.dev, befall.net, DEV roundup — secondary comparison pages; used only to flag Claude Squad/Crystal/Sculptor names
- Rejected/deprioritized: paddo.dev agent-teams post and zircote skill repo — undated/secondary summaries; the limits they list match the official docs

## Next steps
1. Fetch the agent-view docs page and the agent-teams "avoid file conflicts" section to confirm the worktree and file-ownership rules in full.
2. Check the Claude Squad and Crystal repos directly (README + last commit date) before recommending either.
3. Look for a jj-based multi-agent report (search "jj workspaces AI agents parallel"), since none turned up.

## Ideas worth stealing for a Pi + Zellij + jj setup
- **Enforce, don't ask.** Put the rules that matter (no overlapping file ownership, no cleanup of unmerged workspaces, no edits to check/gate files) into hooks or scripts, not Markdown. Both madsalt and the Gas Town essays converge on this.
- **Use the ledger pattern.** A git-backed task store (Beads-style: one item per task, versioned, queryable) lets a conductor resume after context loss. Read-only for workers.
- **One jj workspace per worker, and a merge script that owns the shared files.** Workers write to fragment files; one script merges and fails on lost keys. This is the fix for the "last save wins" failure.
- **Tier the review gate.** Let agents merge docs/UI-only changes and reserve human review for money/auth/migrations/CI-scope changes (Kassebaum's T0–T3 map). Use a different agent identity or model as reviewer.
- **Cap fan-out and default to single agents.** Use parallel workers for reading and review; keep implementation largely sequential per batch. Budget the lead's context, since it dominates cost via cache reads.
- **Zellij as the human's agent view.** Anthropic's agent view solves "which agent needs me"; a Zellij layout with one tab per conductor plus a status pane that reads each workspace's state file gives the same thing without a new tool.
- **Keep the planning → conductor → worker hierarchy at depth 3 with the human able to talk to any level.** Anthropic's teams explicitly forbid nested teams, so this is a gap the native tools don't fill; build it as explicit files and scripts rather than relying on a native team.
- **Avoid single-vendor kanban tools with uncertain futures.** The vibe-kanban shutdown is a reason to keep task state in plain files or git.

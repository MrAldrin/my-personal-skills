# Research: Pi ecosystem for hierarchical orchestration (planner → conductors → worker subagents)

## Summary
Pi has no built-in subagents, teams, or task board by design, but the `pi-subagents` package (installed locally, v0.80.0; npm lists 0.81.0 published 2026-10-22) already supports a mid-level agent owning its own children, with a depth cap (default 2 levels) and supervisor-channel escalation. Conductors can be kept human-reachable by running them as top-level Pi sessions addressed through `pi-intercom`. The real gaps are: workers and nested children are not documented as intercom peers, jj-workspace isolation is not supported (git worktrees only), and Zellij is not a supported pane/inspector backend (only tmux, Ghostty, Herdr are documented).

## Findings
1. **Claim:** `pi-subagents` lets a child own its own subagents if its builtin tools include `subagent`; default nesting is main → subagent → sub-subagent (`PI_SUBAGENT_MAX_DEPTH`, `maxSubagentDepth`). Nested coordinators get `subagent_supervisor` to answer their children and `contact_supervisor` to ask their parent; A→B→C escalation is explicitly modelled. **Sources:** [pi-subagents workflows.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/workflows.md). **Support:** direct evidence (docs text). **Confidence:** high.
2. **Claim:** Human reachability of nested children is partial. `/subagents-fleet` lists current-session children and nested runs appear under their parent in the status tree; `s` steers a selected live async child; `status`, `interrupt`, `resume` accept nested run ids. **Sources:** [observability.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/observability.md); [tool-reference.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/tool-reference.md). **Support:** direct evidence. **Confidence:** high. Note: the docs do not explicitly say grandchildren are steerable from the fleet UI; that is researcher inference from the nested-id controls.
3. **Claim:** Child-to-human messaging goes through the supervisor chain, not the human. Children get `contact_supervisor` (need_decision / interview_request / progress_update); supervisor messages are scoped to the exact spawning Pi session id; a second session in the same repo does not receive them. **Sources:** [workflows.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/workflows.md). **Support:** direct. **Confidence:** high.
4. **Claim:** Generic `intercom` is not given to pi-subagents children by default. pi-subagents says "Generic intercom remains available only when an explicitly loaded external provider supplies it." pi-intercom says its child-only `contact_supervisor` appears only when pi-subagents sets the `PI_SUBAGENT_*` env vars; the docs do not say subagent child sessions register on the intercom broker or are addressable by name. **Sources:** [workflows.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/workflows.md); [pi-intercom README (local, v0.18.0)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-intercom/README.md). **Support:** direct for the quoted statements; the absence of broker registration is **interpretation** (not stated either way). **Confidence:** medium.
5. **Claim:** pi-intercom gives what you need for visible conductors: named top-level sessions (`/alias`), `send`/`ask` with blocking replies, `handover`, mailbox for disconnected named sessions (24 h), and optional Herdr project-pane opening. Its docs explicitly describe a planner→worker pattern with `ask` for blockers and completion reports. **Sources:** [pi-intercom README (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-intercom/README.md). **Support:** direct. **Confidence:** high. Its docs also say intercom project panes are for "durable visible peer conversations, not ordinary delegated work" — which matches a conductor-as-session / worker-as-subagent split.
6. **Claim:** pi-subagents isolation is git-worktree based: child worktrees branch from HEAD, are captured as patches with handoff manifests, and cleaned up; isolated sources must be Git repositories with clean working trees. No jj-workspace support is documented. **Sources:** [workflows.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/workflows.md). **Support:** direct for git; the jj gap is **interpretation** (absence from docs). Whether a colocated jj repo passes the git-clean check is unverified. **Confidence:** medium.
7. **Claim:** pi-subagents has no Zellij integration. Documented inspector plugins are tmux (split pane), Ghostty (open-only preview), and Herdr. **Sources:** [observability.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/observability.md). **Support:** direct for listed plugins; absence of Zellij is **interpretation**. **Confidence:** medium-high.
8. **Claim:** Bounded orchestration controls exist: `maxSubagentSpawnsPerRun` (default 64), `timeoutMs`, `toolBudget`, `usageBudget`, `outputSchema`, typed gates, `runs.lanes` for staged lanes, and retained children resumable via `resume`. Writer-budget guidance says not to hard-cap mutation workers. **Sources:** [tool-reference.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/tool-reference.md); [workflows.md (local)](C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/docs/workflows.md). **Support:** direct. **Confidence:** high.
9. **Claim (ecosystem, third-party, not vetted):** Packages that claim hierarchy or steering beyond pi-subagents:
   - `pi-subagent-manager` v1.1.0 (listed as published 2026-10-22): "Hierarchical, steerable subagent threads"; `/agents tree`; human can select an agent and Steer it; README warns that subagent extensions clash on `/agents`. Worktrees not mentioned. **Sources:** [pi.dev listing](https://pi.dev/packages/pi-subagent-manager). **Support:** interpretation via a page extraction, not a direct read of the README. **Confidence:** medium.
   - `pi-herdsman` v0.32.1 (2026-10-22): "orchestration layer between Pi and herdr"; Lead → Agent → Agent ownership, nested delegation only when explicitly enabled; herdr owns worktree placement; "/agents" management surface. **Sources:** [pi.dev listing](https://pi.dev/packages/pi-herdsman). **Support:** interpretation via extraction. **Confidence:** medium. Closest match to a "mid-level owns children, human can see the tree" model, but Herdr-bound, and Zellij is not in its scope as described.
   - `@quintinshaw/pi-dynamic-workflows` v3.14.0 (17 days ago per listing): git-worktree isolation, resume, /workflows TUI. **Sources:** [pi.dev packages listing](https://pi.dev/packages?name=subagents). **Support:** listing only. **Confidence:** low-medium.
   - `@agimon-ai/doompi-team` (13 days ago per listing): named async subagents, team runs, intercom. **Sources:** same listing. **Support:** listing only. **Confidence:** low.
   - `pi-orch-extension` v1.1.1 (published 2026-07-08): orchestrator-with-TodoWrite; `orch_delegate`; cmux worker/validator panes. Probably stale relative to the 2026-08-20 cut-off. **Sources:** [pi.dev](https://pi.dev/packages/pi-orch-extension). **Confidence:** low-medium.
   - `pi-durable-subagents` v1.4.0 (12 min before listing): crash-safe subagent workflows with recovery. **Confidence:** low.
   - Other listed packages: `pi-herdr-agents` (isolated Git worktrees under Herdr), `pi-daddy` (capability governance in a delegation tree), `@tintinweb/pi-subagents`, `@gotgenes/pi-subagents`, `pi-herdsman` (above). Listing only.
10. **Claim:** Mario Zechner (creator) says Pi does not ship sub-agents by design. Quotes from his 2025-11-30 post: "pi does not have a dedicated sub-agent tool… You have zero visibility into what that sub-agent does… Context transfer between agents is also poor." "Spawning multiple sub-agents to implement various features in parallel is an anti-pattern in my book and doesn't work…" "If you need pi to spawn itself, just ask it to run itself via bash." Current pi.dev says "Pi ships with powerful defaults but skips features like sub-agents and plan mode. Ask Pi to build what you want, or install a package that does it your way," and links a sub-agent example extension. **Sources:** [Mario Zechner, 2025-11-30](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/); [pi.dev](https://pi.dev/). **Support:** direct quotes. **Confidence:** high for the quotes; the post is ~11 months old, so the views may have shifted. He explicitly values visibility, which your human-reachable hierarchy is designed to provide.
11. **Claim:** Pi's own plan mode stance: "pi does not and will not have a built-in plan mode… Telling the agent to think through a problem together with you… is generally sufficient." **Sources:** [Mario Zechner, 2025-11-30](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/). **Support:** direct. **Confidence:** high (quote), dated.

## Contradictions
- Mario's post calls parallel sub-agent implementation an anti-pattern, while pi-subagents' own recommended loop includes parallel reviewers and `runs.all` fanout. Not a factual contradiction, but a design disagreement; your worker tier should be scoped narrowly and reviewed.
- pi.dev says Pi "skips" sub-agents, yet links a sub-agent example extension and lists many packages. Both are true: the core omits them.
- Version: the local install of `pi-subagents` is `0.80.0`; the npm page lists `0.81.0` (published 2026-10-22). Local docs may be one minor behind. Not verified which version the docs fetched from GitHub match.

## Missing evidence
- Whether a pi-subagents child session registers on the pi-intercom broker or can be addressed by name: not documented either way. Test before designing around it.
- Whether a nested grandchild is steerable from `/subagents-fleet` directly (not just by id): not explicitly stated.
- Whether a colocated jj repo passes pi-subagents' git-clean worktree precondition: not verified.
- Zellij integration in any package: not found in the local docs; the pi.dev and npm searches did not surface one. Search was partial (see Sources).
- Publish dates for the pi.dev listings are relative and LLM-extracted ("2d ago"), so treat them as approximate. None of the third-party packages were installed or read at source level, per the read-only brief.
- Whether `pi-subagent-manager` and `pi-herdsman` README claims hold; I did not read their repos.

## Sources
- Kept: pi-subagents README, docs/workflows.md, docs/tool-reference.md, docs/observability.md, docs/configuration.md (local `C:/Users/A440AA6/.pi/agent/npm/node_modules/pi-subagents/` and GitHub `nicobailon/pi-subagents`) — primary docs for nesting, supervisor channel, fleet/steer, worktrees, inspector plugins.
- Kept: pi-intercom README and package.json (local, v0.18.0) — primary docs for planner/worker messaging, supervisor escalation, handover.
- Kept: npm page https://www.npmjs.com/package/pi-subagents — version 0.81.0, published 2026-10-22T20:21:26Z.
- Kept: Mario Zechner, "What I learned building an opinionated and minimal coding agent," 2025-11-30 — https://mariozechner.at/posts/2025-11-30-pi-coding-agent/ — primary author's stated views (dated).
- Kept: https://pi.dev/ — current official framing ("skips… sub-agents and plan mode").
- Kept: https://pi.dev/packages?name=subagents — ecosystem listing (extracted, relative dates).
- Kept: https://pi.dev/packages/pi-subagent-manager and https://pi.dev/packages/pi-herdsman — closest hierarchical-steering candidates (extracted, not read at source).
- Rejected/deprioritized: https://pi.dev/packages/pi-orch-extension — stale (2026-07-08), overlaps with pi-subagents.
- Rejected/deprioritized: the-agent-daily.org deep dives — secondary commentary, not needed.
- Rejected/deprioritized: @groeponline/pi-agent-orchestrator, ruizrica/agent-pi, stew675/pi-orchestration — seen only as search snippets; dates and features unverified.
- Search status: Exa hit a 429 rate limit and DuckDuckGo returned a bot check; the ecosystem list therefore comes from pi.dev listing extraction, not a full web sweep. Brave/Tavily/other providers were not tried (not needed for a read-only brief, but coverage is partial).

## Next steps
1. Test whether a pi-subagents child appears in `intercom({ action: "list" })` in a live session. This decides whether workers can be human-addressed directly.
2. Read `pi-subagent-manager` and `pi-herdsman` READMEs on GitHub (or the npm tarball, without installing) to confirm nested-steer, worktree, and jj behavior before choosing one.
3. Confirm whether pi-subagents git-worktree isolation works in a colocated jj repo, or whether the worker tier should use jj workspaces directly by a Zellij-launched Pi session (an intercom-addressable conductor).

## Structured summary: What Pi already gives you vs gaps

**Already there**
- Mid-level agent owns children: `subagent` in builtin tools; depth cap 2 by default; `subagent_supervisor` for answering children; `contact_supervisor` for asking the parent.
- Human visibility/steer: `/subagents-fleet` (steer `s`, stop `D`), `status` tree with nested ids, `interrupt`/`resume`/`stop` by nested id.
- Named conductor sessions with blocking `ask`, `handover`, and a 24 h mailbox for disconnected named sessions (pi-intercom).
- Background runs, retained children, staged lanes, typed gates, budgets, output schemas.
- Git-worktree isolation with patch capture and cleanup.

**Gaps for your setup**
- Workers/nested children are not documented as intercom peers; human-to-worker messaging goes through steer or `ask` via the parent, not directly.
- jj workspaces not supported by pi-subagents' isolation (git-only, clean-tree precondition).
- No Zellij pane/inspector backend (tmux, Ghostty, Herdr only).
- No built-in task board or planning tier; community packages cover this (unvetted).
- Mario's stated stance: no built-in subagents, plan mode, or MCP; sub-agents are a package concern, and he is skeptical of parallel sub-agent implementation.

# Research: Hierarchical / orchestrator-worker coding agents and human-in-the-loop management (beyond Claude Code)

## Summary
Evidence supports a middle management layer only when the work is decomposable and the management layer stays read-mostly. Cognition (≈Apr 2026) and Cursor (Jan 2026) both report that multi-agent setups work when writes stay single-threaded and additional agents plan, explore, or review. The binding constraint in 2026 data is human review, not agent output: a Jellyfish-based study reported by Ars Technica (Oct 2026) found review time rose 49% after agent adoption. A brief should therefore be a verifiable contract (outcome, scope, done criteria, escalation triggers), not a loose instruction.

## Findings

1. **Claim:** A flat swarm of equal agents failed; a planner/worker/judge hierarchy worked for Cursor, and it removed an integrator role that added bottlenecks. **Sources:** [Scaling long-running autonomous coding (Cursor, Jan 2026)](https://cursor.com/blog/scaling-agents); [Simon Willison summary, 19 Jan 2026](https://simonwillison.net/2026/jan/19/scaling-long-running-autonomous-coding/). **Support:** direct evidence (company blog, self-reported). Flat design: lock-based coordination throttled 20 agents to the throughput of 2–3, and with no hierarchy agents "became risk-averse" and avoided hard tasks. Planners (with sub-planners) created tasks; workers pushed to one branch; a judge agent decided per cycle whether to continue with a fresh start. An integrator role was dropped because it "created more bottlenecks than it solved." **Confidence:** medium (self-reported, no independent verification of the browser's quality; Willison's review found it worked but had rendering glitches and initial CI failures).

2. **Claim:** Multi-agent value is in parallel read/intelligence work; parallel writers fragment decisions. **Sources:** [Multi-Agents: What's Actually Working (Cognition)](https://cognition.com/blog/multi-agents-working); [Don't Build Multi-Agents (Cognition, 2025)](https://cognition.com/blog/dont-build-multi-agents). **Support:** direct evidence for the claim as stated by Cognition. Cognition says "multi-agent systems work best today when writes stay single-threaded." Dating: the post says "10 months ago" relative to the June 2025 original, so ≈Apr 2026 (**researcher inference** on the date). **Confidence:** medium-high on the principle; it is the vendor's own product experience.

3. **Claim:** Clean-context review agents catch bugs the coder misses; Devin Review catches ~2 bugs per PR, ~58% severe (vendor figure). **Sources:** [Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working). **Support:** direct (vendor-reported). Cognition found the coder–reviewer loop worked best when the reviewer shared no context beforehand. **Confidence:** medium (no independent benchmark).

4. **Claim:** Manager agents need dedicated work: they over-prescribe, assume shared state with children, and don't relay cross-agent messages by default. **Sources:** [Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working). **Support:** direct (Cognition's description of Devin's manager/child design, which it says is live). **Confidence:** medium.

5. **Claim:** Worker briefs need an objective, output format, tool/source guidance, and explicit boundaries; short instructions caused duplicated work. Scale effort to complexity with explicit rules (1 agent / 3–10 calls for simple tasks; more subagents only for complex ones). Early agents spawned 50 subagents for simple queries. **Sources:** [How we built our multi-agent research system (Anthropic, June 2025)](https://www.anthropic.com/engineering/multi-agent-research-system). **Support:** direct (company post; research domain, not coding). Dated June 2025, so treat as **background**. **Confidence:** high for the failure modes described; medium for transfer to coding.

6. **Claim:** Multi-agent systems use ~15× the tokens of chats and suit parallelizable tasks. Anthropic says most coding tasks have fewer parallelizable parts than research. **Sources:** [Anthropic research post](https://www.anthropic.com/engineering/multi-agent-research-system). **Support:** direct, research domain. **Confidence:** high for the cited numbers; **background**.

7. **Claim:** Human review is the bottleneck. A study of ~700 firms (Jellyfish data, Chen & Stratton) found review time rose 49%, the share of PRs with changes requested nearly doubled, and comments per PR rose 35% after agent adoption. **Sources:** [Ars Technica, Oct 2026](https://arstechnica.com/ai/2026/10/ai-coding-agents-generate-more-code-but-not-more-software/) (primary paper cited there: [Chen & Stratton, fion.ac/jellyfish.pdf](https://fion.ac/jellyfish.pdf), not fetched). **Support:** direct for the Ars-reported figures. The "30% more code" headline number appears only in secondary blogs and was not verified. **Confidence:** medium-high (recent, large sample; data cutoff Mar 2026).

8. **Claim:** Simon Willison: review is the natural bottleneck for parallel agents; he limits himself to reviewing one significant change at a time; spec-first work is much cheaper to review, and research/maintenance tasks are safe to parallelize. **Sources:** [Embracing the parallel coding agent lifestyle (Willison, 5 Oct 2025)](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/). **Support:** direct (practitioner account). **Confidence:** medium; dated Oct 2025 (**background**).

9. **Claim:** Escalation to a stronger model fails when the weaker primary can't tell when it's out of its depth. Cognition recommends prescribing domain triggers (e.g., always escalate merge conflicts). Cross-frontier routing works better than small-to-large escalation. **Sources:** [Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working). **Support:** direct (vendor experience; "open problem"). **Confidence:** medium. This maps directly onto a brief's explicit escalation list.

10. **Claim:** Codex's subagent docs say to use parallel agents for read-heavy work (exploration, tests, triage) and be careful with parallel write-heavy work, and to give subagents an explicit division of labor and output format. Subagent runs cost more tokens. **Sources:** [Subagents, ChatGPT Learn / Codex docs (undated; current)](https://learn.chatgpt.com/docs/agent-configuration/subagents?surface=app). **Support:** direct (vendor docs). **Confidence:** high for what the docs say; the docs are a product spec, not outcome evidence.

11. **Claim:** Cloud-async delegation (Codex cloud: each task in its own sandbox, returns a PR for review) is the product pattern for human-reviewed batches. **Sources:** [Introducing Codex (OpenAI, May 2025)](https://openai.com/index/introducing-codex/); [Using Codex Cloud (OpenAI Help)](https://help.openai.com/en/articles/20001545-using-codex-cloud). **Support:** direct, but older (**background**). **Confidence:** medium.

12. **Claim:** Devin can "manage Devins": a manager splits work, child Devins run in isolated VMs, and the manager synthesizes. **Sources:** [Devin can now Manage Devins (Cognition)](https://cognition.com/blog/devin-can-now-manage-devins); [agentmarketcap, Apr 2026](https://agentmarketcap.ai/blog/2026/04/10/devin-parallel-sessions-multi-agent-concurrency) (secondary). **Support:** direct for feature existence; date of the Cognition post not verified. **Confidence:** medium.

13. **Claim:** Ralph loop (Huntley): each iteration is a fresh instance with clean context, and memory lives in git history, progress.txt, and a PRD file. **Sources:** [everything is a ralph loop (ghuntley.com, 17 Jan 2026)](https://ghuntley.com/loop/); [snarktank/ralph](https://github.com/snarktank/ralph) (third-party implementation). **Support:** search-snippet level; I did not fetch the full essay. **Confidence:** low-medium. Its fresh-start idea matches Cursor's cycle-reset finding.

14. **Claim:** Addy Osmani describes a progression from "conductors" (one agent, supervised) to "orchestrators" (many agents, architected tasks, outcome evaluation); seasoned engineers adopt orchestration earlier because they can architect and evaluate. **Sources:** [Conductors to Orchestrators (Osmani)](https://addyosmani.com/blog/future-agentic-coding/); [O'Reilly Radar republication](https://www.oreilly.com/radar/conductors-to-orchestrators-the-future-of-agentic-coding/). **Support:** search-snippet level; full text not fetched; date not verified. **Confidence:** low-medium.

15. **Claim:** GitHub Agent HQ lets third-party agents (Claude, Codex) run inside GitHub/VS Code under a Copilot subscription, public preview (Feb 2026). **Sources:** [Agent HQ (GitHub Blog)](https://github.blog/news-insights/company-news/welcome-home-agents/); [Pick your agent (GitHub Blog)](https://github.blog/news-insights/company-news/pick-your-agent-use-claude-and-codex-on-agent-hq/); [WinBuzzer, 5 Feb 2026](https://winbuzzer.com/2026/02/05/github-agent-hq-claude-codex-multi-agent-platform-xcxwbn/). **Support:** direct for availability. It has no evidence on management-layer effectiveness. **Confidence:** medium.

## Contradictions
- **Scale vs. simplicity:** Cursor reports that hundreds of concurrent workers made real progress over a week, yet it also reports that a more complex integrator and locking design hurt. Cognition argues against unstructured swarms and for "map-reduce-and-manage." Both agree on hierarchy with single-threaded writes; they differ on how much coordination machinery is worth it.
- **Parallelism value:** Anthropic reports 90% faster research and 15× tokens. The Jellyfish data suggests that the speed gains in code are offset by review time. These are different task types and different metrics.
- **Smart-friend escalation:** Cognition reports that it fails with weaker primaries and works with frontier pairs. Cursor and Anthropic do not test this directly.

## Missing evidence
- No independent (non-vendor) controlled comparison of manager-layer vs. flat-worker designs for coding was found.
- The Harvard/Chen & Stratton "30% more code" figure is not verified from the primary paper (it was not fetched).
- Amp, Factory, Google Jules, and Kent Beck were not researched (search rate limits). Huntley and Osmani are snippet-level only.
- Cognition's exact publication date is inferred, not stated.
- No evidence was found on how well human stopping-point reviews of batch briefs perform compared with per-PR review.

## Sources
- Kept: Multi-Agents: What's Actually Working, Cognition (https://cognition.com/blog/multi-agents-working) — the most direct source on manager/child design, single-threaded writes, escalation, and review loops.
- Kept: Scaling long-running autonomous coding, Cursor (https://cursor.com/blog/scaling-agents) — planner/worker/judge, failure modes, removing integrator.
- Kept: Ars Technica, Oct 2026 (https://arstechnica.com/ai/2026/10/ai-coding-agents-generate-more-code-but-not-more-software/) — recent review-bottleneck data.
- Kept: How we built our multi-agent research system, Anthropic (https://www.anthropic.com/engineering/multi-agent-research-system) — brief/effort-scaling rules; background (2025).
- Kept: Embracing the parallel coding agent lifestyle, Willison (https://simonwillison.net/2025/Oct/5/parallel-coding-agents/) — review bottleneck, spec-first.
- Kept: Codex subagents docs (https://learn.chatgpt.com/docs/agent-configuration/subagents?surface=app) — read-vs-write parallelism guidance.
- Kept with caveat: Ralph loop essay (https://ghuntley.com/loop/) — snippet only.
- Rejected/deprioritized: ediscoverytoday.com, dromeas.ai, alexcloudstar.com, codex.danielvaughan.com — secondary/SEO summaries of the review-bottleneck study; used only to locate the Ars source.
- Rejected: agentcritiq.com "Devin Teams" — hype-style news page; the feature claim is not supported by Cognition's own post.

## Next steps
1. Fetch the Chen & Stratton Jellyfish PDF to verify the 30%/20%/49% figures and the study design.
2. Fetch Osmani's "Conductors to Orchestrators" and Huntley's "everything is a ralph loop" to extract concrete brief/stopping-point guidance.
3. Search for Amp and Factory "droid" orchestration docs (2026) on how they handle escalation and review gates.

## Evidence-backed principles (for the planning → conductor → worker design)
1. Keep one writer per branch/workspace; let the management layer plan, explore, and review (Cognition; Cursor; Codex docs).
2. Add a middle layer only for decomposable batches with verifiable done criteria (Cursor, Anthropic). Skip it for tightly coupled work.
3. Briefs should state objective, output format, scope boundaries, tool/source hints, and effort limits (Anthropic). Specs make review cheaper (Willison).
4. Put escalation triggers in the brief as explicit domain rules (Cognition's merge-conflict example). Do not rely on the agent sensing its own limits.
5. Use a clean-context reviewer for each batch output (Cognition), and reset cycles with fresh contexts to fight drift (Cursor; Ralph).
6. Budget human review, not agent throughput: the Jellyfish data shows review time rising, so cap the number of parallel batches at what you can review (Willison; Ars/Jellyfish).
7. Watch for failure modes: over-spawning, duplicated work, risk-averse agents with no owner, lock/coordination bottlenecks, unshared state assumptions, and context pollution from noisy output (Anthropic; Cursor; Cognition; Codex docs).

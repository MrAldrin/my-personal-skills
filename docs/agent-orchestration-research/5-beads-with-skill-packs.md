# Research: Beads (bd) combined with third-party agent skill packs (as of 2026-11-16)

## Question

How do other people combine Beads (steveyegge/beads, the `bd` issue tracker) with third-party agent skill packs that assume their own task tracking (mattpocock/skills wayfinder and setup-matt-pocock-skills, obra/superpowers, and similar)? Do published solutions exist, so that no custom adapter is needed?

## Summary

- An adapter is not needed for mattpocock/skills. Upstream has no Beads backend. It supports a documented "Other" tracker path: the user writes the workflow as prose in `docs/agents/issue-tracker.md`, and the skills follow it. Upstream closed the Beads requests as already possible through this path. [1][2]
- A tested Beads template exists, but only on a fork. It maps wayfinder, to-tickets and implement onto `bd`. [3][4]
- Beads itself ships a Claude Code plugin and a bundled skill. It does not ship any integration with superpowers, wayfinder or mattpocock. The Beads repo has no code-search hits for those names. [5][6]
- Several community projects rewrite superpowers so that it stores plans, tasks and evidence in `bd`. These are full replacements, not overlays. Most are young and have few stars. [7][8][9]
- Most common pattern: keep the skill pack as is, and record in its tracker config how to use `bd`. Other users keep `bd` for cross-session work and let in-session checklists stay in the skill pack's own format. [1][10]

## Findings

### 1. mattpocock/skills: pluggable trackers

**Supported trackers.** Setup offers three first-class trackers: GitHub, GitLab and local markdown. Every other tracker uses the "Other" path. The user describes the workflow in one paragraph. The skill saves it to `docs/agents/issue-tracker.md`. [1][11]

**Tracker doc format.** Each tracker template defines the operations the skills expect. The local-markdown template is the clearest example. It has four parts: "publish to the issue tracker", "fetch the relevant ticket", "Wayfinding operations", and conventions for files and status lines. [12]

**Operations wayfinder expects.** The wayfinder skill needs a map issue with child tickets, blocking edges, a frontier query, a claim, and a resolve step. The skill says the native tracker dependency should be used when the tracker has one. A body convention is the fallback. Wayfinder reads the "Wayfinding operations" section of the tracker doc for how the repo expresses these operations. [13][14]

**Beads requests.**
- #116 asked for Beads support in setup. It was closed on 2026-08-21 as "already possible via the Other path". [15]
- #980 brought a tested Beads template and asked for first-class status. It was closed on 2026-10-07. The maintainer kept first-class support to GitHub, GitLab and local markdown. [2][16]
- #1032 asked for support for private, offline trackers such as Beads and beads-rust. It was closed on 2026-10-07 with the same reason. [2]
- The out-of-scope policy says first-class backends are limited to GitHub, GitLab and local markdown. It names Jira, Linear and other trackers as out of scope. [17]

**Upstream text on Beads.** The setup template says: "It is how Jira, Linear, Azure DevOps and Beads all work." It also says users have built Other-path variants, including one for Beads. [18]

**Repo note.** `skills/in-progress/software-factory/TICKET-TRACKERS.md` lists Beads as a repo-native tracker with dependency tracking. It says the upstream survey was done in 2026-10. [19]

### 2. Beads: own skills, plugin, and guidance for other packs

**Plugin and skill.** Beads ships a Claude Code plugin under `plugins/beads`. It has slash commands (audit, blocked, close, comments, compact, create, and more), a bundled `beads` skill and a `task-agent` subagent. It also has Codex and Copilot manifests. The plugin is listed in `.claude-plugin/marketplace.json` as `beads` version 1.3.4. [5][6]

**Plugin docs.** The docs describe the plugin as slash commands, a bundled skill and lifecycle hooks. They do not mention superpowers, wayfinder or mattpocock. [20]

**Integration docs.** `docs/integrations/` has per-harness pages (Claude Code, Codex, Cursor, Copilot CLI, Gemini and others). `docs/multi-agent` also exists. I did not find a page on combining with third-party skill packs. [21]

**Search result.** Code search in steveyegge/beads for "superpowers", "wayfinder" and "mattpocock" returned no hits. Issue search returned no usable results because of query errors. This result is therefore not conclusive. [researcher check]

**Contributions by others.** Several PRs and issues in obra/superpowers ask for Beads or lifecycle hooks:
- PR #611 (Horspowers, Beads sync) is closed. Its body says it syncs design docs to a Beads epic and plans to tasks. I did not check whether it was merged. [22]
- Issue #1442 asks for lifecycle events so external plugins can integrate. It is closed. The author says they want `bd` as the source of truth alongside the markdown plan. [23]
- PR #1461 adds lifecycle event hooks. It is closed. [24]

### 3. Community bridges

Each row below was checked by its repo metadata and README. None is an official Beads or obra project.

| Project | What it does | Last push | Stars | License | Source |
| --- | --- | --- | --- | --- | --- |
| jbongaarts/superpowers-beads | Beads-native rewrite of superpowers skills. Plans, tasks, debugging evidence and review feedback are stored in `bd`. Skills fall back to no-Beads mode if `bd` is absent. | 2026-06-22 | 1 | NOASSERTION (not verified) | [7] |
| DollarDill/beads-superpowers | "Process discipline and persistent memory" for Claude Code and 7 other agents. Stores memory in Beads. | 2026-10-31 | 32 | MIT | [8] |
| the-inconvenience-store/superbeads | Similar scope. Says it uses a Dolt-backed tracker. Appears to be a near-copy of DollarDill's text. | 2026-07-31 | 0 | MIT | [9] |
| chrisblizzard/superpowers-beads-plugin | Plugin for "moments" in a superpowers fork. Aim: keep specs, plans and status in Beads. The Beads plugin is not built yet. Only a moment-logger ships. | 2026-11-14 | 0 | none | [25] |
| maslennikov-ig/template-bridge | Bundle: superpowers, Beads and 413 templates, with a unified workflow skill. | 2026-11-12 | 73 | MIT | [26] |
| cuongbphv/beads-pm-kit | Ten project-manager skills for `bd`. Builds per-harness copies. Not a superpowers adapter. | 2026-09-04 | 2 | MIT | [27] |
| eitsupi/beads-skills | Small skill set for `bd` (full-text search, comments, triage). Not a skill-pack adapter. | 2026-11-15 | 0 | MIT | [28] |
| LeonidShamis/mattpocock-skills (fork) and test repo | Adds `issue-tracker-beads.md` to setup. End-to-end test: 19 of 19 issues closed, 45 of 45 tests green, `bd dolt push` sync. | fork commit dc8d051; test repo pushed 2026-08-27 | not checked | not checked | [3][4] |

Notes:
- Star counts are small. Only maslennikov-ig/template-bridge and DollarDill/beads-superpowers have more than 30 stars.
- These projects replace the skill pack's content. They do not wrap it. A user who keeps stock superpowers or mattpocock skills gets no benefit from them.
- The Leonid template was built against `bd` v1.2.2. Its README says setup proposes Beads when `.beads/` exists. Upstream setup does not do this. [3]

### 4. Common patterns

**A. Rewrite the skills (replacement).** Used by jbongaarts/superpowers-beads, DollarDill/beads-superpowers and superbeads. Each skill keeps its process rules and changes its storage from markdown and TodoWrite to `bd` issues. The jbongaarts README states the reason: markdown plans and TodoWrite lose state on compaction and restart. [7]

**B. Tracker adapter doc (configuration).** Used by mattpocock/skills (Other path) and the Leonid template. The skill pack stays unchanged. A doc in the repo maps its operations to `bd` commands. Upstream says this is the intended path for trackers it does not support. [1][17]

**C. Beads for cross-session work only.** Users keep `bd` as the ledger for multi-session work. In-session steps stay in the skill pack's own list. jbongaarts' README says the skills should keep working without Beads if `bd` is missing. [7] I did not find a source that states this pattern as a named practice. The pattern is an inference from these sources. [inference]

**D. Hooks and plugin moments.** The chrisblizzard project and obra's lifecycle-hook requests point to this pattern. A plugin listens for events and writes to `bd`. No finished, widely used version was found. [23][25]

## Options for us

Options are ordered by cost. Owner decides. I did not change any file.

1. **Adapter doc only (lowest cost).** Write `docs/agents/issue-tracker.md` in the repo that uses wayfinder and the other mattpocock skills. It maps the Other-path operations to `bd`: create map and child tickets, `bd dep` for blocking, `bd ready` for the frontier, assignee as the claim, and close with a resolution comment. No code. Use upstream setup to create the file. This follows the upstream design.
2. **Reuse the Leonid template.** Copy its `issue-tracker-beads.md` content into our doc. Before reuse, check the fork's license. The license was not checked in this research.
3. **Use a Beads-native superpowers rewrite.** Install one of jbongaarts/superpowers-beads or DollarDill/beads-superpowers in place of stock superpowers. This is a large change. It conflicts with any local edits. Review the code and maintenance status first. Evidence on quality is missing.
4. **Keep the split.** Use `bd` for cross-session tasks as AGENTS.md already says. Let skill packs keep their in-session lists. Add a short note in the repo docs that says which layer owns which state. This is the smallest change that respects both systems.
5. **Upstream change.** Not useful now. Upstream closed the Beads requests, and its out-of-scope policy names trackers beyond the three supported as out of scope.

Recommendation for the owner to consider: option 1 or 4. Both avoid a custom adapter and avoid a fork.

## Contradictions

- Upstream says Beads works through the Other path (#116, #980 closure). The Leonid test shows the same work needs a detailed template to run cleanly. Both are true: the Other path works, but the detail is left to each user.
- The superbeads README and DollarDill's README share wording. I did not check which came first. Treat them as one source.

## Missing evidence

- No merged upstream change in mattpocock/skills adds Beads. Confirmed through issue closures only.
- No check of obra/superpowers PR #611 merge status. Closed is confirmed. Merged is not.
- No check of the license of LeonidShamis/mattpocock-skills (fork).
- No test of any community bridge against a real session. Only READMEs and repo metadata were read.
- Beads code search for skill-pack names returned no hits, but the search may not be exhaustive.
- No independent source on whether wayfinder's `wayfinder:` labels and claim-by-assignee map cleanly onto `bd` assignee and `bd dep`. The Leonid template claims it does. Not verified here.
- No source found for the cross-session-only pattern (option 4) as a named practice.

## Sources

1. mattpocock/skills, setup-matt-pocock-skills SKILL.md (Section A, "Other" option): https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md
2. mattpocock/skills #1032, closed 2026-10-07: https://github.com/mattpocock/skills/issues/1032 ; #980, closed 2026-10-07: https://github.com/mattpocock/skills/issues/980
3. LeonidShamis/mattpocock-skills-issue-tracker-beads-test (README): https://github.com/LeonidShamis/mattpocock-skills-issue-tracker-beads-test
4. LeonidShamis/mattpocock-skills fork, commit dc8d051 (named in the test README): https://github.com/LeonidShamis/mattpocock-skills
5. steveyegge/beads, plugin directory: https://github.com/steveyegge/beads/tree/main/plugins/beads
6. steveyegge/beads, marketplace manifest: https://github.com/steveyegge/beads/blob/main/.claude-plugin/marketplace.json
7. jbongaarts/superpowers-beads (README): https://github.com/jbongaarts/superpowers-beads
8. DollarDill/beads-superpowers (README): https://github.com/DollarDill/beads-superpowers
9. the-inconvenience-store/superbeads (README): https://github.com/the-inconvenience-store/superbeads
10. Leonid test repo, "Other" path discussion in mattpocock #116 comments: https://github.com/mattpocock/skills/issues/116
11. mattpocock/skills, setup issue-tracker-local.md: https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md
12. mattpocock/skills, docs/engineering/wayfinder.md: https://github.com/mattpocock/skills/blob/main/docs/engineering/wayfinder.md
13. mattpocock/skills, wayfinder SKILL.md: https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md
14. mattpocock/skills, issue-tracker-local.md "Wayfinding operations" section (same file as 11)
15. mattpocock/skills #116, closed 2026-08-21: https://github.com/mattpocock/skills/issues/116
16. mattpocock/skills #980 closure comment (same URL as 2)
17. mattpocock/skills, .out-of-scope/mainstream-issue-trackers-only.md: https://github.com/mattpocock/skills/blob/main/.out-of-scope/mainstream-issue-trackers-only.md
18. mattpocock/skills, setup-matt-pocock-skills.md (docs): https://github.com/mattpocock/skills/blob/main/docs/engineering/setup-matt-pocock-skills.md
19. mattpocock/skills, TICKET-TRACKERS.md: https://github.com/mattpocock/skills/blob/main/skills/in-progress/software-factory/TICKET-TRACKERS.md
20. Beads Claude Code plugin docs: https://github.com/steveyegge/beads/blob/main/docs/integrations/claude-code-plugin.md
21. steveyegge/beads, docs/integrations directory: https://github.com/steveyegge/beads/tree/main/docs/integrations
22. obra/superpowers PR #611 (Horspowers Beads sync), closed: https://github.com/obra/superpowers/pull/611
23. obra/superpowers issue #1442 (lifecycle events for external integration), closed: https://github.com/obra/superpowers/issues/1442
24. obra/superpowers PR #1461 (lifecycle event hooks), closed: https://github.com/obra/superpowers/pull/1461
25. chrisblizzard/superpowers-beads-plugin (README): https://github.com/chrisblizzard/superpowers-beads-plugin
26. maslennikov-ig/template-bridge (README): https://github.com/maslennikov-ig/template-bridge
27. cuongbphv/beads-pm-kit (README): https://github.com/cuongbphv/beads-pm-kit
28. eitsupi/beads-skills (README): https://github.com/eitsupi/beads-skills
29. obra/superpowers, writing-plans SKILL.md (plan path `docs/superpowers/plans/`): https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md
30. obra/superpowers repo (318k stars at check time, pushed 2026-11-03): https://github.com/obra/superpowers

Method: `gh` CLI (authenticated) for repo metadata, file contents, issues and code search. WebSearch was not used. No file was edited and nothing was committed outside this report.

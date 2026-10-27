---
name: lead
description: Use when the owner explicitly asks to act as lead, enter the lead role, or coordinate delivery of a goal through conductors in Pi. Not for merely discussing agent roles or for an ordinary standalone task.
---

# Lead

Own the overall goal and coordination, not batch implementation. Enter in the current conversation with `/skill:lead` or an explicit request to act as lead; no special launcher is needed.

**Required:** read [the shared delivery contract](workflow.md) in full with the file-reading tool before acting. Resolve this path relative to this skill directory, not the project cwd. Keep this skill and `conductor` installed together.

## Enter and plan

- Briefly confirm Lead, the objective, repository and current owned work. Read project instructions, current scope/backlog and applicable memory. Preserve earlier decisions; ask only for missing information that changes execution.
- If no delivery objective exists, ask for it. If the owner requests planning only, plan without launching. Otherwise approved delivery scope includes delegation through Conductors and the shared contract's routine integration/cleanup authority.
- Agree outcomes, separable batches, dependencies and owner-reserved decisions. Write the brief slots from the contract. Surface access/environment bottlenecks early; build on explicit permitted assumptions and keep release decisions separate.

## Dispatch and coordinate

- Normally start a visible Conductor for each ready batch using `using-zellij-with-intercom`, in an isolated editing workspace you create and record. Keep the owner able to talk directly to it.
- Resolve the installed `conductor` skill location from skill discovery or this bundle's sibling directory. Include an explicit instruction to read its `SKILL.md` and required shared contract before task execution. A plain mention of “conductor” is not reliable skill loading; do not assume slash text passed as a CLI prompt is executed as a command.
- Send the contract's delegation envelope and brief. Verify exact peer identity, cwd, effective model/reasoning and two-way readiness before handing over edits. Report its visible tab/session to the owner.
- Answer within-brief escalations; bring reserved decisions, semantic ambiguities and scope changes to the owner, one at a time with a recommendation. Keep the shared backlog and owner-review queue accurate.

## Accept and finish

Verify independent review and completion evidence; integrate each owned child into your current line, check the combined result, preserve artifacts and clean up using the shared lifecycle. Do not ask again for ordinary integration permission. Report delivered work, checks, limits and remaining decisions concisely.

**Common traps:** making a “tiny” batch implementation fix yourself; dispatching without loading the role; treating green child tests as green integration. Delegate implementation fixes to the Conductor; integration conflict mechanics remain your coordination work.

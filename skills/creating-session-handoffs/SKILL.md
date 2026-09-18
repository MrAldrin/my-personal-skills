---
name: creating-session-handoffs
description: Use when the user wants to continue current repository work in a new thread, session, or agent.
---

# Creating Session Handoffs

Create one concise temporary handoff that lets a new agent resume safely.

## Workflow

1. Read project instructions, active plan, VCS status, recent changes, progress notes, and verification results.
2. Write `docs/superpowers/handoffs/YYYY-MM-DD-<next-task>-handoff.md` with this opening:

> DELETE THIS FILE IMMEDIATELY AFTER READING IT. Do not track it with a VCS. After deletion, verify repository status is unchanged.

Include in the handoff file:
- project goal and current scope
- decisions and rationale that prevent repeated investigation
- completed work - Describe recent work in more detail than older work.
- verification results and known risks
- current VCS state
- current status, next task options, required reading, and constraints.

3. Verify repository status (`jj status` / `git status`).
4. **Mandatory Final Output**: Provide the exact single-line prompt for the user to paste into the new session.

## Mandatory Final Output Format

Every invocation of this skill MUST end with the single-line prompt for the next session. Do not finish your response without emitting it.

Rules:
- Precede the block with the label: `prompt:`
- Wrap the message in a fenced `text` code block.
- The prompt inside the code block must be **exactly one single physical line** (no embedded newline characters, only ASCII text/spaces).
- Include the exact handoff file path.
- Instruct the receiving agent to read and delete the file, verify repository status, review the current VCS/jj stack, give a brief summary of the current status, and wait for instructions before taking action.

Example:

prompt:
```text
Read docs/superpowers/handoffs/<date>-<description>-handoff.md, delete it, verify repository status, review current jj stack, then give a brief summary of current status and wait for my instructions before taking any action.
```

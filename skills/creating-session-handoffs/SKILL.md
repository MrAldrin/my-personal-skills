---
name: creating-session-handoffs
description: Use when the user wants to continue current repository work in a new thread, session, or agent.
---

# Creating Session Handoffs

Create one concise temporary handoff for the specific follow-up the user wants to take into a new session, not a recap of everything in the old session. The receiving agent should be able to name its task and wait for approval.

## Workflow

1. Identify the user's chosen next task. If several possibilities remain and the priority is unclear, ask which one to hand off. Read project instructions, relevant plan and progress notes, VCS status and recent changes, and verification results as needed for that task.
2. Write `docs/superpowers/handoffs/YYYY-MM-DD-<next-task>-handoff.md` with this opening:

> DELETE THIS FILE IMMEDIATELY AFTER READING IT. Do not track it with a VCS. After deletion, verify repository status is unchanged.

Lead with **Next task (awaiting user approval)**: state one specific assignment and its intended outcome in plain language. Include the key constraint or blocker and what is out of scope. Do not turn other possible work into competing next tasks. Then give only the context needed for that assignment:
- relevant decisions and rationale that prevent repeated investigation
- completed work and verification results, distinguishing reported results from checks the receiving agent must run
- current VCS state, known risks, required reading, and constraints.

3. Verify repository status (`jj status` / `git status`). In your response, briefly name the chosen next task and the handoff file so the user can check its focus.
4. **Mandatory Final Output**: Provide the exact single-line prompt for the user to paste into the new session.

## Mandatory Final Output Format

Every invocation of this skill MUST end with the single-line prompt for the next session. Do not finish your response without emitting it.

Rules:
- Precede the block with the label: `prompt:`
- Wrap the message in a fenced `text` code block.
- The prompt inside the code block must be **exactly one single physical line** (no embedded newline characters, only ASCII text/spaces).
- Include the exact handoff file path.
- Instruct the receiving agent to read and delete the file, verify repository status, and review the current VCS/jj stack. Then lead with the specific next task, intended outcome, and key constraint or blocker in 2-3 sentences. If the task is unclear, ask the user. Wait for approval before starting the task; reading, deletion, and status review are permitted preparation.

Example:

prompt:
```text
Read docs/superpowers/handoffs/<date>-<description>-handoff.md, delete it, verify repository status, and review the current jj stack (or Git state). Then tell me in 2-3 sentences your specific next task, its intended outcome, and any key constraint or blocker. If the task is unclear, ask me. Wait for my approval before starting the task.
```

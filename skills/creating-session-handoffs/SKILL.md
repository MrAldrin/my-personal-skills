---
name: creating-session-handoffs
description: Use when the user wants to continue current repository work in a new thread, session, or agent.
---

# Creating Session Handoffs

Create one concise temporary handoff for the specific follow-up the user wants to take into a new session, not a recap of everything in the old session. Help the returning user remember the purpose, settled context, next action, and whether their input is needed.

## Workflow

1. Identify the user's chosen next task. If several possibilities remain and the priority is unclear, ask which one to hand off. Read project instructions, relevant plan and progress notes, VCS status and recent changes, and verification results as needed for that task.
2. Write `docs/superpowers/handoffs/YYYY-MM-DD-<next-task>-handoff.md` with this opening:

> DELETE THIS FILE IMMEDIATELY AFTER READING IT. Do not track it with a VCS. After deletion, verify repository status is unchanged.

Immediately below that notice, put the four-bullet brief defined below. Then give only the supporting context needed for that assignment:
- relevant decisions and rationale that prevent repeated investigation
- completed work and verification results, distinguishing reported results from checks the receiving agent must run
- current VCS state, known risks, required reading, and constraints.

3. Verify repository status (`jj status` / `git status`). Lead your response with the same four-bullet brief, then name the handoff file. Put routine deletion/status/stack bookkeeping after the brief; mention a material repository problem in the brief.
4. Finish with the exact single-line prompt for the user to paste into the new session.

## Four-bullet brief

Use exactly four Markdown bullets, each starting `- **Label:**`, in this order. Use the same bullet format in the file, creator response, and receiving response. Aim for 60-100 words total, in plain language:

- **Goal:** What we want and why it matters, without assuming the answer to an open question.
- **Where we are:** What is done or decided, and the specific part still open. Distinguish verified results from reported or untested claims.
- **Next:** One concrete next action and its expected result. Do not turn other possible work into competing assignments.
- **Your input:** The specific approval or decision needed, or "Already approved" with the execution limits and genuine stop conditions.

Carry forward explicit user approval accurately; do not infer it from backlog placement or from a request to write a handoff. If execution approval is absent, say it is awaiting approval. Preserve project safeguards and separate gates, such as deployment approval. An unknown the agent can investigate within approved scope is next-step work, not automatically a blocker.

## Receiving a handoff

Read and delete the temporary file as instructed, verify repository status, and review the current VCS/jj stack. Lead your substantive reply with the four-bullet brief, deriving its facts from the handoff and checking them against current state. Keep routine bookkeeping secondary.

If execution is explicitly approved and current safeguards allow it, proceed within that scope without asking for general approval again. Otherwise wait for the specific approval or decision named in **Your input**. If the task, authority, or current state conflicts, ask a focused question before the affected operation. Reading, handoff deletion, and status review are permitted preparation.

## Mandatory Final Output Format

When creating a handoff, end with the single-line prompt for the next session. Receiving a handoff does not require creating another handoff or paste prompt.

Rules:
- Precede the block with the label: `prompt:`
- Wrap the message in a fenced `text` code block.
- The prompt inside the code block must be **exactly one single physical line** (no embedded newline characters, only ASCII text/spaces).
- Include the exact handoff file path. Apart from that path, keep the prompt task-neutral: derive task facts from the handoff, not from duplicated instructions in the paste prompt.
- Request the four-bullet brief and make execution conditional on recorded approval and current safeguards, rather than always asking for approval again.

Example:

prompt:
```text
Read docs/superpowers/handoffs/<date>-<description>-handoff.md, delete it, verify repository status, and review the current jj stack (or Git state). Lead with four short bullets (60-100 words total): Goal (what and why), Where we are (settled and open), Next (action and result), Your input (decision needed or recorded approval and limits). Keep bookkeeping secondary. Proceed only within explicit approval recorded in the handoff and current safeguards; otherwise wait for approval. Ask if the task or authority is unclear.
```

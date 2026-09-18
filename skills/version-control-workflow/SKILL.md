---
name: version-control-workflow
description: Use when implementing tasks in a Jujutsu (jj) repository, splitting work into atomic changes, running jj new or jj describe, or reviewing a completed change stack.
---

# Jujutsu change workflow

Use one development loop: plan logical changes, describe intent, implement, verify, and advance. Finish with a reviewable stack, not an extra summary merge.

## Safety and scope

- Use Jujutsu for repository changes. The working copy is the active `@` change; there is no separate Git staging/commit step.
- The user manages `main`. Never move or modify the `main` bookmark.
- Do not create or move `dev` or other bookmarks by default. If the user requests bookmark tracking, inspect its existing target first and ask before redirecting unrelated work. Track the completed change, not the empty working-copy child.
- Preserve existing edits and history. Do not rewrite unrelated changes or mix the current task into them.
- Do not push, merge, squash, or otherwise integrate the stack as part of normal task completion. Stop for user review; integration requires a separate explicit request.

## Description format (mandatory)

Every task change description must use:

```text
<category> - <goal>: <atomic change description>

Optional body explaining reasoning, trade-offs, or verification.
```

- **Task prefix:** `<category> - <goal>` identifies the work stream. Keep it identical across all related changes.
- **Atomic description:** a concise imperative summary of what this specific change does.
- **Title:** the entire first line must be under 72 characters. Choose a short prefix so the summary has room.
- **Body:** optional; separate it from the title with a blank line. Do not claim verification that was not performed.
- A fresh empty working change may remain undescribed until its next task is known. Do not rename existing unrelated history to enforce this format.

Example:

```bash
jj describe -m "search - add filters: support filtering by status

Keep filtering server-side so pagination remains consistent.

- add coverage for combined filters
- verify existing unfiltered queries remain unchanged"
```

## Development loop

### 1. Inspect and plan

Run `jj status`, `jj log`, `jj bookmark list`, and `jj diff` before editing.

Outline logical outcomes for the task. Each change should be independently reviewable and, where practical, testable; later changes may depend on earlier ones.

- Split by outcome, not by file, tool call, or checklist item.
- Keep behavior and its tests in the same change.
- Keep small tasks in one change; do not manufacture extra steps.
- Separate a prerequisite refactor only when it is useful to review independently.

Reuse an appropriate empty `@` change. If `@` contains unrelated work, leave it intact and start a new change only if building on it is appropriate; otherwise ask where to base the task. If resuming this task's in-progress change, inspect it and continue rather than automatically creating another.

### 2. Describe intent

Before editing, describe the next logical outcome:

```bash
# When reusing an appropriate empty working change:
jj describe -m "<task-prefix>: <planned imperative summary>"

# When a new change is needed on top of the current one:
jj new -m "<task-prefix>: <planned imperative summary>"
```

These are alternatives, not consecutive setup commands.

### 3. Implement and verify

Implement only the current logical outcome and its relevant tests.

Run appropriate checks, inspect `jj diff`, and compare the result with the intended scope. Resolve unintended edits and validation failures before advancing, or report a blocker and stop. If checks cannot run, report that limitation rather than claiming success.

Update the description to reflect the actual result:

```bash
jj describe -m "<task-prefix>: <actual imperative summary>"
```

Check the stable prefix, imperative summary, title length, and accuracy of any body.

### 4. Advance

Once the change is complete, use `jj new` to leave it behind and create a clean working change. For another logical outcome, return to step 2 and describe that empty change; do not create a second empty change unnecessarily.

Example stack for one task:

```text
search - add filters: implement status filtering and tests
search - add filters: connect filter controls to queries
search - add filters: document supported filter combinations
(empty working change)
```

The example is not a mandatory three-change template. Include documentation with the implementation when that makes a more coherent change.

## Completion and cleanup

- Inspect the final stack and `jj status`; leave an empty working change above the completed work.
- Summarize the logical changes, checks performed, and any limitations or remaining work.
- Stop for user review and testing. Do not create a feature-summary merge or automatically integrate the stack after approval.
- Do not automatically delete plan files. Retain project documentation unless removal is requested or part of the agreed task.
- Keep agent scratchpads and temporary debugging artifacts out of the delivered changes. Clean up only your own temporary artifacts before advancing; do not create dedicated scratch-file or cleanup-only changes. Intentional project cleanup may still be a legitimate task.

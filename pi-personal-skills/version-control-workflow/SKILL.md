---
name: version-control-workflow
description: Use when creating (jj new), describing (jj describe), or structuring change descriptions and commits in Jujutsu (jj)
---

# Version control workflow using jj (jujutsu)

## Jujutsu (jj) Concepts (for Git-trained models)

- **Change / Revision** = Equivalent to a Git commit.
- **Working Copy** = Always represented by the active `@` change. Files are tracked automatically.
- **`jj new`** = Creates a new empty change (commit) on top of the current one.
- **`jj describe -m "..."`** = Sets or updates the commit message for the active change.
- **`jj diff`** = Inspects diffs in the active change (like `git diff HEAD`).

## Description Format (Mandatory)

Every jj change description MUST follow this multiline structure:

`<task-prefix>: <atomic change description>`
*(optional blank line + detailed body)*

- **`<task-prefix>`**: Descriptive label defining the work stream, formatted as `<category> - <goal>` (e.g., `model training - trying new features`, `docs - redesigning getting started`). Keep it identical across all related changes so rebased history stays clear.
- **`<atomic change description>`**: Concise imperative summary of what this specific revision does.
- **Line 1 (Title)**: Must be under 72 chars (`<task-prefix>: <atomic change description>`). This is all that appears in `jj log` / `git log --oneline`.
- **Line 2**: Blank line.
- **Line 3+ (Body, optional)**: Longer explanation, bullet points, reasoning, or trade-offs.

### CLI Example
```bash
jj describe -m "model training - trying new features: add polynomial feature generation

- generate degree-2 interactions for numerical features
- update training pipeline config to toggle polynomial features
- benchmark shows +1.2% improvement on test set"
```

## Workflow

1. Start with intent on a clean change:
   ```bash
   jj new -m "<task-prefix>: planned intent"
   ```
2. Implement: Keep changes focused and atomic.
3. Verify and update description: Compare diff against intent, then update message to reflect actual changes:
   ```bash
   jj diff
   jj describe -m "<task-prefix>: actual change summary"
   ```

## Rules & Pitfalls

- **Mandatory prefix**: Every revision must include the `<task-prefix>: ` structure.
- **Atomic changes**: One logical change per revision. Create another change only when work is independently reviewable or testable.
- **No separate commits for transient files**: Agent scratchpads, temp notes, or intermediate debug files belong in the active change, not dedicated revisions.
- **Work on a clean change**: Never append unrelated work to an existing change with edits. Use 'jj new' if the current change already has commits/diffs.

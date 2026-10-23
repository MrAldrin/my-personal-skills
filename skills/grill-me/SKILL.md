---
name: grill-me
description: Use when the user asks to be grilled about a one-off plan, decision, or idea, including non-code discussions.
disable-model-invocation: true
---

Load and follow [grilling](../grilling/SKILL.md). Use the harness skill invocation facility when available; otherwise read that file in full with the file-reading tool. Resolve the path relative to this skill directory, not the working directory.

Do not create or edit project files as part of this entry point unless the user asks. For ongoing project discussions that should persist terminology and decisions, offer `grill-with-docs` instead.

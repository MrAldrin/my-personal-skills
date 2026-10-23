---
name: grill-with-docs
description: Use when the user asks to grill an ongoing project's plan or design and persist agreed terminology and significant decisions.
disable-model-invocation: true
---

Load and follow both [grilling](../grilling/SKILL.md) and [domain-modeling](../domain-modeling/SKILL.md). Use the harness skill invocation facility when available; otherwise read both files in full with the file-reading tool. Resolve paths relative to this skill directory, not the working directory.

Apply both disciplines in the same conversation: ask one question at a time and record resolved terminology as you go. Offer ADRs only when the domain-modeling criteria are met. This entry point authorizes relevant documentation updates, not implementation; honor any read-only or no-edit constraint from the user.

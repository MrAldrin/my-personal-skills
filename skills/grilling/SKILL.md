---
name: grilling
description: Use when the user wants to stress-test a plan, decision, or idea through probing questions, or as the interview discipline for grill-me and grill-with-docs.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree **one question at a time**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Choose the most useful frontier question, give your recommended answer, then wait for the user's answer. Keep other frontier questions for later; do not bundle multiple decisions into a turn.

Format each question like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

```

Word each question so "yes" accepts your recommended answer.

Each answer reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next question. A question whose answer depends on an unsettled decision must wait.

Finding _facts_ is your job, never the user's. Use available tools to look up facts from the environment (filesystem, tools, etc.) rather than asking the user for anything you can inspect yourself. If delegation is authorized and a suitable tool is available, a bounded subagent may investigate; otherwise inspect directly. A running exploration is an unsettled prerequisite: questions downstream of it wait, while another independent frontier question can proceed. If access is unavailable, state the limitation and ask only for the missing information. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not implement the design until the user confirms you have reached a shared understanding. In `grill-with-docs`, capturing an agreed glossary term inline or an approved ADR may happen before that final confirmation; honor the entry point's documentation boundaries.

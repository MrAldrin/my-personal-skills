---
name: wasm-compatibility
description: Check if a marimo notebook is compatible with WebAssembly and report issues. Manual only; start it with /skill:wasm-compatibility.
disable-model-invocation: true
---

# wasm-compatibility (manual wrapper)

This skill is a thin wrapper. The real instructions come from the auto-updated Pi package `git:github.com/marimo-team/skills`.

1. Read `~/.pi/agent/git/github.com/marimo-team/skills/skills/wasm-compatibility/SKILL.md`. Resolve relative links from that file's folder.
2. Follow it exactly for the user's request.
3. If the file is missing, stop and tell the user. The marimo team may have renamed or removed this skill. Fix this wrapper or remove it; see `my_programs/docs/pi-manual-wrapper-skills.md`.

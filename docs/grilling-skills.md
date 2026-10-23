# Grilling skills: usage and provenance

## Choose an entry point

| Skill | Use it for | Documentation behavior |
| --- | --- | --- |
| `grill-me` | One-off plans, decisions, non-code or personal discussions | Conversation only unless you ask for files |
| `grill-with-docs` | Ongoing projects where shared language and decisions should persist | Capture agreed domain terms; offer significant ADRs |
| `grilling` | Shared interview discipline used by both entry points | Does not itself grant file-edit permission |
| `domain-modeling` | Sharpening project terminology or editing a glossary/ADR | Follow project conventions; create files lazily |

Examples: “Use grill-me to stress-test my talk proposal.” Or: “Use grill-with-docs to work through this project's cancellation model.” Both entry points ask **one question at a time**, give a recommendation, and wait for your answer. Facts are investigated with available tools; decisions remain yours. Implementation waits for confirmation of shared understanding and the applicable implementation authorization.

`grill-with-docs` is not a documentation dump. Resolved domain terms go into the relevant glossary, with no implementation details. ADRs are offered only for decisions that are hard to reverse, surprising without context, and the result of a real trade-off. Existing project paths/formats take precedence. Without conventions, defaults are `GLOSSARY.md` and `docs/adr/`; `GLOSSARY-MAP.md` supports multiple contexts. Read-only requests produce proposed changes, not writes.

## Packaging and harnesses

Keep all four sibling directories together under `skills/`. `grill-me` loads `grilling`; `grill-with-docs` loads both `grilling` and `domain-modeling`. Domain modeling includes its glossary and ADR format references. No extra skill, setup wizard, or script is required.

The existing `package.json` discovers `./skills` recursively for Pi; there is no per-skill catalog manifest to extend. The bundled `agents/openai.yaml` metadata is retained for harnesses that use it. Entry points retain upstream `disable-model-invocation: true` and OpenAI's explicit-invocation policy, but not every harness enforces those fields. Invoke the desired entry point explicitly. A skill-capable harness may invoke dependencies by name; a harness without a Skill tool must read the linked `SKILL.md` files in full. Relative links resolve from the containing skill directory, not the project cwd.

Repository updates do **not** automatically remove legacy skills from other discovery paths. Before activation, follow the migration checklist below. Do not assume pulling this development checkout deploys home or work installations.

## Sync and migration checklist for agents

When asked to sync these skills on another machine:

1. Inspect the actual harness settings, package installations, skill directories and startup sync/mirror configuration. Preserve unrelated skills and user edits. Do not assume work-machine paths apply at home.
2. Update the intended personal-skills installation to the user-approved revision containing **all four** sibling directories. Include the domain-modeling format references and skill metadata. Fetching alone does not update checked-out files; moving a checkout or pushing/integrating changes requires the user's applicable authorization.
3. Search configured skill sources for another `grill-me`. The legacy standalone version directly says to interview the user, ask one question at a time, recommend answers and explore the codebase. The replacement entry point loads the sibling `grilling` skill. Compare content and resolve symlinks before removing anything; preserve any custom behavior not covered by the new set.
4. With migration approval, retire the obsolete personal installation or discovery link so only the intended `grill-me` is loaded. Remove a link, not its source. **Do not delete a skill from a shared/team repository or modify a shared package merely to resolve a personal collision.** If a package also provides other needed skills, use the harness's supported filtering/configuration or ask how to resolve it.
5. Refresh any generated mirror after fixing its source. A running session's `/reload` may reread the mirror without rebuilding it. Follow the machine's actual startup procedure; do not add a second sync mechanism.
6. Reload/restart the harness, confirm all four intended skills are available without collisions, then smoke-test explicit `grill-me` and `grill-with-docs` invocation. Confirm one-question pacing and no writes for a read-only request. Record untested steps rather than calling discovery or behavior verified.

### Work-machine migration (2026-10-23)

- Windows Pi already loads this checkout's `skills/` directory. Removed only `C:/Users/A440AA6/dotfiles/pi/skills/grill-me`, a symlink into `projects/agent-skills/.claude/skills/grill-me`. The source belongs to JBF's shared `agent-skills` repository and was preserved. No personal custom edits were present in that source file.
- Removed the old generated WSL copy at `/home/hsa/.local/share/pi-skills/dotfiles/grill-me` and mirrored just these four skills into `/home/hsa/.local/share/pi-skills/personal/`. All four mirrored `SKILL.md` files were compared with their Windows sources.
- Normal WSL Fish `pi` startup runs `pi-sync-skills`, mirroring the Windows sources before launching Pi. The removed dotfiles link will therefore stay absent on subsequent syncs. Launching the underlying Pi binary directly bypasses that Fish hook.
- Fresh-session discovery and live interview behavior have not been verified by the agent. Existing sessions need reload/restart. No home-machine installation, shared-repository deletion, remote push or bookmark movement was performed.

## Source and license

Imported from [Matt Pocock's skills](https://github.com/mattpocock/skills) at commit **`5beb35b040e3de97e54fa9e386d7e42d15c295c2`**, inspected 2026-10-23:

- [`skills/productivity/grill-me`](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/grill-me)
- [`skills/productivity/grilling`](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/productivity/grilling)
- [`skills/engineering/grill-with-docs`](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/grill-with-docs)
- [`skills/engineering/domain-modeling`](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/domain-modeling)

The complete upstream MIT notice is preserved in [`licenses/mattpocock-skills-MIT.txt`](../licenses/mattpocock-skills-MIT.txt) and applies to these imported skills and references. This notice does not relicense unrelated repository content.

The [AI Hero changelog](https://www.aihero.dev/skills-changelog-ubiquitous-language-grill-with-docs) provides historical context for the split. It mentions `context.md`; the pinned current source instead uses `GLOSSARY.md` plus optional ADRs. The pinned source, not that older article, defines this import.

### Local adaptations

- Entry-point descriptions clarify when to choose each; tool-specific “Call the Skill tool” instructions become invocation-or-read instructions with relative dependency links.
- `grilling` preserves the design tree, prerequisite frontier, recommendations, user decisions and final confirmation. Upstream asks the **whole frontier in rounds**; this version asks **one frontier question at a time** to retain the user's preferred pace. Its OpenAI short description matches.
- Fact-finding uses available tools directly; subagents are optional and require authorization, rather than being mandatory.
- `grill-me` does not write files by default. `grill-with-docs` scopes permission to relevant documentation, not implementation.
- Domain modeling explicitly respects existing conventions, agreed terminology, ADR approval, and no-edit requests. Grilling's final confirmation gates implementation, not the inline agreed documentation enabled by `grill-with-docs`. Its original description, two format references and OpenAI metadata are unchanged.
- The four upstream directories are flattened into this repository's existing sibling skill layout. No unrelated upstream skills are imported.

For future refreshes, compare only these four pinned directories and their references/metadata, preserve the notice, review these adaptations, update the pin and run checks. Do not blindly overwrite the local behavior or refresh unrelated skills.

## Validation

Run from the repository root:

```bash
uv run --no-project python -m unittest discover -s tests -v
uv run --no-project python -m unittest discover -s skills/agent-memory/tests -v
```

The first suite checks this set's packaging, dependency links, catalog, provenance and adaptation contracts. These are static checks, not proof of model behavior. See the [preparation record](grilling-preparation.md) for actual results and any behavioral smoke-test limitations.

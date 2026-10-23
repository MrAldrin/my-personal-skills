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

This change prepares repository content only. It does **not** update any installed copy, live dotfiles, or home configuration. The older standalone `grill-me` in the work dotfiles remains untouched. Before future activation, inspect actual discovery paths on each machine, retire or disable the duplicate standalone copy with approval, and load the four-skill set from a single intended source. Then reload the harness and smoke-test explicit entry points. Do not assume pulling this development checkout deploys home or work installations.

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

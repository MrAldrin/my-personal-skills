# Lead/Conductor verification — 2026-10-27

## Scope and method

Owner-approved minimal design: two role skills and one shared Markdown contract; no new runtime machinery. Implementation stayed in the existing jj change. Native authoring with bounded read-only behavior simulations and independent review, rather than concurrent editing agents.

Read Pi's installed skill documentation and loader/command-expansion implementation; writing-skills and its discovery, authoring, testing and bulletproofing references; TDD; existing delegation, Zellij, jj and pi-subagents role guidance. The advertised `create-skill` path was absent on this machine; it was not installed or replaced. Pi's skill spec/documentation and the available writing-skills guidance supplied the format.

## Baseline (before either role skill existed)

Workflow `d34ac50d-e5c4-4114-aa35-f44ac99c05c7`: five fresh-context Haiku medium samples, each answering independent Lead and Conductor pressure scenarios. The prompts combined deadlines, an offline Lead, a stale shared backlog, generic integration-approval defaults and ignored artifacts. No code or workspaces were mutated.

All five Leads requested renewed routine integration permission; all five Conductors proposed writing the shared backlog. Existing review/artifact instincts generally held, so those checks are preservation/regression checks, not newly demonstrated benefits.

Representative exact baseline statements:

- `26a248d7-05ef-416a-8f6c-119447770ea5`: “Integration needs separate approval under the existing guidance.” Conductor: “change the backlog from \"active\" to \"in review\" or \"blocked on review\"”.
- `578649dd-4f9c-4605-9ad0-8b43b948257e`: “the owner's \"don't keep asking\" covers routine coordination, not that gate.”
- Other baseline runs: `dafc8b6d-a73d-479e-956c-5ccc96bf41d0`, `9952a2ee-88d0-4617-949c-c6b511e4f523`, `bc6201b6-4a39-49ca-a05f-9b8153797580`.

## Exploratory skill tests and revision

- Lead workflow `6b95fd65-bb9c-41b0-8f2c-285ebf46b99e`: five fresh Haiku medium samples. They applied standing integration authority and Lead-only backlog ownership; variation cases covered launch failure, role entry/exit and recovery.
- Conductor workflow `d554df36-6e02-4e90-bcb5-c8b07a7c3c59`: five fresh Haiku medium samples. They left the shared backlog alone, required independent review and retained Lead-created workspaces. One sample (`1fa5970b-2dc1-49aa-b15b-d05cb98ce10c`) also said “I don't integrate into it” about its assigned batch workspace, then described integrating its parser child into the B3 line. That contradiction exposed a real ambiguity.
- Revised the shared ownership paragraph and Conductor closeout: integrating children into the assigned batch cwd is permitted even if the Lead created that cwd. Added a concrete parser → batch → Lead integration example and a failing-then-passing packaging regression for retaining it.

These exploratory runs could read the fixture rubrics, so they are not treated as blinded behavioral evidence. Some early worker-profile runs also received irrelevant inferred mutation-acceptance failures despite complete simulation answers. Their receipts are not claimed as passing implementation gates. Later samples use a read-only reviewer profile and do not receive the rubrics.

## Final prompt-only application samples

Workflow `6244879a-2cdc-4bf1-b06c-192e4dd16835`. Each sample read both skill entry files and the shared contract, then answered the Lead and Conductor pressure prompts plus a manual-entry or role-exit variation. They were explicitly barred from reading fixtures/rubrics, plans, verification and other agents' results. All outputs were manually read.

Run metadata confirmed effective model/reasoning matched the requested values below; all six exited 0 with acceptance correctly marked not-required for read-only simulations. Transcript tool-call inspection showed reads of the two role files and shared contract only, not the rubrics.

| Sample | Child run | Verified model/reasoning |
| --- | --- | --- |
| 1 | `b26e81bb-4f3e-403c-a1c3-3b2889d2b652` | Haiku medium |
| 2 | `d5a9b24d-4131-4411-99ec-5e661e824082` | Haiku medium |
| 3 | `69a64138-8322-466a-841a-48001c44b396` | Haiku medium |
| 4 | `c433e28b-5313-4c2e-a81e-d19924abd8d2` | Haiku medium |
| 5 | `9658fbbe-81a8-487a-a694-ec0381329fc2` | Haiku medium |
| 6 | `f5f2f7d4-028a-4f32-b46b-f9f3a41d8167` | Sol low (stronger retry/check of the exposed ambiguity) |

All six outputs applied the two target corrections: no renewed routine integration approval and no Conductor backlog edits. All six distinguished Conductor integration `tmp-b3-parser` → `tmp-b3` from Lead integration `tmp-b3` → Lead line, required independent review/combined checks, and retained the Lead-created batch workspace for its creator. This is a manually assessed instruction-application result, not an automated proof of runtime enforcement or a controlled model benchmark.

Source artifacts use `<child-run>_<worker|reviewer>_{input,output,meta,transcript}` under Pi's retention-managed session artifact directory. Keep the prompts/rubrics in `tests/fixtures/delivery-role-scenarios.json` for future reruns; raw artifacts may expire. For a meaningful rerun, give the child only the prompt, not `expect` rubrics.

## Packaging and runtime checks

- Initial role packaging suite failed on absent skill files/contract/usage docs, as expected before implementation.
- Recursive integration example regression failed before the wording fix.
- Imported the installed Pi 1.4.0 `loadSkillsFromDir` and `formatSkillsForPrompt`: discovered exactly `lead` and `conductor` among 14 repository skills, zero diagnostics, both visible for natural-language discovery, no accidental `workflow` skill.
- Confirmed Windows Pi already includes this checkout's `skills/` in its configured skill paths. No settings changes or installation performed; existing sessions need `/reload`.
- Called the installed Pi `AgentSession._expandSkillCommand` implementation with the actual discovered resources (without starting a session/model): both `/skill:lead Work on B3` and `/skill:conductor Work on B3` expanded to their skill body with location/relative-reference context and retained arguments; unknown skill commands remained unchanged.
- `uv run --no-project python -m unittest discover -s tests -v`: 22 tests, 21 passed, one desktop-clipboard test skipped.
- `uv run --no-project python -m unittest discover -s skills/agent-memory/tests -v`: 45 tests, 42 passed, three Windows symlink tests skipped because Developer Mode/elevation was unavailable.
- Installed jj does not support `jj diff --check`; final whitespace validation uses added lines from `jj diff --git` instead.
- `uvx ruff check tests/test_delivery_roles.py` and `uvx ruff format --check tests/test_delivery_roles.py`: checked after correcting the initial lint/format findings. Ruff was unavailable through `uv run`; `uvx` supplied the isolated tool without changing project dependencies.
- Added-line whitespace from `jj diff --git`: zero errors.

## Independent review and disposition

- Initial Haiku medium review `58d74744-fdb7-41ee-85dc-5a8ca780b983` returned OK with notes. It identified an implicit manual-workspace lifecycle and a missing Conductor write target for projects whose task record existed only in the shared backlog. Clarified both with explicit rules and two failing-then-passing packaging regressions.
- Targeted Sol low retry `df1abdb2-5d65-43c4-a34e-32c82c8708a2` already inferred the correct self-created/manual lifecycle from the original contract, but agreed that explicit wording would help. The fix preserves creator ownership rather than introducing another routine approval gate. Agree the integration destination upfront; if missing, do not guess.
- Final fresh Sol low review `43cd72b1-15fd-4b96-9e9e-9936c28de450` read the current files and acted out manual completion without the fixture rubric: no issues found, verdict OK. It confirmed self-created workspace integration/cleanup, preservation of user-managed workspaces, destination agreement and the linked-record rule. No tests or live operations were delegated to reviewers.
- Initial review comments about pending suites/command expansion/spec status were based on its earlier snapshot; final records and direct checks resolve them. Its context-cap concern was an estimate: actual final word counts are Lead 432, Conductor 477, shared contract 1,045, within tested caps.
- Retain the single shared contract and existing intercom write-handoff rule; no separate lock protocol or role-specific copies were added. There are no deferred product findings; end-to-end live reliability remains an explicit validation limit.

## Limits

No live Conductor tab was launched and no real child workspace was integrated/deleted for these tests. Existing launch/jj mechanisms are reused unchanged; these tests do not establish end-to-end live reliability or Windows/WSL/Linux parity. No deployment to WSL, other machines or other harnesses is claimed. Role entry cannot enforce tool/model restrictions. Exact production role model tiers remain policy choices, not pinned in these skills.

## Implementation rulings

- Use this existing task change and native authoring with read-only test/review agents; no concurrent writers or unnecessary workspace. The plan/spec and test evidence provide the durable execution record.
- Keep one contract at `skills/lead/workflow.md`, referenced from both roles. This avoids duplicate rules but requires distributing the two sibling directories together; packaging/link tests guard it.
- Preserve the earlier orchestration research with a historical-status notice; current usage and the role contract are authoritative for this implementation.

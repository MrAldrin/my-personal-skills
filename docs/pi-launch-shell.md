# Interactive shell launch for Pi peers

## Ownership and status

- Owner: `pi-launch-skill`, session `01a16da9-38fe-7509-a054-8218fbe8a916` (`gpt-6.1-sol`, reasoning `low`).
- Coordinator: `pi-shell-launch`, session `01a16da4-52b8-7636-971d-3f64f10e1981`, owns `my_programs` and its `plans/backlog.md` task record.
- Repository: `C:/Users/A440AA6/projects/my-personal-skills`.
- Agent-managed workspace: `tmp-pi-launch-skill`, path `C:/Users/A440AA6/projects/tmp-pi-launch-skill`.
- Task change: `zsxytqyw`, based on `twlpslmx` (`13877cc9`, dev at inspection).
- Status: ready for user review; user approved execution directly in the owner tab and approval was relayed to the coordinator.
- Children: none authorized or launched. Keep the visible owner tab open for user discussion.

## Outcome and boundaries

Pi must run as a foreground child of the normal interactive preferred shell. Exiting Pi must return to that shell's prompt; exiting the shell must close its pane normally. Preserve platform-specific syntax and the existing Windows fullscreen mouse launcher. Do not replace the shell, use a direct Pi pane command, or treat closing the pane on Pi exit as equivalent.

Scope: `skills/using-zellij-with-intercom/SKILL.md`, its `commands.md`, this tracking record, and focused supporting checks if needed. Canonical portable preference belongs to the coordinator's `my_programs/agents/core.md` Shell section. No bookmarks, push, integration, installation, configuration redesign, or active deployment.

## Inspection evidence

- `jj git fetch`: Nothing changed.
- Inspected clean default status/diff, all local and remote bookmarks, `all()` history, branch heads and `main..dev` ancestry/diff.
- Only main (`b7c91a2d`) and dev (`13877cc9`) bookmark lines exist; main is an ancestor of dev. Dev's two newer changes concern grilling, not peer launches. No divergent or missing relevant branch changes found.
- Default workspace's empty change `wzrsmppy` was preserved. Both discussion-only peers (`01a16d8d`, `01a16da3`) were notified before edits and confirmed no conflict or unintegrated launch work.
- Pi settings directly includes `C:/Users/A440AA6/projects/my-personal-skills/skills`. This isolated workspace is not loaded. **Final integration into the default source is activation**; user approval is required. No settings or links were changed.
- Baseline guidance in both target files starts Pi/node directly as `new-tab`'s initial command, which cannot return to an existing interactive shell on exit.
- Local Zellij version: 0.45.1. Inspected `new-tab`, `write-chars`, and `write` help and live pane listing. `new-tab` accepts no initial command and returns a numeric tab ID; both write actions support explicit `--pane-id`. `write` accepts byte values.

## Proposed procedure

1. Inspect environment, local help, configured/default interactive shell and local Pi launcher.
2. Create a named tab with explicit workspace cwd and no initial Pi command, letting the normal shell start.
3. Resolve the returned stable tab ID to its exact terminal pane; inspect cwd, shell and prompt before typing.
4. Submit a correctly shell-quoted foreground Pi command to that pane only, using `write-chars --pane-id` followed by `write --pane-id ... 13` after checking local support.
5. Retain Windows Node/fullscreen-launcher discovery and separate Linux/WSL syntax. Do not use `exec`, a shell replacement, background Pi, or `--close-on-exit` as a substitute.
6. Verify intercom identity, effective model/reasoning and two-way readiness before handing over work. Leave successful interactive peers open.

The only suitable approach within the requested outcome is shell-first submission. Direct Pi as the pane command leaves no interactive parent shell; closing the pane on Pi exit fails the return-to-prompt requirement. A new wrapper/configuration change adds unnecessary scope.

## Disposable verification scope (approved and executed)

Create one uniquely named disposable normal-shell tab in this isolated workspace, record its exact stable tab and terminal-pane IDs, and inspect its shell prompt. Submit the discovered Windows fullscreen Pi launcher as a foreground child with no task, no edits and no child agents. Inspect startup, exit only that disposable Pi instance through its supported exit interaction, and verify return to the normal shell with a harmless marker command. Then submit `exit` to that same verified disposable shell and verify its pane/tab disappears. Never send exit or cleanup input to a live user peer. This scope was approved by the user's instruction to proceed to completion; screen/list help and the running Pi UI's Ctrl+D exit hint were inspected before use.

Native Windows verification does not establish Linux/WSL behavior. Record actual observations and platform limits, not inferred success.

## Execution plan and results

- [x] Add focused static regression tests for shell-only tab creation, explicit pane submission, quoting/platform coverage and lifecycle guidance; witness all three fail against the baseline.
- [x] Update `SKILL.md` and `commands.md` with the agreed shell-first procedure, preserving local launcher discovery and readiness checks.
- [x] Run packaging/guidance suite: `uv run --no-project python -m unittest discover -s tests -v` — 9 passed. Coordinator independently repeated all 9 successfully.
- [x] Run transcript helper suite: `uv run --no-project python -m unittest discover -s skills/agent-memory/tests -q` — 45 run, 42 passed, 3 skipped. Initial verbose run hit a 30-second timeout; rerun with sufficient timeout completed in 58 seconds.
- [x] Execute approved disposable lifecycle test on native Windows: Zellij 0.45.1, Nushell 0.115.1, Pi 1.4.0; tab `5`, `terminal_30`, cwd this isolated workspace. Verified normal Nushell prompt before submitting existing Node/fullscreen launcher. Pi UI showed `gpt-6.1-sol`, `low`. With no task or model call, Ctrl+D exited Pi back to Nushell. `echo PI_SHELL_RETURNED` produced the expected output. Submitted `exit` to that same disposable shell; subsequent pane listing contained neither tab 5 nor terminal_30. No held pane remained. No live user peer received exit input.
- [x] Coordinator reviewed the complete target-file/test diff with no findings; owner reviewed coordinator's core bullet with no findings. Static contracts do not prove agent behavior, and no child-agent pressure tests were authorized. Linux/WSL and alternate Windows shells were not live-tested.

Ruling: use this single approved linked record for design, plan and results, rather than add separate planning files for one documentation outcome. Keep one atomic JJ change with its regression checks. No child-agent fanout or deployment performed.

## Next actions and cleanup

User approved default-checkout integration and temporary workspace cleanup after review. The default empty working change `wzrsmppy` is rebased onto result `zsxytqyw`, preserving the dev ancestry and positioning the configured `jj b a` target at the completed result (`heads(::@ ~ empty())`). This activates guidance through the direct skills source path. The agent-owned `tmp-pi-launch-skill` workspace is forgotten and its directory removed after preserving the result through default ancestry; unrelated workspaces are outside cleanup scope. Both discussion-only default-checkout peers confirmed no pending mutations. Disposable test tab and shell closed normally. The interactive owner tab remains open in the default repository. Bookmark movement and push remain the user's actions.

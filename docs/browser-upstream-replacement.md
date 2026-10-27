# Upstream browser workflow replacement

## Approved scope and ownership

- Outcome: use Microsoft's unmodified `playwright-cli` skill for generic browser operations; retire `using-browser-apps` only after a real Brave attachment test.
- Owner: Pi session `01a17e0a-a011-76a7-a9b9-440714e3ed85`, model `github-copilot/gpt-6.1-sol`, reasoning `low`.
- Workspace: user-managed default workspace, `C:/Users/A440AA6/projects/my-personal-skills`; initially empty `@` `mxluwwvl`. No concurrent edits in approved browser resources. No children or temporary jj workspaces.
- Coordinator/report target: session `01a17d4f` in `agent_improvements`, which owns the audit backlog. The owner subsequently approved proceeding directly without another leader round-trip.
- Authority: local installation/configuration and Windows/WSL deployment only. No pushes, unrelated cleanup, credentials, customer records or transactions.

## Selected design and deployed paths

Use Pi's supported git package mechanism with exact skill selection and other resource types disabled. Keep upstream files and Apache-2.0 attribution intact. A copied/forked skill would need manual updates; a second local workflow would duplicate upstream. Neither matches the approved outcome.

- Windows package: `C:/Users/A440AA6/.pi/agent/git/github.com/microsoft/playwright-cli`.
- WSL package: `/home/hsa/.pi/agent/git/github.com/microsoft/playwright-cli`.
- Both settings files declare `git:github.com/microsoft/playwright-cli` with `skills: ["+skills/playwright-cli/SKILL.md"]` and empty `extensions`, `prompts`, `themes` arrays. Other settings preserved.
- Both checkouts are unmodified at upstream commit `b1a5903c5b633b8c9f843ad7b629c2a78437040c`; upstream Apache-2.0 license remains bundled.
- Windows local setup: four bullets in `C:/Users/A440AA6/.pi/agent/AGENTS.md` identify the CLI fallback, TEMP/named-session discipline, existing Brave executable/extension channel, owner login/MFA/tab approval, non-destructive detach and security boundaries. No new workflow skill or command reference.
- Axxon: `C:/Users/A440AA6/.pi/agent/skills/using-axxon/SKILL.md` now requires upstream `playwright-cli`, not the retired companion. It retains app-specific navigation, evidence and safety guidance, with explicit record/sensitive-data permission and no credential/storage export or approval bypass. Its existing troubleshooting reference is unchanged.
- Retired old workflow: moved intact from `.pi/agent/skills/using-browser-apps` to `C:/Users/A440AA6/.pi/agent/retired-skills/using-browser-apps-2026-10-27`, outside discovery. This is a rollback archive, not an active second workflow.

Windows Brave attachment remains Windows-only; WSL upstream skill discovery does not imply Linux-to-Windows browser support. Axxon remains Windows-local rather than silently broadening its deployment.

## Verification evidence (2026-10-27)

- Windows: Node v24.13.1, npm 11.8.0, `@playwright/cli` 0.1.22. Live `attach --help` confirms `--extension`. Verified handed-off Brave executable exists.
- Initial attachment attempt timed out with no session. Owner said Brave might not have been open and explicitly requested a retry. No token bypass or browser configuration change used.
- Retry from dedicated Windows TEMP, using `PLAYWRIGHT_MCP_EXECUTABLE_PATH` and `-s=browser-migration-check attach --extension=chrome`, succeeded after owner tab approval.
- Attached page was public `https://www.nrk.no/`, title `NRK.no – nyheter, tv og radio fra Norge og hele verden`. No customer data accessed.
- `list` showed named session `browser-migration-check`, `status: open`, `browser-type: chrome (attached)`; `eval 'document.title'` returned the matching title.
- Named-session `detach` succeeded; subsequent `list` returned `(no browsers)`. No close, storage-delete, cookie or login commands were used.
- Actual Pi `DefaultResourceLoader` invoked with each real agent directory: exactly one upstream `playwright-cli` discovered on each side, zero skill diagnostics. After retirement, Windows loads `using-axxon` but not `using-browser-apps`; WSL loads neither Windows-local skill.
- Verification script also asserts exact package filters and Windows Axxon/setup references and boundaries.
- `/home/hsa/.pi/agent/tests/test-pi-skill-mirror.sh`: `Pi skill mirror and fish launcher verified`.
- WSL installation used `fish -lc` (Node v24.15.0 via existing fnm). Bare noninteractive Bash does not initialize Node; no launcher/environment change was made.

No global CLI installation, login/MFA automation, sensitive application access or WSL browser operation was tested or needed. This verifies attachment, read-only page inspection and detachment, not every upstream command or Axxon's current business UI. Page console warnings on NRK did not prevent attachment/title inspection.

## Maintenance and cleanup

Supported future update: `pi update git:github.com/microsoft/playwright-cli` on each side, followed by `/reload`. This is not an automatic updater; review upstream changes before use. A running session needs `/reload` to discover the new skill and forget the retired one. A new session loads the revised global setup.

Task-created TEMP artifacts, reviewed scratch checkout and discovery test script are removed after final verification; no browser output or customer evidence is committed. Retain the old workflow's rollback archive outside discovery. Upstream managed checkouts, package declarations, local setup and Axxon guidance are intentional deployed resources. No bookmarks/remotes changed; no pushes. The jj change records the machine-local deployment and evidence, not vendored upstream files.

Status: verified replacement complete; final checks and cleanup recorded in the session. No remaining approval blocker.

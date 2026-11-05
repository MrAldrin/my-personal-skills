# Agent instructions

- This repository holds personal skills shared across the user's machines. See
  [README](README.md) for the skill list.
- The sibling repository `../my_programs` installs these skills and owns machine
  setup, hooks, Pi/Claude configuration and the cross-machine sync goal. Read its
  `docs/scope.md` when a skill touches setup, hooks or agent configuration; the
  two often change together.
- Do not edit `my_programs` from here. Message an agent working in that
  repository (Pi intercom or Claude peers) for changes there.

## Syncing changes between machines

- This repo serves home Mint/Fedora machines and the work machine's Windows and
  WSL environments. A request to sync work done at home means inspect incoming
  changes and their local activation needs; do not assume a fresh installation
  or ask the owner to explain this topology again.
- Inspect the live setup rather than replaying old transcript commands. On the
  work machine, load `maintaining-pi-environments` for discovery, startup or sync
  changes. Keep machine-specific paths and maintenance details in that local
  skill, not in this shared repository.
- Distinguish four states: the actual remote tip, fetched remote refs/local
  bookmarks, files in the working copy `@`, and what a running agent has loaded.
  Fetching does not move `@`; moving a bookmark does not update checked-out
  files. Inspect `dev` when that is the requested source, not only `main`.
  Preserve local work and follow the version-control workflow; do not move
  bookmarks or push without separate authorization.

### Work-machine activation: normal behavior, not a repair task

- Windows Pi reads this checkout's `skills/` directly. Once the working copy has
  the desired changes, `/reload` or a new Pi session loads them. Ordinary skill
  edits need no package reinstall, publication or push for local use.
- Windows and WSL read the shared Windows skill checkouts directly; WSL uses
  `/mnt/c` paths. The old mirror and `pi-sync-skills` startup sync were removed.
  Do not recreate them or add a second checkout to activate ordinary skill edits.
- The authoritative loading arrangement and platform-specific sources live in
  `../my_programs/docs/work-machine-pi-skills.md`; read that document before
  changing discovery or startup. Inspect both environments' local settings when
  paths change, rather than assuming one settings file configures both.
- Existing Windows and WSL Pi processes need `/reload` or restart to load updated
  skills. No Fish startup sync or manual mirror refresh is required.
- The current remote reminder is advisory: it compares remote `main` with the
  fetched `origin/main`, not with `@`. It does not fetch, move files, check `dev`,
  or prove that loaded skills are current. Do not treat silence as proof of sync.

### Exceptions to check, not reasons to redo setup

- Read incoming changes and the README's migration links. New dependencies,
  renamed skills and duplicate legacy discovery sources can require action;
  ordinary Markdown edits usually do not. Inspect all configured sources before
  removing an obsolete personal link; preserve custom edits and shared sources.
- Updating skill checkouts does not deploy global `AGENTS.md`, extensions, packages or
  machine settings. Route setup changes through `my_programs` and its deployment
  gates. Do not copy entire agent directories, credentials, sessions or home
  machine settings onto this machine.
- Separate stale process state from bad saved configuration. Restarting WezTerm
  or opening a new tab in a surviving Zellij session may retain old environment
  variables. Inspect the affected shell and parent session before prescribing
  restarts or permanent PATH edits; preserve running tasks.
- Report only the actual remaining action: repository update, Windows/WSL reload
  or restart, or a specific migration. Distinguish
  verified files/tests from fresh-session discovery not yet observed. Do not
  turn an optional immediate refresh into a blocker or repeat approval requests
  for actions already authorized within the current task's scope.

## Validation policy

- Do not impose arbitrary word-count caps on skill bodies or shared workflow
  documents. Keep instructions useful and concise through review, not failing
  tests based on prose length. Keep genuine metadata/schema constraints and
  tests for packaging, links and behavior.

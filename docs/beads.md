# Local task store

Beads is the status authority. [The backlog pointer](../backlog.md) maps the
original queue to stable task IDs. Migration does not authorize the queued work.
Skill changes, installation, clipboard access and machine setup need their own
scope and approval.

## Select the store

The sole canonical store is `/home/hsa/projects/my_personal_skills/.beads`,
including when you work in another jj workspace. Never initialize a second
workspace-local task store. Before each operation, select it explicitly and
check `where`; stop if the path or prefix is not the expected one:

```sh
env BEADS_DIR=/home/hsa/projects/my_personal_skills/.beads bd -C /home/hsa/projects/my_personal_skills --readonly where
env BEADS_DIR=/home/hsa/projects/my_personal_skills/.beads bd -C /home/hsa/projects/my_personal_skills --readonly list --all --limit 0
```

These commands work in Fish and POSIX shells. Expected prefix: `ps`. A pointer
in a workspace does not prove canonical activation has completed.

## Ownership

Read the full task, metadata and linked evidence before changing it. Use a
unique actor containing the full current session ID. Claim only explicitly
assigned work with `--actor <unique-actor> update <exact-id> --claim`. A migration
coordination claim is not a claim on imported tasks. Never force another claim.
Use `--if-assignee <your-actor>` and `--if-status in_progress` for guarded status
updates or closure through `update`; stop on a failed guard. Preserve historical
owner and approval text as evidence, not as renewed authority.

## Private operation and recovery

Before the FIRST migration Pi startup, set umask `077` and private roots:
`PI_SUBAGENTS_TEMP_ROOT=/home/hsa/.local/share/beads-migration-runtimes/my_personal_skills/runtime`
and `TMPDIR=/home/hsa/.local/share/beads-migration-runtimes/my_personal_skills/tmp`.
Owned directories must be mode 700 and files mode 600. Verify UID, no symlinks,
ancestry and Pi artifacts. Audit after each writer command. Correct only known,
owned native metadata behind private roots; stop on unexpected paths or owners.
Do not harden shared parent directories. A private child session alone is not
sufficient. Before private child reads, run doctor and a fresh no-tool canary;
verify effective model, reasoning, zero tool calls and process termination.

Anonymous metrics, automatic backup, backup Git push, automatic export and
export staging must remain disabled. Sync follows "Sync with GitHub" in the
shared PRIME.md; the Beads data remote is MrAldrin/my-personal-skills-beads
(private). Do not change code Git remotes, index, hooks or locks.
The local native backup destination is
`/home/hsa/.local/share/beads-backups/my_personal_skills/native`.
With the verified explicit store, `backup init <private-destination>` configures
a destination and `backup sync` makes a full native backup. Test recovery in a
NEW private isolated initialized store, with its own explicit `BEADS_DIR` from
the FIRST init invocation (no `-C` until initialized). Use
`backup restore <backup-path> --force` ONLY in that new disposable initialized
store, never over the canonical store. This overwrites the test store's initial
database. Compare complete exports, metadata, states, graph, all unlimited issue
histories and audit events, entire journal, provenance and full Dolt history.
Preserve the entire native store and sibling `.beads.gate.lock`; JSONL is an
interchange format, not a native backup. Keep private source and review evidence
outside removable workspaces. Canonical activation needs its own NEW backup and
restore check; preparation checks alone do not prove activation.

## Recorded migration limits

The 2026-11-06 import preserved two unchecked source items as administratively
deferred, P2 and unassigned, with no edges. These are dated import facts, not
current queue status. The events journal was disabled and empty; existing audit
events and full native history were retained. No journal history was invented.
Embedded `bd sql` is not a supported inspection route. Writer-recorded standalone
Dolt SELECT/log evidence can support recovery comparison; a final read-only
reviewer must not run standalone Dolt. Native tools can recreate broad-mode
metadata even under private roots, so mode audits remain necessary.

The first synthetic oracle inherited context and was not accepted as fresh.
The replacement used explicit `context: fresh`, Luna/xhigh, zero tool calls and
observed process termination. Final review also requires explicit fresh context.
No skill was activated or installed, no clipboard was read and no machine setup
was resumed by this migration.

# Personal Skills Beads migration, 2026-11-06

## Delivered

The two unfinished root backlog items were migrated to the sole local native
store `/home/hsa/projects/my_personal_skills/.beads`:

1. `ps-q5b`: Mint work-update reconciliation.
2. `ps-1sz`: Mint/Fedora clipboard support.

At import, both were administratively deferred, P2 and unassigned, with no
edges. Current status belongs to Beads. Exact source wording, order, links,
unchecked state, historical owner and approval uncertainty remain in the native
records and protected source companions. Migration did not renew execution
approval, activate skills, install software, access a clipboard or resume setup.

Reviewed setup change: `kxulvnoo/bab4c1ab`. Only `.gitignore`, `AGENTS.md`,
`README.md`, `backlog.md` and `docs/beads.md` changed. The Lead applied the actual
backlog pointer; its reviewed SHA-256 is
`16841e075ac1cb22f5e935476926528517bc4bff57cf9086ad93bbda766e309a`.
No bookmark moved and nothing was published.

## Checks and independent review

- Packaging suite: 25 tests, one desktop-clipboard skip, no failures.
- Fresh read-only oracle run `38e2c52c-9f83-40b0-8363-704c693c00b4` used
  `openai/gpt-6-luna:xhigh`; process termination was observed. Raw verdict:
  **PASS — bounded read-only review.** The reviewer inspected helper safety,
  then executed the fixed read-only audit once and checked source semantics,
  actual pointer, reviewed hashes and the five-file boundary.
- Preparation native backup and a NEW isolated restore matched complete exports,
  import fields, metadata, states, views, graph, all unlimited issue histories
  and audit events, entire journal, all 32 recorded native tables and full
  77-commit recorded Dolt log/provenance. Reviewer compared writer-recorded
  standalone Dolt evidence; it did not run standalone Dolt itself.
- The Lead integrated reviewed files unchanged, verified frozen native hashes,
  and copied the entire store plus sibling `.beads.gate.lock` without overwrite.
  Lead canonical verification reports 50 complete outputs per store matching
  frozen preparation and a NEW canonical backup/restore. Eight known owned
  native metadata mode corrections were recorded; final audit was clean.
- Conductor then independently checked canonical `where`, complete export,
  effective settings (`metrics.disabled=true`, automatic push/backup/export and
  backup Git push/export staging disabled), no task remotes, reviewed file
  hashes, canonical owned modes and the Lead verification proof. These direct
  read-only checks passed.

## Retained evidence and recovery

Private evidence root:
`/home/hsa/.local/share/beads-migration-runtimes/my_personal_skills/evidence`.
It retains original source snapshots and hashes, exact import, per-store command
captures, mode corrections, reviewed files, raw review and activation packet.
The complete frozen native store and sibling gate remain at the adjacent
`frozen` directory, outside the execution workspace.

- Original backlog SHA-256:
  `2a2167450dcd90f138f5cfde057461412c9a65322f8a355df206c8f8c9345144`.
- Exact import SHA-256:
  `e8c1fb3bbd8010386a9b1bf8c3fe33b22cb95ae5bc78a9fb479fb2a355807dc1`.
- Operational native backup:
  `/home/hsa/.local/share/beads-backups/my_personal_skills/native`.
- NEW canonical backup:
  `/home/hsa/.local/share/beads-backups/my_personal_skills/canonical-native-20261106`.
- NEW canonical restore:
  `/home/hsa/.local/share/beads-migration-runtimes/my_personal_skills/canonical-restore-20261106`.
- Lead proof and raw captures:
  `/home/hsa/.local/share/beads-backups/my_personal_skills/lead-activation-20261106/verification.json`.

## Limits and lifecycle

Recovery was tested on this machine, not on another host or an off-machine
backup service. JSONL is not the native backup. The events journal was disabled
and empty; no journal history was invented. Audit events and native history are
retained, but an empty journal is not independent mutation evidence.

The first synthetic oracle inherited context and was not accepted as fresh.
The explicit fresh replacement `9c526276-adc6-483a-bd11-244e986af7b0` passed with
Luna/xhigh, zero tool calls and observed process termination. Final review also
used explicit fresh context. Raw limitations were not relabeled.

All bounded children are terminal. The Lead owns entry-workspace and migration
tab cleanup. Retain private evidence, backups, canonical data and user resources.
Coordination closure is a separate guarded operation; this report does not
claim it has already occurred. See [the operational guide](../beads.md).

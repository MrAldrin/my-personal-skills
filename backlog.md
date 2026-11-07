# Backlog

Task status is tracked in the local Beads store at
`/home/hsa/projects/my_personal_skills/.beads`.
Use this same explicit store from every Jujutsu workspace.
See the [task-store guide](docs/beads.md) for claims, privacy and native recovery.
Read-only checks:

```sh
env BEADS_DIR=/home/hsa/projects/my_personal_skills/.beads bd -C /home/hsa/projects/my_personal_skills --readonly where
env BEADS_DIR=/home/hsa/projects/my_personal_skills/.beads bd -C /home/hsa/projects/my_personal_skills --readonly list --all --limit 0
```

## Source mapping

1. `ps-q5b` — Mint work-update reconciliation. Historical owner, approval,
   activation evidence and remaining process reload/live checks are preserved
   in the native record and [integration evidence](docs/home-integration-review.md#mint-work-update-reconciliation-2026-11-05).
2. `ps-1sz` — Add and verify `copying-to-clipboard` support on the owner's Mint
   and Fedora machines. The source recorded Windows/WSL support as implemented.
   Dependency installation needs owner approval.

As imported on 2026-11-06, both tasks were administratively deferred, P2 and
unassigned, with no dependency edges. Read Beads for current status. Their
original unchecked source state, exact wording, order,
links and uncertainty are retained in record metadata. Historical ownership and
approval do not create a current claim or renew execution authority.

This migration does not authorize skill changes or installation, clipboard
access, machine setup, configuration changes or deployment. Coordinate shared
instructions and Pi settings with the `my_programs` owner.

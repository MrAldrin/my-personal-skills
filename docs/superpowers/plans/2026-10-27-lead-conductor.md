# Lead and Conductor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native implementation; bounded subagents provide behavior tests and independent review.

**Goal:** Add two lightweight, explicitly entered role skills for the existing delivery workflow.

**Architecture:** `lead/SKILL.md` and `conductor/SKILL.md` read the same `lead/workflow.md`. Both ship through the existing whole-skills-directory package. Existing skills provide mechanics; new instructions define role boundaries and recursive workspace ownership.

**Tech Stack:** Markdown Agent Skills, Pi skill loader, Python standard-library unittest, fresh Pi subagents.

**Spec:** `docs/superpowers/specs/2026-10-27-lead-conductor-design.md` (owner approved in conversation).

## Global Constraints

- Preserve Pi, Zellij, intercom, pi-subagents and jj. No new orchestration platform.
- Loading a skill does not change models, remove tools or unload previous context.
- The creator owns each child workspace: creation, coordination, rebasing, review/check verification, integration into its own line, artifact preservation and cleanup.
- Routine integration and cleanup are authorized by the role; no repeated approval request is needed.
- Never discard unintegrated work or remove a workspace before needed ignored/untracked artifacts are preserved.
- No changes to global policy or existing skills unless separately approved.

## Review Focus

- Generic integration/cleanup defaults must not override this workflow's scoped standing authority.
- Missing brief, ownership record or launch dependency must block only the affected action, without invented permissions or alternate launch surfaces.
- Manual Conductor entry must not grant control over an existing Lead's workspace or backlog.
- Child cleanup must not close interactive peers, discard ignored artifacts or strand running writers.
- A role mention in a comparison is not permission to enter it, and role exit must not silently cancel ongoing children.

## Task 1: Shared contract and Lead

**Files:** create `skills/lead/SKILL.md`, `skills/lead/workflow.md`, `tests/test_delivery_roles.py`, `tests/fixtures/delivery-role-scenarios.json`.

**Interfaces:** Lead loads `workflow.md` relative to its skill directory. The shared document defines the batch record, delegation envelope, authority, gates and dependency routing used by both roles.

- [x] Run five fresh-context baseline repetitions before writing skills; manually read all results.
- [x] Add failing packaging/reference tests and repeatable behavior scenarios/rubrics.
- [x] Run `uv run --no-project python -m unittest discover -s tests -p test_delivery_roles.py -v`; confirm missing-skill failures.
- [x] Write the shared workflow and Lead entry instructions. Test metadata, shared reference and Lead requirements independently of the not-yet-written Conductor.
- [x] Run five fresh Lead samples using the same baseline pressure scenario, plus application/role-lifecycle cases. Read results; address failures and re-test.

## Task 2: Conductor and complete package

**Files:** create `skills/conductor/SKILL.md`; update `README.md`, `docs/agent-orchestration.md`; create `docs/lead-conductor.md` and `docs/lead-conductor-verification.md`.

**Interfaces:** Conductor loads `../lead/workflow.md`, preserves the planning-owned brief and writes status/closeout only. The README documents both skills as a bundle and gives explicit commands.

- [x] Write Conductor entry instructions against observed baseline failures.
- [x] Run five fresh Conductor samples against baseline pressures and variation cases, including recursive integration and manual entry. Read all results and fix failures.
- [x] Run all role packaging tests. Import the installed Pi loader to check actual discovery, frontmatter diagnostics and catalog visibility without running a model or starting peers.
- [x] Document minimal usage and dependency/installation boundaries; mark the earlier design record historical with a current-doc link.

## Task 3: Verification and closeout

**Files:** update the verification record, plan checkboxes and design status.

- [x] Obtain fresh independent read-only review of the complete diff against the design; check authority, packaging and unsafe cleanup edge cases. Escalate failed/incomplete bounded work to Sol low.
- [x] Run `uv run --no-project python -m unittest discover -s tests -v` and `uv run --no-project python -m unittest discover -s skills/agent-memory/tests -v`.
- [x] Inspect added-line whitespace from `jj diff --git`, diff and status (installed jj lacks `diff --check`); record exact checks, model/reasoning evidence, run IDs and limits of simulated behavior tests.
- [x] Keep all task work in the existing change; finish with an empty child change, no bookmark moves or push.

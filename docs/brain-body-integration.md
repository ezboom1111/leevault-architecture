# A shared brain for a solo-business body

**September 13 follow-up:** project evidence delivery and attributed result return
are now implemented locally and tested with both native CLIs. See the
[implementation and verification update](integration-verification-2026-09-13.md).
The September 11 audit below is retained as the historical baseline, not current
status for those resolved gaps. General autonomous improvement remains unproven.

Status: source audit and integration contract, September 11, 2026. The local
dashboard prototype already has a knowledge bridge, but this is not yet a closed-loop integration.
The proposed connections below are not reported as implemented.

## Ownership, not two competing brains

| Layer | Owns | Must not pretend to own |
| --- | --- | --- |
| LeeVault brain | Personal source evidence, corrections, project original references, derived work procedures | Business transaction execution or the model's intelligence |
| Dashboard body | Projects, CRM/work records, task/run state, artifacts, reviews, navigation | A second independent personal-memory authority |
| Model worker | Reasoning, artifact generation, scoped proposals | Source authenticity or user authority by assertion |
| Graph lens | Relationship and code-impact exploration | Canonical facts or silent decision promotion |

Business records can remain in the dashboard's database. Personal evidence can
remain in LeeVault. Share stable identities and verifiable references rather than
copying all data into both systems.

## What the code currently connects

- The knowledge bridge calls LeeVault context retrieval, reads curated Markdown,
  and stores project/stage-specific source snapshots with hashes.
- It detects changed or unavailable originals without replacing the preserved
  version. While its server is running, it can periodically recheck pinned notes.
- The dashboard has work-run and review records, selected-material CLI input,
  and an evaluator-report read path for skill maintenance.
- The dashboard's Codex subscription launcher explicitly runs with hooks and memories disabled.
  It is a restricted read-only task lane. The Claude lane is similarly restricted.
  A foreground native chat's memory configuration is not inherited by assumption.

## Missing connections and exact boundaries to change

| Gap | Existing owner / target | Required change |
| --- | --- | --- |
| No shared project-original contract in the bridge | Dashboard knowledge bridge + LeeVault project references | Map project identity; pass current project context and exact revision-pinned original reads |
| Restricted CLI gets only request/selected materials | Dashboard CLI input construction | Host supplies bounded, verified evidence before execution; do not just disable safety restrictions |
| Reviews stop in the dashboard | Work reviews + evaluator/project-job adapter | Emit measured task outcomes and scoped improvement candidates with run/artifact lineage |
| Fixed host paths | Dashboard server and evaluator adapter configuration | Supply vault root/interpreter/evaluator through host configuration |
| Missing unified continuity status | Dashboard project detail | Show captured, retrieved, source-read, result-verified, improvement-published, later-used as separate states |

The current bridge consumes note/reference results, not the full new project
reference contract. Native semantic claims and arbitrary original HTML/code must
not be assumed to reach its worker just because Markdown lookup succeeds.

## Proposed integration envelope

This is a proposed versioned adapter contract, not an existing endpoint schema:

| Field | Purpose |
| --- | --- |
| schema_version | Reject incompatible message formats explicitly |
| project_id | One mapping between dashboard project and memory project |
| project_revision | Pin the project source snapshot, not an artifact hash |
| run_id | Join task, execution, review, and result |
| artifact_id + sha256 | Identify the exact generated or read artifact |
| source_refs | Trace every relevant input to its original |
| event_kind + actor_origin | Distinguish user words, model proposals, and measured results |
| observed_at | Record when the event was observed |
| idempotency_key | Deduplicate retries without losing conflicting evidence |

An application result does not grant direct-user authority. A dashboard test can
report a mechanical outcome; it cannot mint a trusted current-user quote or
declare a new personal preference. Reuse the existing evaluator and derived
project-job boundary for task results. Personal semantic writes need their own
authenticated current-user ingress and exact evidence contract.

## One useful end-to-end acceptance case

Use entirely synthetic project data:

1. Register an original design/token file for project A and a different one for B.
2. Start an A task in the dashboard; verify the model reads A's pinned original.
3. Correct A's reference and verify a stale task is rejected or explicitly refreshed.
4. Produce an artifact and record its actual check result, not just CLI success.
5. Publish a reviewed, project-scoped procedure from the measured failure.
6. Start a new A task and verify it uses the correction; B must remain unchanged.
7. Restart and replay one result; preserve one logical result and its history.

Until this complete path passes, use the label **knowledge-linked dashboard**,
not **autonomously improving business brain**. Do not turn on public deployment,
payments, account changes, or an always-on worker as a side effect of connecting memory.

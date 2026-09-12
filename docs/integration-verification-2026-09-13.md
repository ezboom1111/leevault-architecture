# Evidence delivery and result return — implementation follow-up

This architecture-only update supersedes the missing-connection baseline dated
September 11. Operational source, personal notes, application records, and native
session traces are not exported. These are maintainer-reported local results,
not experiments independently runnable from this public reference repository.

## Connected locally

- A configured project mapping supplies **host-provided evidence** before a
  restricted dashboard CLI task. Originals are hash-verified and revision-pinned;
  changed registered originals refresh into a new snapshot. Truncation is explicit.
- Execution and optional review records return through a durable outbox into
  existing Raw storage and the work-item evaluator. Model output is not promoted
  into personal user claims. Unknown artifact quality stays unknown.
- The next task can receive current originals and attributed earlier results,
  including an explicit indication that an earlier result used a previous revision.
- Completed attempt references are preserved in the same SQLite transaction as
  run state. Retrying a failed task cannot erase its unreturned result or reuse
  the previous attempt's evaluation identity.
- The result loop operates while the local dashboard **server is running**.
  Retries are bounded and backed off; unavailable and failed return states are visible.
  No VPS, Hermes gateway, or new local-model service was enabled.

This is feedback continuity and **mechanical execution outcomes**, not model-weight training,
automatic business-success scoring, or autonomous product-code modification.
Source selection is limited to explicitly registered project paths. Configurable
transport and project mapping do not imply arbitrary tool/plugin permission inheritance.

## Verification boundaries

| Check | Maintainer-reported result |
| --- | --- |
| Existing private memory regression | 840 passed, including two cache-spill regressions |
| New host bridge suite, separate from the 840 | 15 passed |
| Dashboard regression | 271 passed |
| Browser verification | Five scenarios passed, including same-origin memory-status access |
| Native Claude and Codex | Two successive tasks per provider used changed originals and returned two results each |
| Native data boundary | All model trials used synthetic project data; no personal claims created |
| Retry/crash boundary | Finished result survives monitor failure and retry before return; duplicate/conflicting delivery tested |

The native trials demonstrate a small current-source continuity case, not general
long-term improvement. Previous results were included as stale distractors.
The executor did not expose aggregate token usage, so none is invented here.

## Resolved lock defect

Two index writers read metadata through another SQLite connection while their own
transaction was active. A real cache-spill test reproduced the resulting lock in
both Markdown and Raw paths. Reading through the owning transaction fixed these
tests. One already-committed but incomplete live publication was repaired after a
backup, without appending a second semantic publication. An already-running MCP
process still needs to load the updated code; a source edit is not live hot reload.

## What still needs real outcome evidence

Repeated work across UI, backend, design, and business planning; cost-matched
memory-off/on/removal/reapplication comparisons; and delayed regression checks.
Automatic procedure generation/review remains a separate existing project-worker
boundary, not a claim that every returned result silently rewrites the architecture.
The honest label remains **knowledge-linked dashboard with feedback continuity**.

## Later operational check on September 13

After a consistent database backup, the actual local dashboard was started.
One existing-subscription Claude task received three registered project references
and its result returned automatically. The project source report was then updated
with the observed operational evidence. A following existing-subscription Codex
task received the revised source and the previous answer as an explicitly stale
result; it corrected the earlier synthetic-only status and cited the revised source.
Both result envelopes and text hashes were checked. The return status showed two
recorded results, none pending, and none failed.

These are maintainer-reported operational continuity checks, not a same-model
causal comparison: the providers differed and the source changed. They do not
establish autonomous lesson discovery or long-term artifact quality. A separate
synthetic four-condition feedback ablation supported scoped information reuse,
but is not counted as real business impact. Private records, identifiers, prompts,
model responses, and database backups remain excluded from this repository.

The existing Claude memory connection was reconnected without closing its
conversation. Other already-open clients still require their own safe refresh;
a successful dashboard job is not evidence that every client has reloaded.

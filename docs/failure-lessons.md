# Failure lessons

## 1. The harness started replacing judgment

Rules, queues, promotion states, and approval gates accumulated in response to
individual failures. Each local fix looked reasonable, but together they made
knowledge work serve the harness. The correction was to keep mechanical safety
small and return semantic judgment to the current model inside a closed scope.

## 2. Graphs were mistaken for memory

A visually rich graph can be stale, duplicated, or disconnected from current
behavior. Graphs now remain event-driven derived lenses. Canonical knowledge is
source evidence, claims, decisions, corrections, outcomes, and Git history.

## 3. Client auto-memory created split brains

When an assistant stored the same preference in both its own memory and the
shared Vault, later turns could retrieve conflicting histories. The rule became:
one canonical durable memory, with client-native stores disabled or treated as
non-canonical caches.

## 4. Tool-origin context lost user authority

A model was told to call a context tool even though the trusted pre-turn hook had
already created the authoritative turn. The second context became tool-origin
and correctly lost write authority. The fix was subtraction: preserve the native
turn identifier and keep model-created context recall-only.

## 5. Schema hidden inside strings caused guessing

When a memory patch accepted an opaque JSON string, models invented plausible
fields. Typed, flat tool parameters reduced ambiguity and made validation
failures actionable.

## 6. More stored notes did not prove learning

Raw capture can be perfect while durable semantic memory remains empty or useless.
The system now reports storage, semantic reflection, retrieval, correction, and
outcome efficacy as separate states.

## 7. Local semantic backends can fail contracts

A model that writes good prose may still fail structured graph extraction. A
small structured-output canary must pass before a large corpus run. Partial or
hollow results fail closed instead of becoming an impressive-looking graph.

## 8. New code on disk did not retire loaded writers

A long-lived MCP process kept executing an older writer after a safe typed
contract had been installed. Asking the user to perform an app restart would
make correctness depend on a manual ritual. The durable fix was a pre-mutation
writer epoch: current code uses the current signal table while the legacy name
returns a retired-writer tombstone. Old code then rejects itself through the
one-action check it already performs.

A transitional table created during cutover also showed why migrations must be
preserving and idempotent. Its rows were merged into the current epoch before the
intermediate table was retired; an empty new table was never treated as proof
that old state could be discarded.

## 9. Title-only recall looked like grounding

Returning a relevant filename made the system appear to remember, but it did not
give the model enough evidence to change a judgment safely. General-note recall
now carries a bounded excerpt plus declared authority, status, freshness, and
source location. Exposure is logged separately from citation and outcome.

## 10. Tool-origin activity inflated capture readiness

Counting every active health row allowed worker calls and model-created contexts
to resemble independent user sessions. The readiness population now requires a
trusted direct-user origin and assured conversation identity. Ineligible rows
remain visible for diagnosis but cannot satisfy the release gate.

## 11. One tombstone did not retire every stale writer

The first epoch rotation stopped the oldest writer, but processes loaded during
a transitional contract still shared the then-current table. The rule is now:
rotate the writer epoch for every backward-incompatible semantic release,
preserve compatible receipts transactionally, and fail closed on conflicts.

## 12. A project summary did not preserve the original design

A generic taste note could not reproduce an earlier HTML artifact. Original
references now have project identity, source hashes, and revision-pinned reads.
The generated procedure supplements the original; it does not replace it.

## 13. A connected dashboard did not imply a connected memory loop

The dashboard could search and preserve notes while its restricted CLI execution
lane intentionally disabled native hooks. This was a valid read-only lane, not
proof that the worker received memory or returned learning outcomes. Fix the
explicit host context/result adapters; do not silently remove execution controls
or claim that every application result is a trusted user statement.

## 14. A tested alternative was described like a live dependency

Hermes passed a worker experiment, while Claude remained the configured default.
Graphify had a task-routing rule, not a file-count watcher. Public descriptions
must distinguish installed, configured, invoked, tested, and outcome-improving.

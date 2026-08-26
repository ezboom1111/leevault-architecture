# Evaluation

The system does not optimize a single synthetic “memory value” score. It records
a vector of observable properties and keeps causal claims conservative.

## Mechanical floor

- capture success and hash integrity;
- p50/p95 capture and retrieval latency;
- duplicate and collision rate;
- broken source spans;
- stale or superseded claim leakage;
- stale-writer refusal before canonical mutation;
- legacy and transitional writer-receipt preservation during cutover;
- index drift and rebuild recovery;
- lint, tests, and atomic-write failures.

## Retrieval and correction

- whether a required claim appeared in the bounded context;
- whether an irrelevant or superseded claim appeared;
- correction propagation on the next turn;
- exact recurrent error rate;
- multi-session continuity.

## Outcome vector

Only explicit observed evidence can label:

- success or failure against a stated criterion;
- memory helped, harmed, was neutral, or remains unknown;
- memory changed an answer, changed a decision, merely confirmed it, or had no
  influence;
- source age of the claims that were actually cited.

Source age measures recency, not truth. Storage volume measures activity, not
usefulness. Model self-ratings are diagnostic hints, not outcomes.

## Improvement gate

A retrieval or reflection change should be kept only when it improves held-out
real cases without increasing harmful recall, recurrent error, or latency beyond
the declared budget. Synthetic cases remain separate from live outcomes.

# Bounded recursive improvement

LeeVault uses recursion as a feedback loop, not an unbounded call stack.

```text
retrieve → answer → observe → correct/evaluate → retrieve differently
```

## Events that can change the next turn

- a durable preference explicitly stated by the user;
- a decision or direction change;
- a correction to a claim that was actually served;
- an observed success or failure;
- explicit attribution that memory helped, harmed, or changed a decision.

Outcome attribution may cite memory served on the current turn or the
immediately previous turn. The latter lets the user say “that answer helped” naturally in a
follow-up without opening an unbounded attribution window.

## Events that should not become durable memory

- one-off task instructions;
- quoted material without user endorsement;
- inferred permissions;
- model-generated judgments about its own usefulness;
- external effects that have not been observed.

## Why the loop stays bounded

- each write is scoped to one trusted turn receipt;
- retrieval returns a capped candidate set;
- writes are idempotent;
- corrections supersede rather than append contradictory active claims;
- background graph regeneration cannot promote canon;
- evaluation changes ranking experiments, not global rules automatically.

This gives natural improvement without turning the system into an autonomous
governance engine.

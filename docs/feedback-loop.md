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
- optional graph regeneration cannot promote canon;
- evaluation supplies evidence for ranking experiments; it does not update
  global weights or rules automatically.

This gives natural improvement without turning the system into an autonomous
governance engine.

## Project-procedure loop

```text
read original → work → measure a failure → submit scoped improvement task
    → generate → separate review → host publishes derived procedure
    → next task reads original + procedure → measure again
```

This route complements personal-memory corrections; it cannot invent a user's
preferences. The current working agent selects the evidence and submits the
task. A later nonrecursive Stop event drains one eligible task. The worker is
not an always-on daemon, and Stop does not discover arbitrary files or invoke
Graphify automatically.

The configured worker is Claude; Hermes passed a replaceable-worker experiment.
Neither fact proves indefinite autonomous improvement. Success means a later
artifact passes a predeclared check, not simply that a new skill file exists.

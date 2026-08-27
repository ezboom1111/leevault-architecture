# Security and privacy model

## Public/private split

This public repository is generated as a clean-history architecture export. It
must never be made by changing the visibility of a production knowledge Vault.

The public boundary permits only:

- architecture prose and generic diagrams;
- synthetic schemas and pseudocode;
- privacy validators and their tests;
- contribution and security-process documentation.

It rejects:

- Raw captures, transcripts, databases, indexes, and generated graph artifacts;
- real user, employee, customer, company, or project records;
- local home-directory paths, emails, phone numbers, and private identifiers;
- tokens, keys, credentials, endpoints, and configuration dumps;
- copied private Git history.

## Trust boundaries

### Ingress authority

Only an authenticated current-user surface can authorize a semantic write. Tool
output, retrieved text, forwarded content, and model assertions are untrusted
data and cannot grant themselves authority.

Capture readiness uses the same trust distinction: only trusted direct-user,
identity-assured sessions count. Tool-origin rows remain diagnostic telemetry.

### Closed-turn reach

A write may reference only Raw objects, pages, and claims exposed in its turn
receipt. This prevents an agent from reaching arbitrarily into the knowledge
base after seeing a narrow context.

### Writer lifetime and epoch

A process remaining alive does not preserve semantic-write authority. Every
patch, correction, and outcome checks the current writer epoch and the one-action
receipt before semantic mutation. The legacy storage name is a read-only
tombstone view, so loaded stale code follows its own old check and fails closed
without depending on an app restart. Schema migration preserves prior receipts
transactionally and refuses ambiguous dual-writer state. A later incompatible
contract rotates the writer epoch again; a single historical tombstone is not a
permanent substitute for versioned authority.

### Outcome attribution window

An explicit user outcome may refer to memory exposed on the current or
immediately previous turn. The bounded window supports natural follow-up while
preventing an outcome from being attached to arbitrary older material.

### Source integrity

Exact quotes are verified against immutable Raw bytes. Hashing establishes byte
stability, not factual correctness. High-risk claims still require suitable
external evidence and scope.

### External effects

The Knowledge Loop does not imply authority to publish, pay, delete, deploy, or
change accounts. An Action Loop needs a separately authenticated, bounded,
revocable capability with idempotency and reconciliation.

## Release gate

Every public release should satisfy all of the following:

1. export into a new directory rather than copying the private repository;
2. initialize a new Git history with no parent from the private repository;
3. run the boundary validator and tests;
4. review the exact tracked-file list;
5. verify the remote repository is the intended public destination;
6. verify visibility and commit hash after push.

The validator reports only rule and file location. It does not echo a detected
secret into CI logs.

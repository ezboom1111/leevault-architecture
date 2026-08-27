# LeeVault Architecture

LeeVault is a conversation-first reference architecture for durable AI memory.
Its central idea is simple: preserve what the user actually said, let the model
reflect during ordinary conversation, and measure whether remembered knowledge
improves later decisions.

This repository is an **architecture-only public reference**. It contains no
production Vault, user messages, source documents, credentials, local paths,
private decisions, or deployment configuration.

## The short version

```text
Conversation
    ↓
Trusted current-turn capture
    ↓
Immutable Raw + receipt
    ↓
Bounded retrieval with exact source spans and grounded notes
    ↓
Answer + reflection
    ↓
Living Wiki patch / correction / outcome
    ↓
Evaluation changes the next retrieval decision
```

The loop is recursive in the systems sense, not through an unbounded function
call. Each turn can produce a bounded event that changes what the next turn sees.

## Design principles

1. **Conversation is the interface.** Users should not have to tag messages,
   file notes, or approve every internal write.
2. **Raw is immutable.** Semantic notes can change; the captured source does not.
3. **Claims point back to exact evidence.** A file path or embedding score alone
   is not provenance. General notes are exposed only as a bounded excerpt with
   declared authority, status, freshness, and source location.
4. **Corrections supersede immediately.** The next query should see the corrected
   claim, while history remains auditable.
5. **Graphs are lenses, not memory.** Obsidian, Graphify, CodeGraph, and embeddings
   help exploration but do not become canonical truth.
6. **Measure outcomes, not storage volume.** More notes are not automatically a
   better second brain.
7. **Human authority is concentrated at the root.** Reversible internal work can
   be automatic; new authority over money, accounts, public identity, or legal
   commitments requires explicit delegation.
8. **Writer authority expires with the contract.** A long-lived client that
   loaded an older implementation must fail before mutation; process lifetime
   is not proof of current authority.
9. **Recall exposure is observable without copying content.** A content-free
   receipt records which claim or note references were served so later outcomes
   can measure whether memory actually influenced a response.

## Repository map

- [ARCHITECTURE.md](ARCHITECTURE.md) — components, contracts, and data flows
- [SECURITY.md](SECURITY.md) — trust boundaries and public/private separation
- [docs/feedback-loop.md](docs/feedback-loop.md) — bounded recursive improvement
- [docs/evaluation.md](docs/evaluation.md) — outcome and freshness measurements
- [docs/failure-lessons.md](docs/failure-lessons.md) — what failed and why
- [diagrams/system.mmd](diagrams/system.mmd) — standalone Mermaid source
- `scripts/validate_public_repo.py` — fail-closed public-boundary validator

## What is deliberately absent

- user or company data
- production memory databases and indexes
- private prompts, decisions, outcomes, and research bundles
- credentials, account identifiers, and deployment endpoints
- the original private repository history

## Status and license

This is a public architecture reference, not a packaged product or a production
security claim. No reuse license is granted in this first release; a license can
be selected separately without coupling that legal choice to the privacy review.

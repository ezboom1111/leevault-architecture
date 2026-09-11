# LeeVault — evidence that survives the next conversation

[한국어 설명](docs/overview-ko.md) · [Current status](docs/runtime-status.md) · [Brain/body integration](docs/brain-body-integration.md)

LeeVault is a conversation-first reference architecture for durable AI memory.
Its central idea is simple: preserve what the user actually said, let the model
reflect during ordinary conversation, and measure whether remembered knowledge
improves later decisions.

This repository is an **architecture-only public reference**. It contains no
production Vault, user messages, source documents, credentials, local paths,
private decisions, or deployment configuration. The operational runtime remains
private. Public CI validates the documents and publication boundary, not that
private runtime.

The intended use is a shared memory and evidence layer for everyday coding,
design, research, and a solo-business dashboard. It is not a new chat application
that users must move into, and it does not replace the model doing the work.

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
Verified corrections and project procedures inform a later task
    ↓
Measure whether the later artifact actually improved
```

The loop is recursive in the systems sense, not through an unbounded function
call. Each turn can produce a bounded event that changes what the next turn sees.
This is not model-weight training or automatic global search-weight tuning.

## What runs where

| Responsibility | Component | Status at the September 11, 2026 audit |
| --- | --- | --- |
| Capture, provenance, correction, bounded retrieval | Custom LeeVault runtime | Implemented locally; private runtime version 0.2.2 |
| Original HTML/code/design references | Revision-pinned project reference catalog | Implemented and exercised across local Claude/Codex sessions |
| Coding, design, research, and task judgment | Foreground Claude/Codex + task-specific tools | Runs in the user's existing work environment |
| Deferred project-procedure generation and separate review | Replaceable worker interface | Claude configured; Hermes tested as an alternative |
| Document relations / code impact | Graphify / code graph tools | Optional task-driven lenses, not always-on memory |
| Business records, work execution, artifacts, status UI | Separate dashboard body | Local prototype; full brain/body feedback integration remains incomplete |

Submitting an improvement task still requires the working agent to choose useful
evidence. After submission, a later response-end event can run one bounded job.
There is no background project-model call when no task is pending. No VPS,
Ollama, Telegram command, or Hermes chat interface is required for this local path.

## The problem this project tries to solve

"Use the same design as before" is not satisfied by recalling "the user likes
clean interfaces." The model needs the actual reference artifact, the correct
project version, and the latest correction. LeeVault separates original evidence
from generated working knowledge, then checks whether the next artifact respects
that evidence. Storage, retrieval, use, and improved outcomes are different claims.

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
- [docs/runtime-status.md](docs/runtime-status.md) — implemented, tested, optional, and unverified
- [docs/brain-body-integration.md](docs/brain-body-integration.md) — dashboard ownership and missing connections
- [docs/overview-ko.md](docs/overview-ko.md) — Korean project introduction
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
security claim. No reuse license is granted by this repository; a license can
be selected separately without coupling that legal choice to the privacy review.

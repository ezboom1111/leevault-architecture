# Runtime status — September 11, 2026

This page separates implementation, experiments, and future integration. It is
an architecture reference, not an installable release of the private runtime.

## Implemented locally

- Private runtime 0.2.2: current-turn capture, evidence receipts, semantic
  corrections, bounded retrieval, and session provenance.
- SQLite FTS5/BM25 retrieval and evidence links. No mandatory vector database.
- Project-specific original references with revision-pinned reads, immutable
  source snapshots, change detection, and history.
- A durable project job queue with bounded generation/review attempts and
  host-controlled publication of derived procedures, separate from user facts.
- The configured worker is Claude. Generation and review use separate processes
  with bounded input/output and no worker tools or MCP. This is not an OS sandbox.
- Native local hooks start at most one eligible project task at a response-end
  opportunity. Source selection and task submission require the working agent.

## Tested alternatives and optional lenses

Hermes is a tested alternative at the worker boundary. Experiments exercised
procedure creation, correction, later reuse, and Hermes generation followed by
Claude review. This does not mean Hermes is the live default, that all Hermes
features are integrated, or that a fair same-model performance ranking was done.

Graphify is available as a task-driven relationship lens. It is not a file-count watcher,
a nightly job, or the canonical memory store. Code graphs and embeddings are
optional lenses; this release does not prove every such integration runs.

## Maintainer-reported private runtime results

These results are not independently reproducible from this repository because
the operational code, native-session traces, and private corpus are not exported.
They are scoped implementation reports, not a substitute for public CI.

| Experiment | Reported observation | Boundary |
| --- | --- | --- |
| Final runtime regression | 838 passing tests | Private runtime tests; not the test count of this public repo |
| Native Claude/Codex reference reuse | Original values and corrections used in later outputs | Small controlled tasks, not months of business outcomes |
| Cross-worker procedure | Hermes candidate, separate Claude review, host publication | Not an always-on Hermes deployment |
| Interrupted review | Durable candidate reused after worker restart | Local fixture fault test, not a paid-model uptime trial |
| Fresh prompt processes | 22 captures; no acknowledged Raw loss | Small fixture; not whole-corpus latency or all-client readiness |
| Historical cross-surface recheck | Six checks passed; one old strict-JSON wire check remained red | Historical failure retained, not relabeled green |

The separate 78-test worker group overlaps the 838 tests and must not be added
to it. A passing storage or protocol test does not establish outcome improvement.

## Dashboard audit performed for this publication

The separate dashboard's knowledge bridge, subscription policy, work tools,
review, and skill-maintenance tests passed: 25 tests. Four browser scenarios
passed for lookup, changed-source refusal, preserved source versions, and
mobile/origin handling. A read-only lookup against the current local LeeVault
returned available index/reference state. This is not a full dashboard audit.

A separate live semantic-write attempt during the audit returned a database-lock
error. Its success was not confirmed and it was not retried into a claimed pass.
Passing read/fixture tests must not be presented as an all-clear for concurrent
production writes; lock contention remains an observed follow-up issue.

The bridge is not yet a closed-loop integration. See
[brain/body integration](brain-body-integration.md).

## Not claimed

- Automatic capture from arbitrary web chats or unconfigured IDEs.
- Autonomous product-code editing/deployment by the project-procedure worker.
- Automatic global weight updates, model training, or guaranteed answer quality.
- Continuous execution while the local machine is off.
- Automatic discovery and semantic ingestion of every file in every project.
- A full penetration test or a completed dependency vulnerability audit.

## Reproducible public checks

```sh
python -m unittest discover -s tests -v
python scripts/validate_public_repo.py .
```

These check the published boundary and documentation contracts with synthetic
fixtures. GitHub Actions runs the same public checks. Native-runtime results and
business results remain separately labeled.

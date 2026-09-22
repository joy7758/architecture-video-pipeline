---
artifact_type: TITMAS_SCOUT_DISCOVERY_IMPLEMENTATION_ENTRY
implementation_id: TITMAS-OPPORTUNITY-DISCOVERY-MVP-V0.1
runtime: RUBY_STANDARD_LIBRARY_ONLY
network_mode: READ_ONLY
external_action_authorized: false
---

# TITMAS Scout Discovery Prototype v0.1

## Purpose

This directory implements the read-only discovery half of TITMAS Scout. It
collects public GitHub opportunity signals and produces a maximum-five review
queue with evidence-linked, non-executable Action Packs.

The prototype does not comment, create Issues, submit pull requests, contact
people, apply, bid, or send material.

## Module Map

- `source_collector.rb`: probes local `gh`, prefers authenticated Issue search,
  and transparently falls back to anonymous public REST `GET` Issue search.
- `signal_extractor.rb`: extracts source facts, pain classifications, bounded
  evidence snippets, and existing TITMAS role mappings.
- `deduplicator.rb`: merges repeat query hits by source type, repository, and
  Issue number while preserving query lineage.
- `opportunity_ranker.rb`: filters prohibited or non-actionable records and
  applies `heuristic_unvalidated_v0.1` factor bands.
- `action_pack_generator.rb`: creates suggestion-only Action Packs and rejects
  executable or send-ready text patterns.
- `daily_report.rb`: emits Markdown, canonical JSON, and the stable DBA cockpit
  handoff file.
- `cli.rb`: orchestrates one bounded run.
- `support.rb`: deterministic sorting, text normalization, time parsing, and
  digest helpers.

## Backend Selection

```text
if gh is installed and gh auth status succeeds:
  backend=GH_CLI_AUTHENTICATED
else if anonymous public REST is enabled:
  backend=GITHUB_PUBLIC_REST_GET_ONLY
else:
  collection_status=BLOCKED
```

The REST transport exposes only a `get` method and accepts only HTTPS requests
to `api.github.com`. No general request-method parameter exists.

GitHub Discussion discovery requires valid authenticated GraphQL. When it is
unavailable, reports contain a reason-coded coverage gap and no fabricated
Discussion result.

## Run

```bash
ruby src/discovery/cli.rb --date 2026-08-01
```

Useful bounded options:

```text
--config PATH
--date YYYY-MM-DD
--max 1..5
--output-root PATH
--retrieved-at YYYY-MM-DDTHH:MM:SSZ
```

`--retrieved-at` exists for reproducible tests and recorded research runs. It
is not trusted time.

## Output Contract

The CLI writes only these local output classes:

```text
reports/daily/YYYY-MM-DD-opportunity-report.md
reports/daily/YYYY-MM-DD-opportunity-report.json
reports/latest-opportunities.json
```

The JSON Daily Report preserves query text, backend, retrieval time, rate-limit
observations, candidate reconciliation counts, filtering reasons, factor
explanations, unknown facts, Action Packs, and no-write evidence.

`reports/latest-opportunities.json` requests future read-only DBA cockpit
review. It does not modify DBA or claim architecture integration.

## Heuristic Boundary

The prototype does not use Matching Score v0.1 and emits no predicted success
rate or calibrated total. Factor bands are `HIGH`, `MEDIUM`, `LOW`, or
`NEEDS_REVIEW`; effort uses explicit effort bands. The deterministic internal
ordering tuple is documented in `docs/discovery-mvp-v0.1.md`.

An open Issue proves only that the recorded public entry was open at retrieval
time. It does not prove maintainer interest, contribution acceptance, customer
demand, product fit, commercial value, or permission to act.

## No-Write Contract

- external HTTP requests are GitHub public REST `GET` only;
- GitHub CLI commands use a closed read-only prefix allowlist;
- Action Packs set `external_action_authorized=false`;
- no credentials or external-action clients are present;
- only local report generation writes files;
- Agent Review Quorum or human-exception review and Trust Guard remain later,
  separate gates; the discovery report itself never authorizes action.

## Tests

```bash
ruby -I src tests/discovery_test.rb
```

Tests use injected fake command and HTTP transports. They make no network
request and assert GET-only collection, write-command rejection, deterministic
deduplication and ordering, explicit missing-evidence states, Action Pack
constraints, report limits, and false authorization fields.

## Unimplemented

- authenticated GitHub coverage when local credentials are invalid;
- current GitHub Discussion collection without authenticated GraphQL;
- other code forges, grants, procurement portals, jobs, email, and web forms;
- scheduled daily execution, persistent history index, alerts, and retries;
- semantic or model-based extraction beyond deterministic keywords;
- calibrated value, effort, acceptance, adoption, or revenue models;
- automatic review orchestration, Trust Guard integration, or external execution;
- production security, privacy, compliance, deployment, or SLA.

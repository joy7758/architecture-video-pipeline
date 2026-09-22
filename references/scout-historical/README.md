---
artifact_type: TITMAS_SCOUT_REPOSITORY_ENTRY
product_name: TITMAS Opportunity Discovery MVP
version: "0.1"
status: RESEARCH_MVP_DISCOVERY_AND_AGENT_REVIEW
primary_entry: src/discovery/README.md
machine_report_entry: reports/latest-opportunities.json
external_action_authorized: false
---

# TITMAS Opportunity Discovery MVP

TITMAS Scout is a read-only opportunity discovery MVP for finding public,
actionable work related to trustworthy AI Agent infrastructure. It collects
public signals, removes duplicates and non-actionable items, explains an
unvalidated heuristic order, and produces Action Packs for policy-selected
review.

Its primary job is discovery. The discovery component does not contact
maintainers, submit pull requests, comment, apply, bid, send material, or
authorize external action. A separate deterministic Agent Review Quorum can
authorize bounded ordinary open-source actions; no executor is implemented.

## Current Product Boundary

```text
PUBLIC_OPPORTUNITY_DISCOVERY_IMPLEMENTED=true
GITHUB_PUBLIC_ISSUE_DISCOVERY_IMPLEMENTED=true
GITHUB_DISCUSSION_DISCOVERY_AVAILABLE_AT_CURRENT_RUN=false
HEURISTIC_RANKING_CALIBRATED=false
DEFAULT_SELECTION_MODE=AGENT_QUORUM
HUMAN_EXCEPTION_REVIEW_REQUIRED=CONDITIONAL
EXTERNAL_ACTION_AUTHORIZED=false
CUSTOMER_ACQUIRED=false
PRODUCTION_READY=false
```

The current GitHub CLI installation is preferred when authenticated. If its
authentication is unavailable, the MVP may transparently fall back to
anonymous GitHub public REST `GET` requests for Issues only. Every report
records the selected backend, query coverage, rate-limit observations, errors,
and missing source types.

## Pipeline

```text
Source Collection
-> Signal Extraction
-> Deduplication
-> Pain Point Classification
-> TITMAS Capability Mapping
-> Opportunity Ranking
-> Action Pack Generation
-> Daily Report
-> Agent Review Quorum or Human Exception Review
-> Trust Guard
-> Action Authorization
-> External Action
```

The discovery implementation stops at the Daily Report. Agent review and
authorization are separate local components, and no External Action executor
exists.

## Quick Start

From the repository root:

```bash
ruby src/discovery/cli.rb --date 2026-08-01
```

The command writes:

- `reports/daily/YYYY-MM-DD-opportunity-report.md`;
- `reports/daily/YYYY-MM-DD-opportunity-report.json`;
- `reports/latest-opportunities.json`.

The stable JSON entry is intended for future read-only ingestion by the
Digital Biosphere Architecture cockpit. Its presence is a handoff request, not
architecture adoption or integration approval.

## Ranking Boundary

Discovery uses `heuristic_unvalidated_v0.1`, not the uncalibrated Matching
Score v0.1. It emits evidence-linked factor bands and an explainable ordering,
never a predicted success rate or a calibrated product-fit score. Missing
commercial, effort, maintainer, or acceptance evidence remains
`NEEDS_REVIEW`.

## Trust Guard v0.1 Freeze

The existing Opportunity Object, Matching Score Model, Approval Object,
Relationship Model, Validation Model, Validator Prototype, and Validation Runs
remain attributable Trust Guard assets. Historical runs are immutable; current
policy documents may be amended through versioned changes.

Trust Guard is an auxiliary pre-action review surface. It is not the Scout's
primary product loop and is not expanded by this MVP. A Validator result never
creates Approval or external-action authority.

## Safety Contract

- source collection is read-only;
- the public REST fallback exposes only a `GET` transport interface;
- generated Action Packs are suggestions for policy-selected review;
- every Action Pack sets `external_action_authorized=false`;
- output generation performs local file writes only;
- no GitHub comment, Issue, Discussion, pull request, email, application, bid,
  or contact operation is implemented.

## Validation

```bash
ruby -I src tests/discovery_test.rb
ruby -I src tests/validator_test.rb
ruby -I src tests/review_test.rb
```

See [Discovery MVP v0.1](docs/discovery-mvp-v0.1.md) for the source policy,
filters, ranking grammar, Action Pack contract, report schema, and explicit
non-capabilities.

See [Agent Review Quorum v0.1](docs/agent-review-quorum-v0.1.md) and
[review prototype](src/review/README.md) for the bounded internal authorization
policy and deterministic aggregator.

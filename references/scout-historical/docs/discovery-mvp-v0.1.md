---
artifact_type: TITMAS_SCOUT_DISCOVERY_MVP_DESIGN
product_id: TITMAS-OPPORTUNITY-DISCOVERY-MVP-V0.1
version: "0.1"
status: IMPLEMENTATION_CONTRACT
primary_task: EXTERNAL_OPPORTUNITY_DISCOVERY
ranking_model: heuristic_unvalidated_v0.1
default_selection_mode: AGENT_QUORUM
human_exception_review_required: CONDITIONAL
trust_guard_version: TITMAS_SCOUT_TRUST_GUARD_V0.1
external_action_authorized: false
---

# TITMAS Opportunity Discovery MVP v0.1

## Product Correction

The Scout's primary task is to discover external opportunities that can lead
to real implementation experience, adoption, collaboration, reputation, or
revenue learning. Governance models are retained as a bounded Trust Guard, not
continued as the primary product loop.

The MVP produces evidence-linked candidates and Action Packs for
policy-selected review. It does not execute participation.

## Constitutional Position

The MVP is an Application / Governance Service discovery surface built above
the Digital Biosphere open-infrastructure ecosystem. It is not DBOS, SAEE, a
Foundation Model, an authority source, or an architecture decision maker.

It follows these constitutional boundaries:

- Agent-readable evidence precedes human projection;
- Agent recommendation alone does not become Authority or Permission;
- candidate participation proposals are bounded, explainable, and reviewable;
- Human Governance owns exception decisions for contracts, payments, binding
  identity commitments, restricted data, deletion, account security, and
  protected production merges;
- strategy, discovery, adoption evidence, and commercial commitment remain
  distinct states.

The canonical constitution source read for v0.1 is the reference mirror at:

```text
/Users/zhangbin/GitHub/titmas-ecosystem/docs/governance/
open-infrastructure-strategy-constitution.md
```

## Product Pipeline

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

### Source Collection

Collect public, attributable source records without changing an external
system. v0.1 supports public GitHub Issues and conditionally supports GitHub
Discussions when authenticated GraphQL is available.

The backend order is:

1. authenticated local GitHub CLI;
2. anonymous GitHub public REST `GET` fallback for Issues;
3. explicit blocked source type when neither mode is available.

Backend selection, authentication state, raw query, retrieval time, returned
count, GitHub-reported total count, rate-limit observations, and errors must be
retained in the Daily Report.

Anonymous REST fallback is incomplete coverage. It does not silently stand in
for authenticated GitHub search or Discussion discovery.

### Signal Extraction

Extract only source-authored facts and bounded text snippets:

- source URL, repository, issue number, author, state, labels, and timestamps;
- source title and a bounded pain-point excerpt;
- matching keywords and the query that surfaced the record;
- explicit public participation entry and lock state;
- facts that remain unknown.

Keyword matches are discovery evidence, not proof of customer need, product
fit, implementation feasibility, contributor acceptance, or commercial value.

### Deduplication

Deduplicate by canonical GitHub repository and issue number, falling back to a
normalized source URL. A candidate found by several queries retains all query
IDs and matching evidence.

Deduplication never merges different Issue numbers, repositories, or source
types merely because their text is similar.

### Pain Point Classification

The closed v0.1 taxonomy is:

- `AI_AGENT_AUDIT`;
- `EXECUTION_EVIDENCE`;
- `VERIFIABLE_TRACE`;
- `HUMAN_IN_THE_LOOP`;
- `AGENT_AUTHORIZATION`;
- `MCP_SECURITY_AUDIT`;
- `AGENT_GOVERNANCE_COMPLIANCE`;
- `PROVENANCE_REPLAY`;
- `TAMPER_EVIDENCE`.

Every classification retains the matched keyword and source excerpt. No match
produces `OUT_OF_SCOPE`, not a guessed classification.

### TITMAS Capability Mapping

Mappings are bounded pointers to existing ecosystem roles documented by the
DBA repository map and AI discovery index:

- Agent Evidence for execution-evidence packaging and offline verification;
- ARO-Audit for post-execution audit and replay-oriented review;
- Token Governor for policy, permission, and runtime constraints;
- FDO Kernel MVK for execution-integrity reference work;
- Agent Intent Protocol for bounded intent, action, and result semantics;
- Verifiable Agent Demo for a guided verification walkthrough.

Each mapping requires matched source text. A mapping is a reuse hypothesis for
policy-selected review, not a capability guarantee or product-fit decision.

### Opportunity Ranking

v0.1 uses `heuristic_unvalidated_v0.1`. It does not call, implement, or
reinterpret Matching Score v0.1.

The factor vocabulary is:

| Factor | Required question |
| --- | --- |
| `pain_explicitness` | Does source text state a bounded problem? |
| `titmas_relevance` | Does source text map directly to an existing role? |
| `actionability` | Is there an open, unlocked public participation entry? |
| `expected_learning` | Is bounded implementation learning possible? |
| `potential_value` | Is attributable value evidence present? |
| `effort` | Is there enough evidence to estimate a bounded contribution? |
| `freshness` | Was the source active inside the configured window? |
| `evidence_quality` | Are source facts and limitations reviewable? |

Factor results use only:

```text
HIGH
MEDIUM
LOW
NEEDS_REVIEW
```

`effort` uses `LOW_EFFORT`, `MEDIUM_EFFORT`, `HIGH_EFFORT`, or
`NEEDS_REVIEW`. Every factor contains evidence reasons. Missing commercial,
acceptance, maintainer, or implementation evidence remains `NEEDS_REVIEW`.

The deterministic ordering tuple prioritizes direct TITMAS relevance,
actionability, pain explicitness, expected learning, freshness, evidence
quality, potential value, and lower evidenced effort. Source URL is the final
stable tie-breaker.

There is no numeric total, calibrated threshold, predicted success rate,
customer-intent inference, or automatic eligibility decision.

### Action Pack Generation

An Action Pack is a non-executable suggestion record containing:

```yaml
opportunity_summary: <bounded source-derived summary>
original_source: <public html URL>
pain_point: <source-derived pain description>
reusable_components: []
possible_acceptance_reasons: []
possible_rejection_reasons: []
minimum_contribution: <bounded preparation proposal>
suggested_action_type: <allowed-action-enum>
estimated_effort: LOW_EFFORT | MEDIUM_EFFORT | HIGH_EFFORT | NEEDS_REVIEW
key_risks: []
human_exception_decisions_required: []
external_action_authorized: false
```

Allowed action enum values are `COMMENT`, `DISCUSSION`, `PR`, `APPLICATION`,
`BID`, `CONTACT`, and `OBSERVE`.

The generated pack must not contain:

- a ready-to-send comment, email, application, bid, or contact message;
- an API request, shell command, credential, or executable patch;
- an instruction that implies approval or automatic execution;
- an identity claim, customer claim, or acceptance prediction.

### Daily Report

Each run writes:

```text
reports/daily/YYYY-MM-DD-opportunity-report.md
reports/daily/YYYY-MM-DD-opportunity-report.json
reports/latest-opportunities.json
```

The Daily Report contains at most five retained candidates. Every candidate
records:

- source;
- current state;
- pain point;
- mapped TITMAS components and evidence;
- actionable entry;
- recommended next step;
- retention or exclusion reason;
- unconfirmed facts;
- heuristic factor bands and explanations;
- non-authorizing Action Pack.

The JSON report also retains every raw query, collection time, counts before
and after deduplication, filter counts, per-item filter reasons, backend
limitations, and observed network methods.

### Review Selection

The report is a review queue, not an authorization. Ordinary open-source
candidates default to the Agent Review Quorum defined in
`docs/agent-review-quorum-v0.1.md`. Human selection is required only when the
requested action falls into a human-exception class or an unresolved anomaly
requires escalation.

### Trust Guard

Trust Guard v0.1 is the frozen set of existing governance assets:

- Opportunity Object Schema v0.1;
- Matching Score Model v0.1;
- Approval Object Model v0.1;
- Object Relationship Model v0.1;
- Validation Model v0.1;
- Validator Prototype v0.1;
- recorded Validation Runs and Validation Experiment Summary v0.1.

Trust Guard is consulted after a candidate is selected for action and before a
proposed external effect. It does not rank discovery candidates or authorize
action by itself. Its results may be evidence for the separate Agent Review
Quorum.

The freeze may be reopened only if a defect blocks the real discovery path or
would make a proposed external action unsafe. Reopening requires a separately
scoped change and must not rewrite historical runs.

### External Action

External Action is outside the MVP. No executor, GitHub write command, email
sender, application client, bid client, or contact client exists.

## Admission and Exclusion Rules

A retained candidate requires:

- an attributable public source URL;
- `state=OPEN` at retrieval time;
- an unlocked public Issue entry;
- activity within the configured 90-day freshness window;
- at least one source-backed pain classification;
- at least one source-backed TITMAS capability mapping;
- no prohibited participation method;
- no exact match to the excluded historical Issue #636 URL.

The prototype excludes:

- resolved or closed items with no new public action entry;
- stale items without activity inside the freshness window;
- locked items or records without a public participation entry;
- explicitly assigned internal worker tasks that do not invite public
  participation;
- pull requests returned by a broad Issue search;
- pure news, announcements, newsletters, and release-note items;
- items outside the configured TITMAS capability boundary;
- duplicate, invalid, wontfix, spam, or announcement-labelled items;
- opportunities requiring impersonation, private-data misuse, spam comments,
  mass marketing, or unsolicited identity claims;
- Issue #636 unless a different, newly observed public action entry is found.

An open Issue is evidence of a public review entry, not evidence that a pull
request or unsolicited implementation will be accepted. That uncertainty is
retained for policy-selected review.

## Failure Behavior

If live collection is unavailable, the CLI must:

- emit a reason-coded blocker;
- report zero live candidates;
- avoid using fixtures as live results;
- preserve the locally testable pipeline;
- keep `external_action_authorized=false`.

Partial query failures remain visible. Successful queries may still produce a
bounded report, but coverage status becomes `PARTIAL`.

## Read-Only and No-Write Proof

The public REST transport exposes only `get`. The GitHub CLI allowlist contains
only version, authentication-status, and search commands. Tests inject a
recording transport and command runner, then assert:

- every external HTTP method is `GET`;
- no GitHub write command is accepted;
- generated Action Packs contain no executable payload;
- every permission field remains `false`;
- local report paths are the only write targets.

GraphQL Discussion search is not used during a run when authentication is
invalid. Its absence is reported, not fabricated.

## DBA Cockpit Handoff

`reports/latest-opportunities.json` is the stable future cockpit entry. It
contains:

- source Daily Report path and digest;
- current opportunities;
- data-coverage and backend limitations;
- Trust Guard and policy-selected review boundaries;
- an architecture handoff status of
  `READY_FOR_READ_ONLY_REVIEW_NOT_INTEGRATED`;
- `dba_repository_modified=false`.

This file reports progress and requests future architecture review. It does
not modify the DBA repository, create an ADR, or claim ecosystem adoption.

## Acceptance Metrics for v0.1

- at least one live public GitHub Issue query succeeds, or a blocker is
  accurately recorded;
- every selected candidate has a public source and action entry;
- selected candidate count is no greater than five;
- raw, unique, excluded, eligible, and selected counts reconcile;
- exclusion reasons are machine-readable;
- factor bands and ordering reasons are explainable;
- Action Packs remain non-executable and non-authorizing;
- Validator and historical runs remain unchanged;
- syntax, format, existing tests, discovery tests, and no-write checks pass.

## Non-Claims and Unimplemented Capabilities

v0.1 does not establish:

- authenticated GitHub coverage when credentials are invalid;
- current GitHub Discussion coverage;
- exhaustive discovery across GitHub or other ecosystems;
- calibrated ranking, predicted success, or causal value estimation;
- validated customer demand, product fit, willingness to pay, or revenue;
- maintainer interest, contribution acceptance, or partner intent;
- human-exception Approval or legal identity verification;
- external action execution from an Agent Review Quorum `ALLOW` decision;
- automated PR, comment, application, bid, contact, or email execution;
- production scheduling, persistence, monitoring, retries, alerting, or SLA;
- production security, privacy, compliance, or deployment readiness.

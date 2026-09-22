# TITMAS Scout Opportunity Report — 2026-08-02

<!-- markdownlint-disable MD013 -->

> Read-only discovery report. Heuristic ordering is unvalidated.
> Policy-selected review is required; this report does not authorize external action.

## Run Summary

- Status: `LIVE_READ_ONLY_PARTIAL_SOURCE_COVERAGE`
- Backend: `GH_CLI_AUTHENTICATED`
- Retrieved at: `2026-08-02T07:15:00Z`
- Raw retrieved candidates: 94
- Unique candidates: 94
- Excluded candidates: 36
- Selected candidates: 5
- Tracked active conversions: 1
- Discussions: `NOT_COLLECTED`

## Data Coverage

The local GitHub CLI is preferred, but this run records its actual
authentication status and any anonymous public REST fallback. GitHub
Discussion results are absent when authenticated GraphQL is unavailable.

### Raw Queries

- `Q-AI-AGENT-AUDIT` — agent audit is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 15)
- `Q-EXECUTION-EVIDENCE` — "execution evidence" is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 15)
- `Q-VERIFIABLE-TRACE` — "verifiable trace" agent is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 0)
- `Q-HUMAN-IN-THE-LOOP` — human-in-the-loop agent is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 15)
- `Q-AGENT-AUTHORIZATION` — agent authorization is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 15)
- `Q-MCP-SECURITY-AUDIT` — MCP security is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 15)
- `Q-AGENT-GOVERNANCE` — agent governance is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 15)
- `Q-PROVENANCE-REPLAY` — provenance replay agent is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 0)
- `Q-TAMPER-EVIDENCE` — tamper-evident agent is:issue is:open archived:false updated:>=2026-05-04
  (`SUCCESS`, retrieved 4)

## Selected Opportunities

### 1. [arXiv] ZK-proved agent authorization gate (R CVA / Groth16) — Toward cryptographically verifiable authorization for autonomous AI agents

- Source: [mnemonik-dev/nightly-research](https://github.com/mnemonik-dev/nightly-research/issues/27)
- Current state: `OPEN`
- Pain point: [arXiv] ZK-proved agent authorization gate (R CVA / Groth16) — Toward cryptographically verifiable authorization for autonomous AI agents: [arxiv] zk-proved agent authorization gate (r cva / groth16) — toward cryptographically verifiable authorization for autonomous ai agents paper - title: toward cryptographically verifiable…
- TITMAS components: `AGENT_INTENT_PROTOCOL`, `ARO_AUDIT`, `FDO_KERNEL_MVK`, `TOKEN_GOVERNOR`
- Action entry: [open public entry](https://github.com/mnemonik-dev/nightly-research/issues/27)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps AGENT AUTHORIZATION, AGENT GOVERNANCE COMPLIANCE, PROVENANCE REPLAY to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for Agent Review Quorum; do not post automatically.
- External action authorized: `false`

### 2. Agent audit trail and observability

- Source: [praxis-proxy/ai](https://github.com/praxis-proxy/ai/issues/194)
- Current state: `OPEN`
- Pain point: Agent audit trail and observability: agent audit trail and observability every agent action through the gateway produces an auditable record. full task lifecycle tracing across the grid. scope - propagate opentelemetry trace context…
- TITMAS components: `AGENT_EVIDENCE`, `AGENT_INTENT_PROTOCOL`, `ARO_AUDIT`
- Action entry: [open public entry](https://github.com/praxis-proxy/ai/issues/194)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps AI AGENT AUDIT to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for Agent Review Quorum; do not post automatically.
- External action authorized: `false`

### 3. feat: tiered agent authorization roles and sub-agent scope inheritance

- Source: [ptone/scion](https://github.com/ptone/scion/issues/482)
- Current state: `OPEN`
- Pain point: feat: tiered agent authorization roles and sub-agent scope inheritance: feat: tiered agent authorization roles and sub-agent scope inheritance summary agents currently receive a fixed set of hub api scopes with no mechanism for project admins or user roles to constrain…
- TITMAS components: `AGENT_INTENT_PROTOCOL`, `TOKEN_GOVERNOR`
- Action entry: [open public entry](https://github.com/ptone/scion/issues/482)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps AGENT AUTHORIZATION to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for Agent Review Quorum; do not post automatically.
- External action authorized: `false`

### 4. DefraDB ACP integration for defra-agent authorization (experimental major feature)

- Source: [source-inc/gents](https://github.com/source-inc/gents/issues/461)
- Current state: `OPEN`
- Pain point: DefraDB ACP integration for defra-agent authorization (experimental major feature): defradb acp integration for defra-agent authorization (experimental major feature) goal integrate defradb acp as a first-class authorization substrate across defra-agent . high-level design goal:…
- TITMAS components: `AGENT_INTENT_PROTOCOL`, `ARO_AUDIT`, `TOKEN_GOVERNOR`
- Action entry: [open public entry](https://github.com/source-inc/gents/issues/461)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps AGENT AUTHORIZATION to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for Agent Review Quorum; do not post automatically.
- External action authorized: `false`

### 5. [BUG] Pilot can falsely complete embodied tasks without execution evidence

- Source: [syswonder/robonix](https://github.com/syswonder/robonix/issues/189)
- Current state: `OPEN`
- Pain point: [BUG] Pilot can falsely complete embodied tasks without execution evidence: [bug] pilot can falsely complete embodied tasks without execution evidence problem pilot can mark an embodied task as complete based on the planning model's own task update=done response even when…
- TITMAS components: `AGENT_EVIDENCE`, `ARO_AUDIT`
- Action entry: [open public entry](https://github.com/syswonder/robonix/issues/189)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps EXECUTION EVIDENCE, PROVENANCE REPLAY to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for Agent Review Quorum; do not post automatically.
- External action authorized: `false`

## Existing Conversion State

- `READY_FOR_REVIEW` — [agentrust-io/ca2a#36](https://github.com/agentrust-io/ca2a/issues/36)
  (`github:agentrust-io/ca2a:issue:36`; carried from immutable local history; excluded from new discovery)

## Filtering Summary

- `OUTSIDE_TITMAS_CAPABILITY_BOUNDARY`: 35
- `PAIN_POINT_NOT_CLASSIFIED`: 9

## Review and Trust Boundary

The report is a review queue. Ordinary open-source actions require the
five-role Agent Review Quorum; legal, payment, binding identity,
restricted-data, deletion, account-security, and protected-branch merge
actions require human exception review. Trust Guard was not invoked
because report generation does not itself select an external action.

```text
HEURISTIC_RANKING_CALIBRATED=false
DEFAULT_SELECTION_MODE=AGENT_QUORUM
HUMAN_EXCEPTION_REVIEW_REQUIRED=CONDITIONAL
EXTERNAL_ACTION_AUTHORIZED=false
CUSTOMER_ACQUIRED=false
```

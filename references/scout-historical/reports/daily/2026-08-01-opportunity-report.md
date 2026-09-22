# TITMAS Scout Opportunity Report — 2026-08-01

<!-- markdownlint-disable MD013 -->

> Read-only discovery report. Heuristic ordering is unvalidated.
> Human selection is required and external action is not authorized.

## Run Summary

- Status: `LIVE_READ_ONLY_PARTIAL_SOURCE_COVERAGE`
- Backend: `GITHUB_PUBLIC_REST_GET_ONLY`
- Retrieved at: `2026-08-01T16:21:09Z`
- Raw retrieved candidates: 135
- Unique candidates: 116
- Excluded candidates: 74
- Selected candidates: 5
- Discussions: `BLOCKED`

## Data Coverage

The local GitHub CLI is preferred, but this run records its actual
authentication status and any anonymous public REST fallback. GitHub
Discussion results are absent when authenticated GraphQL is unavailable.

### Raw Queries

- `Q-AI-AGENT-AUDIT` — "AI agent" audit is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)
- `Q-EXECUTION-EVIDENCE` — agent "execution evidence" is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)
- `Q-VERIFIABLE-TRACE` — agent "verifiable trace" is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)
- `Q-HUMAN-IN-THE-LOOP` — "human in the loop" agent is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)
- `Q-AGENT-AUTHORIZATION` — "agent authorization" is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)
- `Q-MCP-SECURITY-AUDIT` — MCP security audit is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)
- `Q-AGENT-GOVERNANCE` — "agent governance" compliance is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)
- `Q-PROVENANCE-REPLAY` — agent provenance replay is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)
- `Q-TAMPER-EVIDENCE` — agent "tamper evidence" is:issue is:open archived:false updated:>=2026-05-03
  (`SUCCESS`, retrieved 15)

## Selected Opportunities

### 1. test(conformance): add delegation-link action evidence fixtures

- Source: [agentrust-io/ca2a](https://github.com/agentrust-io/ca2a/issues/36)
- Current state: `OPEN`
- Pain point: test(conformance): add delegation-link action evidence fixtures: delegation block - public delegation verifier - trace/action receipt evidence this would line up with the action receipt discussion in agentrust-io/trace-spec 66 and the embodied action receipt…
- TITMAS components: `AGENT_EVIDENCE`, `AGENT_INTENT_PROTOCOL`, `ARO_AUDIT`
- Action entry: [open public entry](https://github.com/agentrust-io/ca2a/issues/36)
- Suggested next step: `PR`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps EXECUTION EVIDENCE, PROVENANCE REPLAY, VERIFIABLE TRACE to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare a small reproducible test, documentation clarification, or bounded proof of concept for human review before any submission.
- External action authorized: `false`

### 2. [RFC] Agent Credentials

- Source: [cosai-oasis/ws4-secure-design-agentic-systems](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems/issues/99)
- Current state: `OPEN`
- Pain point: [RFC] Agent Credentials: capabilities, security posture, runtime context — so that gateways, policy enforcement points, and other agents can make access-control and delegation decisions. today, claims are expressed…
- TITMAS components: `AGENT_INTENT_PROTOCOL`, `FDO_KERNEL_MVK`, `TOKEN_GOVERNOR`
- Action entry: [open public entry](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems/issues/99)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps AGENT AUTHORIZATION, AGENT GOVERNANCE COMPLIANCE to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for human review; do not post automatically.
- External action authorized: `false`

### 3. Community proposal: Agent Action Boundary Evidence model

- Source: [dinpd/AgentPass](https://github.com/dinpd/AgentPass/issues/43)
- Current state: `OPEN`
- Pain point: Community proposal: Agent Action Boundary Evidence model: outcomes; and 6. later assessments of goal attainment or constraint compliance. without this separation, implementations commonly conflate model output with execution, treat trace context as…
- TITMAS components: `AGENT_EVIDENCE`, `AGENT_INTENT_PROTOCOL`, `ARO_AUDIT`
- Action entry: [open public entry](https://github.com/dinpd/AgentPass/issues/43)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps AGENT GOVERNANCE COMPLIANCE, HUMAN IN THE LOOP, PROVENANCE REPLAY to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for human review; do not post automatically.
- External action authorized: `false`

### 4. [RFC] Agent Manifest: a signed, pre-execution declaration layer for agentic systems

- Source: [cosai-oasis/ws4-secure-design-agentic-systems](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems/issues/149)
- Current state: `OPEN`
- Pain point: [RFC] Agent Manifest: a signed, pre-execution declaration layer for agentic systems: standards target was aaif; as of today the spec header, charter, governance and roadmap name cosai ws4 as the v1.0 path (agent-manifest 253). the two remaining a
- TITMAS components: `AGENT_EVIDENCE`, `AGENT_INTENT_PROTOCOL`, `ARO_AUDIT`, `FDO_KERNEL_MVK`
- Action entry: [open public entry](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems/issues/149)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps AGENT GOVERNANCE COMPLIANCE, HUMAN IN THE LOOP, MCP SECURITY AUDIT, PROVENANCE REPLAY to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for human review; do not post automatically.
- External action authorized: `false`

### 5. [RFC feedback] Agent Inventory Info [5050]: KV-cache-derived identity fingerprint for 151 (not the T12 audit trail, see Agent Tool Activity below)

- Source: [cosai-oasis/ws4-secure-design-agentic-systems](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems/issues/155)
- Current state: `OPEN`
- Pain point: [RFC feedback] Agent Inventory Info [5050]: KV-cache-derived identity fingerprint for 151 (not the T12 audit trail, see Agent Tool Activity below): [5050]: kv-cache-derived identity fingerprint for 151 (not the t12 audit trail, see agent tool activity below) filed against 149 (agent manifest rfc, spec v0.1), phase 1 feedback; companion to 151,…
- TITMAS components: `AGENT_EVIDENCE`, `ARO_AUDIT`, `FDO_KERNEL_MVK`
- Action entry: [open public entry](https://github.com/cosai-oasis/ws4-secure-design-agentic-systems/issues/155)
- Suggested next step: `COMMENT`
- Retention reason: Retained because the public entry is open, unlocked, fresh, and maps AI AGENT AUDIT, PROVENANCE REPLAY, TAMPER EVIDENCE to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed.
- Ranking status: `NEEDS_REVIEW`
- Unconfirmed facts: maintainer_interest, contribution_acceptance, current_unresolved_scope_beyond_open_state, implementation_effort, customer_demand, commercial_budget_or_value, legal_and_license_fit
- Minimum contribution: Prepare an evidence-backed scope question and a bounded component-mapping note for human review; do not post automatically.
- External action authorized: `false`

## Filtering Summary

- `ASSIGNED_INTERNAL_WORK_ITEM`: 1
- `OUTSIDE_TITMAS_CAPABILITY_BOUNDARY`: 69
- `PAIN_POINT_NOT_CLASSIFIED`: 45
- `PURE_NEWS_OR_ANNOUNCEMENT`: 2

## Human and Trust Boundary

The report is a review queue. A human must verify current scope,
contribution policy, implementation effort, legal constraints, and
commercial facts. Trust Guard v0.1 is frozen and was not invoked because
no candidate was selected for external action.

```text
HEURISTIC_RANKING_CALIBRATED=false
HUMAN_SELECTION_REQUIRED=true
EXTERNAL_ACTION_AUTHORIZED=false
CUSTOMER_ACQUIRED=false
```

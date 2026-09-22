---
artifact_id: titmas-scout-architecture
title: TITMAS Scout Architecture
status: DRAFT_SCAFFOLD
version: 0.1.0-draft
inspection_order:
  - docs/01_scout_architecture.md
  - docs/agent-review-quorum-v0.1.md
  - docs/02_opportunity_object_model.md
  - docs/03_matching_score_model.md
---

# TITMAS Scout Architecture

## Purpose

Define an agent-readable design surface for discovering, representing, and
matching bounded ecosystem opportunities. This document is a design scaffold;
it does not claim that a scanner, matcher, customer recommendation, or runtime
integration exists.

## Intended flow

```text
source observations
-> evidence-bounded opportunity candidates
-> OpportunityObject validation
-> matching score proposal
-> policy-selected agent quorum or human exception review
-> bounded authorization decision
-> separately permissioned action
-> bounded outcome evidence
-> feedback candidate and revalidation
```

## Component boundaries

| Component | Contract ID | Responsibility | Current status |
| --- | --- | --- | --- |
| Source adapter | `TITMAS-SCOUT-SOURCE-V0` | Collect source observations with provenance | UNDEFINED |
| Opportunity builder | `TITMAS-SCOUT-OPPORTUNITY-V0` | Produce candidate OpportunityObjects | UNDEFINED |
| Matcher | `TITMAS-SCOUT-MATCH-V0` | Evaluate candidates using an explicit score model | UNDEFINED |
| Review gate | `TITMAS-SCOUT-AGENT-REVIEW-QUORUM-V0.1` | Aggregate independent reviewer evidence into a bounded internal release decision | PROTOTYPE_IMPLEMENTED |
| Action policy | `TITMAS-SCOUT-ACTION-POLICY-V0` | Bound any proposed post-review action | SCAFFOLDED |
| Feedback loop | `TITMAS-SCOUT-FEEDBACK-V0` | Link outcomes to evidence-preserving revalidation | SCAFFOLDED |

## Linked contracts

- `TITMAS-SCOUT-OPPORTUNITY-V0`: `docs/02_opportunity_object_model.md`
- `TITMAS-SCOUT-MATCH-V0`: `docs/03_matching_score_model.md`
- `TITMAS-SCOUT-SOURCE-V0`: `docs/04_data_sources.md`
- `TITMAS-SCOUT-AGENT-REVIEW-QUORUM-V0.1`: `docs/agent-review-quorum-v0.1.md`
- `TITMAS-SCOUT-ACTION-POLICY-V0`: `docs/05_action_policy.md`
- `TITMAS-SCOUT-FEEDBACK-V0`: `docs/06_evidence_feedback_loop.md`

## Truth boundary

```text
SCOUT_ARCHITECTURE_DEFINED=true
SCOUT_DISCOVERY_PROTOTYPE_IMPLEMENTED=true
SCOUT_EXTERNAL_ACTION_EXECUTOR_IMPLEMENTED=false
SCOUT_VALIDATED=false
CUSTOMER_RECOMMENDATION_READY=false
AGENT_QUORUM_AUTHORIZATION_AVAILABLE=true
UNREVIEWED_OR_UNKNOWN_ACTION_AUTHORIZED=false
EXTERNAL_ACTION_EXECUTOR_IMPLEMENTED=false
```

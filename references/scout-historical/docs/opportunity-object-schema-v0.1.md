---
artifact_id: titmas-scout-opportunity-object-schema-v0.1
contract_id: TITMAS-SCOUT-OPPORTUNITY-V0
title: TITMAS Scout Opportunity Object Schema v0.1
status: DRAFT_SCHEMA_PROPOSAL
normative: false
machine_validatable: false
implementation_available: false
validator_available: false
---

# TITMAS Scout Opportunity Object Schema v0.1 (Draft)

## Purpose

Define the minimum proposed structured representation of an external
opportunity signal. This Markdown document is a draft field contract, not an
executable YAML Schema, JSON Schema, validator, or production data format.

## Design Principles

- Agent-readable
- Fail-closed
- Policy-selected review required before external action
- Evidence traceable
- Unknown values remain unknown
- Review and acceptance do not grant action authority

## Candidate Field Contract

| Field | Type | Required | Draft constraint |
| --- | --- | --- | --- |
| `schema_version` | string | yes | Must equal `0.1-draft` for this proposal |
| `id` | string | yes | Non-empty, stable opportunity identifier |
| `source.type` | string | yes | Candidate enum: `repository`, `standard`, `issue`, `publication`, `customer_declaration`, `other` |
| `source.reference` | string | yes | Resolvable or evidence-bound source reference |
| `source.timestamp` | RFC 3339 string | yes | Time represented by the source observation |
| `source.content_digest` | string | yes | Digest binding the object to observed source content |
| `problem` | string | yes | Bounded problem statement; must not assert unobserved customer intent |
| `domain` | string | yes | Non-empty domain label; taxonomy is not yet defined |
| `stakeholders` | array of objects | yes | Each item requires `role`; identifiers and contact data are optional and policy-bound |
| `titmas_alignment` | object | yes | Requires assessment status, rationale, capability references, and evidence references |
| `evidence` | array of objects | yes | At least one attributable evidence reference is required before review |
| `scoring` | object | yes | Must preserve `NOT_COMPUTABLE` until a versioned scoring model exists |
| `recommended_action` | object | yes | Derived, non-authoritative field; default is no action and no authorization |
| `status` | string | yes | Enum: `discovered`, `reviewed`, `accepted`, `rejected` |

## Illustrative Object Shape

The following YAML is an example only. It is not a validation schema or a
customer-derived opportunity.

```yaml
schema_version: 0.1-draft
id: EXAMPLE-NOT-REAL-001

source:
  type: other
  reference: urn:example:not-a-real-source
  timestamp: 2026-08-01T00:00:00Z
  content_digest: sha256:EXAMPLE-NOT-A-REAL-DIGEST

problem: Illustrative problem statement; not an observed customer request.
domain: illustrative-domain

stakeholders:
  - role: unknown
    identifier: null

titmas_alignment:
  status: NOT_ASSESSED
  capability_refs: []
  rationale: No alignment assessment has been performed.
  evidence_refs: []

evidence:
  - evidence_id: EXAMPLE-EVIDENCE-NOT-REAL
    reference: urn:example:not-real-evidence
    evidence_type: illustrative
    observed_at: 2026-08-01T00:00:00Z

scoring:
  status: NOT_COMPUTABLE
  model_version: null
  score_value: null
  reason_codes:
    - SCORING_MODEL_UNAVAILABLE

recommended_action:
  status: NOT_AUTHORIZED
  action_type: NONE
  authoritative: false
  external_action_allowed: false
  rationale: Policy-selected review and separate authorization are required.

status: discovered
```

## Status Semantics

| Status | Meaning | Permitted next states |
| --- | --- | --- |
| `discovered` | Source signal recorded; review not complete | `reviewed`, `rejected` |
| `reviewed` | Bounded policy-selected review record exists | `accepted`, `rejected` |
| `accepted` | Opportunity retained for governed follow-up | none in this draft |
| `rejected` | Opportunity rejected with a recorded reason | none in this draft |

Every transition requires an attributable review or decision record. Neither
`reviewed` nor `accepted` authorizes outreach, execution, spending, deployment,
or a commercial claim.

## Fail-Closed Constraints

- Missing `id`, source provenance, digest, problem, domain, evidence, scoring
  state, recommended-action state, or lifecycle status makes the object invalid
  for review or matching.
- Unknown scoring must remain `NOT_COMPUTABLE` with `score_value: null`; it must
  never default to numeric zero or participate in ranking.
- Missing or unverified evidence must not be inferred as support for a claim.
- `recommended_action` is derived and non-authoritative. Its default is
  `NOT_AUTHORIZED`, `NONE`, and `external_action_allowed: false`.
- Status changes must not mutate or erase the original source and evidence
  references.

## Constraints

This draft schema proposal does not imply:

- automatic decision making
- automatic outreach
- commercial validation
- deployment readiness
- a machine-validatable schema
- a working validator or runtime implementation

## Truth Boundary

```text
OPPORTUNITY_OBJECT_DRAFT_SCHEMA_DOCUMENTED=true
OPPORTUNITY_OBJECT_SCHEMA_DEFINED=false
OPPORTUNITY_OBJECT_SCHEMA_VALIDATED=false
OPPORTUNITY_OBJECT_VALIDATOR_IMPLEMENTED=false
OPPORTUNITY_OBJECT_RUNTIME_IMPLEMENTED=false
AUTOMATIC_DECISION_AUTHORIZED=false
AUTOMATIC_OUTREACH_AUTHORIZED=false
COMMERCIAL_VALIDATION_COMPLETE=false
DEPLOYMENT_READY=false
```

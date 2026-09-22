---
artifact_id: titmas-opportunity-object-model
title: TITMAS Opportunity Object Model
status: DRAFT_SCAFFOLD
version: 0.1.0-draft
normative: false
---

# TITMAS Opportunity Object Model

## Purpose

Describe the future canonical object exchanged between discovery and matching.
The fields below are candidate field groups, not a frozen schema.

## Candidate field groups

| Field group | Intended meaning | Minimum evidence requirement | Required decision |
| --- | --- | --- | --- |
| identity | Stable candidate identifier and object version | Identifier issuer and version record | ID format |
| source | Source reference, observation time, and provenance | Resolvable source reference and observation timestamp | Accepted source types |
| need | Bounded customer or ecosystem need | Attributable need statement or explicit human declaration | Need taxonomy |
| capability | Candidate capability required to address the need | Versioned capability reference plus supporting evidence | Capability registry |
| constraints | Policy, cost, time, compatibility, and risk limits | Reference for every asserted constraint | Constraint vocabulary |
| evidence | Evidence references supporting each claim | At least one attributable reference per supported claim | Evidence profile |
| lifecycle | Draft, reviewed, accepted, rejected, or expired state | Actor, timestamp, prior state, and rationale for each transition | Transition rules |

## Minimum validation direction

- Missing provenance must remain explicit.
- Unknown required fields must not be inferred as satisfied.
- Discovery does not grant execution or outreach authority.
- A candidate object is not proof of customer demand or product fit.

## Truth boundary

```text
OPPORTUNITY_OBJECT_SCHEMA_DEFINED=false
OPPORTUNITY_OBJECT_VALIDATOR_IMPLEMENTED=false
OPPORTUNITY_LIFECYCLE_AUTHORIZED=false
```

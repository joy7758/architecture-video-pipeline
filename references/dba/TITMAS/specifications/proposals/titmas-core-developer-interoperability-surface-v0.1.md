---
id: DRAFT-ID-CORE-INTEROP-001
title: TITMAS Core Developer Interoperability Surface v0.1
title_zh: TITMAS 核心开发者互操作表面 v0.1
category: INTEROPERABILITY
status: DEVELOPMENT_DRAFT
maturity: Development
owner_ref: DBA_STEWARDSHIP
authority_ref: HUMAN_ARCHITECTURE_DECISION_REQUIRED
version: 0.1.0
normative: false
---

# TITMAS Core Developer Interoperability Surface v0.1

## Scope

Define a small, framework-neutral envelope that binds existing identity,
boundary, Evidence, Verification and Evaluation objects without taking their
ownership.

## Non-goals

- creating a canonical Identity, Evidence, Verification or Evaluation object;
- running an Agent or executing a recommendation;
- claiming safety, Truth, adoption, certification or DBOS admission;
- exposing SAEE Core algorithms.

## Object ownership

| Surface | TITMAS role | Canonical owner remains |
|---|---|---|
| Identity Reference | reference | DBOS or explicitly named source |
| Boundary Declaration | portable declaration | declaring entity plus governing source |
| Evidence Binding | reference/binding | Agent Evidence/EEOAP/DBOS source |
| Verification Result Reference | reference | DBOS or named verifier |
| Evaluation Handoff | read-only handoff | SAEE or named evaluator |
| Limitation Declaration | envelope-owned disclosure | envelope producer |

## Required fields

- `profile_version`
- `identity_ref`: `id`, `source`, `version`
- `boundary`: `allowed_actions`, `forbidden_actions`, `constraints`
- `event`: `event_id`, `action`, `result`, `timestamp`
- `evidence_binding`: `evidence_ref`, `source`, `admission_status`
- `verification_result`: `verification_ref`, `status`, `verifier_ref`
- `evaluation_handoff`: `status`, `input_refs`
- `limitations`
- `claims`

## Optional fields

- `extensions`
- `correlation_refs`
- `resource_refs`

Unknown extension fields must be preserved or explicitly rejected. They cannot
be silently converted into required semantics.

## Failure semantics

- missing required field → `INVALID`;
- forbidden action → `BOUNDARY_REJECTED`;
- unresolved Evidence reference → `NOT_ASSESSED`;
- unsupported version → `UNSUPPORTED_VERSION`;
- conflicting source semantics → `CONFLICTED`;
- tool or validator error → `ERROR`, with no success claim.

## Unknown semantics

`UNKNOWN`, `NOT_ASSESSED`, `UNSUPPORTED` and `CONFLICTED` are first-class
results. They must not be coerced to `PASS`, `false`, empty or omitted.

## Version negotiation

Producers declare one `profile_version`. Consumers declare supported versions
and select an exact compatible version. Unsupported major versions fail closed.
Optional additive fields may be ignored only when their semantics are not
required for a claim.

## Security considerations

Validate untrusted paths and sizes; never execute values from the envelope;
bind sources and versions; avoid credentials and real payloads; reject scope
expansion; preserve failed records.

## Privacy considerations

Use references rather than prompts, responses or tool payloads. Include only
synthetic or authorized data, purpose, retention and redaction constraints.

## Positive example

The reference implementation accepts a synthetic event whose action is present
in `allowed_actions`, binds an existing synthetic Evidence reference, records a
Verification reference and creates a read-only Evaluation handoff.

## Negative examples

- Observation relabeled as admitted Evidence;
- Evidence PASS relabeled as Truth;
- Verification relabeled as Authorization;
- Mapping relabeled as Adoption;
- Experimental profile relabeled as Stable;
- Recommendation relabeled as Command;
- Health result relabeled as safety Certification;
- Reference implementation relabeled as specification Authority.

## No semantic elevation

```text
OBSERVATION_NE_EVIDENCE=true
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_AUTHORIZATION=true
MAPPING_NE_ADOPTION=true
EXPERIMENTAL_NE_STABLE=true
RECOMMENDATION_NE_COMMAND=true
HEALTH_NE_CERTIFICATION=true
REFERENCE_IMPLEMENTATION_NE_STANDARD=true
```

## Current status

The local harness and synthetic reference implementation exercise this
Development proposal. Their PASS does not adopt the proposal or prove external
interoperability.

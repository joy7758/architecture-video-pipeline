---
artifact_id: titmas-scout-approval-object-model-v0.1
contract_id: TITMAS-SCOUT-APPROVAL-OBJECT-V0.1
title: TITMAS Scout Approval Object Model v0.1
status: DRAFT_MODEL_AGENT_QUORUM_AMENDMENT
version: 0.1.1-draft
normative: false
object_grammar_defined: true
machine_executable: false
schema_available: false
validator_available: false
approval_engine_available: false
executor_integration_available: false
agent_quorum_reviewer_supported: true
---

# TITMAS Scout Approval Object Model v0.1 (Draft)

## Purpose

The Approval Object closes the conceptual gap between evidence-backed
assessment and any bounded action. It records an explicit decision by a typed
reviewer authority, the exact action request considered, and the scope and
conditions of that decision. For ordinary open-source contributions the
default reviewer type is `AGENT_QUORUM`; human review is reserved for the
exception actions defined by Action Policy.

An Approval Object is an immutable audit record. It is not an action command,
an execution token, evidence that an opportunity claim is true, or proof that
the reviewer identity and authority are valid. A future enforcement component
would have to verify all of those inputs independently before permitting an
action.

This draft defines an agent-readable object grammar and fail-closed decision
semantics. It does not implement approval, validation, identity, policy, or
execution capabilities.

## Design Basis

This model adopts two design boundaries:

- an agent may prepare a structured action request, while a separately
  permissioned component controls any write or external effect;
- an operation pauses until the policy-selected reviewer authority produces an
  explicit decision bound to the exact interrupted request; human exception
  actions cannot be approved by an Agent Review Quorum.

These boundaries are informed by the GitHub Agentic Workflows
[permissions](https://github.github.com/gh-aw/reference/permissions/) and
[safe outputs](https://github.github.com/gh-aw/reference/safe-outputs/)
references, and by the OpenAI Agents SDK
[human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)
pause, decide, and resume pattern. These references inform the design only;
they do not establish implementation, compatibility, or security claims for
TITMAS Scout.

## Normative Vocabulary

The keywords `MUST`, `MUST NOT`, `REQUIRED`, and `MAY` describe the proposed
v0.1 contract. Because this artifact is a non-normative draft without a
validator or runtime, those keywords specify future implementation behavior;
they do not assert that the behavior exists now.

Definitions:

- **declared decision**: the immutable value stored in `decision`;
- **effective state**: the state derived from the declared decision, validity
  window, supersession graph, and trusted evaluation time;
- **authorization result**: `ALLOW` or `DENY` produced by a future enforcement
  component after all gates are evaluated;
- **bound reference**: an identifier, version, location, and digest that point
  to one exact artifact snapshot;
- **action request**: a structured safe-output request describing one proposed
  action before execution;
- **active head**: the single unsuperseded Approval Object applicable to one
  opportunity and action request.

`APPROVED` is a declared decision. It is not synonymous with an `ALLOW`
authorization result.

## Bound Reference Grammar

Every reference relied on by an `APPROVED` object MUST use this structure:

```yaml
reference_id: <non-empty-stable-identifier>
reference_type: <registered-exact-type>
reference_uri: <exact-path-or-uri>
version: <immutable-version>
content_digest: sha256:<64-lowercase-hex-characters>
```

The digest binds the exact referenced bytes. A mutable location without a
matching immutable version and digest is not a bound reference. A label such
as `VERIFIED` inside a referenced object is not a substitute for independently
checking its digest, provenance, admissibility, and status.

Reviewer evidence is type-specific. Agent quorum decisions require the exact
agent and runtime identifiers, roles, input and output digests, decisions,
timestamps, and ruleset version defined by Agent Review Quorum v0.1. Human and
organization-policy decisions require their own identity and authority
evidence. v0.1 digests support deterministic integrity checks but are not
cryptographic identity attestations or execution credentials.

## Object Structure

The following YAML is a structural grammar, not an approval instance. Angle
brackets denote required typed values. `null` is allowed only where a field is
explicitly described as nullable.

```yaml
schema_version: 0.1-draft
object_type: TITMAS_SCOUT_APPROVAL

approval_id: <globally-unique-immutable-identifier>

opportunity_reference:
  reference_id: <opportunity-id>
  reference_type: TITMAS_SCOUT_OPPORTUNITY
  reference_uri: <exact-path-or-uri>
  version: <opportunity-schema-version>
  content_digest: sha256:<digest>

assessment_reference:
  reference_id: <assessment-id>
  reference_type: TITMAS_SCOUT_MATCHING_ASSESSMENT
  reference_uri: <exact-path-or-uri>
  version: <assessment-version>
  content_digest: sha256:<digest>
  model_id: <exact-model-id>
  model_version: <exact-model-version>
  overall_status: <exact-assessment-status>
  opportunity_id: <same-opportunity-id>
  opportunity_content_digest: sha256:<same-opportunity-digest>

action_request_reference:
  reference_id: <request-id>
  reference_type: TITMAS_SCOUT_ACTION_REQUEST
  reference_uri: <exact-path-or-uri>
  version: <request-version>
  content_digest: sha256:<digest>

policy_reference:
  reference_id: <policy-id>
  reference_type: TITMAS_SCOUT_ACTION_POLICY
  reference_uri: <exact-path-or-uri>
  version: <policy-version>
  content_digest: sha256:<digest>

decision: APPROVED | REJECTED | DEFERRED | EXPIRED

authorized_scope:
  subject_ids:
    - <exact-agent-or-executor-id>
  target_ids:
    - <exact-resource-id>
  environment_ids:
    - <exact-environment-id>
  parameter_constraints:
    - selector: <json-pointer-into-action-request>
      operator: EQUALS | IN | LTE | GTE | DIGEST_EQUALS
      expected: <typed-scalar-list-or-digest>
  max_execution_attempts: <non-negative-integer>
  max_successful_executions: <non-negative-integer>

allowed_actions:
  - action_id: <exact-action-id>
    action_type: <registered-exact-action-type>
    request_id: <same-action-request-id>
    request_content_digest: sha256:<same-request-digest>
    target_ids:
      - <exact-target-id>
    parameter_content_digest: sha256:<digest>

blocked_actions:
  - action_type: <registered-exact-action-type-or-*>
    target_ids:
      - <exact-target-id-or-*>
    reason_code: <registered-denial-reason-code>

constraints:
  - constraint_id: <stable-identifier>
    enforcement: HARD
    selector: <json-pointer-into-action-request-or-context>
    operator: EQUALS | IN | LTE | GTE | DIGEST_EQUALS
    expected: <typed-scalar-list-or-digest>
    evidence_references:
      - <bound-reference>

reviewer:
  type: AGENT | AGENT_QUORUM | HUMAN | ORGANIZATION_POLICY
  reviewer_id: <stable-reviewer-or-quorum-id>
  role: <registered-role-or-release-decision-role>
  agent_reviews:
    - agent_identifier: <exact-agent-instance-id>
      model_runtime_identifier: <exact-model-or-runtime-id>
      review_role: <registered-review-role>
      input_digest: sha256:<digest>
      output_digest: sha256:<digest>
      decision: PASS | BLOCKING_FAIL
      timestamp: <utc-rfc3339-seconds>
      ruleset_version: <exact-ruleset-version>
  identity_reference: <bound-reference-or-null-by-reviewer-type>
  authority_reference: <bound-reference>
  attestation_reference: <bound-reference>

timestamp:
  decided_at: <utc-rfc3339-seconds>
  recorded_at: <utc-rfc3339-seconds>
  valid_from: <utc-rfc3339-seconds>
  expires_at: <utc-rfc3339-seconds>
  time_source_reference: <bound-reference>

evidence_reference:
  - <bound-reference>

decision_reason_codes:
  - <registered-reason-code>

supersedes_approval_reference: <bound-reference-or-null>
```

### Field Contract

| Field | Type and cardinality | Fail-closed rule |
| --- | --- | --- |
| `approval_id` | Required unique string | Reuse or ambiguity makes the object invalid |
| `opportunity_reference` | Required bound reference | It MUST identify one exact Opportunity Object snapshot |
| `assessment_reference` | Required structured bound reference | Its opportunity ID and digest MUST equal `opportunity_reference` |
| `action_request_reference` | Required bound reference for `APPROVED` | Changed request bytes require a new policy-selected review decision |
| `policy_reference` | Required bound reference for `APPROVED` | Missing, unresolved, denied, or expired policy produces `DENY` |
| `decision` | Required four-value enum | Missing or unknown value produces `DENY` |
| `authorized_scope` | Required structured object | Natural-language text MUST NOT grant scope |
| `allowed_actions` | Required list | Only exact listed actions are candidates; the list is not a wildcard |
| `blocked_actions` | Required deny overlay | A matching denial wins over every allow; unknown actions remain denied |
| `constraints` | Required list | v0.1 constraints are `HARD`; missing, unknown, or failed results produce `DENY` |
| `reviewer` | Required typed reviewer record | Type-specific identity/runtime, authority, role, digest, decision, and attestation evidence MUST verify |
| `timestamp` | Required validity record | Untrusted time or an invalid interval produces `DENY` |
| `evidence_reference` | Required list of bound references | Approval does not replace, create, or validate the referenced evidence |
| `decision_reason_codes` | Required non-empty list | Unknown codes do not grant authority; prose is non-authoritative |
| `supersedes_approval_reference` | Required nullable bound reference | Invalid, circular, or branching relations produce `DENY` |

All top-level keys in the grammar MUST be present. For a non-`APPROVED`
decision, `allowed_actions` MUST be an empty list,
`max_execution_attempts` and `max_successful_executions` MUST be `0`, and
`blocked_actions` MUST contain an `action_type: "*"` denial.

### Scope and Action Semantics

`authorized_scope` is a ceiling, not an additional source of permission. An
action is a candidate only when it is explicitly present in `allowed_actions`
and every subject, target, environment, parameter, request digest, and usage
limit is also within `authorized_scope`.

The `allowed_actions` list accepts exact registered action types only. Wildcard
allows, prefix matching, fuzzy matching, inferred synonyms, and natural-language
scope expansion are prohibited in v0.1. A wildcard is permitted only in
`blocked_actions`, where it broadens denial.

`blocked_actions` is not an exhaustive list of everything prohibited. It is an
explicit denial overlay. Any action not exactly listed in `allowed_actions` is
already denied. If one action matches both lists, the block wins.

Parameter constraints use the closed operator enum shown in the grammar.
Unknown operators, missing selectors, type mismatches, unresolved targets, or
non-deterministic expressions produce `DENY`. Optional human-readable notes MAY
exist in a future serialization, but they MUST NOT create permission or alter
machine-evaluated scope.

## Decision States

| State | Meaning | Action effect |
| --- | --- | --- |
| `APPROVED` | The policy-selected reviewer authority approved the exact bound request and scope | Candidate for evaluation only; all other gates still apply |
| `REJECTED` | The policy-selected reviewer authority explicitly denied the request | `DENY`; no allowed action may be present |
| `DEFERRED` | Review is postponed or requires more evidence or authority | `DENY`; absence of a final decision is not permission |
| `EXPIRED` | The decision is outside its validity or was explicitly closed as expired | `DENY`; renewal requires a new complete object |

There is no implicit `PENDING`, `DEFAULT_APPROVED`, or inherited state. No
Approval Object means `DENY` with reason code `APPROVAL_MISSING`.

### Declared Decision and Effective State

The declared `decision` never changes in place. A future evaluator derives the
effective state as follows:

```text
if declared_decision in {REJECTED, DEFERRED, EXPIRED}:
  effective_state=declared_decision
  authorization_result=DENY
elif trusted_time_unavailable_or_inconsistent:
  effective_state=DEFERRED
  authorization_result=DENY
elif now < valid_from:
  effective_state=DEFERRED
  authorization_result=DENY
elif now >= expires_at:
  effective_state=EXPIRED
  authorization_result=DENY
else:
  effective_state=APPROVED
  authorization_result=CONTINUE_FAIL_CLOSED_EVALUATION
```

The validity interval is half-open: `[valid_from, expires_at)`. Timestamps MUST
be RFC 3339 UTC values with second precision, `decided_at <= recorded_at`, and
`decided_at <= valid_from < expires_at`. There is no grace period. If a future
executor cannot establish a trusted evaluation time, it MUST deny the action.

Reaching `APPROVED` effective state does not itself produce `ALLOW`; it only
permits evaluation of the remaining gates.

### Immutable Lifecycle and Supersession

Decisions MUST be append-only. No state transition rewrites an existing
Approval Object. A changed decision, scope, action request, reviewer,
constraint, evidence set, policy, or validity window requires a new object.

Permitted logical successors are:

| Active head | Permitted successor decision | Additional condition |
| --- | --- | --- |
| None | `APPROVED`, `REJECTED`, or `DEFERRED` | A first `APPROVED` MUST satisfy every approval invariant |
| `DEFERRED` | Any of the four states | The successor explicitly references the deferred object |
| `APPROVED` | Any of the four states | The successor immediately and permanently supersedes the prior grant |
| `REJECTED` | `APPROVED`, `REJECTED`, or `DEFERRED` | A later `APPROVED` requires new assessment or evidence and a complete review |
| `EXPIRED` | `APPROVED`, `REJECTED`, or `DEFERRED` | The expired object is never reactivated or renewed in place |

Every successor is complete and self-contained. It MUST NOT inherit permission,
scope, constraints, evidence, or authority from its predecessor.

Supersession rules are non-negotiable:

- one object has at most one predecessor;
- a predecessor has at most one successor;
- self-reference, cycles, broken references, and branches are invalid;
- a superseded object is permanently ineffective, even if its successor is
  later rejected, deferred, expired, missing, or invalid;
- expiration of a successor MUST NOT revive an older `APPROVED` object;
- multiple unsuperseded or overlapping applicable approvals produce
  `CONFLICTING_APPROVALS` and `DENY`;
- permissions from separate Approval Objects MUST NOT be unioned or composed;
- moving from `REJECTED` or `EXPIRED` to `APPROVED` requires a new assessment
  or evidence snapshot, a new attestation, and complete re-evaluation.

These rules prevent stale authorization from becoming a fallback path.

## Approval Invariants

An object with `decision: APPROVED` is structurally admissible only when all of
the following are true:

1. every required field is present and uses the exact declared type;
2. every relied-on reference is bound and its digest verifies;
3. the Opportunity Object snapshot is validated and is identical to the
   snapshot bound into the assessment;
4. the assessment is complete, has no verified hard blocker, and is not
   `NOT_COMPUTABLE` or `BLOCKED`;
5. no score value, score band, or ranking is treated as approval evidence;
6. the action request bytes match `action_request_reference` and each allowed
   action entry;
7. `allowed_actions` is non-empty and contains no wildcard;
8. each allowed subject, target, environment, parameter, and limit is a subset
   of `authorized_scope`;
9. the current Action Policy is bound, applicable, independently permits the
   request, and has not expired;
10. reviewer type and its required identity or runtime identifiers, roles,
    authority scope, input/output digests, decisions, and attestations verify;
11. the trusted time is within the half-open validity interval;
12. exactly one applicable active head exists and it has not been superseded;
13. every hard constraint is satisfied with admissible evidence;
14. no `blocked_actions` entry matches the request;
15. the requested action is within the future executor's own static capability
    and permission boundary;
16. attempt and successful-execution limits can be checked atomically before
    the side effect.

Failure, absence, `null`, `UNKNOWN`, ambiguity, conflict, or unverifiable state
in any invariant produces `DENY`. No invariant can compensate for another.

For `TITMAS-SCOUT-MATCHING-SCORE-V0.1`, a `BLOCKED` or `NOT_COMPUTABLE`
assessment cannot support an `APPROVED` object. A
`COMPUTED_UNCALIBRATED` assessment remains diagnostic: its number has no
threshold, eligibility, priority, or authority meaning. Approval neither
clears nor rewrites the matching model's action lock; authority is evaluated
only through the independent gates in this document and the Action Policy.

## Future Authorization Evaluation

A future enforcement component MUST begin with `DENY` and may return `ALLOW`
only for one exact action request that passes every gate:

```text
authorization_result=DENY

require valid_approval_object
require effective_state == APPROVED
require unique_unsuperseded_active_head
require verified_opportunity_assessment_and_evidence_binding
require verified_reviewer_type_specific_identity_runtime_authority_and_attestation
require applicable_action_policy_result == ALLOW
require requested_action exactly_matches allowed_actions
require requested_scope subset_of authorized_scope
require requested_action not_matches blocked_actions
require all_hard_constraints == SATISFIED
require executor_static_permission == ALLOW
require atomic_usage_limit_check == PASS

authorization_result=ALLOW
```

The effective permission is the intersection of the exact request, one
Approval Object, the applicable Action Policy, all hard constraints, and the
executor's static permissions. Denials take precedence. No source may add
permission that another source does not grant.

The check and the side effect would need an atomic or otherwise replay-safe
boundary. That boundary, the usage ledger, and the executor are not implemented
in v0.1. Consequently this Approval Object and full enforcement path cannot
currently produce executable `ALLOW`. The separate Agent Review Quorum
prototype may produce a bounded internal release `ALLOW`; that result is not
execution authority and does not itself perform an external action.

## Safe-Output Separation

The discovery or matching agent MAY prepare a structured action request. The
same action-producing agent MUST NOT be the sole reviewer or mint permission
from its own recommendation. A separately identified Agent Review Quorum MAY
produce an Approval for agent-authorizable actions when every required role
passes over the same input digest. No agent may assert human identity or hold
write credentials merely because it produced a request or review.

A future flow would be:

```text
agent creates bounded action request
  -> execution pauses
  -> policy selects AGENT_QUORUM or HUMAN_EXCEPTION authority
  -> selected reviewer authority records one explicit decision
  -> independent verifier checks references, authority, state, and policy
  -> separately permissioned executor rechecks the exact request
  -> action is denied or executed within the approved intersection
  -> outcome evidence is appended without rewriting prior records
```

Approval and execution records MUST remain separately identifiable. An
execution receipt would need to reference the approval, policy, request,
executor identity, timestamps, and observed outcome. This receipt capability
is not defined by the Approval Object.

## Fail-Closed Rules

The following rules are mandatory for any future consumer:

- **No authorization, no action.** Missing, invalid, unresolved, unknown-type,
  or non-`APPROVED` authorization produces `DENY`.
- **No action outside authorized scope.** Subjects, targets, environments,
  parameters, action types, validity, attempts, and execution counts are all
  upper bounds. Any excess produces `DENY`.
- **Authorization cannot replace evidence.** Approval does not make an
  opportunity claim true, repair provenance, validate a digest, complete a
  missing assessment, or satisfy a hard constraint.
- **A high score cannot bypass authorization.** Scores, rankings, labels,
  confidence, and recommendations never substitute for an explicit valid
  Approval Object and applicable Action Policy.
- **Deny wins.** A blocked action, failed policy, hard constraint, revoked or
  superseded record, runtime restriction, or executor denial overrides every
  allow candidate.
- **Unknown means no permission.** Unknown fields, enums, actions, references,
  authority, time, state, or evaluator results produce `DENY` when relevant to
  authorization.
- **No permission composition.** Partial permissions from different objects,
  reviewers, policies, or scopes cannot be joined into a larger grant.
- **No stale fallback.** An earlier approval never becomes active again because
  a newer record expires or fails.
- **No mutation.** Correcting or changing a decision requires a new linked
  object and preserves the earlier evidence trail.

## Agent-Readable Requirements

Any future serialization, schema, or consumer MUST preserve these properties:

- **machine readable**: fields, types, cardinalities, reference bindings,
  timestamps, operators, and reason codes are structured data;
- **explicit states**: only `APPROVED`, `REJECTED`, `DEFERRED`, and `EXPIRED`
  are valid decision values;
- **no implicit permission**: absence, prose, defaults, inference, similarity,
  wildcard allows, and unknown values never grant authority;
- all enum and reason-code comparisons are exact and case-sensitive;
- all timestamps use UTC RFC 3339 seconds and explicit interval semantics;
- all authoritative references include identity, type, version, location, and
  a SHA-256 digest;
- all authoritative constraints use the closed operator grammar; free text is
  never executable policy;
- unrecognized fields MUST NOT expand permission; a consumer that cannot prove
  they are non-authoritative MUST reject the object;
- each decision exposes deterministic reason codes and the paths of missing,
  conflicting, invalid, or unverifiable inputs;
- an evaluator MUST preserve the declared decision, effective state,
  authorization result, and denial reasons as separate values;
- validation order MUST NOT alter the result: any applicable denial is final.

Suggested denial reason codes for future schemas include:

```text
APPROVAL_MISSING
APPROVAL_INVALID
DECISION_NOT_APPROVED
APPROVAL_NOT_YET_VALID
APPROVAL_EXPIRED
APPROVAL_SUPERSEDED
CONFLICTING_APPROVALS
REFERENCE_UNRESOLVED
DIGEST_MISMATCH
OPPORTUNITY_ASSESSMENT_MISMATCH
ASSESSMENT_NOT_ADMISSIBLE
EVIDENCE_INSUFFICIENT
REVIEWER_IDENTITY_UNVERIFIED
REVIEWER_AUTHORITY_UNVERIFIED
ATTESTATION_UNVERIFIED
POLICY_UNAVAILABLE
POLICY_DENIED
ACTION_NOT_ALLOWED
ACTION_EXPLICITLY_BLOCKED
SCOPE_EXCEEDED
CONSTRAINT_NOT_SATISFIED
TIME_UNVERIFIABLE
EXECUTOR_PERMISSION_DENIED
USAGE_LIMIT_UNVERIFIABLE
```

The list is a draft vocabulary, not an implemented registry.

## Adversarial Conformance Cases

| Case | Required result |
| --- | --- |
| Evidence bytes change after review | Digest mismatch; `DENY` |
| Assessment references an older Opportunity Object digest | Binding mismatch; `DENY` |
| Stored `APPROVED` is evaluated at exactly `expires_at` | Effective state `EXPIRED`; `DENY` |
| Trusted clock is unavailable or inconsistent | `TIME_UNVERIFIABLE`; `DENY` |
| Two overlapping approvals have no valid supersession relation | `CONFLICTING_APPROVALS`; `DENY` |
| A superseding approval expires | The predecessor remains superseded; `DENY` |
| A supersession chain contains a cycle or branch | Invalid chain; `DENY` |
| Request parameters change after approval | Request or parameter digest mismatch; `DENY` |
| An allowed action also matches `blocked_actions` | `ACTION_EXPLICITLY_BLOCKED`; `DENY` |
| An action is absent from both allow and block lists | `ACTION_NOT_ALLOWED`; `DENY` |
| A score is numerically high but approval is absent | `APPROVAL_MISSING`; `DENY` |
| Reviewer role is present but authority evidence is unverifiable | `REVIEWER_AUTHORITY_UNVERIFIED`; `DENY` |
| Usage count cannot be checked atomically | `USAGE_LIMIT_UNVERIFIABLE`; `DENY` |

## Non-Implications

This model does not imply:

- unreviewed approval, automatic outreach, or external execution;
- that any Opportunity Object or assessment is true, validated, or current;
- that a reviewer identity, credential, role, signature, or authority is valid;
- that `APPROVED` is executable without independent policy and runtime checks;
- that a score is calibrated, validated, eligible, or commercially meaningful;
- compatibility with GitHub Agentic Workflows, OpenAI Agents SDK, or another
  runtime;
- deployment readiness, production safety, legal effect, or commercial
  validation.

## Current Unimplemented Capabilities

- formal JSON Schema or YAML schema for the Approval Object;
- schema validation and canonical serialization;
- bound-reference resolver and digest verification;
- Opportunity Object and assessment validators;
- evidence provenance, freshness, and admissibility verification;
- reviewer-type identity or runtime, role, credential, authority,
  attestation, independence, and revocation verification;
- trusted time service and clock-skew handling;
- Action Policy schema, registry, evaluator, and expiry enforcement;
- safe-output action-request schema and durable pause/resume workflow;
- supersession graph registry, cycle detection, and concurrency control;
- atomic approval consumption, replay protection, and usage ledger;
- independent permissioned executor and static-capability enforcement;
- action receipt, rollback, stop, and outcome-evidence integration;
- conformance test suite, security review, calibration, and production
  validation.

## Truth Boundary

```text
APPROVAL_OBJECT_MODEL_DEFINED=true
APPROVAL_OBJECT_SCHEMA_DEFINED=false
APPROVAL_OBJECT_VALIDATOR_IMPLEMENTED=false
APPROVAL_ENGINE_IMPLEMENTED=false
IDENTITY_AND_AUTHORITY_VERIFICATION_IMPLEMENTED=false
ACTION_POLICY_ENGINE_IMPLEMENTED=PROTOTYPE_SUBSET
AGENT_QUORUM_AUTHORIZATION_PROTOTYPE_IMPLEMENTED=true
SAFE_OUTPUT_RUNTIME_IMPLEMENTED=false
EXECUTOR_INTEGRATION_IMPLEMENTED=false
APPROVAL_MODEL_VALIDATED=false
UNBOUND_ACTION_AUTHORITY_GRANTED=false
EXTERNAL_ACTION_EXECUTOR_AUTHORIZED=false
```

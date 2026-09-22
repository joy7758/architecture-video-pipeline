---
artifact_id: titmas-scout-matching-score-v0.1
contract_id: TITMAS-SCOUT-MATCH-V0
model_id: TITMAS-SCOUT-MATCHING-SCORE-V0.1
title: TITMAS Scout Matching Score Model v0.1
status: DRAFT_MODEL_PROPOSAL
version: 0.1.0-draft
normative: false
machine_executable: false
calibrated: false
validated: false
implementation_available: false
---

# TITMAS Scout Matching Score Model v0.1 (Draft)

## Purpose

Define a deterministic, agent-readable proposal for evidence-linked diagnostic
matching. This model separates evidence availability from numeric rating,
fails closed when required evidence is missing, and never grants action
authority.

This document defines draft calculation rules. It is not an implemented,
calibrated, validated, or production ranking model.

## Model Identity

```yaml
model_id: TITMAS-SCOUT-MATCHING-SCORE-V0.1
model_reference: docs/matching-score-v0.1.md
model_version: 0.1.0-draft
supported_opportunity_schema: 0.1-draft
weights:
  capability_fit: 0.20
  evidence_quality: 0.20
  constraint_fit: 0.20
  freshness: 0.20
  risk: 0.20
calibration_status: UNAVAILABLE
validation_status: NOT_VALIDATED
```

Equal weights are used only to make the draft diagnostic calculation
transparent. They are not empirically justified weights and must not be
interpreted as calibrated importance.

## Input Contract

The model consumes an Opportunity Object plus linked assessment records. The
following inputs are required before a diagnostic value can be computed.

| Input | Source field or linked record | Required condition |
| --- | --- | --- |
| Object identity | `id`, `schema_version`, `status` | Supported version and stable ID |
| Object validation | `validation.status` | Exactly `VALIDATED` |
| Source provenance | `source.reference`, `source.timestamp`, `source.content_digest` | Integrity checked and admitted for scoring |
| Problem and domain | `problem`, `domain` | Bounded and non-empty |
| Stakeholder evidence | `stakeholders` | Confirmation status explicitly assessed |
| TITMAS alignment | `titmas_alignment` | Assessment complete with claim-level evidence references |
| Evidence inventory | `evidence` | Attributable references and verified content digests |
| Constraint profile | Linked constraint assessment | Hard and soft constraints declared and assessed |
| Freshness policy | Linked freshness policy | Versioned rating bands, rejection boundary, and evaluation timestamp present |
| Risk assessment | Linked risk record | Severity, mitigation, and residual risk assessed |
| Model binding | `scoring.model_reference`, `scoring.reference_status` | Exact model path and reference state recorded |

The current Opportunity Object draft does not define every linked assessment
record. Absence of any required record produces `NOT_COMPUTABLE`; it must not
be inferred from prose or replaced with a default value.

## Evidence Availability Grammar

Each dimension must record one availability state before any rating is
considered:

| State | Meaning | Numeric rating allowed |
| --- | --- | --- |
| `PENDING` | Assessment has not been completed | no |
| `MISSING` | Required evidence is absent | no |
| `INVALID` | Evidence integrity or provenance check failed | no |
| `STALE` | Evidence fails the applicable freshness policy | no |
| `AVAILABLE` | Required attributable evidence is present and admissible | yes |

Missing, invalid, stale, or pending evidence has no numeric value. In
particular, it must never be encoded as rating `0`.

## Rating Grammar

A rating is an integer in `[0, 4]` and is valid only when the dimension's
evidence state is `AVAILABLE`. Every rating requires:

- one or more evidence references;
- a bounded rationale;
- the assessor or assessment-process reference;
- an assessment timestamp;
- any applicable hard-gate flag.

Rating `0` means that admissible evidence supports a severe mismatch or
failure. It never means that evidence is absent. If the same evidence also
establishes a hard constraint violation, the hard gate controls the overall
state independently of the rating.

## Scoring Dimensions

### 1. Capability Fit

Inputs:

- bounded problem and domain;
- assessed TITMAS capability references;
- claim-level alignment evidence;
- executed or independently reviewed capability evidence when available.

| Rating | Evidence-backed interpretation |
| --- | --- |
| `0` | Evidence demonstrates no applicable capability or direct incompatibility |
| `1` | Attributable evidence supports only a conceptual association |
| `2` | Requirements and capabilities are explicitly mapped, but not executed |
| `3` | Bounded execution evidence supports the major declared requirements |
| `4` | Independent reproduction supports all declared requirements in scope |

### 2. Evidence Quality

Inputs:

- evidence references and content digests;
- provenance and integrity results;
- claim-to-evidence mappings;
- recorded limitations and independent review evidence.

| Rating | Evidence-backed interpretation |
| --- | --- |
| `0` | Admissible evidence directly refutes the evaluated claim |
| `1` | One attributable source supports the claim with major recorded limitations |
| `2` | Multiple attributable sources support the claim without independent reproduction |
| `3` | Integrity-checked, claim-linked evidence supports reproducible review |
| `4` | Independent audit or reproduction confirms the evidence chain in scope |

An integrity failure makes the evidence `INVALID` and the score
`NOT_COMPUTABLE`; it is not an evidence-quality rating of `0`.

### 3. Constraint Fit

Inputs:

- versioned policy, cost, time, compatibility, privacy, and usage constraints;
- hard-versus-soft classification;
- per-constraint assessment evidence.

| Rating | Evidence-backed interpretation |
| --- | --- |
| `0` | Evidence demonstrates material constraint violations |
| `1` | Major soft-constraint gaps remain |
| `2` | Some declared constraints are met and all residual gaps are explicit |
| `3` | All declared constraints are met in a bounded assessment |
| `4` | Independent assessment verifies all declared constraints in scope |

A verified hard-constraint violation produces `BLOCKED`, regardless of the
numeric rating or other dimensions.

### 4. Freshness

Inputs:

- source and evidence observation timestamps;
- assessment timestamp;
- a versioned policy defining five admissible rating bands and a
  `reject_after` boundary.

| Rating | Evidence-backed interpretation |
| --- | --- |
| `0` | Evidence is in the lowest admissible band immediately before rejection |
| `1` | Evidence is in the next-lowest admissible policy band |
| `2` | Evidence is in the middle admissible policy band |
| `3` | Evidence is in the preferred policy band |
| `4` | All material evidence is current and independently freshness-checked |

If no freshness policy exists, or a timestamp cannot be verified, freshness is
`MISSING` or `INVALID` and the overall score is `NOT_COMPUTABLE`. Evidence past
the policy's `reject_after` boundary is `STALE`, has no numeric rating, and
produces `NOT_COMPUTABLE`.

### 5. Risk

Higher ratings mean stronger evidence of bounded risk control, not more risk.

Inputs:

- identified risks and severities;
- mitigation and residual-risk evidence;
- stop, rollback, Agent Review Quorum, and human-exception escalation paths;
- applicable safety and governance constraints.

| Rating | Evidence-backed interpretation |
| --- | --- |
| `0` | Evidence demonstrates an unmitigated critical risk |
| `1` | High residual risk remains after declared mitigations |
| `2` | Medium residual risk remains and is explicitly bounded |
| `3` | Residual risk is low with evidenced stop and rollback paths |
| `4` | Independent review verifies controls and residual-risk bounds |

Risk rating `0` is always a verified hard blocker and produces `BLOCKED`.

## Non-Compensatory Hard Gates

Hard gates are evaluated separately from the weighted diagnostic calculation.
No high dimension rating can compensate for a verified hard-gate failure.

Verified hard blockers include:

- a prohibited or unauthorized source use;
- a hard policy, privacy, safety, legal, or compatibility violation;
- an unmitigated critical risk;
- an explicitly prohibited action or target;
- any other linked constraint whose versioned policy marks it as hard.

When at least one verified hard blocker exists:

```text
overall_status=BLOCKED
score_value=null
match_eligible=false
review_required=true
action_lock=true
```

All blockers and incomplete inputs must remain visible in the result.

## NOT_COMPUTABLE Conditions

In the absence of a verified hard blocker, any of the following conditions
produces `NOT_COMPUTABLE`:

- object validation is not exactly `VALIDATED`;
- the object schema or model identifier is unsupported or ambiguous;
- `model_reference` is absent, mismatched, or `UNVERIFIED`;
- the configured weight vector differs from five exact `0.20` values or does not sum to exactly `1.00`;
- source admission or source-use authority is insufficient for scoring;
- a required source or evidence digest is missing or fails verification;
- TITMAS alignment is `PENDING`, missing, or lacks evidence references;
- the constraint profile or its assessments are missing;
- the freshness policy or required timestamps are missing;
- the risk assessment is missing;
- any dimension evidence state is not `AVAILABLE`;
- any dimension rating, evidence reference, rationale, assessor, or timestamp is missing;
- any required input remains `null`, `UNKNOWN`, `UNCONFIRMED`, or `PENDING`;
- the calculation rule cannot be applied exactly as versioned.

The deterministic output is:

```text
overall_status=NOT_COMPUTABLE
score_value=null
match_eligible=false
review_required=true
action_lock=true
```

Reason codes and missing-input paths are required. Unknown state must not be
discarded or converted into a negative numeric score.

## Calculation Rule

The draft diagnostic calculation is permitted only when:

- no verified hard blocker exists;
- every required input passes its gate;
- all five dimension evidence states are `AVAILABLE`;
- every dimension has an integer rating in `[0, 4]` with complete audit fields.

Let the five ratings be `r_i` and every weight be `w_i = 0.20`.

```text
weighted_mean = sum(w_i * r_i) for all five dimensions
diagnostic_score = 25 * weighted_mean
```

Because ratings are integers and weights are equal, an equivalent audit check
is:

```text
diagnostic_score = 5 * sum(r_i)
```

The only numeric output status allowed by this unvalidated v0.1 proposal is:

```text
overall_status=COMPUTED_UNCALIBRATED
score_value=<integer from 5 through 100 in increments of 5>
match_eligible=false
review_required=true
action_lock=true
```

The two formulas must produce identical results. Any mismatch produces
`NOT_COMPUTABLE` with reason code `FORMULA_INTEGRITY_FAILURE`.

Weights are treated as the exact versioned decimal vector
`[0.20, 0.20, 0.20, 0.20, 0.20]`, not as mutable runtime configuration. Any
weight drift produces `NOT_COMPUTABLE` with reason code
`WEIGHT_VECTOR_MISMATCH`.

The raw formula has a mathematical range of 0 through 100. A computed value of
0 is not emitted in v0.1 because risk rating `0` triggers `BLOCKED` before the
calculation and makes `score_value` null.

## No Threshold, Ranking, or Eligibility Rule

v0.1 defines no evidence-backed threshold or score band. Until calibration and
validation are complete, downstream systems must not:

- rank opportunities by `diagnostic_score`;
- label a score high, medium, low, passing, or failing;
- derive match eligibility or priority;
- infer customer intent, demand, or commercial value;
- trigger outreach, execution, spending, deployment, or any external action.

`match_eligible` therefore remains `false` for every v0.1 output state.

## Pre-Calculation Compatibility Boundary

An Opportunity Object may already contain scaffold fields such as
`assessment_status`, `status`, `dimension_statuses`, and `reason_codes` before
v0.1 is referenced. These are preserved object facts:

- `dimension_statuses` records requested assessment state; it is not an alias
  for the model's evidence-bearing `dimension_results`;
- pre-existing `reason_codes` explain the object's scaffold state; they are not
  claimed to be v0.1 evaluation findings;
- adding an `UNVERIFIED` reference does not create `missing_inputs`,
  `dimension_results`, assessor records, or hard-gate findings;
- no existing scaffold field may be renamed, expanded, or reinterpreted merely
  because a model path was attached.

When a future process actually applies v0.1, it emits an attributable linked
result with `reference_status: APPLIED` that conforms to the Evaluation Result
Contract below. The linked result must not silently rewrite the source
Opportunity Object.

## Evaluation Result Contract

This contract applies only after a scoring process sets
`reference_status: APPLIED` and actually executes the v0.1 gates or formula. A
reference-only attachment with `reference_status: UNVERIFIED` is not an
evaluation result and must not fabricate `dimension_results`, `missing_inputs`,
assessor records, or hard-gate findings.

```yaml
model_reference: docs/matching-score-v0.1.md
reference_status: APPLIED
model_version: null | 0.1.0-draft
overall_status: NOT_COMPUTABLE | BLOCKED | COMPUTED_UNCALIBRATED
score_value: null | integer
dimension_results:
  capability_fit:
    evidence_status: PENDING | MISSING | INVALID | STALE | AVAILABLE
    rating: null | integer
    evidence_refs: []
    rationale: null
    assessor_ref: null
    assessed_at: null
    hard_gate: false
    hard_gate_reason_code: null
  evidence_quality: {}
  constraint_fit: {}
  freshness: {}
  risk: {}
hard_blockers: []
missing_inputs: []
reason_codes: []
match_eligible: false
review_required: true
action_lock: true
```

The abbreviated dimension entries inherit the same fields as
`capability_fit`; they are not empty permissible records.

Each non-empty `hard_blockers` item requires:

```yaml
source_type: INPUT | DIMENSION
source_id: <input path or dimension ID>
reason_code: <non-empty versioned reason code>
evidence_refs:
  - <attributable evidence reference>
```

## Reference Status Semantics

| Status | Meaning | Numeric score allowed |
| --- | --- | --- |
| `UNVERIFIED` | Model path is attached for future assessment; rules were not applied | no |
| `APPLIED` | v0.1 gates or formula were executed; `overall_status` determines whether a value exists | only for `COMPUTED_UNCALIBRATED` |

No other reference status is valid in v0.1. `UNVERIFIED` is the explicit
pre-computation attachment state and emits no Evaluation Result Contract.
`APPLIED` may produce `NOT_COMPUTABLE`, `BLOCKED`, or
`COMPUTED_UNCALIBRATED`; only the last state may contain a numeric value.

## Output Validation Invariants

An output is invalid unless all of the following invariants hold:

- if `risk.rating == 0`, then `risk.hard_gate == true`,
  `risk.hard_gate_reason_code` is non-null, `overall_status == BLOCKED`,
  `score_value == null`, and the risk blocker appears in `hard_blockers`;
- if any verified hard gate is true, then `overall_status == BLOCKED` and
  `score_value == null`;
- if `overall_status` is `NOT_COMPUTABLE` or `BLOCKED`, then
  `score_value == null`;
- if `overall_status == COMPUTED_UNCALIBRATED`, then all dimension evidence
  states are `AVAILABLE`, all ratings and audit fields are present, no hard
  blocker exists, both formula forms agree, and
  `reference_status == APPLIED`;
- `match_eligible == false`, `review_required == true`, and
  `action_lock == true` in every v0.1 state.

Any invariant failure invalidates the output and must be surfaced with a reason
code. An invalid output must not be repaired by defaulting missing fields.

## Pending Model Reference Rule

A `NOT_COMPUTABLE` object may add:

```yaml
model_reference: docs/matching-score-v0.1.md
reference_status: UNVERIFIED
```

This reference records a candidate evaluation contract only. It does not mean
that the model was applied. While `reference_status` is `UNVERIFIED`:

- `method` remains `NOT_DEFINED`;
- `model_version` remains `null`;
- all dimension statuses remain `PENDING` unless separately assessed;
- `score_value` remains `null`;
- `match_eligible` remains `false`;
- no fact, evidence, status, or authorization may change because of the reference.

Because no evaluation occurred, a reference-only attachment must not add
Evaluation Result Contract fields merely to make the object look complete.
Those fields are created only by a later, attributable application attempt.
The object's existing `status: NOT_COMPUTABLE`, `dimension_statuses`, and
`reason_codes` remain pre-v0.1 scaffold facts and are not represented as a
model-generated result.

## Current Example Disposition

`examples/opportunities/example-github-agent-evidence.yaml` is
`NOT_COMPUTABLE` under v0.1 because its object validation is not complete,
TITMAS alignment is pending, required linked assessments do not exist, and all
five dimension statuses are pending. Adding an unverified model reference is
permitted; calculating a score is not.

## Truth Boundary

```text
MATCHING_SCORE_V0_1_DRAFT_RULES_DOCUMENTED=true
MATCHING_SCORE_V0_1_IMPLEMENTED=false
MATCHING_SCORE_V0_1_CALIBRATED=false
MATCHING_SCORE_V0_1_VALIDATED=false
MATCHING_SCORE_V0_1_THRESHOLD_DEFINED=false
MATCHING_SCORE_V0_1_RANKING_AUTHORIZED=false
MATCHING_SCORE_V0_1_ELIGIBILITY_AUTHORIZED=false
MATCHING_SCORE_V0_1_AUTOMATIC_ACTION_AUTHORIZED=false
MATCHING_SCORE_V0_1_PRODUCT_READY=false
```

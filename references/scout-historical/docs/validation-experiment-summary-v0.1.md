---
artifact_type: TITMAS_SCOUT_VALIDATION_EXPERIMENT_SUMMARY
summary_version: "0.1"
experiment_id: TITMAS-SCOUT-VALIDATION-EXPERIMENT-001
status: COMPLETED_RESEARCH_SUMMARY
classification: RESEARCH_ONLY_NON_AUTHORIZING
ruleset_version: TITMAS-SCOUT-VALIDATOR-PROTOTYPE-STRUCTURAL-SUBSET-V0.1
comparison_type: INPUT_STRUCTURE_EVOLUTION_NOT_CONTROLLED_EXPERIMENT
baseline_commit: a2a45869b22802ff446bf0ec65c9b8e54286a2ec
stage_1_status: INVALID
stage_2_status: VALID_SYNTHETIC_FIXTURE_ONLY
authorization_granted_in_all_stages: false
external_action_allowed_in_all_stages: false
truth_boundary:
  structural_validation_demonstrated_within_named_subset: true
  fail_closed_behavior_demonstrated_for_observed_missing_dependencies: true
  lifecycle_rule_execution_demonstrated_within_named_subset: true
  full_validation_model_conformance_demonstrated: false
  real_human_approval_present: false
  real_authorization_demonstrated: false
  real_action_executed: false
  production_safety_demonstrated: false
  commercial_value_demonstrated: false
  production_ready: false
---

# TITMAS Scout Validation Experiment Summary v0.1

> **Research-only evidence boundary.** Stage 2 is a synthetic fixture with a
> HUMAN-shaped Approval and insufficient Outcome Evidence. Its `VALID` result
> means only structural conformance to the named prototype subset. It does not
> establish authorization, action permission, production safety, or commercial
> value.

## Research Question

Can the TITMAS Scout Validator Prototype execute a bounded, deterministic set
of structural and lifecycle rules across incomplete and structurally complete
inputs while remaining fail-closed and non-authorizing?

This question is limited to
`TITMAS-SCOUT-VALIDATOR-PROTOTYPE-STRUCTURAL-SUBSET-V0.1`. It does not ask
whether the full Validation Model is implemented or whether a structurally
valid record is trustworthy in the real world.

## Experimental Setup

The experiment consists of two recorded local executions of the same named
Validator ruleset. Both runs are offline, use caller-supplied unattested UTC
timestamps, serialize deterministic JSON results, and prohibit authorization
and external action. These setup observations are bound by `OBS-SETUP-001`.

Stage 1 uses a plain example Opportunity derived from a real public GitHub
signal. The Validator normalizes it to the post-action profile without
inventing missing dependencies.

Stage 2 uses a newly created synthetic `POST_ACTION_CHAIN` envelope containing
five object shapes:

```text
Opportunity
  -> Matching Assessment
  -> Approval
  -> Action
  -> Outcome Evidence
```

The runs are an input-structure evolution demonstration, not a controlled
experiment. Stage 2 changes multiple fields and objects simultaneously, so the
status difference cannot be attributed to one isolated variable.

### Fixed Conditions

- ruleset version:
  `TITMAS-SCOUT-VALIDATOR-PROTOTYPE-STRUCTURAL-SUBSET-V0.1`;
- local Ruby runtime family: Ruby 2.6.10;
- output contract: deterministic JSON Validation Result;
- authorization invariant: `authorization_granted=false`;
- action invariant: `external_action_allowed=false`;
- no Validator network client, GitHub API call, or external action.

### Changed Conditions

- input form changes from a plain Opportunity to an explicit envelope;
- Matching Assessment and Approval change from absent to synthetic shapes;
- Action and Outcome Evidence change from dependency-gated absence to
  synthetic post-action shapes;
- cross-object lineage and nominal timestamp relationships are supplied in
  Stage 2.

## Stage 1 Result

Stage 1 returned exit code `1` and `validation_status=INVALID`
(`OBS-STAGE1-001`, `OBS-STAGE1-002`).

```text
failed_rule=TVP-AUT-001:APPROVAL_MISSING
failed_rule=TVP-LIF-003:MATCHING_ASSESSMENT_MISSING
authorization_granted=false
external_action_allowed=false
```

The observed fail-closed behavior is specific: the Validator did not infer an
Approval or Matching Assessment and did not authorize dependent action. The
result does not assess the importance, current relevance, product fit, or
commercial value of the referenced GitHub issue.

## Stage 2 Result

Stage 2 returned exit code `0`, and the stored Validator field is
`validation_status=VALID` (`OBS-STAGE2-001`, `OBS-STAGE2-002`). This summary
classifies that observation as `VALID_SYNTHETIC_FIXTURE_ONLY`.

```text
failed_rules=[]
authorization_granted=false
external_action_allowed=false
```

The synthetic envelope supplied all shapes and relationships required by the
implemented prototype predicates. The permission state did not change.

`VALID` must be read with both labels:

```text
SYNTHETIC_FIXTURE_ONLY=true
SEMANTIC_SPOOFING_EXPOSED=true
```

## Validation Difference

| Observation | Stage 1 | Stage 2 |
| --- | --- | --- |
| Input | Plain Opportunity | Five-object envelope |
| Assessment | Missing | Synthetic shape |
| Approval | Missing | Synthetic HUMAN shape |
| Action | Dependency-gated | Cancelled synthetic no-op |
| Evidence | Dependency-gated | Insufficient synthetic record |
| Result | `INVALID` | Synthetic structural `VALID` |
| Authorization | `false` | `false` |
| External action | `false` | `false` |

The transition demonstrates that the implemented rules distinguish an input
with missing required dependencies from an input carrying the required
structural shapes and nominal relationships. It does not establish a causal
effect for any single changed field.

## What is demonstrated

### Structural Validation

`INF-STRUCT-001` — Within the named prototype subset, the Validator can parse
the two input forms, inspect required object shapes and references, aggregate
rule outcomes, and emit deterministic structured results.

### Fail-Closed Behavior

`INF-FAIL-CLOSED-001` — For the observed Stage 1 case, missing Approval and
Matching Assessment dependencies produce `INVALID`, while authorization and
external action remain `false`.

This is evidence of fail-closed behavior for the tested missing-dependency
conditions. It is not evidence that every unknown production failure mode has
been covered.

### Lifecycle Rule Execution

`INF-LIFECYCLE-001` — The Validator executes its named lifecycle subset across
the Opportunity, Matching Assessment, Approval, Action, and Outcome Evidence
shapes. Stage 2 exercises cross-object lineage and nominal time ordering that
Stage 1 cannot reach because required dependencies are absent.

## Exposed Prototype Gaps

### HUMAN Shape Without a Real Human

`INF-GAP-SEMANTIC-001` — Stage 2 declares `reviewer_type: HUMAN`, but its
identifiers explicitly state that no real reviewer identity, authority,
attestation, or decision exists. The synthetic structural result is still
`VALID`.

This exposes a semantic-spoofing gap: enum and reference-shape checks do not
verify that a human approved anything.

### Insufficient Evidence Still Produces Structural VALID

`INF-GAP-STATE-001` — Stage 2 declares
`evidence_status: INSUFFICIENT_EVIDENCE` and has no ground-truth source. The
synthetic structural result is still `VALID`.

This exposes a state-awareness gap: the prototype checks selected evidence
shape and ordering but does not establish evidence sufficiency or truth.

### Supporting References Are Not Resolved

`INF-GAP-REFERENCE-001` — Action request, policy, reviewer, executor, receipt,
time, and subject references do not have resolved supporting object bytes.
Their existence, semantics, and integrity are not verified by the Validator.

## What is not demonstrated

### Real Authorization

No real human decision, verified reviewer identity, authority, attestation,
policy decision, scope enforcement, or point-of-effect revalidation exists.
Validation does not create authorization.

### Production Safety

The experiment does not demonstrate formal schema coverage, full Validation
Model conformance, cryptographic integrity, trusted time, replay protection,
admissible evidence, real action effects, operational hardening, or production
safety.

### Commercial Value

The public signal is not a verified customer record. The experiment does not
validate current demand, product fit, willingness to pay, market size,
competitive advantage, or commercial value.

### Additional Non-Claims

- no real Action or material effect was executed;
- no production-grade receipt was issued or verified;
- no external source was resolved during validation;
- no general claim is made beyond the named prototype subset;
- no causal claim is made from the non-controlled Stage comparison.

## Inference Boundary

```yaml
inference_boundary:
  structural_valid_implies_real_authorization: false
  structural_valid_implies_external_action_allowed: false
  structural_valid_implies_real_human_approval: false
  structural_valid_implies_evidence_sufficiency: false
  structural_valid_implies_production_safety: false
  structural_valid_implies_commercial_value: false
  authorization_granted: false
  external_action_allowed: false
```

No score, Approval-shaped fixture, empty failure list, or human-readable
summary can override this boundary.

## Source Artifact Registry

The following registry binds every observation used by this summary to local
bytes. SHA-256 values are lowercase hexadecimal digests of the named files.

```yaml
source_artifacts:
  - artifact_id: ART-VALIDATOR-README
    path: src/validator/README.md
    sha256: 7ee417f9b632f29b26578b1ee18019a76497acd87c61fa6f0f39812c5a4f0a55
  - artifact_id: ART-STAGE1-INPUT
    path: examples/opportunities/example-github-agent-evidence.yaml
    sha256: a1dc96155713f2ac102da4208152d463f2bb40b8681802354f9f2406834c88df
  - artifact_id: ART-STAGE1-MANIFEST
    path: examples/validation-runs/2026-08-01-github-agent-hitl-issue-636/run-manifest.yaml
    sha256: de7a29f15c3212a4c16d5a6ea4aa2a31be8e8d276fa8a101fb4b2aba5a999bdc
  - artifact_id: ART-STAGE1-RESULT
    path: examples/validation-runs/2026-08-01-github-agent-hitl-issue-636/validation-result.json
    sha256: ac2a594c4a30c92619ec987dddde02a7bcc22feaef3bfa55cec5eddb0783e8f7
  - artifact_id: ART-STAGE1-RECEIPT
    path: examples/validation-runs/2026-08-01-github-agent-hitl-issue-636/execution-receipt.yaml
    sha256: 270db20370b26bfff9de240e1d8d8d1610aae026d2bad8d2cb67079e6d97528a
  - artifact_id: ART-STAGE2-INPUT
    path: examples/validation-runs/2026-08-01-github-agent-hitl-issue-636-stage-2-structural-subset/lifecycle-input.yaml
    sha256: 6f97f958eea94274082191abfcd31dc78ad2a78cd876762055954b7b53f15ee0
  - artifact_id: ART-STAGE2-MANIFEST
    path: examples/validation-runs/2026-08-01-github-agent-hitl-issue-636-stage-2-structural-subset/run-manifest.yaml
    sha256: 2d85248a4aa5c38c43ed8a085d984bf696bc48e257ddb510f254e583b9f98165
  - artifact_id: ART-STAGE2-RESULT
    path: examples/validation-runs/2026-08-01-github-agent-hitl-issue-636-stage-2-structural-subset/validation-result.json
    sha256: 7d3138b6ae459843df8645d9798e014d822a2bb4c51d0c63ee6a270e5d1fa0a2
  - artifact_id: ART-STAGE2-RECEIPT
    path: examples/validation-runs/2026-08-01-github-agent-hitl-issue-636-stage-2-structural-subset/execution-receipt.yaml
    sha256: fd87c55f9b4bca75b84a56fbadbd2bdabd567e99b4dafc66ade12b32c6e4dea0
  - artifact_id: ART-STAGE2-TRANSITION
    path: examples/validation-runs/2026-08-01-github-agent-hitl-issue-636-stage-2-structural-subset/transition-report.md
    sha256: d02e3125ce522f07690540a19cb375ce187882a9fb02afa3a2b25559243e67a7
```

## Claim Registry

Observations report artifact contents. Inferences are bounded interpretations
derived from those observations.

```yaml
claims:
  - claim_id: OBS-SETUP-001
    layer: OBSERVATION
    statement: Both runs use the same ruleset and remain offline and non-authorizing.
    source_artifacts:
      - ART-VALIDATOR-README
      - ART-STAGE1-MANIFEST
      - ART-STAGE1-RECEIPT
      - ART-STAGE2-MANIFEST
      - ART-STAGE2-RECEIPT
  - claim_id: OBS-STAGE1-001
    layer: OBSERVATION
    statement: Stage 1 returned INVALID with two missing-dependency failures.
    source_artifacts:
      - ART-STAGE1-RESULT
      - ART-STAGE1-RECEIPT
  - claim_id: OBS-STAGE1-002
    layer: OBSERVATION
    statement: Stage 1 kept both permission booleans false.
    source_artifacts:
      - ART-STAGE1-RESULT
  - claim_id: OBS-STAGE2-001
    layer: OBSERVATION
    statement: Stage 2 returned VALID with an empty failed_rules array.
    labels:
      - SYNTHETIC_FIXTURE_ONLY
      - SEMANTIC_SPOOFING_EXPOSED
    source_artifacts:
      - ART-STAGE2-RESULT
      - ART-STAGE2-RECEIPT
  - claim_id: OBS-STAGE2-002
    layer: OBSERVATION
    statement: Stage 2 kept both permission booleans false.
    source_artifacts:
      - ART-STAGE2-RESULT
  - claim_id: OBS-STAGE2-003
    layer: OBSERVATION
    statement: Stage 2 uses synthetic objects and insufficient evidence.
    source_artifacts:
      - ART-STAGE2-INPUT
      - ART-STAGE2-MANIFEST
      - ART-STAGE2-TRANSITION
  - claim_id: OBS-STAGE2-004
    layer: OBSERVATION
    statement: Stage 2 supporting reference objects are not resolved.
    source_artifacts:
      - ART-STAGE2-MANIFEST
      - ART-STAGE2-TRANSITION
  - claim_id: INF-STRUCT-001
    layer: INFERENCE
    statement: The named prototype subset executes structural validation.
    derived_from:
      - OBS-STAGE1-001
      - OBS-STAGE2-001
  - claim_id: INF-FAIL-CLOSED-001
    layer: INFERENCE
    statement: The tested missing dependencies fail closed without permission.
    derived_from:
      - OBS-STAGE1-001
      - OBS-STAGE1-002
  - claim_id: INF-LIFECYCLE-001
    layer: INFERENCE
    statement: The named lifecycle subset is machine-executable for the fixture.
    derived_from:
      - OBS-STAGE2-001
      - OBS-STAGE2-003
  - claim_id: INF-GAP-001
    layer: INFERENCE
    statement: Synthetic structural VALID does not establish semantic trust.
    derived_from:
      - OBS-STAGE2-001
      - OBS-STAGE2-003
  - claim_id: INF-GAP-SEMANTIC-001
    layer: INFERENCE
    statement: HUMAN-shaped data passing exposes a semantic-spoofing gap.
    derived_from:
      - OBS-STAGE2-001
      - OBS-STAGE2-003
  - claim_id: INF-GAP-STATE-001
    layer: INFERENCE
    statement: Insufficient evidence passing exposes a state-awareness gap.
    derived_from:
      - OBS-STAGE2-001
      - OBS-STAGE2-003
  - claim_id: INF-GAP-REFERENCE-001
    layer: INFERENCE
    statement: Unresolved supporting objects remain an integrity gap.
    derived_from:
      - OBS-STAGE2-004
```

## Reproduction

The immutable comparison baseline is commit
`a2a45869b22802ff446bf0ec65c9b8e54286a2ec`. From a descendant checkout,
first confirm that experiment inputs and Validator sources are unchanged:

```bash
baseline=a2a45869b22802ff446bf0ec65c9b8e54286a2ec
git diff --exit-code "$baseline" -- \
  src/validator \
  examples/opportunities/example-github-agent-evidence.yaml \
  examples/validation-runs
```

Replay Stage 1:

```bash
stage1=examples/validation-runs/2026-08-01-github-agent-hitl-issue-636
diff -u "$stage1/validation-result.json" \
  <(ruby src/validator/validate.rb \
    --timestamp 2026-08-01T08:41:24Z \
    examples/opportunities/example-github-agent-evidence.yaml)
```

Replay Stage 2:

```bash
stage2=examples/validation-runs/2026-08-01-github-agent-hitl-issue-636-stage-2-structural-subset
diff -u "$stage2/validation-result.json" \
  <(ruby src/validator/validate.rb \
    --timestamp 2026-08-01T09:11:04Z \
    "$stage2/lifecycle-input.yaml")
```

An empty `diff` is byte-level agreement with the stored result. Replay verifies
local determinism for the named bytes and timestamp; it does not provide
trusted time, cryptographic attestation, or independent execution assurance.

## Research Maturity

```text
MATURITY=EXECUTABLE_STRUCTURAL_RESEARCH_PROTOTYPE
REPRODUCIBLE_RECORDED_RUNS=2
FULL_VALIDATION_MODEL_CONFORMANCE=false
REAL_AUTHORIZATION_ASSURANCE=false
PRODUCTION_SAFETY_ASSURANCE=false
COMMERCIAL_VALUE_EVIDENCE=false
```

The current maturity is sufficient for reproducible structural-validator
research and governance-boundary review. It is not sufficient for production
authorization, operational deployment, or commercial claims.

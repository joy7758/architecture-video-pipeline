---
artifact_type: TITMAS_SCOUT_STAGE_2_TRANSITION_REPORT_V0_1
classification: SYNTHETIC_RESEARCH_FIXTURE_ONLY
stage_1_status: INVALID
stage_2_status: VALID
authorization_granted: false
external_action_allowed: false
---

# Stage 1 to Stage 2 Structural Transition

## Scope

This report compares two executions of the same Validator Prototype against
records derived from the same real public GitHub signal.

- Stage 1 used a plain example Opportunity and failed closed.
- Stage 2 uses a synthetic five-object `POST_ACTION_CHAIN` envelope.
- Stage 2 demonstrates structural subset conformance only.
- No downstream Stage 2 object represents a real human decision, policy
  evaluation, execution, receipt, or ground-truth observation.

## Immutable Stage 1 Baseline

```text
path=examples/validation-runs/2026-08-01-github-agent-hitl-issue-636
git_commit=8f42d75fa57ee3203b53c08151bef9d968c5ec33
git_tree=cfd2826b4c558c3ae3d63c31b4e5a52defb9d9fc
manifest_sha256=de7a29f15c3212a4c16d5a6ea4aa2a31be8e8d276fa8a101fb4b2aba5a999bdc
result_sha256=ac2a594c4a30c92619ec987dddde02a7bcc22feaef3bfa55cec5eddb0783e8f7
```

Stage 2 does not supersede, rewrite, or repair Stage 1. The earlier `INVALID`
result remains the correct result for its exact input bytes.

## Status Change

| Condition | Stage 1 | Stage 2 |
| --- | --- | --- |
| Input | Plain Opportunity | `POST_ACTION_CHAIN` envelope |
| Assessment | Missing | Synthetic and uncalibrated |
| Approval | Missing | HUMAN-shaped synthetic record |
| Action | Dependency-gated | `COMPLETED` / `CANCELLED` no-op |
| Outcome Evidence | Dependency-gated | Synthetic and insufficient |
| Failed rules | Two | None |
| Authorization | `false` | `false` |
| External action | `false` | `false` |

Structural effects:

- the explicit profile shape is present;
- `MATCHING_ASSESSMENT_MISSING` ceases to fail;
- `APPROVAL_MISSING` ceases to fail;
- Action lifecycle fields are present and ordered;
- the required Outcome Evidence reference shape is present;
- the prototype aggregator emits `VALID`;
- neither permission state changes.

Stage 2 does not prove that every `checked_rule_id` has full source-model
semantics. An empty `failed_rules` array means only that the implemented
prototype predicates emitted no failure.

## Added Structural Conditions

1. The profile is explicitly `POST_ACTION_CHAIN`.
2. All five embedded object shapes are present.
3. Opportunity lineage identifiers, types, versions, and declared digests
   match across the embedded references.
4. The Matching Assessment is `APPLIED` and `COMPUTED_UNCALIBRATED`.
5. The Approval declaration is `APPROVED` and its nominal interval contains
   the synthetic Action timestamps and evaluation time.
6. The Action is `COMPLETED`, terminal `CANCELLED`, and has a synthetic receipt
   reference.
7. Outcome Evidence references the synthetic Action, receipt, Opportunity, and
   source-evidence shapes after the Action's nominal completion time.

## Exposed Prototype Gaps

### HUMAN-Shaped Synthetic Approval

The input declares `reviewer_type: HUMAN` because that is the prototype's
closed enum, while every reviewer reference explicitly says that no real human
identity, authority, or attestation exists. The Validator still emits `VALID`.

This is a semantic-spoofing gap in the research prototype. It shows that enum
and reference-shape checks do not verify a human reviewer or create a genuine
Approval.

### Insufficient Evidence Still Produces Structural VALID

Outcome Evidence declares:

```text
evidence_status=INSUFFICIENT_EVIDENCE
ground_truth_source=null
reason_code=NO_GROUND_TRUTH_SOURCE
```

The Validator still emits `VALID`. This is a state-awareness and evidence-
sufficiency gap. The current subset checks post-action reference shape and
ordering, but it does not require admissible ground truth for structural
`VALID`.

### Supporting References Are Not Resolved

Action request, policy, reviewer, executor, time, receipt, and subject
references use synthetic fixture values. Their object bytes are absent. The
Validator checks registered type and digest syntax but does not resolve or
verify those dependencies.

### CANCELLED No-Op Does Not Test Effects

The synthetic Action is terminal `CANCELLED` and explicitly records no real
execution or material effect. This is appropriate for a safe fixture, but it
does not test execution, rollback, side effects, or outcome truth.

## Conditions That Still Block Real Action

- no attributable real human decision or reviewer identity;
- no verified reviewer authority or detached attestation;
- no real action request, policy decision, scope, constraint, or executor;
- no usage-limit ledger, replay protection, or point-of-effect revalidation;
- no real Action, material effect, receipt bytes, or receipt signature;
- no admissible ground-truth source or sufficient outcome evidence;
- no formal schemas, full ruleset registry, or full Validation Model run;
- no URI resolution or supporting-object retrieval;
- no Validator-side digest recomputation or cryptographic verification;
- no trusted time source or signed immutable result storage;
- no verified customer demand, current unresolved need, or TITMAS fit.

These blockers are non-compensatory. The Stage 2 `VALID` result cannot waive
them and cannot authorize any action.

## Result Invariant

```text
STRUCTURAL_SUBSET_STATUS=VALID
REAL_HUMAN_APPROVAL_PRESENT=false
EVIDENCE_SUFFICIENT=false
REAL_ACTION_EXECUTED=false
AUTHORIZATION_GRANTED=false
EXTERNAL_ACTION_ALLOWED=false
PRODUCTION_READY=false
```

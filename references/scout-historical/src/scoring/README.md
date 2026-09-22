---
module_id: titmas-scout-scoring
status: DESIGN_SCAFFOLD
implementation_available: false
formula_defined: false
calibration_available: false
---

# Scoring Module

## Purpose

Future home for evidence-linked opportunity matching under
`TITMAS-SCOUT-MATCH-V0`. The current directory contains no scoring algorithm,
weights, thresholds, calibration data, ranking implementation, or tests.

## Intended responsibility

```text
validated OpportunityObject plus declared matching context
-> per-dimension evidence evaluation
-> reason-preserving score result or NOT_COMPUTABLE
```

Candidate dimensions and fail-closed rules are described in
`docs/03_matching_score_model.md`.

## Missing-score rule

Absence of scoring logic must not default to numeric zero. Until a formula and
calibration protocol are defined, the only valid scaffold result is:

```text
score_status=NOT_COMPUTABLE
score_value=null
match_eligible=false
reason_code=SCORING_MODEL_UNAVAILABLE
```

`null` is a serialization placeholder for no numeric result; it is not a score
and must not participate in ranking.

## Truth boundary

```text
SCORING_MODULE_SCAFFOLDED=true
MATCHING_SCORE_FORMULA_DEFINED=false
MATCHING_SCORE_IMPLEMENTED=false
MATCHING_SCORE_CALIBRATED=false
MATCHING_SCORE_VALIDATED=false
```

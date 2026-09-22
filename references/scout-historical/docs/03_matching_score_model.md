---
artifact_id: titmas-matching-score-model
title: TITMAS Matching Score Model
status: DRAFT_SCAFFOLD
version: 0.1.0-draft
normative: false
---

# TITMAS Matching Score Model

## Purpose

Define the review surface for a future evidence-linked matching score. No
formula, weight, threshold, calibration result, or production ranking is
defined by this scaffold.

## Candidate dimensions

| Dimension | Question | Current status |
| --- | --- | --- |
| capability fit | Does the candidate capability address the bounded need? | UNDEFINED |
| evidence quality | Is the supporting evidence attributable and reviewable? | UNDEFINED |
| constraint fit | Are declared policy, cost, time, and compatibility limits met? | UNDEFINED |
| freshness | Is the evidence current for the declared observation window? | UNDEFINED |
| risk | Which unresolved conditions require rejection, agent review, or human-exception review? | UNDEFINED |

## Fail-closed rules

- Unknown evidence must not be converted into a positive match.
- A score must retain per-dimension reasons and evidence references.
- Ranking must not be treated as authorization, customer intent, or outreach consent.
- Scoring never authorizes action; the current governance decision requires a
  separate Agent Review Quorum or, for exception actions, human review.

When required evidence is missing, the deterministic default is:

```text
score_status=NOT_COMPUTABLE
match_eligible=false
review_required=true
reason_code=INSUFFICIENT_EVIDENCE
```

`NOT_COMPUTABLE` is not a numeric zero. No numeric default is valid until a
formula and calibration protocol are explicitly defined.

## Truth boundary

```text
MATCHING_SCORE_FORMULA_DEFINED=false
MATCHING_SCORE_CALIBRATED=false
MATCHING_SCORE_VALIDATED=false
AUTOMATED_RECOMMENDATION_AUTHORIZED=false
```

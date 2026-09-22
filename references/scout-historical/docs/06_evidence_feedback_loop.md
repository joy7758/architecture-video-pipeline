---
artifact_id: titmas-scout-evidence-feedback-loop
contract_id: TITMAS-SCOUT-FEEDBACK-V0
title: TITMAS Scout Evidence Feedback Loop
status: DRAFT_SCAFFOLD
version: 0.1.0-draft
normative: false
---

# TITMAS Scout Evidence Feedback Loop

## Purpose

Define how future observed outcomes may become evidence candidates for
revalidation. Feedback does not silently rewrite source observations,
OpportunityObjects, scores, policies, or prior decisions.

## Candidate feedback record

| Field | Intended meaning | Current definition |
| --- | --- | --- |
| `feedback_id` | Stable feedback identifier and version | UNDEFINED |
| `signal_type` | Outcome, correction, rejection, expiry, drift, or other signal | UNDEFINED |
| `observed_at` | Time represented by the signal | UNDEFINED |
| `source_evidence_ref` | Attributable reference for the observed signal | UNDEFINED |
| `ground_truth_source` | Declared basis for treating a signal as ground truth | UNDEFINED |
| `subject_refs` | Linked opportunity, score, policy, action, and evidence records | UNDEFINED |
| `drift_policy_id` | Versioned rule for material drift | UNDEFINED |
| `revalidation_trigger` | Condition requesting bounded re-evaluation | UNDEFINED |

## Fail-closed feedback handling

```text
if source_evidence_or_ground_truth_missing:
  feedback_status=INSUFFICIENT_EVIDENCE
  score_update_allowed=false
if drift_policy_missing:
  drift_status=NOT_COMPUTABLE
  revalidation_required=true
if subject_linkage_missing:
  feedback_status=UNLINKED
  automatic_update_allowed=false
```

Unknown or rejected feedback must be retained with its reason code rather than
silently discarded. `NOT_COMPUTABLE` is not numeric zero, and no feedback may
retroactively alter an audit record.

## Truth boundary

```text
FEEDBACK_RECORD_SCAFFOLD_DEFINED=true
FEEDBACK_SCHEMA_DEFINED=false
GROUND_TRUTH_POLICY_DEFINED=false
DRIFT_THRESHOLD_DEFINED=false
FEEDBACK_PROCESSOR_IMPLEMENTED=false
FEEDBACK_LOOP_VALIDATED=false
AUTOMATIC_MODEL_UPDATE_AUTHORIZED=false
```

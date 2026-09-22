---
module_id: titmas-scout-manual-review
status: DESIGN_SCAFFOLD
implementation_available: false
review_contract_defined: false
authorization_enabled: false
---

# Manual Review Module

## Purpose

Future home for recording human-exception review evidence for legal, payment,
binding identity, restricted-data, deletion, account-security, and protected
branch merge actions. Ordinary open-source actions use Agent Review Quorum by
default. Manual review is not itself execution permission.

## Candidate review record

| Field | Intended meaning | Current definition |
| --- | --- | --- |
| `review_id` | Stable review record identifier | UNDEFINED |
| `subject_refs` | Opportunity, score, source, and policy references | UNDEFINED |
| `reviewer_ref` | Evidence-bound reviewer identity | UNDEFINED |
| `reviewed_at` | Review timestamp | UNDEFINED |
| `observations` | Bounded reviewer findings | UNDEFINED |
| `evidence_refs` | Evidence supporting each finding | UNDEFINED |
| `review_status` | Draft, complete, or invalid review state | UNDEFINED |

## Fail-closed boundary

```text
default_review_status=NOT_REVIEWED
authorization_enabled=false
state_change_allowed=false
external_action_allowed=false
```

Missing reviewer identity, evidence, or subject linkage must produce an invalid
or incomplete review record. A recorded opinion cannot change opportunity,
score, policy, or action state until a separate, explicit authorization
contract exists.

## Truth boundary

```text
MANUAL_REVIEW_MODULE_SCAFFOLDED=true
MANUAL_REVIEW_CONTRACT_DEFINED=false
MANUAL_REVIEW_IMPLEMENTED=false
REVIEW_AUTHORITY_GRANTED=false
ACTION_AUTHORITY_GRANTED=false
```

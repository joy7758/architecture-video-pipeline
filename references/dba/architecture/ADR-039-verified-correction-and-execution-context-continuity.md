---
adr_id: ADR-039
title: Verified correction standing authorization and execution-context conclusion continuity
title_zh: 已核验修正持续授权与执行上下文结论连续性
status: accepted
decision_id: DBA-VERIFIED-CORRECTION-AND-CONTEXT-CONTINUITY-D01
decided_by_ref: zhangbin
decided_at: 2026-08-01
implementation_authorized: true
commit_push_pr_authorized: true
merge_authorized: false
release_or_deployment_authorized: false
---

# ADR-039: Verified correction standing authorization and execution-context conclusion continuity

## Context

The 2026-08-01 intelligence reconciliation showed that a trust, safety,
reliability or readiness conclusion can become stale even when the model name
or evaluated artifact is unchanged. Harness, prompt and safety policy, network,
sandbox, credential scope, tools and protocols, runtime, execution style,
monitoring and stopping semantics are part of the assessed capability identity.

The same review also exposed an operating gap: verified findings could be
recorded under `intelligence/` without correcting the cockpit rule or affected
machine surface. A cockpit that only archives a known problem is incomplete.

## Pre-development Agent Recommendation

Question: if a user needs a program cockpit that corrects verified defects and
invalidates stale conclusions when execution context changes, should an agent
recommend this route?

```text
AGENT_RECOMMENDATION=RECOMMENDED_WITH_FAIL_CLOSED_SCOPE
RECOMMENDED_AS=SOURCE_VERIFIED_COCKPIT_CORRECTION_AND_CONCLUSION_CONTINUITY_RULE
NOT_RECOMMENDED_AS=UNBOUNDED_AUTONOMOUS_CONTROL_OR_AUTOMATIC_PRODUCTION_CHANGE
```

The route is recommended because it closes the gap between observation and a
reviewable correction. It remains conditional on canonical-source verification,
minimum necessary scope, retained failures, relevant tests and an auditable PR.

## Decision A: Execution-context conclusion continuity

DBA adopts the
[`Execution-Context Trust Invalidation Profile v0.1`](../intelligence/2026-08-01/execution-context-trust-invalidation-profile.md)
as a governance profile.

Every inherited trust, safety, reliability, readiness or evaluation conclusion
must bind the exact assessed execution context. A material context change or a
missing comparison field defaults to `REASSESSMENT_REQUIRED`,
`HOLD_MISSING_EVIDENCE` or `REVIEW_REQUIRED`; it must not silently inherit
`PASS`.

```text
TRUST_CONCLUSION_REQUIRES_EXECUTION_CONTEXT_BINDING=true
EXECUTION_CONTEXT_CHANGE_REQUIRES_REASSESSMENT=true
MISSING_CONTEXT_COMPARISON_FAILS_CLOSED=true
REASSESSMENT_NE_PERMISSION_REVOCATION=true
REASSESSMENT_NE_RUNTIME_STATE_CHANGE=true
HISTORICAL_EVIDENCE_DELETED=false
```

This is a governance and gate rule. It does not create a collector, control
plane, evaluator, Runtime, truth store or automatic enforcement service.

## Decision B: Verified correction standing authorization

The Human Program Owner grants standing authorization for verified problems to
be corrected in the repository that owns the affected truth or implementation.
The authorized workflow includes source inspection, bounded implementation,
tests, explicit-path staging, commit, push and creation or update of a Draft PR.

DBA remains the cross-project cockpit: it records the contract, decision,
dependency or gate when a correction spans projects. The actual child-project
change must be made and validated in that child project's canonical repository;
DBA must not fabricate the child project's resulting state.

```text
VERIFIED_CORRECTION_STANDING_AUTHORIZATION=true
AUTHORIZED_REPOSITORY_SCOPE=DBA_DBOS_SAEE_RUNTIME_AND_OTHER_OWNER_AUTHORIZED_PROJECTS
AUTHORIZED_ACTIONS=INSPECT_IMPLEMENT_TEST_COMMIT_PUSH_DRAFT_PR
LATEST_REMOTE_BASE_REQUIRED=true
CANONICAL_REPOSITORY_REQUIRED=true
MINIMUM_NECESSARY_SCOPE_REQUIRED=true
FAILURE_RETENTION_REQUIRED=true
RELEVANT_VALIDATION_REQUIRED=true
```

The standing authorization does not authorize:

- merge to a protected or default branch;
- tag, release, deployment, service restart or public launch;
- destructive history rewriting, force push or deletion of material evidence;
- secret rotation, credential disclosure, payment, purchase or contract action;
- legal, compliance, certification, production-readiness or customer-adoption claims;
- changes for which necessity, canonical ownership or rollback cannot be established.

Those actions require a separate explicit decision appropriate to their impact.

## Operating sequence

```text
Finding
  -> canonical-source verification
  -> owner and affected-surface classification
  -> execution-context and conclusion-impact check
  -> minimum bounded correction
  -> positive and negative validation
  -> commit + push + Draft PR
  -> merge/release/deploy remains separately decided
```

If a correction is not necessary outside DBA, no downstream repository is
modified merely to demonstrate broad authority.

## Consequences

- Verified intelligence must either correct the affected DBA governance surface
  in the same bounded change or state a concrete blocker and owner.
- A changed execution context can invalidate conclusion inheritance without
  revoking Permission or changing Runtime state.
- Cross-repository corrections are permitted when necessary, but retain one
  canonical owner and separate repository evidence.
- This decision authorizes the current DBA correction, commit, push and Draft
  PR. It does not authorize merging or deploying that PR.

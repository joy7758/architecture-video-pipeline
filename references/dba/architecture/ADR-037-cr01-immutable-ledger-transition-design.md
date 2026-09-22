# ADR-037: CR-01 Immutable Ledger Transition Design

## Status

```text
decision_id=CR01-D02
status=ACCEPTED_DESIGN_ONLY
decided_by_ref=zhangbin
decided_at=2026-07-31T18:44:30+08:00
implementation_authorized=false
```

## Context

CR-01 restored 1,661 historical synthetic Receipts. All chain links are
continuous, but two signatures cannot be verified because the ephemeral
integration-test public key was never retained. The records cannot be repaired
without falsifying history.

## Decision

Hold CR-01 and design an immutable transition. The reviewed candidate is:

```text
OPTION_C=IMMUTABLE_EXCEPTION_MANIFEST_PLUS_TENANT_SCOPED_CLEAN_LEDGER_EPOCH
OPTION_C_STATUS=RECOMMENDED_NOT_AUTHORIZED
```

The historical ledger remains exact and read-only. A future signed transition
manifest may describe, but not validate, the two exceptions. Each Tenant may
start a clean epoch whose signed genesis binds the manifest digest and the
Tenant's legacy chain tip.

## Why not the alternatives

- quarantine-only cannot make the active verification contract unambiguous
  without skip logic or a validity override;
- an unanchored clean ledger loses audit continuity and risks a second truth
  source;
- deleting, rewriting, re-signing or allowlisting would hide the retained
  failure.

## Consequences

- CR-01 remains blocked and RTO remains unestablished;
- public reports continue to show `1659 valid / 2 unverifiable`;
- Gateway code, database migration, deployment and soak remain unauthorized;
- a new Human Decision, CR01-D03, is required before implementation;
- any future active-epoch PASS coexists with, and never replaces, the legacy
  `INCOMPLETE_KEY_UNAVAILABLE` result.

## Agent recommendation gate

Three separate `qwen3.7-max` role-scoped reviews selected Option C. One
returned `RECOMMENDED`; two returned `CONDITIONALLY_RECOMMENDED`. Their shared
blocker is explicit Human authorization plus a reviewed manifest, threat model,
restore protocol and rollback plan. Agent recommendation does not grant that
authority.

## Invariants

```text
LEGACY_RECORDS_DELETED=false
LEGACY_RECORDS_REWRITTEN=false
LEGACY_RECORDS_RESIGNED=false
LEGACY_FAILURE_ALLOWLISTED=false
LEGACY_ANCHOR_NE_LEGACY_VERIFICATION=true
QUARANTINE_NE_VALIDITY_OVERRIDE=true
ONE_ACTIVE_EPOCH_PER_TENANT=true
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_AUTHORIZATION=true
DECISION_NE_EXECUTION=true
```

## Next gate

```text
NEXT_HUMAN_DECISION=CR01-D03_AUTHORIZE_OR_REJECT_OPTION_C_IMPLEMENTATION_AND_CAP_EXCEPTION
SECOND_DEPLOYMENT_RETRY_AUTHORIZED=false
SOAK_EXECUTION_AUTHORIZED=false
```

---
adr_id: ADR-038
title: D04 final closure and adopt-before-build architecture
title_zh: D04 最终关闭与优先采用成熟上游架构
status: accepted
decision_id: TITMAS-D04-FINAL-CLOSURE-AND-ADOPTION-AUDIT-D01
decided_by_ref: zhangbin
decided_at: 2026-08-01
implementation_authorized: false
release_authorized: false
---

# ADR-038: D04 final closure and adopt-before-build architecture

## Context

CR01-D04 attempted three bounded internal clean-ledger canaries. All three
failed and are retained as failures:

1. `RESTORE_TOOL_ARGUMENT_CONTRACT_MISMATCH`;
2. `SIGNER_OWNERSHIP_CONTEXT_MISMATCH`;
3. `CLEAN_LEDGER_QUERY_ROUTING_GAP`.

The third attempt requested `titmas_cr01_internal.receipts`, while the runtime
query resolved to `titmas.receipts`; PostgreSQL returned `PERMISSION_DENIED`.
That result demonstrates fail-closed database permissions. It does not
demonstrate a working clean ledger.

PR [joy7758/titmas-sandbox-gateway#36](https://github.com/joy7758/titmas-sandbox-gateway/pull/36)
was verified on 2026-08-01 as `CLOSED`, draft, unmerged, with head
`3b8356d90b5eea3a0056e4672fdd7be077ec8177`.

## Decision

```text
D04_FINAL_STATUS=CLOSED_FAILED_RETAINED
D04_FINAL_RESULT=BLOCKED_FINAL_CANARY_FAILED
D04_CANARY_ATTEMPTS_TOTAL=3
D04_FURTHER_CANARY_RETRIES_AUTHORIZED=false
PR36_REOPEN_AUTHORIZED=false
PR36_MERGE_AUTHORIZED=false
PR36_CHERRY_PICK_AUTHORIZED=false
```

The legacy ledger is permanently classified as:

```text
LEGACY_LEDGER_CLASSIFICATION=INTERNAL_EXPERIMENTAL_LEDGER
LEGACY_LEDGER_WRITE_MODE=EXISTING_RUNTIME_ONLY
LEGACY_LEDGER_PRODUCTION_AUTHORITY=false
LEGACY_LEDGER_COMMERCIAL_AUTHORITY=false
LEGACY_LEDGER_CUSTOMER_LEDGER=false
```

Its 1,661 receipts, including 1,659 valid signatures and two unverifiable
signatures, remain immutable historical development evidence. They must not be
deleted, re-signed, allowlisted, promoted, or migrated into a production chain.

Any future production ledger must use `CLEAN_GENESIS`: an independent database
or schema, independent `ledger_id`, sequence starting at one, null previous
hash, separate signer and public key set, separate backup/recovery plan, and
separate tenant initialization. Creation is deferred until a separate
`PAID_BETA_LAUNCH_AUTHORIZED` decision.

```text
FUTURE_PRODUCTION_LEDGER_MODE=CLEAN_GENESIS
LEGACY_TO_PRODUCTION_MIGRATION=false
LEGACY_CHAIN_INHERITANCE=false
LEGACY_SEQUENCE_INHERITANCE=false
LEGACY_SIGNATURE_EXCEPTION_INHERITANCE=false
PRODUCTION_LEDGER_CREATION_TRIGGER=PAID_BETA_LAUNCH_AUTHORIZED
PRODUCTION_LEDGER_CREATED=false
PRODUCTION_SIGNER_CREATED=false
KMS_PURCHASE_AUTHORIZED=false
NO_MORE_INTERNAL_CLEAN_LEDGER_PROJECTS=true
NO_MORE_LEGACY_LEDGER_TRANSITION_PROJECTS=true
NO_MORE_D04_CANARIES=true
RESULT_REQUIRING_PRODUCTION_LEDGER=DEFERRED_UNTIL_PAID_BETA_PRODUCTION_LEDGER
```

TITMAS adopts an `ADOPT_BEFORE_BUILD` rule. Commodity persistence, proxying,
telemetry, SDK generation, protocol transport, SBOM generation, artifact
signing and CI are adopted from mature upstream projects. Custom code is
limited to TITMAS-specific trust semantics and thin integration boundaries.

## Consequences

- No fourth D04 canary and no replacement internal clean-ledger project.
- No PR #37, cherry-pick, implementation copy, Migration 0005, deployment,
  restart or soak is authorized.
- D04 experience may be cited as design evidence; its implementation is not
  adopted.
- The Build-versus-Adopt matrix becomes the input to a later Human Decision,
  not implementation authority.
- Licenses, security posture and release versions must be rechecked before any
  dependency is introduced or upgraded.

## Verification boundary

Read-only checks on 2026-08-01 confirmed the live service remained active on
release `9bbfce6154d67f4ab50e911b5e49611f5a4a8b57`, the live ledger still held
1,661 receipts, no `titmas_cr01_internal` schema existed, and no D04/canary
database remained. These observations do not authorize writes or assert
production readiness.

```text
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_AUTHORIZATION=true
ARCHITECTURE_PLAN_NE_IMPLEMENTATION_COMPLETE=true
TECHNICAL_CANDIDATE_NE_PRODUCTION_READY=true
```

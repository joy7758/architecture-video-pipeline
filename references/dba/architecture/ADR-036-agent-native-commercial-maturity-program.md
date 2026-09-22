# ADR-036: TITMAS Agent-Native Commercial Maturity Program

## Status

```text
decision_id=TITMAS-AGENT-NATIVE-COMMERCIAL-MATURITY-PROGRAM-D01
decision=AUTHORIZE_RESUMABLE_COMMERCIAL_INFRASTRUCTURE_PROGRAM
decided_by_ref=zhangbin
accepted_at=2026-07-30T19:04:07+08:00
status=ACCEPTED_EXECUTION_AUTHORIZED_WITH_HUMAN_GATES
```

## Context

TITMAS has a released Developer Preview, a bounded stateless Sandbox and
Stage 5.8 multi-Agent composition evidence. It does not yet have the durable,
tenant-isolated, metered and operationally recoverable service required for an
Agent-native commercial technical candidate.

Stage 5.8 is retained as a mixed input:

- canonical data-plane source:
  `joy7758/titmas-sandbox-gateway@dee6c2861d917950c057a8dc2d2feccfc7527ede`;
- 24 recorded sessions, 12 valid and 12 `POST_DISPATCH_UNKNOWN`;
- comparison conclusion `NOT_ASSESSED`;
- structured handoff rate `1.0`;
- Agent replacement `4/6 = 0.666667`, below the frozen `0.75` threshold;
- `NOT_ASSESSED` preservation `0/4`;
- authority-critical failures `0`;
- active Agent keys after the run `0`.

The final zero-active-key state is lease cleanup evidence, not evidence that
commercial credentials already work.

## Decision

1. Continue from the Developer Preview into a resumable commercial
   infrastructure program with separate technical, paid-beta, production and
   maturity states.
2. Keep `joy7758/titmas-sandbox-gateway` as the single private implementation
   repository. Do not create `titmas-commercial-control-plane` now.
3. Preserve `/sandbox/v0.1` as the stateless Developer Preview surface.
4. Add a separately namespaced `/api/v1` commercial candidate subsystem with a
   distinct data model, storage boundary and service configuration.
5. Use the existing Baidu server and install its Ubuntu-repository PostgreSQL
   16 candidate only after migration, isolation and rollback tests pass.
6. Prefer machine-readable interfaces; an HTML console is optional and derived.
7. Do not activate prices, payment, contracts, legal terms, DNS, certificates,
   formal SLA, production customer data or certification without a new Human
   Decision.

## Technical reference baseline

- JSON receipt canonicalization candidate: RFC 8785 JCS. It creates a
  deterministic, UTF-8 representation suitable for hashing and signing, but is
  an Informational RFC rather than an Internet Standards Track standard.
- receipt signature candidate: Ed25519 as specified by RFC 8032; the private
  key must remain outside Git, logs, model providers and plaintext database
  fields.
- machine error representation: RFC 9457 Problem Details for HTTP APIs.
- persistence candidate: Ubuntu 24.04 repository PostgreSQL 16; the installed
  minor version must be the current supported package at deployment time.
- tenant isolation: every object operation must enforce object-level
  authorization and carry explicit tenant, Agent and credential binding;
- database defense in depth: PostgreSQL Row-Level Security is mandatory for
  tenant-owned tables, not an optional substitute for application checks;
- control plane: the first vertical slice uses only an offline administration
  tool; no network management API is activated.

These are implementation candidates, not formal TITMAS standards adoption.

## Repository decision

```text
CONTROL_PLANE_HAS_DISTINCT_DEPLOYMENT_LIFECYCLE=false
CONTROL_PLANE_HAS_DISTINCT_SECURITY_BOUNDARY=true
CONTROL_PLANE_CANNOT_CLEANLY_LIVE_IN_GATEWAY=false
DUPLICATE_COMPONENT_CREATED=false
NEW_PRIVATE_REPOSITORY_CREATED=false
```

The commercial subsystem may later be split only through a new ADR after its
deployment lifecycle becomes materially independent.

## Consequences

- the private Gateway expands beyond its old repository-wide stateless rule,
  while the existing Sandbox subsystem retains that rule unchanged;
- a database is allowed only for commercial metadata and ledgers;
- raw request and response payload persistence remains disabled;
- receipts prove bounded service processing, not truth, authorization,
  certification or standard adoption;
- Stage 5.8 failures and unknowns remain visible and are not rerun merely to
  improve metrics;
- long-running and external-usage gates can legitimately remain waiting.

## Rejected alternatives

### Create a second Gateway

Rejected because it duplicates ingress, authentication and preflight behavior
before a distinct lifecycle is demonstrated.

### Upgrade `/sandbox/v0.1` in place

Rejected because it would silently convert a stateless preview contract into a
commercial stateful API.

### Start public paid access immediately

Rejected because tenant isolation, signed receipts, operational recovery,
external Agent Beta and Human commercial decisions are missing.

## Authority boundary

```text
AUTONOMOUS_TECHNICAL_EXECUTION_AUTHORIZED=true
REVERSIBLE_INFRASTRUCTURE_CHANGES_AUTHORIZED=true
PUBLIC_PAID_LAUNCH_AUTHORIZED=false
REAL_PAYMENT_ACCEPTANCE_AUTHORIZED=false
PRICING_ACTIVATION_AUTHORIZED=false
CONTRACT_ACCEPTANCE_AUTHORIZED=false
LEGAL_TERMS_PUBLICATION_AUTHORIZED=false
DNS_CHANGE_AUTHORIZED=false
CERTIFICATE_CHANGE_AUTHORIZED=false
FORMAL_CONFORMANCE_SERVICE_AUTHORIZED=false
CERTIFICATION_AUTHORITY_AUTHORIZED=false
```

## Drift Check

```text
TITMAS_DRIFT_CHECK
CORE_INTEROPERABILITY_OBJECTIVE_PRESERVED=true
NEW_CONTROL_AUTHORITY_CREATED=false
NEW_TRUTH_SOURCE_CREATED=false
DUPLICATE_EVIDENCE_OR_VERIFICATION_CREATED=false
RUNTIME_OR_EXECUTOR_CREATED=false
CURRENT_CAPABILITY_OVERCLAIMED=false
PUBLIC_LAUNCH_AUTHORIZED=false
COMMUNITY_ESTABLISHED=false
TITMAS_DRIFT_CHECK_RESULT=PASS_WITH_RECORDED_LIMITATIONS
```

## References

- <https://www.rfc-editor.org/info/rfc8785>
- <https://www.rfc-editor.org/info/rfc8032>
- <https://www.rfc-editor.org/info/rfc9457>
- <https://www.postgresql.org/support/versioning/>
- <https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/>

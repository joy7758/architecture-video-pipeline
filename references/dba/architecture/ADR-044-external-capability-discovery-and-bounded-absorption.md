---
adr_id: ADR-044
title: External capability discovery and bounded absorption
title_zh: 外部能力发现与有界吸收
status: proposed
decision_id: DBA-EXTERNAL-CAPABILITY-DISCOVERY-ABSORPTION-v0.1
proposer_ref: zhangbin
proposal_source: human-synchronized-dcell-external-capability-report
proposed_at: 2026-08-29
decision_status: pending_human_review
implementation_authorized: false
merge_authorized: false
release_or_deployment_authorized: false
---

# ADR-044: External Capability Discovery and Bounded Absorption

中文：外部能力发现与有界吸收。

## Context

A manually supplied DCell report identified mature external memory, temporal knowledge, conflict,
consolidation and context-budget capabilities. Treating that report as a one-time adoption decision
would leave the underlying architecture defect unresolved.

The current D19 path starts from reproducible internal problems and produces bounded repair or evolution
candidates. The current Build-versus-Adopt audit and component matrix provide strong point-in-time
comparison semantics. Neither contract continuously observes external capability maturity, converts
internal negative results into non-authoritative gap signals, or links a new source observation to a
versioned absorption candidate and canonical-owner handoff.

The absence of this result was therefore primarily a discovery-scope and lifecycle gap. It is not
evidence that an existing Runtime failed, because no such external capability radar is currently
declared active.

## Proposed decision

Extend the logical Discovery Evolution Layer with two compatible, non-executable architecture tracks:

1. `Capability Intelligence Track`: source-bound external observation, source verification, capability
   fingerprinting, internal gap and overlap comparison, freshness and drift.
2. `Bounded Absorption Track`: duplication review, license and security review, sandbox evaluation,
   recommendation, Human Decision and canonical-owner handoff.

Reuse D19 provenance and risk boundaries, the Architecture Evolution Policy recommendation gate, and
the existing Build-versus-Adopt matrix semantics. Do not create a new central scanner, DCell core,
Evidence owner, Evaluation owner, Authority, Runtime or thirteenth Weekly Cockpit Cell.

Define automated absorption narrowly as automatic creation and maintenance of a quarantined candidate
package. Automatic package installation, source copying, dependency adoption, core modification, merge,
release, deployment and production activation remain outside the meaning of absorption.

The detailed proposed contract is
[`titmas-external-capability-discovery-and-bounded-absorption-amendment-v0.1.md`](titmas-external-capability-discovery-and-bounded-absorption-amendment-v0.1.md).
The machine-readable profile is
[`external-capability-discovery-absorption-profile-v0.1.json`](external-capability-discovery-absorption-profile-v0.1.json).

## Why an agent would recommend this

```text
AGENT_RECOMMENDATION=CONDITIONALLY_RECOMMENDED
RECOMMENDED_AS=source-bounded capability radar and adoption-proposal generator
NOT_RECOMMENDED_AS=autonomous dependency installer, legal approver, production controller or novelty oracle
```

The proposal is recommendable because it reduces duplicate construction, connects retained experiment
evidence to future comparison without rewriting history, and makes upstream replacement and provenance
machine-readable.

It is not unconditionally recommendable because discovery indexes can be incomplete, upstream claims
can be wrong, licenses and advisories drift, benchmarks may not be comparable, and automation can create
vendor lock-in or silent Authority expansion. Primary-source binding, expiry, quarantine, independent
evaluation and Human Decision are required repairs.

## Alternatives considered

### Record only the supplied DCell report

Rejected. It preserves one finding but does not change time-to-detection, source coverage, freshness or
future duplicate-build prevention.

### Automatically install every high-scoring upstream component

Rejected. A score cannot approve license obligations, security posture, data egress, protected-state
writes or production effects. It would collapse Recommendation, Decision and Execution.

### Create a new central capability-intelligence platform

Rejected. It duplicates existing discovery, evidence admission, upgrade, drift, memory and handoff
responsibilities and risks becoming a new control plane.

### Expand DCell core with the discovered mechanisms

Rejected. Mature memory and graph techniques should remain replaceable capabilities. The existing DCell
identity, mission, lifecycle, permission intersection and replacement semantics remain unchanged.

### Extend D19 and reuse Build-versus-Adopt assets

Proposed. This preserves current ownership and history while closing the discovery-to-decision gap.

## Compatibility and ownership

- DBA remains normative owner of the architecture profile.
- External projects retain ownership of their code, claims and releases.
- The DCell project remains owner of its implementation and experiment truth.
- DBOS and SAEE ownership boundaries are unchanged.
- Human Decision remains required for adoption and any consequential implementation.
- Mapping, comparison, conformance or recommendation does not create adoption.

DBOS and SAEE domain positions are not yet recorded. This ADR cannot enter `accepted` until the required
architecture review and decision are explicit.

## Consequences if accepted

- Manual reports become valid discovery inputs but never bypass source verification.
- External changes and internal gap signals can enter one comparable candidate lifecycle.
- Point-in-time adoption matrices gain refresh triggers rather than permanent clearance.
- Failed, rejected, deferred, stale and inconclusive candidates remain historical evidence.
- DCell can compare replaceable external Skills without changing its frozen core definition.
- Implementation still requires a separate owner task, authorization and evidence package.

## Review gates before acceptance

1. Architecture Review confirms no duplicate Runtime, Truth Source or Authority.
2. DBOS and SAEE positions are recorded or explicitly marked not applicable with reasons.
3. Source, fingerprint, lifecycle and failure semantics receive conformance review.
4. The DCell seed case is treated as unverified manual input until primary sources are bound.
5. An explicit Human Decision records accept, revise, defer or reject.

## Current status and non-authorizations

```text
ADR_044_STATUS=PROPOSED
HUMAN_DIRECTION_RECORDED=true
HUMAN_ADOPTION_DECISION=NOT_RECORDED
ARCHITECTURE_REVIEW_STATUS=PENDING
IMPLEMENTATION_AUTHORIZED=false
AUTOMATIC_DISCOVERY_ACTIVE=false
AUTOMATIC_ABSORPTION_ACTIVE=false
NEW_RUNTIME_CREATED=false
NEW_CONTROL_PLANE_CREATED=false
NEW_TRUTH_SOURCE_CREATED=false
NEW_AUTHORITY_CREATED=false
NEW_COCKPIT_CELL_CREATED=false
DCELL_CORE_CHANGED=false
FROZEN_EXPERIMENT_CHANGED=false
DEPENDENCY_ADOPTED=false
CODE_REUSED=false
TASK_REGISTRY_CHANGED=false
MERGE_AUTHORIZED=false
RELEASE_AUTHORIZED=false
DEPLOYMENT_AUTHORIZED=false
```

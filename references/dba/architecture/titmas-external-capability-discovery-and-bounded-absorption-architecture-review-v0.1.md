---
review_id: DBA-REVIEW-20260829-EXTERNAL-CAPABILITY-DISCOVERY-ABSORPTION-001
title: External Capability Discovery and Bounded Absorption Architecture Review v0.1
title_zh: 外部能力发现与有界吸收架构评审 v0.1
status: completed_advisory_review
review_type: architecture_boundary_and_specification_maturity
review_independence: not_independent_domain_owner_review
proposal_reference: architecture/titmas-external-capability-discovery-and-bounded-absorption-amendment-v0.1.md
profile_reference: architecture/external-capability-discovery-absorption-profile-v0.1.json
adr_reference: architecture/ADR-044-external-capability-discovery-and-bounded-absorption.md
review_decision: request_revision
implementation_authorized: false
---

# External Capability Discovery and Bounded Absorption Architecture Review v0.1

中文：外部能力发现与有界吸收架构评审 v0.1。

## 1. Review purpose

本评审检查 ADR-044 及其修正案是否可以从 `PROPOSED` 进入 Human Decision。评审只判断
架构方向、对象所有权、自动化边界、兼容性和规范成熟度，不判断任何外部项目的技术质量，
也不授权实现、网络扫描、依赖安装、代码复用、合并或部署。

本评审由同一工作上下文中的 Codex 完成，因此不是 DBOS Domain Owner、SAEE Domain
Owner、法律、安全或独立科学评审。不能用本记录伪造尚未取得的 Domain Position。

## 2. References reviewed

- D19 bounded discovery and evolution amendment v2.1;
- ADR-040 bounded discovery self-healing and evolution;
- Architecture Evolution Policy v0.1;
- TITMAS Build-versus-Adopt Audit v1.0;
- TITMAS component adoption matrix v1.0;
- DBA main constitutional coherence amendment;
- TITMAS unified entry and DCell amendment;
- ADR-043 DCell constitutional coherence;
- proposed external capability discovery and bounded absorption amendment v0.1;
- proposed machine-readable profile v0.1;
- proposed ADR-044.

## 3. Executive review result

```text
ARCHITECTURE_DIRECTION=SUPPORTED
ROOT_CAUSE_DIAGNOSIS=PASS
EXISTING_ASSET_REUSE=PASS
AUTOMATION_AUTHORITY_BOUNDARY=PASS
DCELL_CORE_COMPATIBILITY=PASS
FROZEN_HISTORY_COMPATIBILITY=PASS
OBJECT_OWNERSHIP_CLARITY=REQUEST_REVISION
SOURCE_IDENTITY_AND_DEDUPLICATION=REQUEST_REVISION
STATE_TRANSITION_GUARDS=REQUEST_REVISION
DBOS_DOMAIN_POSITION=MISSING
SAEE_DOMAIN_POSITION=MISSING
REVIEW_DECISION=REQUEST_REVISION
IMPLEMENTATION_READINESS=NOT_READY
```

`REQUEST_REVISION` does not reject the direction. It means the proposal correctly identifies the
discovery gap but is not yet precise enough to become an accepted machine contract.

## 4. Review matrix

| Area | Result | Reason |
|---|---|---|
| Problem statement | `PASS` | Correctly distinguishes a missing external capability radar from failure of an existing Runtime |
| Reuse before build | `PASS` | Extends D19 and Build-versus-Adopt instead of creating a new platform |
| DBA role | `PASS` | DBA remains normative architecture owner and not an executor |
| Automation boundary | `PASS` | Candidate preparation is separated from install, merge, release and activation |
| Weekly Cockpit composition | `PASS` | Reuses existing logical responsibilities and creates no thirteenth Cell |
| DCell compatibility | `PASS` | External capabilities remain replaceable Skills and do not alter DCell core identity or mission |
| Frozen experiment compatibility | `PASS` | TKDE and other frozen evidence cannot be rewritten |
| Discovery record ownership | `REQUEST_REVISION` | `ExternalCapabilityObservation` can be mistaken for a second canonical Observation or Evidence object |
| Evaluation ownership | `REQUEST_REVISION` | `AbsorptionEvaluation` can be mistaken for a second SAEE Evaluation owner |
| Source identity | `REQUEST_REVISION` | Source classes exist, but canonical source-reference syntax and source-list ownership are not defined |
| Deduplication | `REQUEST_REVISION` | No exact candidate identity or deduplication key is specified |
| State transitions | `REQUEST_REVISION` | State lists exist, but transition guards and invalid transitions are not machine-defined |
| DBOS position | `MISSING` | No authorized DBOS Domain Owner position has been recorded |
| SAEE position | `MISSING` | No authorized SAEE Domain Owner position has been recorded |

## 5. Blocking finding AR-01: discovery planning record ownership

### Finding

The proposal introduces `ExternalCapabilityObservation`. Although it says Observation is not Evidence
Truth, the name and required fields can still be interpreted as a new canonical Observation object.
DBOS already owns bounded operational Observation and Evidence semantics.

### Required revision

The next draft MUST either:

1. rename the object to `CapabilityDiscoveryRecord`; or
2. define it as a DBA architecture-planning envelope that references, but never replaces, DBOS or
   external source records.

Its owner, updater, verifier and truth effect MUST be explicit. The recommended owner mapping is:

```text
OWNER=DBA_CAPABILITY_DISCOVERY_PROFILE
RECORD_CLASS=ARCHITECTURE_PLANNING_METADATA
DBOS_OBSERVATION_CREATED=false
DBOS_EVIDENCE_CREATED=false
SOURCE_CLAIM_PROMOTED_TO_TRUTH=false
```

## 6. Blocking finding AR-02: evaluation ownership

### Finding

`AbsorptionEvaluation` includes functional fit, evidence quality, resources, security and a recommendation.
Without a stricter wrapper rule, this can duplicate SAEE Evaluation or imply that DBA owns evolution
fitness conclusions.

### Required revision

The next draft MUST rename the planning object to `AbsorptionAssessment` or define it as a reference
envelope. It MUST separate:

- source verification;
- architecture fit and duplication assessment owned by DBA;
- scientific or evolutionary Evaluation owned by SAEE when applicable;
- implementation benchmark evidence owned by the canonical implementation project;
- Human adoption decision.

The planning object MAY aggregate references and limitations. It MUST NOT become a canonical fitness,
scientific validity or production-readiness result.

## 7. Blocking finding AR-03: source identity and deduplication

### Finding

The v0.1 profile lists valid source classes but does not define a canonical source reference, source-list
owner, refresh rule or candidate deduplication key. Different URLs, paper versions, repository mirrors or
renamed projects could create duplicate candidates or merge unrelated capabilities.

### Required revision

The next draft MUST define a canonical source reference containing:

```text
source_type
canonical_uri_or_identifier
source_owner
version_or_revision
content_digest_when_available
observed_at
fresh_until
retrieval_mode
```

The source allowlist or source policy MUST have an owner and version. Discovery indexes MAY locate a
candidate but MUST NOT become canonical evidence.

Candidate deduplication MUST use an explicit key. At minimum:

```text
candidate_key = hash(
  upstream_identity
  + version_or_revision
  + capability_fingerprint_digest
  + canonical_source_digest_or_identifier
)
```

Same upstream with a materially different version must create a new candidate version, not overwrite
history. Different upstreams with similar fingerprints remain separate candidates linked by an overlap
group.

## 8. Blocking finding AR-04: state transition guards

### Finding

The profile defines ordered state arrays but not the evidence required for each transition. A consumer
could move directly from `CANDIDATE` to `ADOPTION_PLANNED` without license, security, sandbox or Human
Decision references.

### Required revision

The next profile MUST define, for every transition:

- required input references;
- actor or owner allowed to record the transition;
- fail-closed result;
- forbidden skipped states;
- whether a Human Decision is required;
- whether implementation, release or deployment authority changes.

At minimum, `ADOPTION_PLANNED` MUST require an exact `AbsorptionDecisionReference` with
`implementation_authorized=true` and bounded scope. No transition may infer release or deployment
authorization.

## 9. Blocking finding AR-05: domain positions

### Finding

The proposal correctly marks DBOS and SAEE positions as `NOT_ASSESSED`. The architecture change process
requires affected domain positions before acceptance. This review cannot manufacture them.

### Advisory position for DBOS review

```text
DBOS_ADVISORY_RECOMMENDATION=NO_OBJECTION_IF_PLANNING_RECORDS_DO_NOT_DUPLICATE_OPERATIONAL_OBSERVATION_OR_EVIDENCE
DBOS_DOMAIN_OWNER_DECISION=NOT_RECORDED
```

DBOS review should confirm that no discovered source, candidate package or adoption handoff creates
Identity, Lifecycle, Permission, operational Observation or Evidence truth.

### Advisory position for SAEE review

```text
SAEE_ADVISORY_RECOMMENDATION=NO_OBJECTION_IF_ASSESSMENT_REFERENCES_DO_NOT_DUPLICATE_EVOLUTION_EVALUATION
SAEE_DOMAIN_OWNER_DECISION=NOT_RECORDED
```

SAEE review should confirm that architecture-fit comparison and adoption recommendation do not become
fitness, scientific validity, survival or evolution conclusions.

## 10. Non-blocking implementation gates

The following do not block a revised architecture proposal, but they block implementation:

- implementation owner remains unassigned;
- no source adapter, scheduled scanner or network budget is authorized;
- no privacy and data-egress review exists for future discovery adapters;
- no conformance test vectors exist;
- no first bounded source allowlist is approved;
- the named DCell upstream candidates remain source-unverified;
- no license, security or benchmark review has been completed for those candidates.

These items MUST remain `NOT_ASSESSED` rather than being repaired through narrative claims.

## 11. Required v0.2 revision scope

The revision MUST remain limited to specification maturity:

1. replace or bind `ExternalCapabilityObservation` as DBA planning metadata;
2. replace or bind `AbsorptionEvaluation` as a non-canonical assessment envelope;
3. add an object ownership table;
4. add canonical source-reference and source-policy identity;
5. add candidate identity and deduplication rules;
6. add transition guards and forbidden transition rules;
7. request and record DBOS and SAEE Domain Owner positions;
8. preserve every current automation and non-implementation boundary.

The revision MUST NOT add source adapters, network access, task-registry entries, dependencies, code,
Runtime, a new Cell, or implementation authorization.

## 12. Review decision

```text
REVIEW_ID=DBA-REVIEW-20260829-EXTERNAL-CAPABILITY-DISCOVERY-ABSORPTION-001
REVIEW_DECISION=REQUEST_REVISION
ARCHITECTURE_DIRECTION_REJECTED=false
REVISION_SCOPE=SPECIFICATION_MATURITY_ONLY
READY_FOR_HUMAN_ADOPTION_DECISION=false
READY_FOR_IMPLEMENTATION_REVIEW=false
IMPLEMENTATION_AUTHORIZED=false
```

Allowed next action:

```text
NEXT_ALLOWED_ACTION=CREATE_V0_2_SPECIFICATION_REVISION
```

Not allowed:

```text
AUTOMATIC_DISCOVERY_EXECUTION
AUTOMATIC_ABSORPTION_EXECUTION
SOURCE_ADAPTER_IMPLEMENTATION
TASK_REGISTRY_ACTIVATION
DEPENDENCY_ADOPTION
CODE_REUSE
MERGE_OR_RELEASE
DEPLOYMENT
```

## 13. Architecture change checklist

```text
CHANGE_ID=DBA-CHG-20260829-EXTERNAL-CAPABILITY-DISCOVERY-ABSORPTION-001
CURRENT_RULE_REFERENCED=true
EXISTING_ADRS_REVIEWED=true
AFFECTED_AUTHORITY_DOMAINS=DBA,DBOS,SAEE,HUMAN_DECISION
DBOS_DOMAIN_POSITION_RECORDED=false
SAEE_DOMAIN_POSITION_RECORDED=false
ARCHITECTURE_REVIEW_RECORDED=true
DECISION_SOURCE_EXPLICIT=false
ADOPTION_RECORDED=false
DOCUMENTATION_SCOPE_MATCHES_DECISION=not-applicable
RUNTIME_CHANGE_CLAIMED=false
CAPABILITY_CHANGE_CLAIMED=false
EVIDENCE_CHANGE_CLAIMED=false
PERMISSION_CHANGE_CLAIMED=false
STATUS=reviewed_request_revision
```

## 14. TITMAS drift check

```text
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

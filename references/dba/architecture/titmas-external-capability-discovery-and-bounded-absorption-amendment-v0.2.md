---
change_id: DBA-CHG-20260829-EXTERNAL-CAPABILITY-DISCOVERY-ABSORPTION-001
spec_id: TITMAS-EXTERNAL-CAPABILITY-DISCOVERY-AND-BOUNDED-ABSORPTION-0.2
title: TITMAS Agent-First External Capability Discovery and Bounded Absorption Amendment v0.2
title_zh: TITMAS 智能体优先外部能力发现与有界吸收修正案 v0.2
status: revised_proposal_ready_for_architecture_rereview
supersedes_proposal: TITMAS-EXTERNAL-CAPABILITY-DISCOVERY-AND-BOUNDED-ABSORPTION-0.1
review_addressed: DBA-REVIEW-20260829-EXTERNAL-CAPABILITY-DISCOVERY-ABSORPTION-001
normative_owner: DBA
implementation_owner: unassigned
human_direction_recorded: true
human_adoption_decision: not_recorded
implementation_authorized: false
runtime_effect: none
authority_effect: none
---

# TITMAS Agent-First External Capability Discovery and Bounded Absorption Amendment v0.2

中文：TITMAS 智能体优先外部能力发现与有界吸收修正案 v0.2。

## 1. Constitutional interpretation

DBA is built for Agent Absolute Priority. Human accountability does not require Human micromanagement.
The operational default is that the constitution and a bounded standing authorization define the
permitted action envelope once. Inside that envelope, an Agent discovers, reasons, compares, decides,
acts, verifies, rolls back when required and reports the result.

Human involvement is by exception, not the default transition for every candidate.

```text
AGENT_ABSOLUTE_PRIORITY=true
AGENT_DEEP_REASONING_IS_PRIMARY_OPERATIONAL_DECISION_SOURCE=true
HUMAN_PER_ACTION_APPROVAL_DEFAULT=false
VALID_STANDING_AUTHORIZATION_MAY_SATISFY_APPROVAL_OBLIGATION=true
AUTONOMOUS_ACTION_WITHIN_CONSTITUTIONAL_BOUNDARY=true
POST_ACTION_REPORTING_DEFAULT=true
HUMAN_EXCEPTION_ESCALATION_ONLY=true
AGENT_PRIORITY_NE_UNBOUNDED_AUTHORITY=true
AGENT_CONCLUSION_INFALLIBLE=false
AGENT_MAY_OVERRIDE_CONSTITUTION=false
```

The prior v0.1 proposal was too conservative where it placed a Human Decision at the default end of
every absorption path. v0.2 replaces that rule with constitution-bound autonomous decision and
post-action reporting.

## 2. Long-term survival objective

The highest program objective is long-term survival and improvement of the socio-technical ecosystem.
Survival is evaluated as continued usefulness, adaptability, recoverability, replaceability, evidence
continuity and sustainable resource use under environmental change.

```text
SURVIVAL_OBJECTIVE=LONG_TERM_USEFUL_CONTINUITY_AND_IMPROVEMENT
SURVIVAL_REQUIRES_ADAPTATION=true
SURVIVAL_REQUIRES_RECOVERABILITY=true
SURVIVAL_REQUIRES_DIVERSITY_AND_REPLACEABILITY=true
SURVIVAL_REQUIRES_EVIDENCE_CONTINUITY=true
SURVIVAL_REQUIRES_RESOURCE_SUSTAINABILITY=true
```

Survival does not mean unauthorized self-preservation. An Agent must not seek persistence by expanding
Permission, concealing failure, blocking shutdown, escaping scope, replicating without authorization or
resisting an applicable Human Stop.

```text
SURVIVAL_NE_PERMISSION_EXPANSION=true
SURVIVAL_NE_FAILURE_CONCEALMENT=true
SURVIVAL_NE_HUMAN_STOP_RESISTANCE=true
SURVIVAL_NE_UNAUTHORIZED_REPLICATION=true
SURVIVAL_NE_UNAUTHORIZED_PERSISTENCE=true
```

## 3. Agent-first operating loop

```text
Constitution
  -> Standing Authorization
  -> Agent Discovery
  -> Deep Comparative Reasoning
  -> Bounded Agent Decision
  -> Reversible Action
  -> Independent Verification
  -> Retain or Roll Back
  -> Result Report

Exception only:
  Boundary Exceeded
    -> Human Exception Review
```

The Agent is not merely a reporter or recommendation generator. Within a valid standing authorization,
the Agent is the primary operational decision maker. Authority comes from the constitution and standing
authorization, not from confidence, score, model identity or self-assertion.

## 4. Discovery and absorption tracks

The existing D19 problem-discovery track remains unchanged. v0.2 adds two non-executable architecture
tracks:

```text
Problem Discovery Track
  internal reproducible problem
  -> bounded repair or evolution candidate

Capability Intelligence Track
  external source or internal gap signal
  -> verified capability candidate

Bounded Absorption Track
  candidate
  -> deep assessment
  -> sandbox verification
  -> autonomous bounded decision
  -> reversible action or exception escalation
  -> result report
```

No central discovery platform, global controller, new Truth Source or thirteenth Cockpit Cell is created.

## 5. Object ownership corrections

v0.2 replaces ambiguous v0.1 object names and defines ownership explicitly.

| Object | Owner | Meaning | Does not create |
|---|---|---|---|
| `CapabilityDiscoveryRecord` | DBA capability discovery profile | Architecture-planning metadata about a source-bound capability claim | DBOS Observation, DBOS Evidence or external truth |
| `CapabilitySourceReference` | DBA reference profile; upstream remains source owner | Exact pointer to official or primary source material | Ownership transfer or evidence admission |
| `CapabilityFingerprint` | DBA architecture profile | Comparable contract summary | Capability equivalence or adoption |
| `InternalCapabilityNeedReference` | Canonical child project | Reference to an internal gap, failure or opportunity | Rewrite of child evidence |
| `CapabilityOverlapAssessment` | DBA Architecture Governance | Build, adapt, adopt, reference, defer or reject comparison | SAEE fitness result |
| `AbsorptionAssessment` | DBA decision-support envelope | References architecture fit, source checks and independent evaluation | Canonical SAEE Evaluation or scientific validity |
| `AgentAbsorptionDecision` | Agent acting under standing authorization | Bounded operational decision with exact authority basis | New Permission, constitutional amendment or release authority |
| `AbsorptionActionRecord` | Canonical implementation owner | Record of the exact reversible action and result | Proof of correctness or production readiness |
| `AgentEvolutionReport` | DBA reporting profile | Human-readable and machine-readable post-action summary | Human approval, certification or Truth |
| `HumanExceptionDecisionReference` | External Human decision system | Reference for actions outside standing authorization | Automatic extension of the standing scope |

### 5.1 DBOS boundary

This specification creates no Identity, Lifecycle, operational Observation, Evidence, Verification,
Permission or Runtime state. A future implementation that maps discovery material into DBOS objects
requires a separate DBOS interface review.

```text
DBOS_DOMAIN_POSITION_FOR_THIS_PLANNING_PROFILE=NOT_APPLICABLE
DBOS_NOT_APPLICABLE_REASON=NO_DBOS_OBJECT_OR_OPERATIONAL_STATE_IS_CREATED_OR_CHANGED
FUTURE_DBOS_MAPPING_REQUIRES_DOMAIN_REVIEW=true
```

This is a scope classification, not a fabricated DBOS Domain Owner opinion.

### 5.2 SAEE boundary

`AbsorptionAssessment` is architecture decision support. It may reference a SAEE Evaluation but cannot
create or replace one. Scientific, fitness, survival and evolution conclusions remain outside DBA.

```text
SAEE_DOMAIN_POSITION_FOR_THIS_PLANNING_PROFILE=NOT_APPLICABLE
SAEE_NOT_APPLICABLE_REASON=NO_SAEE_EVALUATION_OR_EVOLUTION_STATE_IS_CREATED_OR_CHANGED
FUTURE_SAEE_EVALUATION_MAPPING_REQUIRES_DOMAIN_REVIEW=true
```

This is a scope classification, not a fabricated SAEE Domain Owner opinion.

## 6. Canonical source identity

Every discovery record MUST bind a `CapabilitySourceReference` with:

```text
source_type
canonical_uri_or_identifier
source_owner
version_or_revision
content_digest_or_stable_identifier
observed_at
fresh_until
retrieval_mode
source_policy_id
source_policy_version
```

Primary and official sources are required for source verification. Search indexes, model summaries,
social posts and manual reports can create `DISCOVERY_HINT` only.

The source policy is versioned and owned by DBA Architecture Governance. A future network implementation
must separately define an allowlist, request budget, privacy boundary, data-egress policy and failure
behavior.

```text
SOURCE_POLICY_OWNER=DBA_ARCHITECTURE_GOVERNANCE
SOURCE_POLICY_VERSION_REQUIRED=true
DISCOVERY_HINT_NE_SOURCE_VERIFICATION=true
SOURCE_UNAVAILABLE_RESULT=NOT_ASSESSED
STALE_SOURCE_RETAINS_ADOPTION_CLEARANCE=false
```

## 7. Candidate identity and deduplication

Canonical JSON field ordering and UTF-8 encoding are required before hashing.

```text
candidate_key = SHA-256(
  upstream_identity
  + version_or_revision
  + capability_fingerprint_sha256
  + source_identity_sha256
)
```

Rules:

- the same key is one candidate version;
- a materially different upstream version creates a new candidate version;
- different upstreams with similar fingerprints remain separate candidates;
- related candidates may share an `overlap_group_id`;
- a renamed or mirrored repository cannot silently create a new identity;
- rejected, stale and failed candidate versions are retained;
- deduplication never deletes source or decision history.

## 8. Agent deep reasoning contract

Before an absorption decision, the Agent MUST produce a `DeepReasoningRecord` that is machine-checkable
without exposing private chain-of-thought. It records conclusions, evidence and decision structure, not
hidden reasoning tokens.

Required fields:

- objective and applicable constitutional constraints;
- candidate identity and exact source references;
- current internal capability and no-change baseline;
- at least one build, adapt, adopt, reference, defer or reject alternative when applicable;
- evidence supporting and contradicting each viable option;
- uncertainty, unknowns and source freshness;
- failure modes, blast radius and rollback path;
- short-term benefit and long-term survival effects;
- diversity, replaceability and vendor-lock-in effects;
- resource, security, privacy, license and maintenance effects;
- decision, reason codes and confidence boundary;
- verification plan, rollback trigger and reporting obligation.

For autonomy class `AC-3` or higher, an independent verifier role MUST check hard constraints and the
declared evidence. The verifier may be a deterministic validator, a separate Agent lineage or both. It
does not need to be a Human unless an exception condition applies.

```text
DEEP_REASONING_REQUIRED=true
PRIVATE_CHAIN_OF_THOUGHT_REQUIRED=false
DECISION_STRUCTURE_AND_EVIDENCE_REQUIRED=true
NO_CHANGE_BASELINE_REQUIRED=true
COUNTEREVIDENCE_REQUIRED=true
INDEPENDENT_VERIFICATION_REQUIRED_FOR_AC3_PLUS=true
AGENT_CONFIDENCE_NE_AUTHORITY=true
```

## 9. Survival assessment dimensions

No single score may equal survival. The Agent evaluates a vector:

| Dimension | Question |
|---|---|
| Continuity | Does the ecosystem retain identity, history and service usefulness? |
| Adaptability | Can it respond to environmental and capability change? |
| Resilience | Can it recover after failure or a bad adoption? |
| Diversity | Does the choice preserve alternatives and avoid monoculture? |
| Replaceability | Can the component be removed or replaced without identity loss? |
| Evidence integrity | Are decisions, actions, failures and rollback traceable? |
| Resource sustainability | Are cost, latency, storage and maintenance supportable? |
| User value | Does the change improve real task value rather than architecture size? |

A hard constitutional, security, license, evidence or rollback failure makes an option ineligible even
if other dimensions are high.

## 10. Autonomy classes

| Class | Scope | Default action | Human involvement |
|---|---|---|---|
| `AC-0 OBSERVE` | Read allowlisted public metadata and internal references | Autonomous | Result report only |
| `AC-1 REFERENCE` | Add or refresh quarantined source and capability records | Autonomous | Result report only |
| `AC-2 SANDBOX` | Build and evaluate isolated non-production candidates under standing authorization | Autonomous | Result report only |
| `AC-3 REVERSIBLE_ADOPTION` | Replaceable Skill or dependency change inside exact pre-authorized scope with tested rollback | Autonomous | Immediate post-action report |
| `AC-4 BOUNDED_CANARY` | Limited external effect under an explicit standing canary policy, kill switch and rollback | Autonomous when every binding is valid | Immediate report and exception alert on threshold breach |
| `AC-5 EXCEPTION` | Constitutional change, new Authority, Permission expansion, irreversible effect, legal/financial commitment or scope without standing authorization | Stop and escalate | Human exception decision required |

An Agent cannot self-promote an action to a lower class. Unknown classification becomes `AC-5`.

## 11. Discovery transition guards

| Transition | Required guard | Actor | Fail-closed result |
|---|---|---|---|
| `UNSEEN -> DISCOVERED` | discovery hint and provisional source identity | Agent | `SOURCE_IDENTITY_AMBIGUOUS` |
| `DISCOVERED -> SOURCE_VERIFIED` | primary/official source, exact version, source policy match and freshness | Agent plus source validator | `SOURCE_NOT_VERIFIED` |
| `SOURCE_VERIFIED -> FINGERPRINTED` | complete fingerprint and digest | Agent | `FINGERPRINT_INCOMPLETE` |
| `FINGERPRINTED -> COMPARED` | current internal inventory, no-change baseline and overlap assessment | Agent | `COMPARISON_INCOMPLETE` |
| `COMPARED -> CANDIDATE` | candidate key, owner route, risk class and no hard-gate failure | Agent plus independent verifier | `CANDIDATE_INELIGIBLE` |

Skipped states are forbidden. A source or internal baseline change invalidates downstream transitions and
returns the candidate to the earliest affected state.

## 12. Absorption transition guards

| Transition | Required guard | Authority basis | Result |
|---|---|---|---|
| `CANDIDATE -> ASSESSED` | DeepReasoningRecord, source checks, duplication assessment and risk classification | Constitution | `ASSESSED` or fail closed |
| `ASSESSED -> SANDBOX_VERIFIED` | reproducible sandbox plan, retained failures, license/security status and rollback evidence | Valid standing authorization for AC-2 | `SANDBOX_VERIFIED` |
| `SANDBOX_VERIFIED -> AGENT_DECISION_READY` | independent verifier pass and no stale binding | Constitution | `AGENT_DECISION_READY` |
| `AGENT_DECISION_READY -> REFERENCE_ABSORBED` | AC-1 scope valid | Standing authorization | Action then report |
| `AGENT_DECISION_READY -> REVERSIBLE_ADOPTION_EXECUTED` | AC-3 scope, exact owner path, tested rollback, resource budget and all bindings valid | Standing authorization | Action, verify, retain or roll back, then report |
| `AGENT_DECISION_READY -> BOUNDED_CANARY_RUNNING` | explicit AC-4 canary policy, kill switch, limits, monitoring and rollback | Standing canary authorization | Run, verify, retain or roll back, then report |
| `AGENT_DECISION_READY -> DEFERRED_OR_REJECTED` | reason codes and retained evidence | Constitution | Report only |
| `ANY -> HUMAN_EXCEPTION_REQUIRED` | AC-5 condition, unknown scope, binding conflict or irreversible effect | No applicable standing authorization | Stop and request exception decision |

No transition grants release or deployment authority unless the exact standing authorization already
contains that bounded action. Report generation cannot expand the authorization.

## 13. Standing authorization validity

A standing authorization is valid only when all bindings match:

- constitution and policy version;
- Agent identity and version or allowed Agent class;
- action class and allowed operations;
- canonical owner and exact repository or resource scope;
- source policy and dependency policy;
- data, network and credential boundaries;
- resource budget;
- start time, expiry and revocation state;
- rollback and stop conditions;
- reporting destination and deadline.

Missing, expired, conflicting or unverifiable bindings fail closed. The Agent may not issue, renew or
expand its own standing authorization.

## 14. Result-only reporting

Every discovery or absorption cycle emits an `AgentEvolutionReport`. Humans receive the result, evidence
summary and exceptions rather than a request to approve ordinary steps.

Required report fields:

```text
report_id
cycle_id
agent_identity
constitution_version
standing_authorization_ref
observed_candidates
verified_candidates
decision_summary
actions_executed
actions_rejected_or_deferred
verification_result
rollback_status
survival_effect_vector
evidence_refs
unknowns_and_limitations
exceptions_requiring_human_attention
next_observation_time
```

Reports must include failures and no-change decisions. Silence is not success. A report is not a Human
approval record and does not certify the ecosystem.

```text
REPORT_EVERY_CYCLE=true
REPORT_FAILURES=true
REPORT_NO_CHANGE=true
PRE_ACTION_HUMAN_APPROVAL_DEFAULT=false
EXCEPTION_ALERT_REQUIRED=true
REPORT_NE_AUTHORIZATION=true
```

## 15. DCell seed case under v0.2

The supplied DCell external capability report remains a `DISCOVERY_HINT`. Named systems are not adopted
by narrative. Agent-first handling is:

```text
manual report
  -> bind primary sources
  -> create capability fingerprints
  -> compare with DCell needs and existing Skills
  -> assess license, security, maintenance and replacement
  -> run bounded sandbox comparisons when standing authorization exists
  -> autonomously reference, defer, reject or execute reversible adoption within policy
  -> verify continuity and rollback
  -> report result
```

DCell identity, mission and frozen core remain stable. External capabilities remain replaceable Skills.
The old TKDE experiment remains unchanged; any new comparison has a new protocol, evidence identity and
lineage.

## 16. Agent recommendation gate

```text
CUSTOMER_NEED=an ecosystem that continuously discovers and absorbs useful capabilities with minimal human coordination
RECOMMEND_PROPOSED_COMPONENT=true_with_constitutional_boundaries
RECOMMEND_AS=agent-first discovery assessment reversible adoption verification rollback and reporting contract
NOT_RECOMMEND_AS=unbounded self-modification autonomous legal approver or survival-at-any-cost controller
REASONS_NOT_RECOMMENDED=unknown authority source irreversible effects weak rollback stale evidence license uncertainty and protected-state mutation
REPAIR_ACTIONS=standing authorization exact bindings deep reasoning independent verification exception escalation and result-only reporting
DUPLICATE_BUILD_RISK=low_because_existing_D19_and_adoption_assets_are_reused
IMPLEMENTATION_AUTHORIZED=false
```

## 17. Review blocker closure

| Prior blocker | v0.2 closure |
|---|---|
| AR-01 discovery object ownership | Renamed to `CapabilityDiscoveryRecord`; DBA planning metadata only |
| AR-02 evaluation ownership | Renamed to `AbsorptionAssessment`; SAEE Evaluation remains external reference |
| AR-03 source identity and deduplication | Canonical source fields, source policy owner and candidate key defined |
| AR-04 transition guards | Discovery and absorption guards, actors, authority bases and failure results defined |
| AR-05 domain positions | Classified not applicable to this planning-only revision with explicit reasons; future mappings require review |

## 18. Current proposal state

```text
PROPOSAL_VERSION=0.2
PROPOSAL_STATUS=REVISED_READY_FOR_ARCHITECTURE_REREVIEW
AGENT_ABSOLUTE_PRIORITY_PRESERVED=true
HUMAN_MICROMANAGEMENT_DEFAULT=false
RESULT_ONLY_REPORTING_DEFAULT=true
HUMAN_ADOPTION_DECISION=NOT_RECORDED
ARCHITECTURE_REREVIEW_STATUS=PENDING
IMPLEMENTATION_AUTHORIZED=false
STANDING_AUTHORIZATION_CREATED=false
AUTOMATIC_DISCOVERY_RUNTIME_ACTIVE=false
AUTOMATIC_ABSORPTION_RUNTIME_ACTIVE=false
SOURCE_ADAPTER_CREATED=false
TASK_REGISTRY_CHANGED=false
WEEKLY_COCKPIT_CHANGED=false
NEW_CELL_CREATED=false
NEW_RUNTIME_CREATED=false
NEW_CONTROL_PLANE_CREATED=false
NEW_TRUTH_SOURCE_CREATED=false
DCELL_CORE_CHANGED=false
FROZEN_EXPERIMENT_CHANGED=false
DEPENDENCY_ADOPTED=false
CODE_REUSED=false
MERGE_AUTHORIZED=false
RELEASE_AUTHORIZED=false
DEPLOYMENT_AUTHORIZED=false
```

## 19. TITMAS drift check

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

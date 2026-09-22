---
change_id: DBA-CHG-20260829-EXTERNAL-CAPABILITY-DISCOVERY-ABSORPTION-001
spec_id: TITMAS-EXTERNAL-CAPABILITY-DISCOVERY-AND-BOUNDED-ABSORPTION-0.1
title: TITMAS External Capability Discovery and Bounded Absorption Amendment v0.1
title_zh: TITMAS 外部能力发现与有界吸收修正案 v0.1
status: proposed
compatibility: compatible-extension
normative_owner: DBA
implementation_owner: unassigned
adr_reference: architecture/ADR-044-external-capability-discovery-and-bounded-absorption.md
implementation_authorized: false
runtime_effect: none
authority_effect: none
---

# TITMAS External Capability Discovery and Bounded Absorption Amendment v0.1

中文：TITMAS 外部能力发现与有界吸收修正案 v0.1。

## 1. Proposal purpose

本提案解决的不是一次性吸收 A-MEM、APEX-MEM、Graphiti/Zep、StructMem、TiMem、
EMBER 或 LightMem，而是一个系统性缺口：为什么现有发现层没有持续识别外部成熟能力，
为什么既有 Build-versus-Adopt 审计没有形成持续、可追踪的吸收闭环。

本提案扩展现有 D19 bounded discovery and evolution contract，不创建第二个 Discovery
Runtime、扫描平台、控制中心或 Truth Source。

```text
ONE_TIME_ABSORPTION_RECORD_IS_NOT_ENOUGH=true
CONTINUOUS_CAPABILITY_DISCOVERY_REQUIRED=true
AUTOMATED_CANDIDATE_ABSORPTION_REQUIRED=true
AUTOMATIC_IMPLEMENTATION_ADOPTION=false
AUTOMATIC_PRODUCTION_ACTIVATION=false
```

## 2. Architecture change record

| Field | Record |
|---|---|
| `change_id` | `DBA-CHG-20260829-EXTERNAL-CAPABILITY-DISCOVERY-ABSORPTION-001` |
| `proposer_ref` | Human direction from `zhangbin`, 2026-08-29 |
| `problem` | Existing discovery is problem-driven and registry-bounded; external capability maturity, prior-art collision and adopt-before-build opportunities are not continuously discovered or routed |
| `current_rule` | D19 v2.1, ADR-040, Architecture Evolution Policy v0.1, TITMAS Build-versus-Adopt Audit v1.0 and component adoption matrix v1.0 |
| `proposed_change` | Add a capability-intelligence track and a bounded absorption track that reuse current evidence, ownership, evaluation and human decision boundaries |
| `scope` | Architecture Governance and Program Governance; DCell is the first seed case, not the only target |
| `compatibility` | Compatible extension; no current object owner, Runtime or Authority changes |
| `domain_positions` | DBA proposal recorded; DBOS and SAEE positions are `NOT_ASSESSED` until review |
| `alternatives` | One-time report intake, autonomous dependency installer, new central scanning platform, and direct DCell core expansion |
| `risks_and_unknowns` | Source quality, license drift, security drift, novelty overclaim, benchmark mismatch, vendor lock-in, false positives and automation overreach |
| `adr_reference` | `ADR-044` draft |
| `decision_result` | `pending` |
| `decided_by_ref` | `NOT_RECORDED` |
| `adoption_record` | `NOT_CREATED` |
| `validation_result` | `NOT_ASSESSED` |

## 3. Why the current layer did not discover this

The missed discovery is a contract gap, not evidence that the current code failed its declared job.

| Gap | Current behavior | Consequence |
|---|---|---|
| Source scope | Known repositories, registered projects and supplied evidence are primary inputs | Papers, upstream projects, releases and standards outside the registry are invisible |
| Trigger scope | D19 starts from a reproducible internal problem | A mature external capability without a current failure does not create a discovery event |
| Semantic comparison | No shared capability fingerprint connects an upstream system to an internal responsibility | Similar capabilities cannot be reliably deduplicated or compared |
| Freshness | Build-versus-Adopt is a point-in-time audit | New releases, license changes, maintenance decline and new research do not automatically reopen comparison |
| Research feedback | Negative or bounded experiment results remain correctly frozen | They do not yet emit a separate, non-authoritative `CAPABILITY_GAP_SIGNAL` |
| Absorption lifecycle | Adoption recommendations exist as documents and matrices | There is no continuous state chain from observation to verified candidate to human adoption decision |
| Automation meaning | “Automatic absorption” is undefined | It can be misread as automatic package installation, source copying or production activation |

Therefore the current system could record the supplied DCell report after a human found it, but it
was not designed to find the underlying external capability families first.

## 4. Two-track Discovery Evolution Layer

The existing logical layer gains a second track. It does not gain a new Runtime or Authority.

```text
Discovery Evolution Layer
  |
  +-- Problem Discovery Track
  |     OBSERVED -> REPRODUCED -> REPAIR OR EVOLUTION PROPOSAL
  |     Existing D19 v2.1 behavior
  |
  +-- Capability Intelligence Track
        EXTERNAL OBSERVATION
          -> SOURCE VERIFICATION
          -> CAPABILITY FINGERPRINT
          -> INTERNAL GAP / OVERLAP COMPARISON
          -> BOUNDED ABSORPTION CANDIDATE
          -> INDEPENDENT REVIEW
          -> HUMAN DECISION
```

Problem discovery answers “what is failing?”. Capability intelligence answers “what mature capability
now exists, what internal work it overlaps, and whether it should be referenced, adapted, adopted,
deferred or rejected?”. Neither answer authorizes implementation.

## 5. Discovery source model

### 5.1 Source classes

The discovery track MAY observe:

- primary research records with stable paper identifiers and version references;
- official upstream repositories, documentation, releases and changelogs;
- official standards and protocol publications;
- official license texts, security policies and advisory feeds;
- internal canonical experiment evidence and retained negative results;
- manually supplied reports treated as discovery hints.

Search results, model summaries, social posts and secondary articles MAY locate a candidate, but MUST
NOT satisfy source verification. Claims must be rebound to primary or official sources.

### 5.2 Discovery event types

```text
NEW_CAPABILITY
MATERIAL_VERSION_CHANGE
LICENSE_OR_TERMS_CHANGE
SECURITY_POSTURE_CHANGE
MAINTENANCE_DECAY
INTERNAL_CAPABILITY_GAP
NOVELTY_COLLISION
DUPLICATE_BUILD_RISK
REPLACEMENT_OPPORTUNITY
```

### 5.3 Freshness

Every source observation MUST carry `observed_at`, exact source identity, version or revision when
available, source kind, freshness deadline and limitations. Expired observations become `STALE` and
cannot retain an adoption recommendation without refresh.

## 6. Required machine objects

| Object | Purpose | Authority boundary |
|---|---|---|
| `ExternalCapabilityObservation` | Record a source-bound external claim or change | Observation is not Evidence Truth or adoption |
| `CapabilitySourceSnapshot` | Bind exact source, version, digest and observation time | Snapshot does not copy ownership from upstream |
| `CapabilityFingerprint` | Normalize user problem, I/O, state, side effects and lifecycle semantics | Similarity is not equivalence |
| `InternalCapabilityNeed` | Record an internal gap signal and its evidence reference | Need is not implementation authorization |
| `OverlapAssessment` | Compare existing internal and external capabilities | Mapping is not adoption |
| `AbsorptionCandidate` | Package a bounded reference, adapter, dependency or reuse option | Candidate is quarantined and non-operational |
| `AbsorptionEvaluation` | Compare fit, evidence, cost, replaceability and risks | Evaluation is not decision |
| `AbsorptionDecisionReference` | Point to an explicit Human Decision | Reference cannot create the decision |
| `AdoptionHandoff` | Route accepted scope to one canonical implementation owner | Handoff is not execution |

No object duplicates DBOS Evidence, SAEE Evaluation, TITMAS Receipt or Human Authorization semantics.

## 7. Capability fingerprint

Every candidate comparison MUST normalize at least:

- user problem and value hypothesis;
- capability class and declared non-goals;
- input and output contracts;
- state model and persistence assumptions;
- external side effects and data access;
- permission and authority assumptions;
- evidence and provenance support;
- versioning, replacement, rollback and exit semantics;
- resource, latency, storage and operating requirements;
- license, distribution and supply-chain constraints;
- known limitations and unsupported claims.

The fingerprint prevents a project name or marketing category from being treated as a capability match.

## 8. Discovery lifecycle

```text
OBSERVED
  -> SOURCE_VERIFIED
  -> FINGERPRINTED
  -> COMPARED
  -> CANDIDATE

Side states:
NOT_ASSESSED
SOURCE_CONFLICT
DUPLICATE
STALE
DEFERRED
REJECTED
```

Unknown license, unresolved source identity, missing version, contradictory evidence or inability to
separate upstream claims from observed behavior MUST fail closed as `NOT_ASSESSED` or
`SOURCE_CONFLICT`.

## 9. Bounded absorption lifecycle

```text
CANDIDATE
  -> DUPLICATION_ASSESSED
  -> LICENSE_SECURITY_REVIEWED
  -> SANDBOX_EVALUATED
  -> RECOMMENDATION_READY
  -> HUMAN_DECISION_PENDING
  -> {REFERENCE_ONLY | ADOPTION_PLANNED | DEFERRED | REJECTED}
  -> OWNER_HANDOFF_CREATED
```

`ADOPTION_PLANNED` means only that a Human Decision approved a bounded implementation plan. The
implementation owner must create a separate task, authorization, branch, evidence and release path.

### 9.1 Absorption modes

| Mode | Meaning | Default risk |
|---|---|---|
| `IDEA_REFERENCE` | Reuse an idea with citation and independent implementation | ER-0 analysis |
| `INTERFACE_COMPATIBILITY` | Map an existing interface without source reuse | ER-1 or ER-2 |
| `SANDBOX_ADAPTER_CANDIDATE` | Build an isolated replaceable adapter candidate | ER-2 |
| `DEPENDENCY_ADOPTION_CANDIDATE` | Propose a pinned upstream dependency | ER-2 or ER-3 |
| `SOURCE_REUSE_OR_FORK_CANDIDATE` | Propose code reuse or fork with license and maintenance obligations | ER-3 |

Risk classification may only increase after review; it cannot be lowered to obtain automation.

## 10. Meaning of automated absorption

Within this proposal, automated absorption means moving verified information into a quarantined,
non-authoritative candidate package. It does not mean operational adoption.

### 10.1 Allowed automation after separate implementation authorization

- read allowlisted public sources without mutation;
- detect version, license, security and maintenance changes;
- bind source metadata and content digests;
- normalize capability fingerprints;
- deduplicate candidates and compare against the internal capability inventory;
- create novelty-collision and duplicate-build warnings;
- prepare a bounded sandbox evaluation plan;
- generate an adoption recommendation package and Human Decision request;
- retain rejected, failed, stale and inconclusive candidates.

### 10.2 Actions requiring separate authorization

- network scanning beyond an approved source list;
- downloading or executing external code;
- installing a package or adding a dependency;
- creating an adapter implementation or Draft PR;
- running benchmarks with private data, credentials or paid services;
- changing an internal component, schema, public interface or frozen experiment.

### 10.3 Forbidden automatic actions

- treat an upstream claim as verified truth;
- approve a license or legal obligation;
- copy, vendor, fork or rename upstream source without review;
- modify DCell identity, mission, core definition or protected state;
- rewrite Alpha-001, TKDE or any other frozen evidence;
- grant Permission, Authority or production credentials;
- merge, release, deploy or activate an absorbed component;
- silently delete rejected candidates or failed evaluations.

## 11. Reuse of the existing 12-Cell cockpit

This proposal does not add a thirteenth Cell. A future implementation MAY route capability discovery
through existing logical responsibilities:

| Existing responsibility | Capability-discovery use |
|---|---|
| Project Discovery | Locate candidate projects, papers, standards and release changes |
| Evidence Admission | Verify primary source, version, time and limitations |
| Security | Surface supply-chain and security review requirements |
| Upgrade | Compare compatibility, replacement and version effects |
| Drift | Detect source, license, interface and maintenance drift |
| Memory | Retain prior comparisons, rejections, expiry and refresh history |
| Handoff | Produce a bounded decision package for the canonical owner |

This table is architecture mapping only. It does not change the current Weekly Cockpit implementation,
schedule, source allowlist or Cell contracts.

## 12. DCell seed case

The supplied “DCell external mature capability absorption” report enters only as a
`MANUAL_DISCOVERY_INPUT`. Its claims are not yet source-verified by this proposal.

Initial candidate families are:

1. temporal knowledge capability;
2. entity-event and conflict-analysis capability;
3. memory-consolidation and context-budget capability;
4. atomic-record and semantic-link capability.

The report's suggested first three organs are retained as `PROPOSER_PRIORITY`, not accepted priority.
Every named upstream must receive an exact source identity, version, license, security, maintenance,
capability fingerprint and bounded comparison before entering `CANDIDATE`.

No candidate may become the DCell core. The allowed relationship is a replaceable Skill or capability
module governed by the existing DCell contract.

## 13. Internal research feedback

Retained negative or bounded experiment results MAY emit `INTERNAL_CAPABILITY_GAP` or
`NOVELTY_COLLISION` discovery signals. The signal MUST reference the frozen result and MUST NOT
change its data, interpretation boundary or scientific status.

For the current TKDE example:

- the old experiment remains unchanged;
- the result may motivate a new candidate comparison;
- any external-skill evaluation requires a new protocol, holdout and evidence identity;
- no new result may be merged into the old baseline.

## 14. Agent customer recommendation gate

```text
CUSTOMER_NEED=continuously detect mature external capabilities and avoid duplicate internal construction
EXISTING_CANDIDATES=D19 v2.1; Architecture Evolution Policy; Build-versus-Adopt Audit; component adoption matrix
RECOMMEND_EXISTING_COMPONENT=conditional
RECOMMEND_PROPOSED_COMPONENT=conditional
RECOMMEND_AS=source-bounded capability radar and adoption-proposal generator
NOT_RECOMMEND_AS=autonomous dependency installer or production self-modifier
REASONS_NOT_RECOMMENDED=source quality; stale license and security facts; benchmark mismatch; vendor lock-in; silent authority and core drift
DUPLICATE_BUILD_RISK=high_if_new_platform_is_created
BOUNDARY_GAPS=continuous source coverage; capability fingerprint; refresh triggers; end-to-end candidate lifecycle
REPAIR_ACTIONS=reuse D19 and adoption matrix; add source verification; quarantine; human adoption gate; canonical owner handoff
IMPLEMENTATION_AUTHORIZED=false
```

## 15. Review and decision gates

| Gate | Minimum result |
|---|---|
| Source gate | Exact source identity, version, observed time, primary source and limitations |
| Capability gate | Complete fingerprint and internal owner mapping |
| Duplication gate | Build, adapt, adopt, reference, defer and reject alternatives compared |
| License and security gate | Exact version obligations and current security posture reviewed |
| Sandbox gate | Reproducible evaluation plan, no private data leakage and failed results retained |
| Authority gate | No self-approval, protected-state write, history rewrite or permission expansion |
| Adoption gate | Explicit Human Decision and one canonical implementation owner |

Failure at any gate remains visible and does not automatically terminate future rediscovery after a new
version or new evidence.

## 16. Research and operating metrics

The layer SHOULD measure:

- source-class coverage and freshness coverage;
- time from primary-source publication to verified observation;
- percentage of candidates with complete fingerprints;
- duplicate-build risks identified before development authorization;
- stale recommendation detection rate;
- candidate-to-decision lead time;
- rejected and inconclusive candidate retention;
- post-adoption replaceability and rollback evidence when later implementation exists.

Adoption count, automatic acceptance rate and number of installed dependencies MUST NOT be treated as
success metrics.

## 17. Failure semantics

```text
SOURCE_UNAVAILABLE
SOURCE_IDENTITY_AMBIGUOUS
SOURCE_CONFLICT
VERSION_UNPINNED
LICENSE_NOT_ASSESSED
SECURITY_NOT_ASSESSED
CAPABILITY_FINGERPRINT_INCOMPLETE
INTERNAL_OWNER_UNRESOLVED
DUPLICATION_REVIEW_INCOMPLETE
BENCHMARK_NOT_COMPARABLE
STALE_OBSERVATION
HUMAN_DECISION_REQUIRED
```

Missing evidence never defaults to adoption. Conflicting evidence is retained, not averaged into a
single confidence score.

## 18. Proposal state and non-effects

```text
PROPOSAL_STATUS=PROPOSED
HUMAN_DIRECTION_RECORDED=true
HUMAN_ADOPTION_DECISION=NOT_RECORDED
ARCHITECTURE_REVIEW_STATUS=PENDING
DBOS_DOMAIN_POSITION=NOT_ASSESSED
SAEE_DOMAIN_POSITION=NOT_ASSESSED
IMPLEMENTATION_AUTHORIZED=false
AUTOMATIC_DISCOVERY_RUNTIME_AUTHORIZED=false
AUTOMATIC_ABSORPTION_RUNTIME_AUTHORIZED=false
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

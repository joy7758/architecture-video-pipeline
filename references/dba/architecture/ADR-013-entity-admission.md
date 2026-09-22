---
adr_id: ADR-013
title: Establish the Digital Entity Admission Boundary
title_zh: 建立数字实体准入边界
status: accepted-for-architecture-specification-v0.1
decision_scope: candidate-to-registered-entity-admission-rules-only
implementation_effect: none
registration_effect: none
entity_effect: none
capability_effect: none
permission_effect: none
---

# ADR-013: Establish the Digital Entity Admission Boundary

## Problem（问题）

现有架构已经定义 Candidate Proposal、Review、Registration Request 和 `Proposed → Registered` Entity lifecycle，但没有回答：什么条件、决定和授权允许 Candidate 正式进入 DBOS Registration？

若缺少 Admission Boundary：

- Candidate Proposal 可能被误写为 Entity；
- Review `APPROVED` 可能被误写为 Registered 或 Active；
- Registration Request `ACCEPTED` 可能被误写为 DBOS 已登记；
- Capability Declaration 可能被提升为 Capability Verification/Grant；
- DBOS 可能在没有治理决定时自行登记；
- SAEE Evaluation 可能被误用为 Entity Admission approval；
- Candidate 或 Registered Entity 可能跳过生命周期进入 Digital Organism。

## Decision（决策）

建立独立 Digital Entity Admission Boundary：

1. Admission 是 Candidate 到 Registered Entity 的受控过程，不是 Activation；
2. 准入最低条件包括 Identity Reference、Owner Responsibility、Capability Declaration、Lifecycle Compatibility、Evidence Boundary 和 Governance Review；
3. Admission Review 使用六个评价维度，评价结果不自动批准；
4. Admission Decision 使用独立 `admission_id`、Candidate/Review 引用、显式 decision authority、conditions 和 timestamp；
5. `APPROVED`、Registration Authorized、DBOS Registration 和 Registered Entity 是四个不同 truth surface；
6. Registration Authorization 必须独立、可追溯、可过期和可撤销；
7. DBOS 在授权有效时仍执行自身 identity、deduplication、policy 和 safety checks；
8. Admission 的最大状态结果为 `REGISTERED`，不产生 Verified、Active、Capability、Permission 或 Runtime；
9. SAEE 不拥有 Admission Approval 权；DBOS 不得跳过 Decision；
10. Candidate → Active、Candidate → Digital Organism 和 Registered → Digital Organism 的直接转换被禁止；
11. Admission Decision 与现有 Recommendation-based Governance Decision Object 的 schema mapping 保持未决，不伪造 `source_recommendation`；
12. 本 ADR 不实现 DBOS Entity Registration Execution，不创建任何实例。

```text
Candidate ≠ Entity
Admission ≠ Activation
Registration ≠ Permission
Review ≠ Decision
Decision ≠ Authorization
Authorization ≠ DBOS Registration
```

## Alternatives（替代方案）

### A. Registration Request 被接收后由 DBOS 直接登记

拒绝。它把请求状态升级为授权和执行，允许 DBOS 绕过治理决定。

### B. Candidate Review `APPROVED` 直接等于 Registered

拒绝。Review 是评价记录，不是 Admission Decision、Registration Authorization 或 DBOS state record。

### C. 由 SAEE 评价并批准 Candidate

拒绝。SAEE 负责 Evolution Evaluation，不拥有 Entity Identity 或 Admission authority；Candidate 尚无运行历史时也不能伪造 Fitness 输入。

### D. 由 DBOS 自行决定并执行准入

拒绝。DBOS 负责 Existence Governance 和 Registration execution，不应同时发明独立治理批准。

### E. Admission Approved 直接创建 Active Entity

拒绝。它跳过 Registered、Verified、独立生命周期 gate 和 Permission separation。

### F. Capability declarations 齐全即自动准入

拒绝。Declaration 不证明 Capability 存在、已验证、低风险或获授权，也不能替代 Identity、Responsibility 和 Governance Review。

## Impact（影响）

### Positive（正面影响）

- Candidate、Approved Candidate、Registration-authorized Candidate 与 Registered Entity 可被准确区分；
- DBOS Registration Execution 获得明确的未来输入闸门；
- SAEE、DBOS、Architecture Governance 和 Governance Decision 的权力保持分离；
- Research Agent 获得合法但仍未执行的准入路径；
- Capability、Permission、Activation 与 Digital Organism 的错误提升被明确禁止；
- reviewer、decision authority、registration authority 和 DBOS recorder 可以独立审计。

### Costs and unresolved issues（代价与未决问题）

- Admission Decision 尚未加入 Core Data Contracts；
- Admission Decision 与现有 `source_recommendation`-based Governance Decision Object 的映射未定义；
- Registration Authorization Object/schema、Owner 与最终 authority assignment 未定义；
- Candidate identity/reference 与未来 canonical `entity_id` 的去重和连续性规则未定义；
- Architecture role 与 DBOS entity type 的正式映射仍缺失；
- Admission criteria 的证据格式、签名、时间、有效期和撤销验证尚未实现；
- DBOS Registration failure、retry、partial write 和 compensation contract 尚未定义；
- 规范版本的 Release/Adoption 尚未发生。

这些问题必须保持 `unknown` 或未实现，不能由本 ADR 自动补齐。

## Consequence Boundaries（后果边界）

```text
DIGITAL_ENTITY_ADMISSION_SPECIFICATION_DEFINED=true
ADMISSION_CRITERIA_MODEL_DEFINED=true
ADMISSION_DECISION_MODEL_DEFINED=true
ENTITY_STATUS_TRANSITION_RULES_DEFINED=true
ADMISSION_PROCESS_IMPLEMENTED=false
ADMISSION_DECISION_INSTANCE_CREATED=false
REGISTRATION_AUTHORIZATION_CREATED=false
DBOS_REGISTRATION_EXECUTED=false
ENTITY_INSTANCE_CREATED=false
AGENT_INSTANCE_CREATED=false
RUNTIME_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
DIGITAL_ORGANISM_CREATED=false
DBOS_CHANGED=false
SAEE_CHANGED=false
API_CREATED=false
CODE_CHANGED=false
```

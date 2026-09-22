---
spec_id: DBA-ADMISSION-DECISION-MODEL-0.1
title: Digital Entity Admission Decision Model v0.1
title_zh: 数字实体准入决策模型 v0.1
status: non-executable-architecture-decision-model
decision_model_defined: true
decision_authority_assigned: false
decision_instance_created: false
registration_effect: none
entity_effect: none
permission_effect: none
---

# Digital Entity Admission Decision Model v0.1（数字实体准入决策模型 v0.1）

本模型定义 Candidate Admission 的 Decision record（决策记录）、状态与权限分离。Admission Decision 决定候选是否可以继续进入 Registration Authorization 路径，不创建 Entity，也不执行 DBOS Registration。

```text
Admission Review ≠ Admission Decision
APPROVED ≠ Registration Authorized
APPROVED ≠ Registered
Decision Authority ≠ DBOS Execution Authority
```

## 1. Admission Decision Object（准入决策对象）

| 字段 | 语义 | 约束 |
|---|---|---|
| `admission_id` | 一次 Admission Decision 的稳定、不透明引用 | 不等于 `entity_id`、request ID 或 execution ID |
| `candidate_id` | 被审查 Candidate 的引用 | Candidate reference 不是 Entity Identity |
| `review_reference` | 指向已完成 Admission Criteria Review 的不可变引用 | Review 不能由 Decision 内容替代 |
| `decision_result` | `PENDING`、`APPROVED`、`REJECTED` 或 `REVOKED` | 必须遵守本模型状态转换 |
| `decision_authority` | 对作出决定的明确授权主体或授权记录的引用 | v0.1 不指定该主体；记录字段本身不授予 authority |
| `conditions` | 批准条件、限制、有效期、补充材料或拒绝理由 | 不得静默丢失或由 DBOS 扩大 |
| `timestamp` | 决策事件时间及其时间来源 | 时间值不证明 authority 或决定有效 |

Admission Decision Object 还应由采用方保留版本、scope、provenance、history 和 revocation reference，但本规范不选择序列化格式或创建对象实例。

## 2. Decision States（决策状态）

```text
PENDING
  ├─ explicit approval ─→ APPROVED
  └─ explicit rejection → REJECTED

APPROVED
  └─ explicit revocation → REVOKED
```

| 状态 | 最小进入条件 | 允许结果 | 不表示 |
|---|---|---|---|
| `PENDING` | Candidate 与 review reference 可解析，尚无最终决定 | `APPROVED` 或 `REJECTED` | 审查结果倾向或默许批准 |
| `APPROVED` | decision authority 可追溯；conditions、scope 和有效期明确 | 可进入独立 Registration Authorization 审查；也可 `REVOKED` | 已授权登记、已登记或已激活 |
| `REJECTED` | 明确拒绝决定、理由和来源记录 | 同一 admission 的终态 | Candidate history 被删除或永久禁止重新申请 |
| `REVOKED` | 原批准被明确撤销，撤销来源和时间可追溯 | 同一 admission 的终态 | 已完成 Registration 被自动回滚或实体历史被删除 |

重新提交必须创建新的 `admission_id` 或按未来版本化规则形成明确 revision；不能原地把 `REJECTED/REVOKED` 改回 `APPROVED`。

## 3. Approval Conditions（批准条件）

`APPROVED` 必须保留所有尚未完成的 conditions，例如：

- identity material 补充或去重确认；
- owner/human responsibility 确认；
- requested entity type mapping；
- Capability scope、unknown 与 forbidden 项限制；
- risk mitigation（风险缓解）和 Human Oversight；
- Evidence/Failure history readiness；
- 有效期、撤销条件与 DBOS-specific pre-registration checks。

有未满足条件的 `APPROVED` 只能表示 conditional approval（有条件批准）。它不得被序列化、展示或解释为无条件 Registration Authorization。

## 4. Registration Authorization Boundary（登记授权边界）

Registration Authorization 是 Admission Decision 被另行采纳并允许 DBOS 进入登记处理的治理记录。最低要求：

1. 引用 `admission_id`；
2. 批准仍为 `APPROVED` 且未过期、未撤销；
3. conditions 已满足或被明确转化为 DBOS registration constraints；
4. 授权主体、scope、有效期和撤销方式可追溯；
5. 目标只允许 `REGISTERED`；
6. 不包含 Permission、Activation 或 Capability Grant。

Registration Authorization Object 的正式字段、状态、scope、签发前提和 DBOS 使用边界由 [`registration-authorization-contract.md`](registration-authorization-contract.md) 定义。该契约仍不创建授权记录；本模型中的 `APPROVED` 只允许进入独立 authorization issuance review（授权签发审查）。

## 5. Relationship to Governance Decision Model（与治理决策模型的关系）

Admission Decision 遵守 [`governance-decision-model.md`](governance-decision-model.md) 的 Authority Separation（权力分离）与 `Decision ≠ Execution` 原则，但它不是对 SAEE Recommendation 的决定：其 source 是 Candidate、Admission Review 与 Registration Request。

因此 v0.1 将 Admission Decision 定义为 domain-specific governance decision profile（领域特定治理决策配置），属于 Governance Decision framework 的 `decision_type=admission`。正式对象字段见 [`admission-decision-data-contract.md`](admission-decision-data-contract.md)，通用框架映射见 [`admission-governance-mapping.md`](admission-governance-mapping.md)。

该 profile 使用 `subject_reference`、`review_reference` 与 `criteria_summary` 作为治理输入；通用 `source_recommendation` 对此类型明确不适用。不得通过填充虚假 SAEE Recommendation 来满足字段，也不得把 mapping definition（映射定义）描述成 Decision Object 已实例化或已被采用。

## 6. Authority Separation（权力分离）

| 角色 | 可以 | 不能 |
|---|---|---|
| Admission Reviewer | 评价 criteria、记录限制并给出 recommendation | 自动批准、分配 Identity 或执行登记 |
| Admission Decision Authority | 在明确授权范围内批准、拒绝或撤销 | 直接写 DBOS registry、激活 Entity 或授予 Permission |
| Governance Decision Layer | 保存 Decision record 与状态历史 | 自行成为 decision authority |
| DBOS | 验证 Decision/Authorization 并执行有界 Registration | 发明 Admission Decision、忽略条件或把 Registration 升级为 Active |
| SAEE | 必要时提供非绑定评价材料 | 批准 Candidate、创建 Identity 或命令 DBOS 登记 |
| Architecture Governance | 定义本模型和变更规则 | 审批具体 Candidate 或执行 Registration |

同一人或组织未来可以承担多个明确角色，但 Review、Decision、Authorization 与 Registration records 不得合并。

## 7. Revocation Boundary（撤销边界）

- Registration 前撤销：Registration Authorization 必须失效，DBOS 不得开始登记；
- Registration 处理中撤销：DBOS 必须停止在安全边界并记录已发生事实，不得伪装为未发生；
- Registration 完成后撤销：不得删除 Entity Identity；需要新的 DBOS lifecycle decision 处理限制、暂停或 Retired；
- 撤销不删除 Proposal、Review、Decision、Authorization 或 Registration history。

## 8. Non-implementation Status（非实现状态）

```text
ADMISSION_DECISION_MODEL_DEFINED=true
ADMISSION_DECISION_DATA_CONTRACT_DEFINED=true
ADMISSION_GOVERNANCE_MAPPING_DEFINED=true
REGISTRATION_AUTHORIZATION_CONTRACT_DEFINED=true
ADMISSION_DECISION_OBJECT_INSTANCE_CREATED=false
ADMISSION_DECISION_AUTHORITY_ASSIGNED=false
ADMISSION_REVIEW_EXECUTED=false
ADMISSION_APPROVED=false
REGISTRATION_AUTHORIZATION_CREATED=false
DBOS_REGISTRATION_EXECUTED=false
ENTITY_INSTANCE_CREATED=false
ACTIVE_STATE_CREATED=false
PERMISSION_GRANTED=false
SAEE_ADMISSION_APPROVAL_AUTHORITY_CREATED=false
```

---
spec_id: DBA-ADMISSION-DECISION-DATA-CONTRACT-0.1
title: Admission Decision Data Contract v0.1
title_zh: 准入决策数据契约 v0.1
status: non-executable-data-contract-specification
decision_type: admission
decision_object_defined: true
decision_object_instantiated: false
authorization_effect: none
registration_effect: none
permission_effect: none
---

# Admission Decision Data Contract v0.1

本契约定义 `decision_type=admission` 的 Admission Decision Object（准入决策对象）。它是 Governance Decision framework（治理决策框架）的专用数据配置，只记录准入判断，不形成 Registration Authorization、不执行 DBOS Registration，也不创建 Entity。

## 1. Object Definition（对象定义）

Owner：Governance Decision Layer（治理决策层）管理对象定义、状态历史和来源引用。实际 decision authority（决策授权者）由 `decision_authority` 引用；Owner 不等于 authority。

| 字段 | 必需性 | 语义 | 强制边界 |
|---|---|---|---|
| `admission_id` | required | Admission Decision Object 的稳定、不透明标识 | 特化通用 `decision_id`；不等于 Candidate、Authorization 或 Entity ID |
| `decision_type` | required | 固定值 `admission` | 类型分类不产生准入、登记或执行权限 |
| `subject_reference` | required | 被审查 Candidate 的稳定引用 | 不是 canonical `entity_id` |
| `review_reference` | required | 指向完整 Admission Criteria Review | Review 不是 Decision；引用存在不证明内容有效 |
| `review_status` | required | 决策时所依赖的 review status | 必须可验证且不能跳过 required review gate |
| `criteria_summary` | required | 六个准入维度的结果、理由、限制、unknown 和 evidence references 摘要 | 不是综合分数、Evidence truth 或自动批准器 |
| `decision_result` | required | `PENDING`、`APPROVED`、`REJECTED` 或 `REVOKED` | `APPROVED` 不等于 Authorization、Registration、Active 或 Permission |
| `decision_authority` | conditional | 作出最终决定的主体及其 authority record 引用 | `APPROVED` / `REJECTED` 必需；字符串存在不证明 authority 有效 |
| `conditions` | required | 对批准、拒绝、后续授权或复审适用的有界条件 | 不得包含直接 DBOS 写入、Permission grant 或 Active transition |
| `timestamp` | required | 决策事件时间与时间来源 | 时间值不证明签名、有效性或未撤销 |

对象还必须保留 schema/version、provenance、status history、supersession/revocation reference 和 reviewer conflict disclosure。本规范不选择具体 JSON、YAML、数据库或 API 表示。

## 2. Criteria Summary Contract（条件摘要契约）

`criteria_summary` 必须分别记录以下 criterion，不能只保存一个 aggregate score（综合分数）：

| criterion_id | 领域 | 最低内容 |
|---|---|---|
| `ADM-CRIT-01` | Identity Reference | status、reason、source references、unknown/conflict |
| `ADM-CRIT-02` | Owner Responsibility | status、responsible human/owner reference、限制 |
| `ADM-CRIT-03` | Capability Declaration | declared scope、constraints、risk 与 forbidden/unknown |
| `ADM-CRIT-04` | Lifecycle Compatibility | target=`REGISTERED` 与不允许 Activation 的确认 |
| `ADM-CRIT-05` | Evidence Boundary | readiness、source plan、failure/history preservation |
| `ADM-CRIT-06` | Governance Review | reviewer、authority separation、conditions 与 conflict |

缺失、无法验证或冲突的 criterion 必须保留为 `UNKNOWN`、`UNSATISFIED` 或 `CONFLICTED`。不得用 reviewer confidence、SAEE score 或默认值将其改写为满足。

## 3. Decision States（决策状态）

```text
PENDING
  ├─ explicit decision → APPROVED
  └─ explicit decision → REJECTED

APPROVED
  └─ explicit revocation → REVOKED
```

| `decision_result` | 语义 | 允许的下一步 | 不表示 |
|---|---|---|---|
| `PENDING` | 已形成待决记录，尚无最终决定 | 继续审查或由明确 authority 决定 | 将被批准 |
| `APPROVED` | authority 在明确 criteria 与 conditions 下批准 Candidate 准入 | 独立 Registration Authorization issuance review | `AUTHORIZED`、Registered 或 Active |
| `REJECTED` | authority 明确拒绝该次准入 | 保留记录；新材料需要新/修订流程 | Candidate 被删除或永久禁止 |
| `REVOKED` | 既有 Approval 的后续效力被撤销 | 停止新 Authorization；处理关联记录 | 已完成 Registration 自动回滚 |

## 4. Approval Preconditions（批准前提）

`decision_result=APPROVED` 至少要求：

1. `subject_reference`、`review_reference` 与 Candidate materials 可解析；
2. required review 已完成，reviewer scope 与 conflict 记录完整；
3. 六个准入 criterion 均有独立结果和来源；
4. 所有 mandatory criterion 已满足，或 conditions 明确阻止下游授权直到满足；
5. `decision_authority` 的身份、scope、有效期和撤销状态可验证；
6. `conditions` 不扩大 Candidate 声明、Capability、Authority 或 Permission；
7. lifecycle target 不超过 `REGISTERED`；
8. 没有把 SAEE Evaluation、reviewer recommendation 或 DBOS readiness 当作自动批准。

不满足时必须保持 `PENDING` 或形成有理由的 `REJECTED`；不得 fail open（失败开放）。

## 5. Generic Governance Decision Mapping（通用治理决策映射）

| Governance Decision field | Admission Decision field | 规则 |
|---|---|---|
| `decision_id` | `admission_id` | 一对一标识映射 |
| `decision_type` | `decision_type=admission` | 固定值 |
| `source_recommendation` | not applicable | Admission 使用 `subject_reference`、`review_reference`、`criteria_summary`；不得伪造 SAEE Recommendation |
| `review_status` | `review_status` | 保留语义与来源 |
| `decision_result` | `decision_result` | 使用本契约的大写状态 vocabulary（词汇表） |
| `approved_by` | `decision_authority` | 仅在适用状态引用明确 authority |
| `execution_reference` | not stored at decision creation | 后续 DBOS Registration Result 作为独立引用链，不预填执行事实 |

详细流程见 [`admission-governance-mapping.md`](admission-governance-mapping.md)。

## 6. Mutation and History（变更与历史）

- Decision history 必须 append-only 保留；
- 状态变化必须生成有来源事件，不得原地抹除先前状态；
- `REVOKED` 不删除 `APPROVED` 曾经发生的历史事实；
- conditions 的扩大或 subject 变化需要新的 Decision revision/object；
- Registration Authorization 不得修改 Decision Object 后冒充原决定；
- DBOS 不得回写 `decision_result`；执行失败由独立 Registration Result 表达。

## 7. Non-claim Boundary（非声明边界）

Admission Decision Object 不声明：

- Candidate 已成为 Entity；
- Registration Authorization 已签发；
- DBOS Registration 已成功；
- Entity 已 Verified 或 Active；
- Capability、Permission、Runtime、Execution 或 Evidence 已产生；
- SAEE 已评价或认可 Candidate；
- Digital Organism 资格已形成。

## 8. Agent-readable Contract（智能体可读契约）

```text
ADMISSION_DECISION_DATA_CONTRACT_DEFINED=true
DECISION_TYPE=admission
ADMISSION_DECISION_OBJECT_INSTANTIATED=false
SOURCE_RECOMMENDATION_REQUIRED=false
SUBJECT_REFERENCE_REQUIRED=true
CRITERIA_SUMMARY_REQUIRED=true
DECISION_AUTHORITY_REQUIRED_FOR_FINAL_RESULT=true
APPROVED_NE_AUTHORIZED=true
APPROVED_NE_REGISTERED=true
AUTHORIZATION_ISSUED=false
DBOS_REGISTRATION_EXECUTED=false
ENTITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
```


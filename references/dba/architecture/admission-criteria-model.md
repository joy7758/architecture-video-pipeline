---
spec_id: DBA-ADMISSION-CRITERIA-MODEL-0.1
title: Digital Entity Admission Criteria Model v0.1
title_zh: 数字实体准入条件模型 v0.1
status: non-executable-architecture-evaluation-model
criteria_model_defined: true
criteria_evaluation_executed: false
automatic_approval: false
entity_effect: none
permission_effect: none
---

# Digital Entity Admission Criteria Model v0.1（数字实体准入条件模型 v0.1）

本模型定义 Admission Review（准入审查）的评价维度、保守状态和记录要求。它帮助 reviewer 解释候选材料是否足以进入 Admission Decision，不计算自动分数，也不批准、登记或激活 Entity。

```text
Criteria Evaluation ≠ Admission Decision
Criteria Satisfied ≠ Approved
Unknown ≠ Satisfied
Risk Classification ≠ Authorization
```

## 1. Criteria Record（条件评价记录）

每个条件评价至少表达：

| 字段 | 语义 |
|---|---|
| `criterion_id` | 稳定条件标识 |
| `candidate_id` | Candidate reference；不是 `entity_id` |
| `dimension` | 本规范定义的评价维度 |
| `criteria_status` | `SATISFIED`、`SATISFIED_WITH_CONDITIONS`、`UNSATISFIED`、`UNKNOWN` 或 `NOT_APPLICABLE` |
| `material_references` | 支持判断的候选材料、来源和版本引用 |
| `reviewer_reference` | reviewer 或审查记录引用；不是 decision authority |
| `conditions` | 必须在登记授权或 DBOS Registration 前满足的条件 |
| `limitations` | 未覆盖范围、不确定性、冲突和过期条件 |

这些是 conceptual fields（概念字段），不是已实现 schema、API 或 Criteria Object instance。

`NOT_APPLICABLE` 需要明确理由，不能用于跳过 [`digital-entity-admission-specification.md`](digital-entity-admission-specification.md) 定义的六项最低条件。

## 2. Admission Evaluation Dimensions（准入评价维度）

### 2.1 Identity Completeness（身份完整性）

检查：

- Candidate reference 是否稳定且与 Repository、Agent name、Runtime ID 区分；
- 提议者、来源、版本和候选材料是否可追溯；
- 是否明确未来由 DBOS 分配或解析 canonical Entity Identity；
- 是否存在重复候选、冲突身份或无法解析来源。

Identity Completeness 不要求 Candidate 已有 `entity_id`。提前填充 `entity_id` 不能提高准入分数，反而必须作为身份边界冲突审查。

### 2.2 Capability Clarity（能力清晰度）

检查：

- 拟议 Capability 名称、description、scope 和 constraints 是否明确；
- Allowed、Limited、Forbidden 与 Unknown 是否可区分；
- 是否把 Capability Declaration 错写成 Verified、Authorized 或 Permission；
- Capability profile 是否与候选角色和生命周期目标一致。

Capability Clarity 评价描述完整性，不验证候选实际拥有能力。

### 2.3 Risk Level（风险等级）

检查：

- risk level、影响对象、外部副作用、可逆性和影响半径；
- 数据、身份、金融、医疗、安全和外部系统风险；
- 未知风险、条件、缓解措施和停止规则；
- 风险分类来源及版本。

风险为 Low 不自动批准；风险为 High/Critical 也不由本模型自动拒绝，而是要求更严格治理。风险未知且可能改变决定时必须保持 `UNKNOWN` 或 `UNSATISFIED`，不能默认 Low。

### 2.4 Evidence Readiness（证据就绪度）

检查：

- 输入、过程、输出、失败和版本的 provenance plan（来源计划）；
- 初始 Execution/Evidence History 是否明确为空或有来源，而不是缺失；
- canonical Evidence Owner、integrity 和 Verification 边界是否与 DBOS 规范一致；
- 历史保留、更正、撤销和失败记录是否可追溯。

Evidence Readiness 表示未来可形成记录的治理准备，不创建 Evidence Object，也不证明 Candidate、Capability 或描述真实。

### 2.5 Human Responsibility（人类责任）

检查：

- Owner/Human Research Owner 或其他责任主体引用；
- 监督、异常处理、数据责任、最终判断和外部发布责任；
- 责任主体是否同意并理解候选范围；
- 责任中断、撤回和替代机制。

Human responsibility 不把人类的广泛权限转移给 Candidate，也不使 Candidate 成为 Scientist、Author 或最终责任主体。

### 2.6 Governance Compatibility（治理兼容性）

检查：

- Candidate role、requested entity type 与 Architecture classification 是否有显式映射；
- Lifecycle target 是否仅为 `REGISTERED`；
- 是否遵守 SAEE/DBOS、Decision/Execution 与 Capability/Permission 分离；
- 是否存在冲突、重复建设、无 authority 的批准或绕过 DBOS 的路径；
- Admission Decision、Registration Authorization 和 DBOS Registration 是否保持独立。

Governance Compatibility 不表示采用方已经接受规范，也不授权 DBOS 实现。

## 3. Criteria Outcome（条件评价结果）

| 结果 | 语义 | 允许的下一步 | 禁止推断 |
|---|---|---|---|
| `SATISFIED` | 在声明范围内材料充分 | 提交 Admission Decision | 将被批准 |
| `SATISFIED_WITH_CONDITIONS` | 基本材料充分，但有必须保留的条件 | 将 conditions 带入 Decision | 条件会自动满足 |
| `UNSATISFIED` | 明确不符合最低条件 | 拒绝、补充或重新提交 | 自动永久禁止 |
| `UNKNOWN` | 证据或规则不足 | 保持待审或补充材料 | 当作满足 |
| `NOT_APPLICABLE` | 非最低条件在有理由时不适用 | 保留理由 | 跳过强制条件 |

本模型不采用总分阈值。某一维度的高分不能抵消身份来源缺失、权限混淆或生命周期越权。

## 4. Review Recommendation（审查建议）

Reviewer 可以形成：

- `eligible_for_decision`；
- `eligible_with_conditions`；
- `not_eligible`；
- `insufficient_information`。

这些 recommendation（建议）不是 Admission Decision。Reviewer 只有在另有明确、可追溯授权时才能同时承担 decision authority；即使角色由同一人承担，Review record 与 Decision record 仍必须分离。

## 5. Fail-closed Rules（失败关闭规则）

1. `UNKNOWN` 不得自动转换为 `SATISFIED`；
2. 缺少 Owner/Human responsibility 时不得进入无条件批准；
3. Capability Declaration 不得被当作 Capability Verification；
4. Evidence Readiness 不得被当作 Evidence existence 或 truth；
5. `requested_lifecycle_state=ACTIVE` 必须判定为不兼容；
6. reviewer reference 不得冒充 decision authority；
7. criteria 结果不得直接触发 DBOS Registration；
8. conditions 必须在 Decision、Authorization 与 Registration records 中保持可追溯。

## 6. Non-implementation Status（非实现状态）

```text
ADMISSION_CRITERIA_MODEL_DEFINED=true
CRITERIA_RECORD_INSTANCE_CREATED=false
CRITERIA_EVALUATION_EXECUTED=false
AUTOMATIC_SCORE_CALCULATED=false
ADMISSION_AUTOMATICALLY_APPROVED=false
CAPABILITY_VERIFIED=false
EVIDENCE_CREATED=false
ENTITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
```

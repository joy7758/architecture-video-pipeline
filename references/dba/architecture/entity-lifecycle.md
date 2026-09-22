---
spec_id: DBA-ENTITY-LIFECYCLE-0.1
title: Digital Entity Lifecycle v0.1
status: conceptual-lifecycle-specification
creates_entity: false
creates_identity: false
grants_capability: false
grants_permission: false
definition_reference: digital-entity-specification.md
admission_reference: digital-entity-admission-specification.md
admission_process_implemented: false
registration_authorized: false
---

# Digital Entity Lifecycle v0.1（数字主体生命周期 v0.1）

## 1. Definition source 与状态生命周期

Digital Entity 的正式定义、最低要求与 Entity/Repository/Agent/Runtime 边界以 [`digital-entity-specification.md`](digital-entity-specification.md) 为准。

Canonical Entity State Lifecycle（规范实体状态生命周期）仍由七个状态组成。Admission 是 `Proposed → Registered` 之间的强制治理过程，不是第八个 Entity state：

```text
Proposed Candidate
    ↓ Admission Review
Decision Pending
    ↓ Approved + separate Registration Authorization
DBOS Registration
    ↓ canonical record formed
Registered
    ↓
Verified
    ↓
Active
    ↓
Evaluated
    ↓
Adapted
    ↓
Retired
```

| 状态 | 首要治理责任 | 关键边界 |
|---|---|---|
| Proposed | 提议者 / Architecture Governance | Entity Candidate，不是已创建或注册实体 |
| Registered | DBOS | 已登记最低记录，不等于 Verified、Active 或 Authorized |
| Verified | DBOS | 有界身份与最低记录验证，不等于执行权 |
| Active | DBOS | 可被治理和接受另行授权，不等于当前运行或无限自治 |
| Evaluated | SAEE 参与；DBOS 保持状态 Owner | Evaluation 不直接修改状态 |
| Adapted | SAEE 建议；Governance Decision 采纳；DBOS 执行、验证并记录 | Adapted 不自动等于改进或新权限 |
| Retired | DBOS | 历史保留，不删除 Identity、Execution 或 Evidence 记录 |

DBOS 管理 Registered、Verified、Active 和 Retired。SAEE 参与 Evaluated 与 Adapted，但只产生 Evaluation 与 Recommendation；Governance Decision 决定是否采纳，DBOS 执行和记录变化。

Admission 的完整条件、Decision 与异常路径见 [`digital-entity-admission-specification.md`](digital-entity-admission-specification.md)。`Approved`、Registration Authorized 与 Registered 是不同事实；没有 DBOS Registration record 时必须继续称为 Candidate。

## 2. Responsibility Processing Lifecycle（责任处理生命周期）

```text
Admission
    ↓
Registration
    ↓
Identity
    ↓
Capability
    ↓
Execution
    ↓
Evidence
    ↓
Verification
    ↓
Evaluation
    ↓
Evolution
    ↓
Retirement
```

该十阶段序列是 responsibility processing view（责任处理视图），不是 Entity State 枚举。Admission 发生在 Entity 创建前；其余阶段说明 Identity、Capability、Execution、Evidence、Verification、Evaluation 与 Evolution 分别由谁处理。该视图不与七状态 Entity State Lifecycle 竞争，也不是已实现 workflow（工作流）、自动状态机或执行授权。

## 3. 阶段职责

| stage_id | 阶段 | 首要责任域 | 阶段输出语义 | 强制边界 |
|---|---|---|---|---|
| `LIFECYCLE-00` | Admission（准入） | 明确 reviewer / decision authority；Governance Decision Layer 记录；Architecture 定义规则 | Candidate criteria review、Admission Decision 与 Registration Authorization 引用 | Admission 不创建 Entity、Active、Capability 或 Permission；SAEE 不能批准，DBOS 不能跳过 Decision |
| `LIFECYCLE-01` | Registration（注册） | DBOS | 主体候选记录及其注册状态 | 注册不等于身份已验证、能力已确认或获得权限 |
| `LIFECYCLE-02` | Identity（身份） | DBOS | 可引用身份及其验证状态 | 身份引用必须与能力、权限和生命状态分离 |
| `LIFECYCLE-03` | Capability（能力） | DBOS | 声明、证据支持和状态化的能力记录 | 登记能力不创造真实能力；未知保持未知 |
| `LIFECYCLE-04` | Execution（执行） | DBOS | 在既定授权边界内的执行记录 | 本规范不创建执行权，也不证明 DBOS 已实现执行能力 |
| `LIFECYCLE-05` | Evidence（证据） | DBOS | 有来源与范围的 Evidence Bundle | 采集成功不等于主张被证明 |
| `LIFECYCLE-06` | Verification（验证） | DBOS | 有界 Verification Result | 验证只覆盖明确对象、规则和输入 |
| `LIFECYCLE-07` | Evaluation（评价） | SAEE | Fitness Assessment、Risk Assessment 等派生评价 | 评价不修改 DBOS，不自动成为选择或授权 |
| `LIFECYCLE-08` | Evolution（演化） | SAEE | Evolution Recommendation、Governance Suggestion 与模型结果 | SAEE 负责演化建模和建议，不直接执行 DBOS 状态变化 |
| `LIFECYCLE-09` | Retirement（退役） | DBOS 的 Existence Governance（存在治理） | 生命周期终止、停用或归档状态记录 | SAEE 可以建议退役；最终授权主体未由本规范指定；退役不抹除历史证据 |

## 4. 责任分段

### 4.1 DBOS 负责

- Registration；
- Identity；
- Capability；
- Execution；
- Evidence；
- Verification；
- Retirement 的生命周期状态记录。

DBOS 的阶段责任属于 Existence Governance，不表示所有动作都可自动执行。每个具体部署仍需独立定义授权主体、状态转换规则和审计要求。

DBOS 不负责作出 Admission Decision。它读取并验证已批准、已采纳且另有有效 Registration Authorization 的准入材料，然后决定自身登记约束是否允许执行；失败时保持 Candidate 或明确失败状态。

### 4.2 SAEE 负责

- Evaluation；
- Evolution。

SAEE 的“负责”指评价、建模和建议责任，不包含修改 DBOS 身份、能力、执行或退役状态的权限。

### 4.3 Digital Entity 负责

Digital Entity 在 Execution 阶段承担具体任务行为，在 Evidence 阶段成为行为和结果材料的来源之一。Canonical Evidence Object 仍由 DBOS 管理；Digital Entity 不是身份、证据、验证或适应度的自证权威。

## 5. 阶段 gate（闸门）

| 转换 | 最小前提 | 不得自动发生的提升 |
|---|---|---|
| Candidate Submission → Admission Review | Candidate Proposal、reviewer scope、来源与材料可解析 | “已提交” → “已审查/批准” |
| Admission Review → Registration | Admission Decision=`APPROVED`、独立 Registration Authorization 有效、conditions 满足、DBOS checks 通过 | “Review/Approved/Authorized” → “Registered” |
| Registration → Identity | 存在可核验的身份材料与状态规则 | `registered` → `verified` |
| Identity → Capability | 身份可引用，能力声明与支持材料可区分 | “有身份” → “有能力” |
| Capability → Execution | 能力状态、授权范围、资源与策略条件均明确 | “声明能力” → “获准执行” |
| Execution → Evidence | 执行记录可定位，采集范围明确 | “执行完成” → “证据完整” |
| Evidence → Verification | 验证对象、规则、输入与版本明确 | “有证据” → “主张成立” |
| Verification → Evaluation | SAEE 获得足够且可追溯的输入 | “验证通过” → “适应度高” |
| Evaluation → Evolution | 目标、环境、风险和不确定性已表达 | “评价完成” → “建议已采用” |
| Evolution → Retirement / new cycle | 独立授权与 DBOS 生命周期规则明确 | “建议退役/变化” → “状态已改变” |

## 6. 演化回环

Evolution 产生的建议若被独立授权采用，应回到 DBOS 所管理的相应生命周期阶段重新登记、验证或执行，而不是绕过生命周期：

```text
Evolution Recommendation
    ↓ independent authorization（独立授权；本规范不授予）
DBOS-managed lifecycle stage
    ↓ new records and evidence（新记录与证据）
SAEE re-evaluation（重新评价）
```

这不是自动闭环。建议、授权、实施、记录、验证和再评价必须保持为不同状态。

## 7. Retirement 未决点的 v0.1 处理

原始阶段清单包含 Retirement，但前六阶段与后两阶段的责任分段未显式指定它。v0.1 依据“DBOS 管理生命周期、SAEE 管理演化”的总原则，将 Retirement 的状态所有权归入 DBOS Existence Governance；SAEE 只能提供相关风险或演化建议。谁拥有最终退役授权仍是 deployment-specific（部署特定）的未决治理问题，本规范不自行创造该权限。

## 8. Admission 非实现状态

```text
ADMISSION_STAGE_DEFINED=true
ADMISSION_PROCESS_IMPLEMENTED=false
ADMISSION_DECISION_INSTANCE_CREATED=false
REGISTRATION_AUTHORIZATION_CREATED=false
DBOS_REGISTRATION_EXECUTED=false
ENTITY_INSTANCE_CREATED=false
ACTIVE_STATE_CREATED=false
PERMISSION_GRANTED=false
```

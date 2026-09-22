---
spec_id: DBA-ADMISSION-GOVERNANCE-MAPPING-0.1
title: Admission and Governance Decision Mapping v0.1
title_zh: 准入与治理决策映射 v0.1
status: non-executable-architecture-mapping
mapping_defined: true
mapping_applied: false
decision_instance_created: false
authorization_instance_created: false
registration_executed: false
---

# Admission and Governance Decision Mapping v0.1

本规范定义 Governance Decision（治理决策）框架与 Admission Decision（准入决策）类型之间的映射，以及它们与 Registration Authorization（登记授权）和 DBOS Registration（DBOS 登记执行）的边界。它不创建 Decision、Authorization、Entity 或 Permission，也不调用 DBOS。

```text
Governance Decision = decision framework
Admission Decision = decision_type: admission
Admission Decision ≠ Registration Authorization
Registration Authorization ≠ DBOS Registration
Governance Decision ≠ Execution
```

## 1. Decision Hierarchy（决策层级）

```text
Architecture Governance
  defines decision rules（定义决策规则）
        ↓
Governance Decision Framework
  defines common decision semantics（定义通用决策语义）
        ↓ decision_type=admission
Admission Decision
  records explicit admission judgment（记录明确准入判断）
        ↓ separate issuance gate
Registration Authorization
  permits a bounded DBOS registration attempt（允许有界登记尝试）
        ↓ DBOS pre-registration checks
DBOS Registration
  executes the approved governance result（执行已批准治理结果）
```

上图表示 framework specialization（框架特化）与受控交接，不表示 Architecture Governance、Decision Layer 或 Admission Reviewer 可以写入 DBOS，也不表示 DBOS 可以作出 Admission Decision。

## 2. Governance Decision 与 Admission Decision

Governance Decision Object 是通用框架。Admission Decision Object 是该框架的 versioned decision profile（版本化决策配置）：

| 通用语义 | Admission profile（准入配置） | 边界 |
|---|---|---|
| `decision_id` | `admission_id` | 标识准入决策记录，不是 Authorization ID 或 Entity ID |
| `decision_type` | 固定为 `admission` | 类型值不产生权限 |
| decision subject | `subject_reference` | 指向 Candidate，不是 canonical Entity Identity |
| governance input | `review_reference` + `criteria_summary` | 不得虚构 SAEE Recommendation |
| `review_status` | Admission review status | Review 不等于 Approval |
| `decision_result` | `PENDING` / `APPROVED` / `REJECTED` / `REVOKED` | `APPROVED` 不等于 Authorization 或 Registration |
| `approved_by` | `decision_authority` | 仅引用实际 authority；Decision Layer 不是批准者 |
| execution linkage | 后续 Registration Result reference | 决策形成时不得预填执行事实 |

Admission Decision 的规范字段以 [`admission-decision-data-contract.md`](admission-decision-data-contract.md) 为准。通用框架中的 `source_recommendation` 对 recommendation-originated decision（建议来源决策）是必需字段；对 `decision_type=admission` 不适用，必须由 `subject_reference`、`review_reference` 和 `criteria_summary` 表达治理输入。不得为了满足字段形状而伪造 SAEE Recommendation。

## 3. Admission Governance Flow（准入治理流程）

```text
Recommendation
    ↓
Review
    ↓
Decision
    ↓
Authorization
    ↓
Execution
```

| 阶段 | Admission 语义 | 形成的记录 | Owner / actor | 不表示 |
|---|---|---|---|---|
| Recommendation | Admission Reviewer 对 criteria 形成有来源、非绑定的 reviewer recommendation | Admission Criteria Review | Review record 由治理流程保存；reviewer 负责内容 | SAEE Recommendation、Decision 或 Approval |
| Review | 检查 Candidate、责任、能力声明、风险、证据准备与治理兼容性 | Review status、criteria result 与限制 | 明确 Admission Reviewer | Decision 已形成 |
| Decision | 显式 decision authority 对 Candidate 准入作出 `APPROVED`、`REJECTED` 或后续 `REVOKED` 判断 | Admission Decision Object | Governance Decision Layer 管理记录；明确 authority 作出判断 | Registration Authorization、Registered 或 Active |
| Authorization | 明确 issuer 把已批准 Decision 转换为有界登记授权 | Registration Authorization Object | Governance Decision Layer 管理记录；issuer 作出签发 | Permission、Capability Grant 或 Registration success |
| Execution | DBOS 验证 Authorization 和自身约束后尝试形成 canonical registration record | Registration Result / Entity registration record | DBOS | Active、Capability、Permission 或科学/演化结论 |

这里的 Recommendation 是 admission-domain reviewer recommendation（准入领域审查者建议），不是 SAEE 的 Evolution Recommendation。SAEE 可以提供非绑定 risk/evaluation material（风险/评价材料），但不是准入链的必需决策来源，也不拥有准入或登记权。

在 `decision_type=admission` profile 中，Registration Authorization 是特定 registration scope 的 explicit adoption/authorization record（显式采纳/授权记录）。它承接通用 Decision Lifecycle 的 Adoption 语义，但不把 `APPROVED` 改名为 `AUTHORIZED`，也不消除独立 issuer、scope、有效期和撤销检查。

## 4. State Mapping（状态映射）

| 上游状态 | 可进入的下游 gate | 禁止推断 |
|---|---|---|
| Review complete | Decision Pending | 将被批准 |
| Admission `APPROVED` | Authorization issuance review | 已 `AUTHORIZED` |
| Admission `REJECTED` | 无登记授权路径 | Candidate 或历史被删除 |
| Admission `REVOKED` | 停止新授权；处理既有授权冲突 | 已登记事实被追溯删除 |
| Authorization `AUTHORIZED` 且有效 | DBOS pre-registration checks | 已 Registered |
| Authorization `PENDING` / `REJECTED` / `REVOKED` / ineffective | fail closed | DBOS 可自行改写上游状态 |
| DBOS Registration succeeded | `REGISTERED` lifecycle record | Verified、Active 或 Permission |

所有跨层状态转换都必须形成新记录或有来源引用；不得覆盖上游对象来制造下游事实。

## 5. Authority Mapping（权力映射）

| 角色 | 可以 | 不能 |
|---|---|---|
| Architecture Governance | 定义规则和 ADR | 审批具体 Candidate、签发 Authorization 或执行登记 |
| Admission Reviewer | 形成 criteria review 与 reviewer recommendation | 作出最终 Decision，除非另有独立且明确的 authority assignment |
| Decision Authority | 作出 Admission Decision | 直接写 DBOS、授予 Permission 或激活 Entity |
| Authorization Issuer | 在明确 authority 和 scope 内签发 Registration Authorization | 扩大 Decision conditions、授予 Permission 或保证登记成功 |
| DBOS | 验证授权并执行有界 Registration | 发明 Admission conclusion、补造 Authorization 或产生演化判断 |
| SAEE | 提供非绑定 Evaluation/Risk material | 批准 Admission、签发 Authorization、登记或激活 Entity |

## 6. Agent-readable Mapping（智能体可读映射）

```text
GOVERNANCE_DECISION_FRAMEWORK_DEFINED=true
ADMISSION_DECISION_TYPE=admission
ADMISSION_DECISION_CONTRACT=admission-decision-data-contract.md
REGISTRATION_AUTHORIZATION_CONTRACT=registration-authorization-contract.md
SOURCE_RECOMMENDATION_REQUIRED_FOR_ADMISSION=false
FABRICATE_SAEE_RECOMMENDATION=false
ADMISSION_DECISION_NE_AUTHORIZATION=true
AUTHORIZATION_NE_REGISTRATION=true
REGISTRATION_NE_PERMISSION=true
MAPPING_APPLIED=false
DECISION_INSTANCE_CREATED=false
AUTHORIZATION_INSTANCE_CREATED=false
DBOS_REGISTRATION_EXECUTED=false
```

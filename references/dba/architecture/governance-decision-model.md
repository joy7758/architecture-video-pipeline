---
spec_id: DBA-GOVERNANCE-DECISION-MODEL-0.1
title: Digital Biosphere Governance Decision Model v0.1
title_zh: 数字生物圈治理决策模型 v0.1
status: non-executable-architecture-specification
decision_layer_role: decision-record-and-state-boundary
decision_layer_is_runtime: false
decision_layer_is_entity: false
decision_layer_is_dbos_module: false
decision_layer_is_saee_module: false
final_authorizer_defined: false
capability_effect: none
evidence_effect: none
authority_effect: none
---

# Digital Biosphere Governance Decision Model v0.1

本规范定义 Recommendation（建议）或经版本化声明的 domain governance input（领域治理输入）如何经过 Review（审查）、Decision（决策）、Adoption（采纳）、Execution（执行）和 Verification（验证），形成受控且可追溯的 governance loop（治理闭环）。Recommendation-originated decision（建议来源决策）是通用默认配置；`decision_type=admission` 使用 Candidate、Admission Review 与 criteria summary，不要求或伪造 SAEE Recommendation。

Governance Decision Layer（治理决策层）是在 Architecture Governance（架构治理）规则下工作的 Decision record and state boundary（决策记录与状态边界），但不等于完整的 Architecture Authority。它不是 DBOS 模块、SAEE 模块、Runtime（运行时）、Agent（智能体）或 Digital Entity（数字主体），也不自带授权者；`approved_by` 必须引用本规范之外明确确认的授权主体。

## 1. 核心不变量

```text
RECOMMENDATION_NE_DECISION=true
EVALUATION_NE_AUTHORITY=true
DECISION_NE_EXECUTION=true
EXECUTION_REQUIRES_DBOS_LIFECYCLE_CONTROL=true
DECISION_OBJECT_MODIFIES_OPERATIONAL_FACTS=false
```

1. Recommendation != Decision：SAEE 建议不是命令或决策。
2. Evaluation != Authority：产生评价不自动获得审查、批准或执行权。
3. Decision != Execution：批准或采纳记录不证明变化已经执行。
4. Execution requires DBOS lifecycle control：任何获准变化必须回到 DBOS 的能力、执行、证据、验证和生命周期边界。

## 2. Decision Lifecycle（决策生命周期）

```text
Recommendation / Governance Input Created
        ↓
Review Pending
        ↓
Under Review
      ↙     ↘
Rejected   Approved
              ↓
           Adopted
              ↓
           Executed
              ↓
           Verified
```

`Approved` 与 `Rejected` 是 `Under Review` 之后的互斥分支，不是连续阶段。被拒绝的 Decision Object 不得继续进入 Adopted；如需重新审查，应引用新的或修订后的 Recommendation，并创建新的 Decision Object。

| 生命周期阶段 | 责任角色 | 所形成的记录 | 不表示 |
|---|---|---|---|
| Recommendation Created / Governance Input Recorded | SAEE 或显式定义的 originating domain | Recommendation Object，或版本化的领域治理输入 | Decision、Authorization 或 Execution |
| Review Pending | Governance Decision Layer | Decision Object 候选及待审状态 | 已开始审查或已批准 |
| Under Review | 明确授权的 reviewer（审查者） | 审查过程、范围与来源记录 | 已形成 Decision |
| Approved | 明确授权的 decision authority（决策授权者） | `decision_result=approved` 与 `approved_by` | 已采纳、已执行或能力已改变 |
| Rejected | 明确授权的 decision authority | `decision_result=rejected` 及理由来源 | Recommendation 被删除或事实被改写 |
| Adopted | 明确授权的 adoption authority（采纳授权者） | 决策进入受控变更路径的采纳记录 | DBOS 已执行变化 |
| Executed | DBOS | `execution_reference` 指向的执行记录与 Evidence | 执行已验证、决策正确或结果有效 |
| Verified | DBOS Verification | 有界 Verification Result | 全局正确、永久有效或 SAEE 评价已更新 |

Review、Decision 与 Adoption 的授权主体可以由具体治理制度定义，但 v0.1 不创建或指定这些主体。Architecture Governance 定义规则，Governance Decision Layer 记录状态；二者都不冒充授权主体。

## 3. Governance Decision Object（治理决策对象）

Owner：Governance Decision Layer

Purpose（目的）：记录一个 Recommendation 或明确领域治理输入的审查、决策、采纳和后续执行引用，使治理输入、Decision、Execution 与 Verification 保持不同 truth surface（事实表面）。

| 字段 | 语义 | 状态约束 |
|---|---|---|
| `decision_id` | Decision Object 的稳定、不透明标识符 | 必须唯一引用该决策记录；不等于执行标识 |
| `source_recommendation` | 对 SAEE Recommendation Object 的不可变引用 | 对 recommendation-originated decision 必须存在；对有独立数据契约的 domain profile 可以明确为不适用，且不得伪造建议 |
| `decision_type` | 决策类型 | 必须是本规范定义或后续版本化的类型 |
| `review_status` | 审查与治理状态 | 必须遵循治理状态机，不得跳过必要 gate（闸门） |
| `decision_result` | `pending`、`approved`、`rejected` 或 `revoked` 的决策结果 | `approved` 必须有显式授权来源；其他状态不得伪造批准者 |
| `approved_by` | 显式批准主体或授权记录的引用 | 仅在批准状态必需；未批准或被拒绝时必须为空或不适用 |
| `execution_reference` | 指向 DBOS Execution Object 的引用 | 在执行前必须为空；Decision Object 不能自行生成执行事实 |

Decision Object 还必须复用接口通用追溯语义：版本、来源、时间、scope（范围）、provenance references（来源引用）、状态、限制与理由。

Domain profile 必须通过版本化数据契约声明 subject、review input、状态词汇和通用字段映射。Admission Decision 的配置见 [`admission-decision-data-contract.md`](admission-decision-data-contract.md) 与 [`admission-governance-mapping.md`](admission-governance-mapping.md)。它使用 `subject_reference`、`review_reference` 和 `criteria_summary`，不把 Candidate 准入伪装成 SAEE 演化建议。

### 3.1 Decision Object 不修改事实

创建 Decision Object 会形成一条新的 governance record（治理记录），但不会修改：

- Entity Object；
- Capability record 或 capability truth（能力事实）；
- Execution Object；
- Evidence Object 或 evidence truth（证据事实）；
- SAEE Evaluation 或 Recommendation；
- DBOS lifecycle state（生命周期状态）。

只有 DBOS 在另行有效的授权、采纳和生命周期控制下执行变化后，才可以产生新的运行记录；是否改变能力或生命周期事实仍需执行 Evidence 与 Verification 支持。

## 4. Decision Types（决策类型）

| `decision_type` | 决策名称 | 典型来源 | 决策范围 | 强制边界 |
|---|---|---|---|---|
| `evolution` | Evolution Decision（演化决策） | Evolution Recommendation | 是否采纳某一演化方向 | 决策层不生成演化结论；DBOS 不改写 SAEE 结论 |
| `capability_change` | Capability Change Decision（能力变更决策） | Fitness/Risk Evaluation 或 Governance Suggestion | 是否允许进入能力变更流程 | Approved/Adopted 不改变 capability truth；DBOS 执行与验证后另行形成记录 |
| `lifecycle` | Lifecycle Decision（生命周期决策） | Risk Assessment、Evolution Recommendation 或治理输入 | 是否允许进入 DBOS 生命周期变化流程 | Decision Object 不直接修改 `lifecycle_state` |
| `governance_policy` | Governance Policy Decision（治理策略决策） | Governance Suggestion | 是否采纳候选治理策略 | 不自动成为 DBOS policy，不修改 SAEE 算法 |
| `admission` | Admission Decision（准入决策） | Candidate、Admission Criteria Review 与 Registration Request | Candidate 是否可进入独立 Registration Authorization 审查 | `APPROVED` 不等于 Authorization、DBOS Registration、Active 或 Permission |

这些类型是决策记录分类，不是新增运行能力、API、权限或可执行命令类型。

## 5. Authority Separation（权限分离）

```text
SAEE
  produces Recommendation（产生建议）
        ↓
Governance Decision Layer
  records Review, Decision and Adoption（记录审查、决策与采纳）
        ↓ explicit authorization required（需要显式授权）
DBOS
  executes adopted change under lifecycle control（在生命周期控制下执行已采纳变化）
        ↓
DBOS Verification
  records bounded verification result（记录有界验证结果）
```

该图描述 SAEE recommendation-originated flow（SAEE 建议来源流程）。Admission flow 是同一 Decision framework 的领域配置：Admission Reviewer 提供非绑定 review input，明确 Decision Authority 作出 Admission Decision，明确 issuer 另行签发 Registration Authorization，DBOS 才可执行有界登记。SAEE 不因此获得准入或登记权。

| 架构角色 | 产生的规范对象或记录 | 权限边界 |
|---|---|---|
| SAEE | 产生 Recommendation Object | 不产生 Decision，不执行建议 |
| Governance Decision Layer | 在显式授权记录支持下产生 Governance Decision Object | 不自行成为授权者，不修改 SAEE 或 DBOS 对象 |
| DBOS | 执行已批准且已采纳的变化，并产生 Execution、Evidence 与 Verification 记录 | 不发明演化结论，不把 Decision 自动当作执行事实 |

### 5.1 SAEE

- 产生 Evaluation 与 Recommendation；
- 提供理由、置信范围和来源引用；
- 不审查并批准自己的建议；
- 不采纳、执行或验证 DBOS 状态变化。

### 5.2 Governance Decision Layer

- 拥有 Decision Object 的规范和状态转换语义；
- 记录明确授权者作出的 Review、Decision 与 Adoption；
- 不生成 SAEE 演化结论；
- 不成为授权者、执行者或 Verification 事实权威；
- 不修改 DBOS 对象或 SAEE 对象。

### 5.3 DBOS

- 检查已批准且已采纳的 Decision Object 是否满足自身生命周期与运行约束；
- 只在另行有效的授权范围内执行；
- 产生 Execution、Evidence 与 Verification 记录；
- 不发明 Evolution Conclusion（演化结论），不修改 SAEE 模型或建议；
- 可以因生命周期、能力、权限或安全约束拒绝执行，并形成明确记录。

## 6. Adoption 与 Execution 的分离

Adoption 表示一个已批准 Decision 被接受进入受控变更路径。它不保证：

- DBOS 能够执行；
- 当前授权仍有效；
- 所需能力存在；
- 执行已开始或完成；
- 验证一定通过。

DBOS 在执行前仍必须检查 Decision Object、授权范围、生命周期状态、能力边界、依赖条件和撤销状态。检查失败时不得执行，并必须保留原因。

## 7. Verification 与闭环

Execution 必须产生 Evidence，并由 DBOS 形成有界 Verification Result。只有满足以下条件，Decision Lifecycle 才能进入 Verified：

1. `execution_reference` 指向可解析的 DBOS Execution Object；
2. Execution 产生有来源、有范围的 Evidence Object；
3. Verification Result 明确对象、规则、输入、版本和状态；
4. Decision Object、Execution Object 与 Evidence Object 的引用链可追溯；
5. 没有把“执行完成”自动解释为“建议正确”或“适应度提高”。

Verified 关闭的是本次决策执行的验证回路，不自动修改原 Recommendation，也不自动触发新的 SAEE Evaluation。若需要再评价，DBOS 必须把新的执行、证据和验证记录作为新的 SAEE 输入。

## 8. 非实现状态

```text
GOVERNANCE_DECISION_MODEL_DEFINED=true
ADMISSION_DECISION_TYPE_DEFINED=true
ADMISSION_GOVERNANCE_MAPPING_DEFINED=true
GOVERNANCE_DECISION_RUNTIME_CREATED=false
GOVERNANCE_DECISION_ENTITY_CREATED=false
DECISION_OBJECT_INSTANCE_CREATED=false
ADMISSION_DECISION_OBJECT_INSTANCE_CREATED=false
FINAL_AUTHORIZER_DEFINED=false
DECISION_EXECUTION_AUTOMATED=false
CAPABILITY_TRUTH_CHANGED=false
EVIDENCE_TRUTH_CHANGED=false
```

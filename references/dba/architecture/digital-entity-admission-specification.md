---
spec_id: DBA-DIGITAL-ENTITY-ADMISSION-0.1
title: Digital Entity Admission Specification v0.1
title_zh: 数字实体准入规范 v0.1
status: non-executable-architecture-specification
admission_model_defined: true
admission_process_implemented: false
registration_authorized: false
registration_authorization_contract_defined: true
entity_instance_created: false
agent_instance_created: false
runtime_created: false
capability_instance_created: false
permission_granted: false
---

# Digital Entity Admission Specification v0.1（数字实体准入规范 v0.1）

本规范定义 Candidate（候选对象）如何经过 Admission Review（准入审查）、显式治理决定和 DBOS Registration（DBOS 登记）成为 Registered Entity（已登记数字实体）。它是 architecture rule（架构规则），不是审批系统、API、DBOS 实现或实体创建授权。

```text
Candidate ≠ Entity
Admission ≠ Activation
Registration ≠ Permission
Capability Declaration ≠ Capability Verification
Governance Decision ≠ DBOS Execution
```

## 1. Admission Definition（准入定义）

Admission 是 Candidate 到 Registered Entity 的受控准入过程。它检查候选材料是否满足最低架构条件，记录独立审查和明确决定，并在另有有效 Registration Authorization（登记授权）时允许 DBOS 进入登记处理。

Admission 不是：

- Activation（激活）；
- Permission Grant（权限授予）；
- Capability Verification（能力验证）；
- Entity Identity 的提前分配；
- DBOS Registration 已经发生的证明；
- SAEE Evaluation 或 Digital Organism qualification（数字有机体资格）。

Admission 的完成只可能使候选具备进入 DBOS Registration 的资格。只有 DBOS 实际形成 canonical Entity record（规范实体记录）后，才能描述为 Registered Entity。

## 2. Admission Inputs（准入输入）

Admission Review 至少需要以下有来源材料：

| 输入 | 最低语义 | 不表示 |
|---|---|---|
| Candidate Proposal | `candidate_id`、候选类型、角色、描述、提议者引用和状态 | 已有 `entity_id` |
| Candidate Review | reviewer、范围、结论、限制和来源引用 | 已批准准入或已注册 |
| Registration Request | 请求类型、架构映射、请求状态和候选引用 | DBOS 必须接受或执行 |
| Responsibility Material | Owner/Human responsibility 与监督边界 | 所有权、作者身份或无限控制权 |
| Capability Declarations | 拟议能力、scope、constraints、unknown 与 forbidden 项 | Capability Object、Verification、Authorization 或 Permission |
| Risk and Evidence Readiness | 风险分类、来源计划、历史容器和验证边界 | Evidence Object 已创建或内容正确 |

缺失、冲突、过期或无法解析的输入必须保持 `unknown`、`incomplete` 或 `conflicted`，不得用默认值补造准入资格。

## 3. Admission Criteria（准入条件）

最低条件如下；详细评价模型见 [`admission-criteria-model.md`](admission-criteria-model.md)。

| criterion_id | 最低条件 | 必须回答 | 强制边界 |
|---|---|---|---|
| `ADM-CRIT-01` | Identity Reference（身份来源） | Candidate 与提议材料如何稳定引用，来源是否可追溯？ | Candidate reference 不是 canonical `entity_id` |
| `ADM-CRIT-02` | Owner Responsibility（责任主体） | 谁承担候选、监督、异常和后续使用责任？ | Owner reference 不授予 Permission |
| `ADM-CRIT-03` | Capability Declaration（能力声明） | 拟议能力、scope、constraints、风险、未知和禁止项是否明确？ | Declaration 不是 Verification 或 Grant |
| `ADM-CRIT-04` | Lifecycle Compatibility（生命周期兼容） | 请求是否只进入 `Registered`，并与 DBOS 生命周期规则兼容？ | Admission 不得请求或产生 `Active` |
| `ADM-CRIT-05` | Evidence Boundary（证据边界） | 初始历史、来源、失败记录和未来 Evidence 责任是否明确？ | Readiness 不创建 canonical Evidence |
| `ADM-CRIT-06` | Governance Review（治理审查） | reviewer、decision authority、conditions 与冲突是否可追溯？ | Review 或 criteria result 不自动批准 |

Criteria 可以形成 reviewer recommendation（审查者建议），但不能形成自动批准。满足全部条件也仍需要显式 Admission Decision；任一强制条件为 `UNSATISFIED`、`UNKNOWN` 或存在未解决冲突时，默认不得进入 Registration Authorization。

## 4. Admission Lifecycle（准入生命周期）

正常路径：

```text
Candidate Submitted
        ↓
Admission Review
        ↓
Decision Pending
        ↓ explicit decision authority
Approved
        ↓ separate adoption / registration authorization
Registration Authorized
        ↓ DBOS pre-registration checks
DBOS Registration
        ↓ canonical DBOS record formed
Registered Entity
```

异常路径：

```text
Admission Review ──→ Rejected
Candidate / Request ──→ Withdrawn
Pending / Approved / Authorized ──→ Expired
Approved / Authorized ──→ Revoked
```

| 阶段 | 形成的事实 | 不表示 |
|---|---|---|
| Candidate Submitted | 候选材料已提交 | Entity、Review 已开始 |
| Admission Review | 准入条件及限制被审查 | Decision 已形成 |
| Decision Pending | Admission Decision record 处于待决状态 | 将被批准 |
| Approved | 明确 decision authority 形成批准记录 | 已采纳、已授权登记或已注册 |
| Registration Authorized | 有效、可追溯且条件明确的登记授权已形成 | DBOS 已执行或一定能登记 |
| DBOS Registration | DBOS 在自身约束下处理登记 | 成功、Verified、Active 或 Permission |
| Registered Entity | DBOS 已形成最低 Entity record 与 `REGISTERED` lifecycle record | 已验证、已激活、获授权或可执行 |

`Rejected`、`Withdrawn`、`Expired` 或 `Revoked` 不删除历史。若 DBOS Registration 已完成，后续撤销 Admission Decision 不得追溯抹除 Registered Entity；必须进入独立 DBOS Lifecycle Decision（生命周期决策）处理暂停、限制或退役。

## 5. Admission Records and Ownership（准入记录与归属）

| 记录 | 规范责任 | 运行责任 | 权限边界 |
|---|---|---|---|
| Candidate records | Architecture 定义语义；候选流程保存来源 | 未来采用方 | 不创建 Entity Identity |
| Admission Criteria Review | [`admission-criteria-model.md`](admission-criteria-model.md) 定义语义 | 明确 reviewer 形成记录 | 评价不是批准 |
| Admission Decision | Governance Decision Layer 记录 | 明确 decision authority 作出决定 | Decision Layer 不是授权主体 |
| Registration Authorization | [`registration-authorization-contract.md`](registration-authorization-contract.md) 定义对象与边界；明确 issuer 形成具体记录 | DBOS 只读取、验证并在有界 scope 内使用 | 批准不自动产生授权；授权不等于登记或 Permission |
| Entity Registration | Architecture 定义边界 | DBOS 形成 canonical runtime record | DBOS 不能跳过 Decision 或扩大范围 |

Architecture Governance 维护准入规则，但不审批具体 Candidate。SAEE 不拥有初始 Entity Admission authority；它可以在有明确输入时提供非绑定风险或评价材料，但不能批准 Candidate。DBOS 管理 Registration，却不能自行补造 Admission Decision 或 Registration Authorization。

## 6. DBOS Registration Gate（DBOS 登记闸门）

未来 DBOS 进入 Registration 前必须确认：

1. Candidate、Review、Admission Decision 与符合 [`registration-authorization-contract.md`](registration-authorization-contract.md) 的 Registration Authorization 引用均可解析；
2. `decision_result=APPROVED`，且决定未过期、未撤销、未冲突；
3. 所有 conditions 均已满足或被明确纳入登记限制；
4. requested entity type 与 Architecture classification 的映射明确；
5. Lifecycle target 只能是 `REGISTERED`；
6. Capability 仍是 declaration boundary，不转换为 Verification、Authorization 或 Permission；
7. 初始 Execution/Evidence History 是显式空历史或有来源引用，不伪造执行和证据；
8. DBOS 自身 identity、deduplication、policy 和 safety checks 通过。

任一条件失败时，DBOS 可以拒绝、保持待处理或请求补充材料，并形成有来源记录。它不得因 Admission Approved 而被迫登记，也不得把拒绝登记改写为 Admission Rejected。

## 7. Research Agent Admission Path（科研智能体准入路径）

Research Agent 只能沿以下非自动路径进入 Digital Entity 生命周期：

```text
Research Agent Candidate
  ↓ bounded proposal + human responsibility
Admission Criteria Review
  ↓ explicit Admission Decision
Registration Authorization
  ↓ DBOS Registration
Registered Operational Entity
  ↓ separate DBOS verification and lifecycle decision
Verified / Active
```

Research Agent capability profile 在 Admission 中仍是 declaration template（声明模板），不创建 Capability instance；Human Oversight 是准入条件之一，但不替代 Permission、任务授权、伦理批准或发表责任。

## 8. Agent-readable Admission Gate（智能体可读准入闸门）

智能体在把 Candidate 描述为 Registered Entity 前必须回答：

```text
CANDIDATE_REFERENCE_RESOLVED=
IDENTITY_SOURCE_RECORDED=
OWNER_RESPONSIBILITY_RECORDED=
CAPABILITY_DECLARATIONS_BOUNDED=
LIFECYCLE_TARGET=REGISTERED
EVIDENCE_BOUNDARY_RECORDED=
ADMISSION_REVIEW_REFERENCE=
ADMISSION_DECISION_RESULT=
DECISION_AUTHORITY_REFERENCE=
REGISTRATION_AUTHORIZATION_REFERENCE=
DBOS_REGISTRATION_REFERENCE=
ENTITY_ID=
LIFECYCLE_STATE=
```

若缺少 `DBOS_REGISTRATION_REFERENCE`、`ENTITY_ID` 或 `LIFECYCLE_STATE=REGISTERED`，只能称为 Candidate、Approved Candidate 或 Registration-authorized Candidate，不能称为 Registered Entity。

## 9. Non-implementation Status（非实现状态）

```text
DIGITAL_ENTITY_ADMISSION_SPECIFICATION_DEFINED=true
REGISTRATION_AUTHORIZATION_CONTRACT_DEFINED=true
ADMISSION_PROCESS_IMPLEMENTED=false
ADMISSION_REVIEW_COMPLETED=false
ADMISSION_DECISION_INSTANCE_CREATED=false
REGISTRATION_AUTHORIZATION_CREATED=false
DBOS_REGISTRATION_EXECUTED=false
ENTITY_INSTANCE_CREATED=false
ENTITY_ID_ASSIGNED=false
ACTIVE_STATE_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
AGENT_INSTANCE_CREATED=false
RUNTIME_CREATED=false
SAEE_ADMISSION_AUTHORITY_CREATED=false
DBOS_ADMISSION_DECISION_AUTHORITY_CREATED=false
```

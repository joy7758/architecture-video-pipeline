---
spec_id: DBA-ENTITY-STATUS-TRANSITION-RULES-0.1
title: Digital Entity Status Transition Rules v0.1
title_zh: 数字实体状态转换规则 v0.1
status: normative-non-executable-architecture-rules
state_machine_implemented: false
registration_authorized: false
entity_instance_created: false
active_state_created: false
digital_organism_created: false
permission_effect: none
---

# Digital Entity Status Transition Rules v0.1（数字实体状态转换规则 v0.1）

本规范区分 Candidate workflow（候选工作流）、Admission Decision（准入决策）、Digital Entity Lifecycle（数字实体生命周期）与 Digital Organism Qualification（数字有机体资格）。它定义允许和禁止的跨边界转换，不实现状态机。

## 1. State Domains（状态域）

| 状态域 | 典型状态 | Owner / 责任边界 | 不得替代 |
|---|---|---|---|
| Candidate workflow | Proposed、Review、Registration Request | 候选流程记录 | Entity Lifecycle |
| Admission decision | `PENDING/APPROVED/REJECTED/REVOKED` | Governance Decision Layer 记录；明确 authority 决定 | DBOS Registration state |
| Entity lifecycle | `REGISTERED/VERIFIED/ACTIVE/EVALUATED/ADAPTED/RETIRED` | DBOS 保持 canonical state Owner；SAEE 只参与评价 | Permission 或 Organism qualification |
| Organism qualification | Entity、Candidate Organism、Digital Organism | DBOS records + SAEE Evaluation + Governance Decision | Entity identity 或 lifecycle state |

同名的 “candidate” 在不同域中必须带限定词。Entity Candidate 不是 Candidate Digital Organism。

## 2. Allowed Candidate to Registered Path（允许的候选登记路径）

唯一允许的 Candidate → Registered 路径为：

```text
Candidate Proposal
  ↓
Admission Criteria Review
  ↓
Admission Decision = APPROVED
  ↓
Registration Authorization valid
  ↓
DBOS Registration checks and execution
  ↓
DBOS Entity record + lifecycle_state=REGISTERED
```

只有最后一步完成后，状态才从 Entity Candidate 语义进入 Registered Entity。前面任一记录都不能提前形成 `entity_id` 或 `REGISTERED` truth（登记事实）。

### `ESTR-001`: Candidate may transition to Registered only through Admission

转换必须引用 Candidate、Review、Admission Decision、Registration Authorization 与 DBOS Registration record。缺少任何引用时保持 Candidate 或 pending，不得补造。

### `ESTR-002`: DBOS owns the Registered state record

Decision authority 允许进入登记路径；只有 DBOS 能形成 canonical Entity Identity 和 `REGISTERED` lifecycle record。DBOS 仍可因冲突、重复、失效条件或自身安全约束拒绝执行。

### `ESTR-003`: Registered is the maximum Admission outcome

Admission 的最大生命周期结果是 `REGISTERED`。Verified、Active、Capability Authorized、Permission Granted 和 Runtime Execution 都需要后续独立流程。

## 3. Prohibited Direct Transitions（禁止的直接转换）

### `ESTR-004`: Candidate cannot transition directly to Active

```text
Candidate ─X→ Active
```

Candidate 尚无 canonical Entity Identity 和最低历史。Admission Approved、Registration Authorized 或 Registered 都不自动满足 Verification、Activation 或任务授权。

### `ESTR-005`: Candidate cannot transition to Digital Organism

```text
Candidate ─X→ Digital Organism
```

Entity Candidate 与 Candidate Digital Organism 是不同资格域。没有 Registered Entity Identity、持续历史、Execution/Evidence、SAEE Evaluation 和 Governance Decision 时不得进入 Organism qualification。

### `ESTR-006`: Registered cannot transition directly to Digital Organism

```text
Registered Entity ─X→ Digital Organism
```

Registered 只证明最低实体记录存在，不证明长期持续性、适应、生态交互、Fitness 或 Lineage。

### `ESTR-007`: Admission cannot create Permission or Capability state

Admission Criteria、Decision、Authorization 和 Registration 均不得把 Capability Declaration 改为 Verified/Authorized，也不得产生 Permission。

### `ESTR-008`: SAEE cannot approve Entity Admission

SAEE 可以提供 Evaluation input，但 Admission Approval、Registration Authorization 和 DBOS Registration 不属于 SAEE Evolution Authority。

### `ESTR-009`: DBOS cannot bypass Admission Decision

DBOS 管理登记执行，但不能把 Registration Request、Reviewer recommendation 或 Candidate template 当作 Admission Decision/Authorization。

## 4. Post-registration Lifecycle（登记后生命周期）

```text
REGISTERED
  ↓ DBOS bounded identity/minimum-record verification
VERIFIED
  ↓ separate lifecycle authorization; no task permission implied
ACTIVE
  ↓ DBOS Execution/Evidence/Verification records
EVALUATED
  ↓ SAEE Evaluation + Recommendation
ADAPTED / ACTIVE new baseline / RETIRED
  ↓ Governance Decision + DBOS controlled record
```

每次状态变化必须保持 Decision、Authorization、DBOS execution/recording 与 Verification 分离。`ACTIVE` 只表示可进入另行授权的任务路径，不表示 Runtime 正在运行。

## 5. Digital Organism Qualification Path（数字有机体资格路径）

Digital Entity 进入 Digital Organism 资格必须至少经过：

```text
DBOS Lifecycle: Registered → Verified → Active
  ↓ multiple bounded Execution / Evidence / Verification records
Candidate Digital Organism eligibility review
  ↓
SAEE Evaluation: persistence / adaptation / fitness / stability
  ↓ Recommendation
Governance Decision: Review → Approved → Adopted
  ↓
DBOS qualification record
  ↓
Digital Organism qualification
```

该路径以 [`digital-organism-crosswalk.md`](digital-organism-crosswalk.md) 为准，不创建第二个 `entity_id`。Organism qualification 仍不产生 Permission。

## 6. Transition Decision Table（转换决策表）

| 请求转换 | v0.1 结果 | 最低缺失或要求 |
|---|---|---|
| Candidate → Registered | `CONDITIONAL_ALLOWED` | Admission Review、Decision、Authorization、DBOS Registration |
| Candidate → Verified | `PROHIBITED_DIRECT` | 必须先 Registered，再由 DBOS Verification |
| Candidate → Active | `PROHIBITED` | Admission 不能跳过 Registered/Verified |
| Candidate → Digital Organism | `PROHIBITED` | 尚不是 Digital Entity |
| Registered → Active | `PROHIBITED_DIRECT` | 必须先 Verified 并经过独立生命周期 gate |
| Registered → Digital Organism | `PROHIBITED_DIRECT` | 缺少持续历史、SAEE Evaluation、Decision 与 DBOS qualification record |
| Approved Admission → Registered | `NOT_YET` | 还需 Registration Authorization 和 DBOS Registration |
| Registration Authorized → Registered | `NOT_YET` | 还需 DBOS 成功形成 canonical record |
| Registered → Permission Granted | `PROHIBITED_INFERENCE` | Permission 是独立 Context-scoped decision |

## 7. Revocation and History（撤销与历史）

- Candidate withdrawal 不删除 Proposal 或 Review；
- Admission rejection/revocation 不删除 Candidate history；
- Registration 前授权撤销阻止新的登记；
- Registration 后 Admission 撤销不删除 Entity Identity；
- Active、Organism 或 Permission 不得因旧 Admission record 改写而自动变化；
- 所有更正、拒绝、过期、撤销和后续决定必须 append-only（仅追加）保留。

## 8. Non-implementation Status（非实现状态）

```text
ENTITY_STATUS_TRANSITION_RULES_DEFINED=true
ENTITY_STATE_MACHINE_IMPLEMENTED=false
CANDIDATE_TRANSITION_EXECUTED=false
ENTITY_REGISTRATION_EXECUTED=false
ACTIVE_STATE_CREATED=false
DIGITAL_ORGANISM_CREATED=false
SAEE_ADMISSION_AUTHORITY_CREATED=false
DBOS_DECISION_BYPASS_AUTHORIZED=false
CAPABILITY_STATE_CHANGED=false
PERMISSION_GRANTED=false
```

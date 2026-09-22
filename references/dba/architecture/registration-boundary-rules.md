---
spec_id: DBA-REGISTRATION-BOUNDARY-RULES-0.1
title: Digital Entity Registration Boundary Rules v0.1
title_zh: 数字实体登记边界规则 v0.1
status: non-executable-architecture-rules
registration_boundary_defined: true
registration_executed: false
entity_instance_created: false
permission_granted: false
---

# Digital Entity Registration Boundary Rules v0.1

本规范定义 Admission（准入）、Registration Authorization（登记授权）与 DBOS Registration（登记执行）之间必须 fail closed（失败关闭）的边界。

## Rule 1 — Admission Decision is not Registration Authorization

`decision_result=APPROVED` 只表示准入判断已形成。它允许进入独立 Authorization issuance review（授权签发审查），不得直接传给 DBOS 作为登记授权。

## Rule 2 — Registration Authorization is not Registration

只有当前有效、未撤销且 scope 有界的 `status=AUTHORIZED` 才允许 DBOS 开始 pre-registration checks。`AUTHORIZED` 不表示 DBOS 已接受、已执行或已生成 `entity_id`。

## Rule 3 — Registration Authorization is not Permission

Authorization Object 的唯一 operation 是 `entity_registration`，最大 lifecycle target 是 `REGISTERED`。它不得包含任务执行 Permission、资源访问 Permission、外部系统授权或 Capability authorization。

## Rule 4 — Registration cannot activate an Entity

DBOS Registration 成功只形成 `REGISTERED` lifecycle record。`VERIFIED`、`ACTIVE`、`EVALUATED`、`ADAPTED` 或 `RETIRED` 必须遵循各自独立状态转换与授权。

## Rule 5 — Registration cannot grant Capability

Candidate capability material 在登记前后都只是 declaration/reference（声明/引用）。Registration 不得将其自动转换为 Verified Capability、Authorized Capability、Capability Grant 或 Permission。

## Rule 6 — DBOS executes; DBOS does not decide admission

DBOS 可以验证引用、拒绝无效授权或因 operational constraints（运行约束）停止登记。它不能创建、补造、批准或改写 Admission Decision，也不能把 registration failure 改写为 Admission Rejection。

## Rule 7 — SAEE evaluates; SAEE does not register

SAEE 可以在明确请求和来源边界下提供 Risk Assessment 或 Evaluation material。SAEE 不审批 Candidate、不签发 Registration Authorization、不调用 DBOS Registration，也不分配 Entity Identity。

## Rule 8 — Scope cannot expand downstream

Admission conditions → Registration Authorization scope → DBOS registration operation 的信息只能保持或收窄，不能扩大。任何 target type、Candidate、lifecycle target、期限或 exclusion 变化都需要新的显式治理记录。

## Rule 9 — Unknown or conflict fails closed

Decision、issuer authority、scope、conditions、时间、revocation、Candidate mapping 或 identity conflict 中任一关键事实为 unknown/conflicted 时，DBOS 不得登记。

## Rule 10 — History is preserved

Rejected、Revoked、Expired/ineffective、failed、duplicate 和 partial registration records 必须保留。撤销不删除过去事实，也不自动删除已登记 Entity。

## Allowed Path（允许路径）

```text
Admission Criteria Review
  ↓ explicit Admission Decision
Admission Decision: APPROVED
  ↓ independent authorization issuance
Registration Authorization: AUTHORIZED + effective
  ↓ DBOS validation and pre-registration checks
DBOS Registration
  ↓ only after canonical record is formed
Entity lifecycle_state=REGISTERED
```

## Forbidden Paths（禁止路径）

```text
Admission Decision ─X→ Entity Active
Admission Decision ─X→ DBOS Registration
Registration Authorization ─X→ Permission
Registration Authorization ─X→ Capability Grant
Registration Authorization ─X→ Active
Registration ─X→ Capability Verification / Grant
Registration ─X→ Permission / Runtime / Execution
SAEE Evaluation ─X→ Admission Approval / Authorization / Registration
DBOS readiness ─X→ Admission Decision
```

## DBOS Registration Gate（DBOS 登记闸门）

| gate | 必需条件 | 失败结果 |
|---|---|---|
| Decision integrity | Admission Decision 可解析、`APPROVED`、未撤销 | 不登记，保留失败原因 |
| Authorization integrity | Authorization 为 `AUTHORIZED`、当前有效、未撤销 | 不登记 |
| Issuer authority | issuer identity、scope、有效期与 revocation 可验证 | 不登记 |
| Subject continuity | Candidate、Decision、Authorization 指向同一 subject | 不登记并记录冲突 |
| Type mapping | target entity type 与批准的 mapping 一致 | 不登记 |
| Scope | operation=`entity_registration`，target=`REGISTERED` | 不登记 |
| Conditions | 所有下游条件已满足或明确可执行 | 不登记或保持待处理 |
| DBOS checks | identity collision、deduplication、policy 与 safety checks 通过 | 拒绝/停止执行，但不改写 Decision |

DBOS 成功输出必须是独立 Registration Result/Record，并引用使用过的 Authorization；不得通过修改 Authorization status 来冒充 Registration fact。

## Agent-readable Boundary（智能体可读边界）

```text
ADMISSION_DECISION_NE_REGISTRATION_AUTHORIZATION=true
REGISTRATION_AUTHORIZATION_NE_REGISTRATION=true
REGISTRATION_AUTHORIZATION_NE_PERMISSION=true
REGISTERED_NE_ACTIVE=true
REGISTRATION_GRANTS_CAPABILITY=false
REGISTRATION_GRANTS_PERMISSION=false
SAEE_CAN_REGISTER_ENTITY=false
DBOS_CAN_DECIDE_ADMISSION=false
ENTITY_INSTANCE_CREATED=false
REGISTRATION_EXECUTED=false
```


---
spec_id: DBA-REGISTRATION-AUTHORIZATION-CONTRACT-0.1
title: Digital Entity Registration Authorization Contract v0.1
title_zh: 数字实体登记授权契约 v0.1
status: non-executable-data-contract-specification
authorization_contract_defined: true
authorization_object_instantiated: false
authorization_issued: false
registration_executed: false
entity_instance_created: false
permission_granted: false
runtime_created: false
---

# Digital Entity Registration Authorization Contract v0.1

本契约定义 Registration Authorization（登记授权）的对象语义、状态、签发条件和 DBOS consumption boundary（使用边界）。它把 Admission Decision（准入决定）与 DBOS Registration（DBOS 登记执行）分开，不创建授权记录、Entity、Permission、Runtime 或 API。

```text
Admission Decision ≠ Registration Authorization
Registration Authorization ≠ Permission
AUTHORIZED ≠ Registered
Governance Decision ≠ Execution
```

## 1. Authorization Definition（授权定义）

Registration Authorization 是明确 issuer（签发者）在有界 scope（范围）内，允许 DBOS 对指定 Candidate 进入 Entity Registration processing（实体登记处理）的治理记录。对 `decision_type=admission`，它同时是 domain-specific adoption/authorization record（领域专用采纳/授权记录），但不是 Admission Decision 的状态或副本。

它只授权一种受控操作：DBOS 尝试形成 `REGISTERED` Entity record。它不表示：

- DBOS 必须接受或一定能够完成登记；
- Entity 已经存在或已分配 `entity_id`；
- Lifecycle 已进入 Verified 或 Active；
- Capability 已验证、授权或授予；
- 当前任务 Permission 已产生；
- Runtime、Execution、Evidence 或 Digital Organism 已创建。

## 2. Registration Authorization Object（登记授权对象）

Owner：Governance Decision Layer（治理决策层）管理规范记录与历史；`issuer_reference` 指向真正作出授权的外部明确主体。Owner 不等于 issuer，也不自动拥有授权权力。

| 字段 | 语义 | 强制边界 |
|---|---|---|
| `authorization_id` | 登记授权记录的稳定、不透明标识 | 不等于 `entity_id`、Permission ID 或 Execution ID |
| `decision_reference` | 指向 `decision_type=admission` 且已批准的 Admission Decision | Decision 本身不是授权；引用必须可验证且未撤销 |
| `candidate_id` | 被允许进入登记处理的 Candidate reference | 不是 canonical Entity Identity |
| `target_entity_type` | 允许 DBOS 登记的目标实体类型或已批准映射结果 | 不授予该角色对应的能力或权力 |
| `authorized_scope` | 允许的登记动作、目标 lifecycle、conditions、有效范围和期限 | 最大 lifecycle target 只能是 `REGISTERED`；不得包含 Permission/Activation |
| `issuer_reference` | 对实际签发主体及其 authority record 的引用 | 字符串存在不证明 authority 有效 |
| `status` | `PENDING`、`AUTHORIZED`、`REJECTED` 或 `REVOKED` | 只有有效 `AUTHORIZED` 才可进入 DBOS pre-registration checks |
| `timestamp` | 授权状态事件时间及时间来源 | 时间值不证明签发真实性、有效期或未撤销 |

该对象还必须按通用对象规则保留 version、provenance、status history、conditions evaluation 与 revocation reference。本契约不选择 JSON、YAML、数据库或 API 序列化。

## 3. Authorization States（授权状态）

```text
PENDING
  ├─ explicit issuance → AUTHORIZED
  └─ explicit rejection → REJECTED

AUTHORIZED
  └─ explicit revocation → REVOKED
```

| 状态 | 最小语义 | DBOS 处理 | 不表示 |
|---|---|---|---|
| `PENDING` | 授权候选已记录，尚无有效签发 | 不得登记 | 将获授权 |
| `AUTHORIZED` | issuer authority、Decision、scope、conditions 和时间边界均通过签发审查 | 可以进入独立 DBOS pre-registration checks | Registered、Active 或 Permission |
| `REJECTED` | 授权请求被明确拒绝并保留理由 | 不得登记 | Admission Decision 被删除或永久禁止新请求 |
| `REVOKED` | 已签发授权的后续效力被撤销 | 不得开始新的登记；处理中按停止规则记录事实 | 已完成登记自动回滚或 Entity 被删除 |

`AUTHORIZED` 的有效性还取决于 `authorized_scope` 中的时间、conditions 和撤销边界。v0.1 没有单独 `EXPIRED` 状态；超出时间范围时必须视为 ineffective authorization（无效授权）并 fail closed，不能继续登记。若未来增加 `EXPIRED`，需要版本化契约变更。

## 4. Authorization Issuance Preconditions（授权签发前提）

进入 `AUTHORIZED` 必须同时满足：

1. `decision_reference` 指向可解析、未撤销的 Admission Decision；
2. Admission Decision 的 `decision_type=admission` 且 `decision_result=APPROVED`；
3. Admission Decision 已被明确采纳进入 registration path；本 Authorization 是该特定 scope 的独立 adoption/authorization record；
4. `subject_reference` 与 `candidate_id` 指向同一 Candidate；
5. `criteria_summary`、Review 与 Decision conditions 可解析；
6. 未满足条件已被关闭，或被明确转换为不扩大范围的 registration constraints；
7. `issuer_reference` 的 authority、scope、有效期和撤销状态可验证；
8. `target_entity_type` 与已批准 mapping reference 一致；
9. `authorized_scope` 只允许形成 `REGISTERED` record；
10. 不存在冲突授权、重复使用、身份碰撞或未知关键事实。

任一前提未知、冲突、过期或无法验证时，状态必须保持 `PENDING`、进入 `REJECTED`，或由既有有效记录进入 `REVOKED`；不得默认 `AUTHORIZED`。

## 5. Authorized Scope（授权范围）

`authorized_scope` 至少表达：

| scope component | 必需值或语义 |
|---|---|
| operation | `entity_registration` |
| lifecycle_target | `REGISTERED` |
| candidate | 与 `candidate_id` 一致 |
| entity_type | 与 `target_entity_type` 一致 |
| conditions | 从 Admission Decision 继承且不可扩大 |
| validity | 生效时间、失效时间或显式无固定期限说明 |
| single_use / idempotency | 是否单次使用及重复请求处理规则；未知时 fail closed |
| exclusions | `ACTIVE`、Capability Grant、Permission、Runtime、Execution、Organism qualification |

授权范围不得使用“full access”“all lifecycle states”或等价无界表达。

## 6. DBOS Consumption Contract（DBOS 使用契约）

DBOS 在处理授权前必须：

1. 验证 Authorization Object 完整、状态为 `AUTHORIZED` 且当前仍有效；
2. 解析并验证 Admission Decision、Candidate、Criteria Review 与 issuer authority 引用；
3. 检查 scope、conditions、target type、deduplication 和 identity conflict；
4. 检查授权是否已使用、撤销、替代、冲突或过期；
5. 保持 Candidate reference 与新 `entity_id` 分离；
6. 只执行 registration operation，不执行 Activation、Capability transition 或 Permission grant；
7. 形成独立 Registration Result/Record，不修改 Authorization Object 后冒充原授权；
8. 失败、拒绝、部分处理或重复请求必须保留记录，不能静默丢弃。

DBOS 的 pre-registration checks 是 Operational Authority（运行权力）下的执行前检查，不是重新作出 Admission Decision。DBOS 可以拒绝执行，但不能把自己的拒绝改写为 Decision `REJECTED`。

## 7. Revocation and Post-registration Boundary（撤销与登记后边界）

- 登记开始前 `REVOKED`：DBOS 不得开始；
- 登记处理中 `REVOKED`：DBOS 在安全边界停止，并记录已经发生或未发生的事实；
- 登记完成后 `REVOKED`：不得删除 Entity Identity 或把 Registration 描述为未发生；需要新的 Lifecycle Decision 处理限制、暂停或 Retired；
- Authorization history 必须 append-only（仅追加）保留；
- 撤销不创建 Permission denial、Capability revocation 或 SAEE Evaluation。

## 8. Agent-readable Authorization Gate（智能体可读授权闸门）

```text
AUTHORIZATION_ID=
DECISION_REFERENCE=
DECISION_TYPE=admission
DECISION_RESULT=APPROVED
CANDIDATE_ID=
TARGET_ENTITY_TYPE=
AUTHORIZED_OPERATION=entity_registration
LIFECYCLE_TARGET=REGISTERED
ISSUER_REFERENCE=
ISSUER_AUTHORITY_VALID=
AUTHORIZATION_STATUS=
AUTHORIZATION_CURRENTLY_EFFECTIVE=
DBOS_REGISTRATION_REFERENCE=
```

`AUTHORIZATION_STATUS=AUTHORIZED` 但缺少有效 issuer、scope、conditions、时间或 revocation 检查时，不得调用或声称 DBOS Registration。缺少 `DBOS_REGISTRATION_REFERENCE` 时仍不是 Registered Entity。

## 9. Non-implementation Status（非实现状态）

```text
REGISTRATION_AUTHORIZATION_CONTRACT_DEFINED=true
REGISTRATION_AUTHORIZATION_OBJECT_DEFINED=true
REGISTRATION_AUTHORIZATION_OBJECT_INSTANTIATED=false
REGISTRATION_AUTHORIZATION_ISSUED=false
REGISTRATION_AUTHORIZATION_STATUS_UNSET=true
DBOS_REGISTRATION_EXECUTED=false
ENTITY_INSTANCE_CREATED=false
ENTITY_ID_ASSIGNED=false
ACTIVE_STATE_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
RUNTIME_CREATED=false
API_CREATED=false
```

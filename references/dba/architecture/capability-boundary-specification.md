---
spec_id: DBA-CAPABILITY-BOUNDARY-0.1
title: Digital Biosphere Capability Boundary Specification v0.1
title_zh: 数字生物圈能力边界规范 v0.1
status: non-executable-architecture-specification
capability_model_defined: true
capability_instance_created: false
authorization_created: false
permission_granted: false
runtime_effect: none
entity_effect: none
---

# Digital Biosphere Capability Boundary Specification v0.1

本规范定义 Digital Entity（数字实体）的 Capability（能力）如何被声明、审查、验证、授权、执行、评价和撤销，并保持 Capability、Authority、Permission 与 Execution 分离。

## 1. Capability Definition（能力定义）

Capability 是数字实体可以声明、验证或执行的一类行为能力描述。

其中：

- Digital Entity 可以作为声明来源，但不能自证能力；
- Verification（验证）必须在 DBOS 的有界记录与验证治理下形成；
- Execution（执行）只能在另行有效的 Authorization、Permission、Context 和 Lifecycle control 下发生；
- Capability 描述“某类行为是否处于已知能力边界”，不证明一次行为已经发生。

Capability 不表示：

- Authority（权力）；
- Authorization（授权决定）；
- Permission（当前执行许可）；
- Execution Result（执行结果）；
- Fitness、可靠性或安全性结论。

### 1.1 核心不变量

```text
CAPABILITY_NE_AUTHORITY=true
CAPABILITY_NE_PERMISSION=true
PERMISSION_NE_EXECUTION=true
DECLARED_NE_VERIFIED=true
VERIFIED_NE_AUTHORIZED=true
AUTHORIZED_NE_EXECUTED=true
SAEE_CAN_GRANT_CAPABILITY=false
DBOS_CAN_AUTO_EXPAND_CAPABILITY=false
```

## 2. Capability Layers（能力层级）

| 层级 | 定义 | 主要记录责任 | 不表示 |
|---|---|---|---|
| Declared Capability（声明能力） | Entity 或有来源的代表声明候选行为能力、scope 和 constraints | DBOS 登记声明及来源 | 声明真实、已验证或可执行 |
| Verified Capability（验证能力） | DBOS 对明确对象、方法、环境和版本形成有界 Verification Result | DBOS | 已授权、已许可、适用于所有环境 |
| Authorized Capability（授权能力） | 在明确 scope、constraints、期限和 authority reference 下获准进入使用路径 | Governance Decision 或外部明确授权记录；DBOS 保存状态引用 | 当前 Permission 已授予或执行已发生 |

三层不可自动转换：

```text
Declared Capability ≠ Verified Capability
Verified Capability ≠ Authorized Capability
Authorized Capability ≠ Permission
Authorized Capability ≠ Execution
```

Verification 失败、证据不足或环境不匹配时必须保留 `unknown`、`partial`、`failed` 或等价状态，不能用声明补足。

## 3. Capability Lifecycle（能力生命周期）

```text
Declared
   ↓
Reviewed
   ↓
Verified
   ↓
Available
   ↓
Authorized
   ↓
Executed
   ↓
Evaluated
   ↓
Revoked
```

| 状态 | 主要参与者 | 状态语义 | 不表示 |
|---|---|---|---|
| Declared（已声明） | Entity 声明；DBOS 登记 | 能力描述、来源和初始边界存在 | 能力成立 |
| Reviewed（已审查） | DBOS 与明确 reviewer | scope、constraints、风险和验证要求已审查 | 已验证或已批准 |
| Verified（已验证） | DBOS | 在声明范围内形成验证记录 | 已授权或获准执行 |
| Available（可用候选） | DBOS | 能力在当前 Entity lifecycle 中可进入授权审查 | Permission 已存在 |
| Authorized（已授权） | 明确授权主体；高风险变化经过 Governance Decision | 有范围的授权记录有效 | 当前 Context 已允许或 Execution 已发生 |
| Executed（已执行里程碑） | Digital Entity 行为来源；DBOS 记录 | 某次 Execution 引用了该能力 | 能力永久有效或结果成功 |
| Evaluated（已评价里程碑） | SAEE | SAEE 基于 Execution/Evidence 评价能力表现 | 权限扩大或授权续期 |
| Revoked（已撤销） | 显式治理决定；DBOS 记录 | 后续使用路径被关闭或限制 | 历史 Execution、Evidence 或 Evaluation 被删除 |

该图表示最小治理顺序。`Executed` 与 `Evaluated` 是可重复事件关联的里程碑，不应被实现为只能发生一次的永久全局状态。`Revoked` 可以从 Available、Authorized 或后续阶段触发；撤销不得追溯改写历史。

## 4. Capability Object（能力对象）

Owner：DBOS

Declaration source：Digital Entity 或有来源的代表。

| 字段 | 语义 |
|---|---|
| `capability_id` | 稳定、不透明的能力记录引用 |
| `entity_id` | 指向 DBOS 管理的 Entity Identity |
| `description` | 可审查的行为能力描述，不是营销声明 |
| `scope` | 对象、任务、环境、时间和资源边界 |
| `constraints` | 禁止项、限制、依赖与失败条件 |
| `risk_level` | Low、Medium、High、Critical 或 unknown；风险不产生授权 |
| `verification_status` | DBOS 有界验证状态及验证引用 |
| `authorization_status` | 授权记录的派生摘要或引用；不是 Permission 来源 |

Capability Object 还应保留版本、来源、状态历史、Verification reference、Authorization reference 和限制。本表只定义结构，不实现 schema、API 或对象实例。

## 5. Capability Risk Model（能力风险模型）

风险等级必须结合 scope、数据、环境、可逆性、外部副作用和影响半径审查；示例不是永久分类，也不构成授权。

| 风险等级 | 参考特征 | 示例 | 治理要求 |
|---|---|---|---|
| Low Risk（低风险） | 可逆、无外部副作用、只读且影响有限 | 文本分析 | 仍需明确 Capability、Context 和 Permission |
| Medium Risk（中风险） | 可能改变受控环境或产生可执行材料 | 代码执行 | 需要更严格验证、隔离、约束与显式授权 |
| High Risk（高风险） | 操作外部系统、具有持久副作用或较大影响半径 | 外部系统操作 | Capability change 或授权变化必须经过 Governance Decision |
| Critical Risk（关键风险） | 影响医疗、金融、身份、安全或不可逆关键状态 | 医疗决策、金融操作、身份修改 | 必须经过显式高强度治理；v0.1 不定义或授予执行路径 |

Risk Assessment 可以由 SAEE 形成，但 SAEE 的风险评价是 Recommendation input（建议输入），不是自动禁止、授权或执行命令。

## 6. Capability Boundary Model（能力边界模型）

| 边界分类 | 含义 | 默认处理 |
|---|---|---|
| Allowed Capability（允许能力） | 可以进入验证和授权路径 | 不自动授予 Permission |
| Limited Capability（限制能力） | 只能在明确 scope、constraints 或 Context 下进入使用路径 | 超出限制时 fail closed |
| Forbidden Capability（禁止能力） | 当前架构边界不允许进入授权或执行 | 变更需显式 Governance Decision 与 DBOS 记录 |
| Unknown Capability（未知能力） | 证据、描述或验证不足 | 不得执行或推断为允许 |

Allowed 表示 eligible（可进入治理流程），不是 authorized 或 permitted。

## 7. Capability Boundary Rules（能力边界规则）

1. Capability ≠ Authority：能描述或验证某类行为，不表示有资格决定是否执行。
2. Capability ≠ Permission：能力记录不产生当前任务许可。
3. Permission ≠ Execution：许可存在不证明执行发生或成功。
4. Declared、Verified、Authorized 三层不得自动转换。
5. DBOS 管理 Capability Object、Verification、Availability、Permission gate 和生命周期记录，但不能自动扩大 scope 或风险等级。
6. SAEE 评价 Capability performance、Reliability、Efficiency、Adaptability、Stability 和 Risk，但不能授予、验证或执行 Capability。
7. Governance Decision 对 High/Critical capability change 及治理策略要求的变化形成 Decision；Decision 不直接修改 Capability Object。
8. DBOS 只有在有效 Capability、Authorization、Permission、Context、Entity lifecycle 和 constraints 同时满足时，才能记录受约束 Execution。
9. Unknown、Forbidden、Revoked、expired 或 conflicted 状态必须 fail closed。
10. Capability change、task authorization 和 Runtime permission 是三个不同治理事项，不得合并。

## 8. Responsibility Summary（职责摘要）

```text
Digital Entity: declares a bounded capability
DBOS: records, reviews, verifies and controls lifecycle/permission
SAEE: evaluates observed capability performance
Governance Decision: decides governed high-risk changes and adoption
Execution: occurs only under separate valid context and permission
```

## 9. 非实现状态

```text
CAPABILITY_BOUNDARY_SPECIFICATION_DEFINED=true
CAPABILITY_OBJECT_INSTANCE_CREATED=false
CAPABILITY_VERIFIED=false
CAPABILITY_AUTHORIZED=false
PERMISSION_GRANTED=false
EXECUTION_CREATED=false
SAEE_EXECUTION_AUTHORITY_CREATED=false
DBOS_EVOLUTION_AUTHORITY_CREATED=false
API_CREATED=false
CODE_CHANGED=false
```

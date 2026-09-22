---
spec_id: DBA-INTERFACE-BOUNDARY-RULES-0.1
title: SAEE-DBOS Interface Boundary Rules v0.1
status: normative-architecture-boundary-rules
implementation_authorized: false
capability_effect: none
evidence_effect: none
authority_effect: none
---

# SAEE–DBOS Interface Boundary Rules v0.1（SAEE–DBOS 接口边界规则 v0.1）

## 1. 适用范围

这些规则用于保护 DBOS 与 SAEE 的职责分离，并阻止重复建设、对象所有权漂移和权限升级。这里的“事实”特指 bounded operational record（有界运行记录），不是对现实世界的无限真理声明。

## 2. 五条核心规则

### `IBR-001`：DBOS 负责事实

DBOS 负责 Entity、Execution、Resource、Behavior、Evidence 与 Verification 的 canonical operational records（规范运行记录）。DBOS 必须记录来源、范围、状态和限制；记录存在不自动证明完整真实性。

SAEE 不得建立一个与 DBOS 平行的身份、执行、证据或生命周期事实权威。

### `IBR-002`：SAEE 负责解释事实

SAEE 负责基于 DBOS 对象形成 Fitness、Risk、Stability 与 Evolution 评价。解释必须引用输入对象、模型版本、范围和不确定性。

DBOS 不得内建、复制或重写 SAEE 评价算法后继续声称是原始 SAEE 结果。

### `IBR-003`：DBOS 产生 Evidence

DBOS 负责采集、登记或封装 canonical Evidence Object（规范证据对象）及有界 Verification Result。底层事件或材料可以来自 Digital Entity 或外部来源，但接口中的 Evidence Object Owner 保持为 DBOS。

“产生 Evidence”不等于创造事实、证明主张或宣称 Evidence Collection 已实现。

### `IBR-004`：SAEE 评价 Evidence

SAEE 可以评价 Evidence 的适用性、充分性、风险意义和适应度意义，但必须把评价写入新的 Evaluation Object，并引用原 Evidence Object。

SAEE 不得修改 Evidence、`integrity_status`、`verification_level` 或 `verification_status` 后仍声称它们来自 DBOS。

### `IBR-005`：SAEE 建议不能直接执行

所有 SAEE → DBOS 输出的 authority class（权限类别）都是 `Recommendation`，不是 `Command`。DBOS 接收建议不等于审查、授权、采用或执行建议。

任何运行或生命周期状态变化必须经过独立 policy and authorization gate（策略与授权闸门）；该 gate 不由本规范创建。

## 3. 禁止重复建设规则

### `IBR-006`：一个对象类型只有一个规范 Owner

- Entity、Execution、Evidence Object：DBOS；
- Evaluation、Recommendation Object：SAEE。

缓存、副本、索引、adapter 或展示层不得自称新的 canonical Owner。

### `IBR-007`：验证与评价不得合并

DBOS Verification 回答“在明确规则下检查结果是什么”；SAEE Evaluation 回答“这些记录对适应度、风险和演化意味着什么”。不得用一个无类型的 `score`、`status` 或 `result` 同时承载两种语义。

### `IBR-008`：模型与记录不得互相回写

SAEE 模型变化不得追溯性修改 DBOS 历史；DBOS 记录变化不得静默覆盖已产生的 SAEE Evaluation。需要重新评价时，应创建新的 Evaluation Object 并保留旧版本。

### `IBR-009`：同名字段不自动同义

不同对象中的 `status`、`level`、`confidence` 或 `result` 必须通过对象类型、Owner、版本和 scope（范围）解释。不得仅凭字段同名合并 schema。

### `IBR-010`：支持组件不自动获得顶层职责

POP、ARO、Agent Evidence、Token Governor 或未来 adapter 可以支持接口对象形成、传递或审查，但必须保留 DBOS/SAEE 的规范 Owner 边界。支持关系不等于并入、替代、集成或获得权限。

## 4. 冲突判定表

| 发现的设计 | 判定 | 修正方向 |
|---|---|---|
| SAEE 创建或修改 `entity_id`、`lifecycle_state` | 违反 `IBR-001` | 改为只读引用 DBOS Entity Object |
| DBOS 计算或改写 Fitness 模型 | 违反 `IBR-002` | DBOS 只提供输入并引用 SAEE Evaluation |
| SAEE 复制 Evidence 后成为新事实权威 | 违反 `IBR-003/004/006` | 保留 DBOS Evidence Object 和 provenance 引用 |
| DBOS 把 Verification Status 当作 Fitness | 违反 `IBR-007` | 分离 Verification Object semantics 与 Evaluation Object |
| SAEE Recommendation 直接触发执行 | 违反 `IBR-005` | 增加独立审查与授权状态，不改变原建议 |
| adapter 同时拥有 DBOS 和 SAEE 对象 | 违反 `IBR-006/010` | adapter 仅转换并保留 Owner 与来源 |

## 5. 新增组件的进入条件

任何拟加入接口路径的组件必须先回答：

1. 它读取和产生哪一种 contract object？
2. 它是 Owner、Consumer、Source 还是 Adapter？
3. 它是否建立了与 DBOS 或 SAEE 平行的事实或评价权威？
4. 它是否把 Recommendation 升级为 Command？
5. 现有项目是否已经满足同一需求？
6. 不推荐复用现有项目的具体原因是什么？

任一答案不明确时，应停止实现决定并回到 architecture review（架构审查）。

## 6. 边界状态常量

```text
DBOS_GOVERNS_OPERATIONAL_RECORDS=true
SAEE_GOVERNS_DERIVED_ASSESSMENTS=true
DBOS_GOVERNS_SAEE_ALGORITHMS=false
SAEE_GOVERNS_DBOS_STATE=false
SAEE_RECOMMENDATION_IS_COMMAND=false
DUPLICATE_CANONICAL_OWNER_ALLOWED=false
```


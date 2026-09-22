---
spec_id: DBA-STACK-INTERFACE-0.1
title: Digital Biosphere Stack Interface Specification v0.1
title_zh: 数字生物圈技术栈接口规范 v0.1
status: non-executable-interface-specification
parent_contract: saee-dbos-contract.md
schema_format_selected: false
api_created: false
endpoint_created: false
integration_claimed: false
capability_effect: none
evidence_effect: none
authority_effect: none
---

# Digital Biosphere Stack Interface Specification v0.1

本规范定义 DBOS 与 SAEE 之间的 field-level data contract（字段级数据契约）和 authority boundary（权限边界）。它细化 [`saee-dbos-contract.md`](saee-dbos-contract.md)，但不替代该文件的语义与非授权约束。

本规范不是 API（应用程序接口）、endpoint（端点）、可执行 schema（模式）、消息协议或集成实现。字段名称只定义稳定语义；编码类型、序列化方式、传输机制、认证和部署均未选择。

## 1. 契约层级

| 层级 | 规范文件 | 职责 |
|---|---|---|
| Semantic Contract（语义契约） | `saee-dbos-contract.md` | 定义交换方向、语义和非授权边界 |
| Interface Profile（接口配置） | 本文件 | 定义 v0.1 字段及兼容规则 |
| Object Contract（对象契约） | `data-contracts.md` | 定义核心对象及 Owner（所有者） |
| Boundary Rules（边界规则） | `interface-boundary-rules.md` | 阻止跨层修改和重复建设 |

## 2. 通用契约语义

每个接口项都应与现有概念契约中的追溯语义结合使用：`spec_version`、`contract_item_id`、`entity_ref`、`source_ref`、`observed_or_generated_at`、`scope`、`provenance_refs`、`status`、`payload` 与 `limitations`。

这些是 semantic requirements（语义要求），不是已实现的 wire format（线上格式）。字段缺失、冲突或不可解析时必须保持 `unknown`、`partial` 或 `conflicted` 等明确状态，不得静默补造事实。

## 3. DBOS → SAEE Interface

DBOS 向 SAEE 提供有来源、有范围的 operational records（运行记录）、Evidence（证据）与 Verification Result（验证结果）。DBOS 是下列接口对象的规范提供方；SAEE 是只读消费者和派生评价方。

### 3.1 Entity Identity（主体身份）

Contract item：`DBOS-SAEE-01`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `entity_id` | Opaque identifier（不透明标识符） | 必需 | DBOS 管理的主体引用；传输该字段不创建、验证或授权身份 |
| `entity_type` | Controlled classification（受控分类） | 必需 | DBOS 所记录的主体类型；值域由 DBOS 责任域定义，本规范不新增类型 |
| `lifecycle_state` | Controlled lifecycle state（受控生命周期状态） | 必需 | DBOS 所记录的当前生命周期状态；不得由 SAEE 修改或推断升级 |

### 3.2 Execution History（执行历史）

Contract item：`DBOS-SAEE-02`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `execution_id` | Opaque identifier | 必需 | 一次执行记录或执行记录集合的稳定引用；不证明执行成功或获授权 |
| `event_history` | Ordered record collection（有序记录集合） | 必需 | 事件记录或事件引用的有序集合；必须保留缺口和未知项 |
| `timestamps` | Scoped timestamp collection（有范围的时间戳集合） | 必需 | 观察、发生或记录时间及其语义；不得把记录时间等同为事件发生时间 |

### 3.3 Evidence Bundle（证据包）

Contract item：`DBOS-SAEE-03`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `evidence_id` | Opaque identifier | 必需 | Evidence Object（证据对象）或证据包的稳定引用 |
| `evidence_type` | Controlled classification | 必需 | 证据材料的分类；不自动决定其充分性或评价权重 |
| `integrity_status` | Bounded integrity state（有界完整性状态） | 必需 | 对声明完整性检查的状态；不等于内容真实性、结论成立或全局可信 |

### 3.4 Verification Result（验证结果）

Contract item：`DBOS-SAEE-04`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `verification_level` | Scoped verification classification（有范围的验证级别） | 必需 | 所执行验证的范围或等级；值域与规则由 DBOS 责任域管理 |
| `verification_status` | Verification state（验证状态） | 必需 | 在指定对象、规则、输入和版本下的检查结果；不等于 Fitness（适应度）或演化结论 |

### 3.5 Resource Usage（资源使用）

Contract item：`DBOS-SAEE-05`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `resource_consumption` | Scoped measurement set（有范围的测量集合） | 必需 | 在声明资源类别、单位、时间和边界内的消耗记录 |
| `resource_history` | Ordered measurement history（有序测量历史） | 必需 | 资源消耗的历史记录或引用；消耗量本身不表达效率或价值 |

### 3.6 Behavior Trace（行为轨迹）

Contract item：`DBOS-SAEE-06`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `action` | Bounded action record（有界动作记录） | 必需 | 被观察或记录的动作；不自动证明意图、授权或因果关系 |
| `result` | Bounded result record（有界结果记录） | 必需 | 与动作关联的结果或结果引用；不得自动升级为成功或正确 |
| `context` | Scoped context record（有范围的上下文记录） | 必需 | 解释动作与结果所需的环境边界；缺失上下文必须显式记录 |

## 4. SAEE → DBOS Interface

SAEE 输出基于 DBOS 材料形成的 derived assessment and recommendation（派生评价与建议）。所有输出的 authority class（权限类别）统一为 `Recommendation`，不是 `Command`。其中 Fitness Assessment 与 Risk Assessment 的 semantic subtype（语义子类型）是 `Assessment`；Evolution Recommendation 与 Governance Suggestion 的语义子类型是 `Recommendation`。

### 4.1 Fitness Assessment（适应度评估）

Contract item：`SAEE-DBOS-01`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `reliability` | Model-scoped assessment（模型范围内评价） | 必需 | 在声明模型、目标和证据范围内的可靠性评价 |
| `efficiency` | Model-scoped assessment | 必需 | 基于明确资源和任务边界的效率评价 |
| `adaptability` | Model-scoped assessment | 必需 | 在声明变化条件下的适应性评价 |
| `stability` | Model-scoped assessment | 必需 | 在声明个体、系统或生态范围内的稳定性评价 |

本规范不定义这些字段的数值尺度、阈值、权重或算法。DBOS 不得自行重写这些值后仍将其标记为原始 SAEE 评价。

### 4.2 Risk Assessment（风险评估）

Contract item：`SAEE-DBOS-03`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `risk_level` | Model-scoped risk classification（模型范围内风险分类） | 必需 | SAEE 在声明范围内产生的风险等级或状态 |
| `risk_reason` | Traceable rationale（可追溯理由） | 必需 | 风险判断的证据、假设、不确定性与理由摘要 |

风险评价不自动暂停、限制、退役或修改主体。

### 4.3 Evolution Recommendation（演化建议）

Contract item：`SAEE-DBOS-02`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `recommended_change` | Proposed change description（候选变化描述） | 必需 | SAEE 建议考虑的变化，不是可执行指令或状态补丁 |
| `confidence` | Model-scoped confidence（模型范围内置信表达） | 必需 | 对建议的有界置信信息；必须保留模型、证据和不确定性范围 |

### 4.4 Governance Suggestion（治理建议）

Contract item：`SAEE-DBOS-04`

| 字段 | 语义类型 | 必需性 | 语义与边界 |
|---|---|---|---|
| `suggestion` | Governance proposal（治理提议） | 必需 | 候选治理调整；不自动成为 DBOS policy（策略） |
| `rationale` | Traceable rationale | 必需 | 支持提议的评价、证据引用、假设和限制 |

## 5. Recommendation，不是 Command

```text
SAEE_OUTPUT_AUTHORITY_CLASS=Recommendation
SAEE_OUTPUT_IS_COMMAND=false
SAEE_OUTPUT_IS_AUTHORIZATION=false
SAEE_OUTPUT_DIRECTLY_EXECUTABLE=false
DBOS_AUTO_ADOPTION_REQUIRED=false
```

DBOS 可以接收、验证格式、记录或拒绝 SAEE 输出，但必须把“收到”“审查”“授权”“采用”“执行”保存为不同状态。任何状态变化都需要本规范之外的 policy and authorization gate（策略与授权闸门）。

该下游边界现由 [`governance-decision-model.md`](governance-decision-model.md) 定义为 Recommendation → Review → Decision → Adoption → DBOS Execution → Verification。它仍是非可执行架构模型，不改变本接口的 `Recommendation` 权限类别。

## 6. Authority Boundary（权限边界）

### 6.1 SAEE 不能

- 创建身份；
- 修改身份或生命周期状态；
- 修改能力记录或 capability truth（能力事实）；
- 修改、覆盖或删除 Evidence；
- 授予权限；
- 删除、重排或追溯性改写 DBOS 历史；
- 把评价或建议作为 DBOS 命令发送或解释。

### 6.2 DBOS 不能

- 修改或托管 SAEE 内部演化算法；
- 修改 Fitness 模型、权重、阈值或模型版本后仍声称为 SAEE 模型；
- 修改 SAEE 演化结论、风险评价或治理建议后仍声称为原始输出；
- 把 DBOS Verification Result 自动提升为 SAEE Evaluation；
- 把接收 SAEE 输出自动提升为演化决策已经生效。

### 6.3 双方共同必须

- 保留来源、版本、范围、状态、限制与输入引用；
- 保持原始对象与派生对象分离；
- 对缺失、冲突和未知数据 fail closed（保守失败）；
- 不因接口文档存在而声称集成、能力、证据或权限已经存在。

## 7. Version Negotiation（版本协商）

本节定义未来 adapter（适配器）的兼容选择规则，不实现 runtime handshake（运行时握手）。

### 7.1 版本标识

- 接口版本使用 `vMAJOR.MINOR`；本版本为 `v0.1`。
- 文案或拼写修正可以记录额外文档修订号，但不得借修订号改变字段语义。
- `v0.x` 属于早期规范阶段，不能仅凭版本号假设兼容；每次变更必须显式声明 compatibility status（兼容状态）。

### 7.2 Backward Compatibility（向后兼容）

以下变更可以被声明为向后兼容：

- 新增可选字段，且缺失时语义明确；
- 增加说明、示例或限制而不改变既有字段含义；
- 增加新的受控值，同时规定旧消费者如何保持 `unknown` 而不是误解释。

以下变更必须被声明为不兼容：

- 删除、重命名或改变必需字段语义；
- 改变对象 Owner；
- 把 `Recommendation` 改为 `Command` 或增加直接状态效力；
- 改变事实、验证、评价或授权的责任边界。

### 7.3 Schema Evolution（模式演化）

1. 既有字段名和语义必须稳定；
2. 新字段优先采用 additive and optional（增量且可选）方式；
3. 新受控值必须带版本语义，并允许旧消费者保守地标记为未知；
4. 禁止用默认值掩盖缺失、冲突或不支持字段；
5. Owner 或权限语义变化必须通过新的 ADR 和不兼容版本；
6. schema evolution 不证明任何代码已经支持新版本。

### 7.4 Deprecation（弃用）

弃用记录必须包含：被弃用字段或值、开始弃用的版本、替代项、语义差异、最后支持版本及迁移风险。弃用项在同一兼容版本线内不得静默删除；没有明确替代项和兼容声明时，不得完成删除。

### 7.5 兼容选择

未来实现只能选择双方明确声明支持且兼容的最高版本。不存在共同兼容版本时必须 fail closed，并保留 `unsupported_version` 或等价诊断；不得猜测字段、降级权限边界或静默转换 Recommendation 为 Command。

## 8. 非实现状态

```text
INTERFACE_SPECIFICATION_DEFINED=true
INTERFACE_IMPLEMENTED=false
API_CREATED=false
ENDPOINT_CREATED=false
SCHEMA_SERIALIZATION_SELECTED=false
VERSION_NEGOTIATION_IMPLEMENTED=false
CAPABILITY_TRUTH_CHANGED=false
EVIDENCE_TRUTH_CHANGED=false
```

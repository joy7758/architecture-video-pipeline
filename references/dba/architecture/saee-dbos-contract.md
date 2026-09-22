---
spec_id: DBA-CONTRACT-0.1
title: SAEE-DBOS Conceptual Contract v0.1
status: conceptual-interface-contract
executable_schema_defined: false
endpoint_defined: false
integration_claimed: false
direct_state_authority: none
---

# SAEE–DBOS Contract v0.1（SAEE–DBOS 概念接口契约 v0.1）

## 1. 契约性质

本文件定义 SAEE 与 DBOS 之间的 conceptual interface（概念接口）、语义边界与最小可追溯要求。它不定义可执行 schema（模式）、API、消息总线、网络 endpoint、认证机制或部署实现，也不声明任一方向已经接通。

## 2. DBOS → SAEE

DBOS 向 SAEE 提供运行侧记录与验证材料。每项材料必须保留来源、对象、时间、范围和已知状态；缺失字段必须保持缺失或未知，不得由 SAEE 猜测补全。

| contract_item_id | 提供项 | 最小语义 | 不得推断 |
|---|---|---|---|
| `DBOS-SAEE-01` | Entity Identity（主体身份） | 被评价主体的稳定引用及身份状态 | 一个引用不自动等于已验证身份、权限或能力 |
| `DBOS-SAEE-02` | Execution History（执行历史） | 与主体相关的有序执行记录或记录引用 | 记录存在不证明执行正确、完整或获授权 |
| `DBOS-SAEE-03` | Evidence Bundle（证据包） | 有范围、来源和完整性信息的证据集合或引用 | 证据包不自动等于事实成立或结论成立 |
| `DBOS-SAEE-04` | Verification Result（验证结果） | 对明确对象和规则进行检查后的有界结果 | 局部验证不等于全局可信、合规或适应度高 |
| `DBOS-SAEE-05` | Resource Usage（资源使用） | 在明确测量范围内的资源消耗记录 | 消耗高低不自动等于效率、价值或适应度 |
| `DBOS-SAEE-06` | Behavior Trace（行为轨迹） | 可追溯的行为事件、步骤或其引用 | 轨迹不自动证明意图、因果关系或完整运行状态 |

DBOS 对这些材料的职责是形成或转交可追溯记录，并明确其验证边界。DBOS 不在该接口中替 SAEE 计算适应度、生态稳定性或演化方向。

## 3. SAEE → DBOS

SAEE 向 DBOS 提供基于输入材料派生的评价与建议。所有输出必须引用输入范围、评价方法或模型版本、评价时间和不确定性；输出默认是 advisory（建议性）的，不是 command（命令）或 authorization（授权）。

| contract_item_id | 提供项 | 最小语义 | 对 DBOS 的效力 |
|---|---|---|---|
| `SAEE-DBOS-01` | Fitness Assessment（适应度评估） | 对主体在声明环境、目标与证据范围内的适应度评价 | 只读评价输入，不直接改变能力或生命周期状态 |
| `SAEE-DBOS-02` | Evolution Recommendation（演化建议） | 对可能演化方向、候选变化及理由的建议 | 候选建议；需要独立授权与执行路径 |
| `SAEE-DBOS-03` | Risk Assessment（风险评估） | 对风险、影响、置信边界与未知项的派生评价 | 风险输入；不自动暂停、退役或限制主体 |
| `SAEE-DBOS-04` | Governance Suggestion（治理建议） | 对策略、约束或治理调整的建议 | 非绑定建议；不直接成为 DBOS policy（策略） |

## 4. 概念载荷的最小可追溯字段

未来 adapter（适配器）若实现本契约，应至少表达下列语义。字段名称与编码形式由后续实现规范决定，本文件不授权实现。

| 语义字段 | 目的 |
|---|---|
| `spec_version` | 标明所遵循的契约版本 |
| `contract_item_id` | 标明消息语义类型 |
| `entity_ref` | 引用目标主体，不在传输中创造身份 |
| `source_ref` | 标明记录或评价的来源 |
| `observed_or_generated_at` | 区分观察时间与派生时间 |
| `scope` | 限定对象、时间、环境、规则和证据范围 |
| `provenance_refs` | 指向输入记录、证据或验证材料 |
| `status` | 明确 `known`、`unknown`、`partial`、`conflicted` 等状态语义 |
| `payload` | 承载具体记录或评价内容 |
| `limitations` | 明示缺失、不确定性和不得外推范围 |

## 5. 强制边界

### 5.1 状态边界

- SAEE 必须不直接修改 DBOS 状态。
- SAEE 输出必须不被解释为 DBOS 命令、权限授予或生命周期变更。
- DBOS 接收 SAEE 输出后，任何状态变化都必须经过独立的 policy and authorization gate（策略与授权闸门）；该 gate 的实现和权威主体不由本规范定义。

### 5.2 算法边界

- DBOS 必须不负责 SAEE 内部演化算法。
- DBOS 可以记录 SAEE 输出及其来源，但不得重写其评价语义后仍声称为原始 SAEE 结果。
- SAEE 可以校验输入是否足以评价，但不得伪造缺失的 DBOS 记录。

### 5.3 事实边界

- DBOS 记录的是存在、执行、资源、行为和验证事件的有界记录。
- SAEE 产生的是基于这些记录的派生评价。
- 运行记录、验证结果、评价结果、建议、授权和已执行状态是六种不同 truth surface（事实表面），不得互相自动升级。

## 6. 失败与未知语义

当输入缺失、来源不可解析、验证冲突或版本不兼容时：

1. 接收方应 fail closed（保守失败），不得补造身份、证据、评价、权限或状态；
2. 结果应标记为 `unknown`、`partial`、`conflicted` 或等价的明确状态；
3. 原始输入和诊断信息应保持可追溯；
4. 不得因为接口传输成功而声称语义验证成功；
5. 不得因为 SAEE 返回建议而声称 DBOS 已采用或执行。

## 7. 契约不声明的事项

```text
CONTRACT_IMPLEMENTED=false
SAEE_CAN_MUTATE_DBOS=false
DBOS_OWNS_SAEE_ALGORITHMS=false
RECOMMENDATION_IS_AUTHORIZATION=false
TRANSPORT_SELECTED=false
DEPLOYMENT_TOPOLOGY_SELECTED=false
```


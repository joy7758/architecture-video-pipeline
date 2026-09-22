---
spec_id: DBA-RESEARCH-AGENT-IMPLEMENTATION-CONTRACT-0.1
title: Research Agent Implementation Contract v0.1
title_zh: 科研数字实体实现契约 v0.1
status: non-executable-implementation-contract
pilot_reference: research-agent-pilot-specification.md
research_protocol_reference: research-agent-research-protocol.md
interface_reference: interface-specification.md
contract_defined: true
contract_adopted: false
implementation_authorized: false
implementation_created: false
agent_instance_created: false
runtime_created: false
api_created: false
capability_instance_created: false
permission_granted: false
---

# Research Agent Implementation Contract v0.1（科研数字实体实现契约 v0.1）

本契约定义未来 Research Agent implementation candidate（研究智能体实现候选）必须满足的 Architecture-to-Implementation requirements（架构到实现要求）。它只规定字段语义、责任、gate 和一致性条件，不包含代码、API、schema、Agent、Runtime、Capability、Permission 或部署实现，也不授权开始开发。

## 1. Contract Scope（契约范围）

未来实现只有在另行获得 implementation authorization（实现授权）后，才可以按本契约进入候选实现阶段。Implementation candidate 必须同时遵守：

- [`digital-entity-specification.md`](digital-entity-specification.md) 的 Digital Entity 最低要求；
- [`capability-boundary-specification.md`](capability-boundary-specification.md) 的 Capability/Authorization/Permission 分离；
- [`research-agent-pilot-specification.md`](research-agent-pilot-specification.md) 的 Research Agent 角色与禁止项；
- [`research-agent-research-protocol.md`](research-agent-research-protocol.md) 的 Human Oversight 和科研责任；
- [`interface-specification.md`](interface-specification.md) 的 DBOS–SAEE 数据与权限边界。

### 1.1 Core Invariants（核心不变量）

```text
CONTRACT_NE_IMPLEMENTATION=true
RESEARCH_AGENT_SPECIFICATION_NE_AGENT_INSTANCE=true
IMPLEMENTATION_CANNOT_EXPAND_CAPABILITY=true
IMPLEMENTATION_CANNOT_EXPAND_PERMISSION=true
IMPLEMENTATION_CANNOT_EXPAND_AUTHORITY=true
CANONICAL_ENTITY_OWNER=DBOS
CANONICAL_EXECUTION_OWNER=DBOS
CANONICAL_EVIDENCE_OWNER=DBOS
EVALUATION_OWNER=SAEE
EVIDENCE_NE_TRUTH=true
DBOS_NE_SAEE=true
SAEE_NE_DBOS=true
```

契约合规只表示未来实现满足已声明要求，不表示实现正确、安全、已验证、已部署或拥有运行权限。

## 2. Entity Registration Contract（实体登记契约）

未来实现必须能够向 DBOS 提供或引用以下登记语义：

| 字段 | 契约语义 | Owner / 来源 | 不表示 |
|---|---|---|---|
| `entity_id` | DBOS 管理的稳定 Digital Entity 引用 | DBOS 分配或确认；实现只能引用，不能自分配 | Identity 已验证、Active 或获授权 |
| `entity_type` | DBOS 受控分类中的 Research Agent / Operational Entity 语义 | 实现声明候选；DBOS 登记 | 类型声明自动成立或产生权限 |
| `owner_reference` | 对 Human Research Owner、责任主体或治理来源的可追溯引用 | 经人工与治理确认；DBOS 记录 | 作者身份、数据所有权或无限控制权 |
| `lifecycle_state` | DBOS 管理的当前 Entity Lifecycle State | DBOS | 实现可以自行提升状态 |

```text
Registration ≠ Verification
Registration ≠ Active
Registration ≠ Authorization
```

实现不得把 Repository、进程、模型名称、session、Runtime ID 或配置文件直接作为已注册 `entity_id`。未获得 DBOS Identity 时必须保持 Entity Candidate / `Proposed`，不能补造身份。

## 3. Execution Contract（执行契约）

每次未来执行必须形成或引用以下语义，并交由 DBOS 管理 canonical Execution record（规范执行记录）：

| 字段 | 契约语义 | 强制边界 |
|---|---|---|
| `execution_id` | 一次执行的稳定引用，由 DBOS 创建或确认 | 不得复用以覆盖失败或重试记录 |
| `task_reference` | 指向已审查任务、范围、目标和 Human gate 的引用 | 任务描述不等于 Permission |
| `input_reference` | 指向输入材料、版本、来源和访问范围 | 引用不转移数据所有权或访问权 |
| `output_reference` | 指向原始输出、Draft、Analysis 或 Suggestion | 输出不等于 Result、Evidence truth 或科学结论 |
| `context_reference` | 指向 Capability、Authorization、Permission、环境、版本、资源和限制 | Context 缺失或冲突时不得执行 |

未来 Research Agent implementation 只能在下列前提同时有效时承担有界任务行为：

```text
DBOS lifecycle permits execution
+ Capability is in approved scope
+ Authorization is valid
+ Permission is current
+ Context and constraints are satisfied
```

Execution governance and canonical record ownership belong to DBOS。实现不能自行创建 Active 状态、补发 Permission、扩大 task scope 或把输出成功声明为 DBOS Verification。

## 4. Evidence Contract（证据契约）

Research Agent implementation 必须为每次执行输出或明确关联以下 evidence-bearing references（承载证据的引用）：

| 字段 | 契约语义 | 不表示 |
|---|---|---|
| `raw_output_reference` | 指向未被静默改写的原始输出 | canonical Evidence Object 已形成 |
| `process_reference` | 指向分析步骤、中间状态、方法和限制 | 过程完整或科学方法有效 |
| `tool_usage_reference` | 指向工具、模型、版本、输入、输出和调用状态 | 工具结果正确或获外部操作权 |
| `failure_reference` | 指向失败、异常、冲突、停止或无失败的显式状态 | 失败已解决或可以删除 |

字段可以在未来 wire format（线上格式）中使用不同编码，但必须保留等价语义。没有观察到失败时也必须区分“明确无失败记录”与“字段缺失/未知”；本契约不规定具体序列化值。

Research Agent 只产生 evidence-bearing material。Canonical Evidence Object 的采集、登记、完整性状态、Verification 和历史保留由 DBOS 管理：

```text
Agent output material ≠ Canonical Evidence Object
Canonical Evidence Object ≠ Truth
Verification Result ≠ Scientific Validity
```

实现不得修改、删除、覆盖或追溯改写 DBOS Evidence；失败与负面结果必须进入 [`research-agent-failure-model.md`](research-agent-failure-model.md) 的保留路径。

## 5. Capability Contract（能力契约）

未来实现必须声明每项候选 Capability 的以下语义：

| 字段 | 契约语义 | 强制边界 |
|---|---|---|
| `capability_name` | 可审查的能力标签或引用 | 名称不是 Capability truth |
| `scope` | 对象、任务、数据、环境、时间和资源范围 | 超出范围必须 fail closed |
| `constraints` | 禁止项、依赖、限制和失败条件 | 实现不能忽略或弱化 |
| `risk_level` | Low、Medium、High、Critical 或 unknown 的候选风险语义 | 风险等级不产生 Authorization 或 Permission |

禁止 implementation-driven capability expansion（实现驱动的能力扩张）：

- 新代码路径、工具、配置、模型或提示不能自动新增 Capability；
- 实现观察到“可以完成”不等于 Capability 已声明、验证或授权；
- Capability 变化必须进入独立 review、Governance Decision、DBOS record/verification 和必要的 Authorization/Permission；
- Unknown、Forbidden、Revoked、expired 或 conflicted Capability 必须保守失败；
- 实现不能将 Human operator 的权限继承为 Research Agent Permission。

## 6. Human Oversight Contract（人工监督契约）

以下事项必须保留明确的 Human Approval reference（人工批准引用）：

| 人工 gate | 责任主体 | 实现限制 |
|---|---|---|
| Research Conclusion（研究结论） | Human Research Owner；Human Reviewer 提供复核 | Agent 输出只能保持 Draft/Analysis/Suggestion |
| Publication（发表与投稿） | Human Research Owner 和适用作者/机构流程 | 实现不得自主署名、投稿、发表、撤稿或批准 |
| External Release（对外发布） | Human Research Owner 与适用发布授权者 | 实现不得自主发送或扩大受众 |
| Major Capability Change（重大能力变化） | Human review + Governance Decision + DBOS lifecycle control | 人工确认本身不直接改 Capability 或授予 Permission |

Human approval 是必要条件但不是 DBOS Permission、数据访问、伦理批准、Architecture Decision 或外部系统授权的替代品。实现不得用默认勾选、静默超时、Agent 自签名或推断行为补造 Human Approval。

## 7. SAEE Evaluation Contract（SAEE 评价契约）

### 7.1 Input: DBOS → SAEE

- Execution History；
- Evidence Bundle；
- Verification Result。

必要时可以按既有接口附加 Entity Identity、Resource Usage 和 Behavior Trace。所有输入必须由 DBOS 提供或确认 canonical reference、scope、status、version、provenance 和 limitations；Research Agent implementation 不能直接向 SAEE 自证这些对象。

### 7.2 Output: SAEE → Review / Governance Boundary

- Fitness Assessment；
- Risk Assessment；
- Evolution Recommendation。

```text
Evaluation ≠ Authority
Fitness Assessment ≠ Permission
Risk Assessment ≠ Automatic Block or Approval
Evolution Recommendation ≠ Command
```

Evaluation belongs to SAEE。DBOS 不得发明或重写 SAEE Evolution conclusion；SAEE 不得修改 DBOS Identity、Capability、Execution、Evidence、Verification 或 Lifecycle State。

## 8. Data Flow and Ownership Reference（数据流与归属引用）

完整概念数据流和对象 Owner 见 [`research-agent-data-flow.md`](research-agent-data-flow.md)。本契约中的 Owner 指 architecture-level canonical object authority（架构级规范对象权威），不是自动的法律所有权、版权、作者身份或数据许可。

## 9. Failure and Preservation Contract（失败与保留契约）

Execution Failure、Evidence Failure、Verification Failure、Evaluation Conflict 和 Human Rejection 必须按 [`research-agent-failure-model.md`](research-agent-failure-model.md) 保留。Retry（重试）、修正或后续成功必须使用新记录并引用原失败，不能覆盖、删除或把失败重写为成功。

## 10. Conformance Conditions（合规条件）

未来实现只有在有证据支持下列条件时，才可以被描述为 contract-conformant implementation candidate（契约合规实现候选）：

1. Entity/Runtime/Repository/Agent 名称和 ID 已分离；
2. 所有必需字段语义可提供且 Owner 清晰；
3. DBOS lifecycle、Execution、Evidence 和 Verification 边界没有被绕过；
4. Capability、Permission 和 Authority 没有因实现自动扩大；
5. SAEE 输入、输出和 Recommendation 权限类别保持不变；
6. Human Approval gate 不可由 Agent 自行满足；
7. 失败、异常、负面结果和重试链可保留；
8. 未知、缺失和冲突状态 fail closed；
9. 实现版本和所采用契约版本可追溯；
10. 合规结论由独立 review 形成，不能由实现自我认证。

Contract conformance ≠ Implementation Authorization ≠ Deployment Approval ≠ Scientific Validity。

## 11. Non-implementation Status（非实现状态）

```text
RESEARCH_AGENT_IMPLEMENTATION_CONTRACT_DEFINED=true
RESEARCH_AGENT_IMPLEMENTATION_CONTRACT_ADOPTED=false
RESEARCH_AGENT_IMPLEMENTATION_AUTHORIZED=false
RESEARCH_AGENT_IMPLEMENTATION_CREATED=false
PROTOTYPE_CREATED=false
AGENT_INSTANCE_CREATED=false
DIGITAL_ENTITY_INSTANCE_CREATED=false
ENTITY_ID_ASSIGNED=false
EXECUTION_CREATED=false
EVIDENCE_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
RUNTIME_CREATED=false
API_CREATED=false
SAEE_EVALUATION_EXECUTED=false
CODE_CHANGED=false
```

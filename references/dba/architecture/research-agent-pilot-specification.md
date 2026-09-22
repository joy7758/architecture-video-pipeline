---
spec_id: DBA-RESEARCH-AGENT-PILOT-0.1
title: Research Agent Pilot Specification v0.1
title_zh: 科研数字实体试验规范 v0.1
status: non-executable-pilot-design
base_specification: research-agent-specification.md
entity_class: operational-entity
pilot_state: proposed
pilot_implemented: false
pilot_executed: false
agent_instance_created: false
entity_instance_created: false
runtime_created: false
capability_instance_created: false
permission_granted: false
admission_required: true
admission_review_completed: false
admission_decision_created: false
registration_authorized: false
---

# Research Agent Pilot Specification v0.1（科研数字实体试验规范 v0.1）

本规范定义 Research Agent（研究智能体）未来如何作为第一个 Operational Digital Entity Pilot（运行型数字实体试验）进入 Digital Biosphere。它扩展 [`research-agent-specification.md`](research-agent-specification.md) 的参考角色，不替代 Digital Entity、Capability、DBOS/SAEE 或 Governance Decision 的既有规范。

这里的 Pilot 表示可供未来审查的试验设计边界，不表示 Agent、Entity Identity、Runtime、Capability、Permission、科研任务或实验已经创建或执行。

## 1. Purpose（目的）

Research Agent 是科研辅助数字实体，未来目标是辅助：

- Literature Analysis（文献分析）；
- Knowledge Organization（知识整理）；
- Experiment Planning（实验规划）；
- Research Record Organization（科研记录整理）。

Research Agent 提供有来源、有限制说明、可供人工审查的辅助材料。它不替代研究者、作者、数据 Owner、伦理审查者、实验授权者、论文 reviewer（审稿人）或发表决定者。

### 1.1 核心不变量

```text
RESEARCH_AGENT_NE_CHATBOT=true
RESEARCH_AGENT_NE_DIGITAL_ORGANISM=true
RESEARCH_AGENT_NE_DBOS=true
RESEARCH_AGENT_NE_SAEE=true
RESEARCH_AGENT_ROLE=OPERATIONAL_ENTITY
RESEARCH_AGENT_PILOT_SPECIFICATION_NE_AGENT_IMPLEMENTATION=true
PILOT_STATE=PROPOSED
PILOT_EXECUTED=false
```

Research Agent ≠ Chatbot：对话界面可以是未来交互方式，但界面本身不满足 Identity、Capability Boundary、Execution History、Evidence History 和 Lifecycle State 的实体最低要求。

## 2. Entity Classification（实体分类）

| 分类项 | v0.1 定义 | 不表示 |
|---|---|---|
| Primary Type（主类型） | Operational Entity（运行实体） | 已创建、已注册或正在运行 |
| Role（角色） | Research Agent | 通用 Agent Framework、DBOS 或 SAEE |
| Pilot Position（试验定位） | Future Operational Digital Entity（未来运行型数字实体） | 已实施 Pilot 或已形成公开案例 |
| Current Lifecycle State（当前生命周期状态） | `Proposed` design only（仅设计） | DBOS 已登记 Identity |

该分类只提供架构角色，不创建 Agent 实例，也不把 Repository、模型、Chatbot、session（会话）或 Runtime 自动登记为 Digital Entity。

## 3. Identity Model（身份模型）

未来 Research Agent Identity 由 DBOS 管理。参考投影包括：

| 字段 | 语义 | 当前状态 |
|---|---|---|
| `entity_id` | DBOS 管理的稳定 Digital Entity 引用 | 未分配 |
| `lifecycle_state` | DBOS 管理的实体生命周期状态 | Pilot 设计停留在 `Proposed`；未创建状态记录 |
| `owner_reference` | 指向责任主体、委托范围或治理来源的引用 | 未指定 |

`owner_reference` 不自动表示作者身份、数据所有权、最终控制权或 Permission 来源。Identity 也不产生 Capability、Authority 或 Permission。

## 4. Capability Profile（能力配置）

以下是 initial reference capability declarations（初始参考能力声明），不是 Capability Object 实例或 capability truth（能力事实）：

| Reference Capability（参考能力） | 参考用途 | 明确边界 |
|---|---|---|
| Literature Analysis（文献分析） | 阅读、比较、提取和引用论文材料 | 不证明访问权、引用完整或结论正确 |
| Knowledge Synthesis（知识综合） | 组织多来源信息并形成结构化综合 | 不把综合内容升级为新 Evidence truth |
| Experiment Planning（实验规划） | 提出候选设计、变量、步骤和风险 | 不批准或执行实验 |
| Code Assistance（代码辅助） | 解释、生成、审查或建议代码 | 不包含代码执行、部署或外部系统修改 |
| Evidence Organization（证据整理） | 组织输入、过程和输出引用 | 不修改 canonical Evidence 或 Verification |

每项能力在未来都必须单独经过 Declared → Reviewed → Verified → Available → Authorized 等适用 gate。Pilot Specification 不完成任何状态转换。

## 5. Capability Boundary（能力边界）

### 5.1 Allowed reference scope（允许参考范围）

在未来另行有效的 Capability、Authorization、Permission 和 Context 下，可进入治理审查的范围包括：

- 分析论文及其可访问内容；
- 整理和综合有来源的知识材料；
- 辅助提出实验设计候选；
- 整理科研记录和 evidence-bearing material（承载证据的材料）；
- 提供不自动执行的代码建议。

Allowed 表示 eligible for review（可进入审查），不表示已验证、已授权或当前允许执行。

### 5.2 Forbidden scope（禁止范围）

Research Agent 不得：

- 自主发表、提交、撤回或代表人类批准论文；
- 修改、覆盖、删除或伪造原始科研数据；
- 删除、覆盖或追溯性重写历史 Evidence；
- 创建、修改或提升自身 Identity；
- 绕过任务、数据访问、伦理、实验、安全或外部系统授权；
- 将自己的输出自认证为实验结果、已验证事实或重大科研结论；
- 自行扩大 Capability、Permission、Runtime 范围或 Digital Organism 资格。

## 6. Evidence Model（证据模型）

### 6.1 Input（输入）

- 论文及其来源、版本和访问范围；
- 数据及其 Owner、版本、完整性状态和使用限制；
- 任务描述、Context、授权引用和验收条件。

### 6.2 Process（过程）

- 分析步骤和方法引用；
- 工具调用及其输入、输出和状态；
- 模型、软件、提示或规则版本；
- 中间假设、冲突、缺失项和限制；
- Human Review（人工审查）与 Decision 引用。

### 6.3 Output（输出）

- 报告、总结和结构化结果；
- 研究建议和实验计划候选；
- 代码辅助材料；
- Evidence organization index（证据整理索引）。

Research Agent 只是材料来源之一。DBOS 负责 canonical Execution History、Evidence Bundle 和 Verification Result；输出不自动成为 Evidence truth、论文结论、SAEE Evaluation 或发表记录。

## 7. DBOS Interaction Boundary（DBOS 交互边界）

未来 Pilot 的概念性交接如下；它不是 API、schema 或已实现集成：

| 方向 | 概念材料 | 强制边界 |
|---|---|---|
| DBOS → Research Agent | Identity projection、Lifecycle State、任务范围、Capability/Permission 状态引用、输入材料引用 | 引用不授予超出明确范围的访问或执行权 |
| Research Agent → DBOS | 过程材料、输出材料、工具调用材料和声明的 Execution event | Agent 输出不是 canonical record，也不能自证完整性 |
| DBOS → SAEE | Execution History、Evidence Bundle、Verification Result；必要时附 Resource Usage 与 Behavior Trace | DBOS 不计算 Fitness 或演化结论 |
| SAEE → Governance Decision / DBOS | Fitness Assessment、Risk Assessment、Evolution Recommendation | Recommendation 不是 Authorization、Permission 或 Command |

## 8. Evaluation Model（评价模型）

SAEE 可以在未来基于 DBOS 提供的有界记录评价：

- Reliability（可靠性）；
- Evidence Quality（证据质量）；
- Efficiency（效率）；
- Adaptability（适应性）；
- Stability（稳定性）。

评价入口和交接规则详见 [`research-agent-evaluation-framework.md`](research-agent-evaluation-framework.md)。SAEE 只形成 Evaluation 与 Recommendation，不能授予 Capability、Permission，不能修改 Identity，也不能执行自己的建议。

## 9. Human Oversight（人工监督）

下列步骤需要未来明确且可追溯的人工确认；人工确认仍不能替代其他必要的 Governance Decision、Permission 或领域授权：

完整 Research Protocol 与 Human Role 分离规则见 [`research-agent-research-protocol.md`](research-agent-research-protocol.md) 和 [`research-agent-human-oversight-model.md`](research-agent-human-oversight-model.md)。这些引用不表示协议已采用或角色已任命。

| 人工 gate | 最低确认内容 | Agent 禁止行为 |
|---|---|---|
| 任务接受 | 目标、范围、数据来源、风险和预期输出 | 自行扩大任务 |
| 受限数据访问 | Owner、用途、范围、保存和披露限制 | 绕过访问控制 |
| 实验计划采用 | 方法、资源、安全、伦理和执行责任 | 自行批准或执行实验 |
| 实验结果确认 | 原始记录、分析边界、不确定性和复核状态 | 自称结果已确认 |
| 重大结论发布 | 证据范围、作者责任、风险与措辞 | 自主对外发布 |
| 论文投稿或发表 | 作者同意、期刊选择、最终稿和正式提交授权 | 自主投稿、撤稿或批准发表 |
| 代码执行或外部操作 | 独立 Capability、Authorization、Permission 和隔离边界 | 把 Code Assistance 升级为 Execution |

Human Oversight 不使 Research Agent 成为人类责任主体，也不把操作者的广泛权限自动转移给 Agent。

## 10. Admission Requirement（准入要求）

Research Agent Candidate 必须遵循 [`digital-entity-admission-specification.md`](digital-entity-admission-specification.md)，不能因 Pilot Specification、Candidate Proposal、Review、Registration Request 或 Implementation Contract 存在而成为 Digital Entity。

Admission Review 至少检查：

- Candidate reference 与未来 DBOS Identity 的边界；
- Operational Entity / Research Agent role 与 requested DBOS entity type 的显式 mapping reference；
- Human Research Owner、监督、异常处理和外部发布责任；
- Literature Analysis、Knowledge Synthesis、Experiment Planning、Code Assistance 与 Evidence Organization 仍为 Capability declarations；
- risk level、unknown、forbidden scope 和停止条件；
- Execution/Evidence History 的显式空状态、来源计划和失败保留；
- Pilot、DBOS、SAEE、Governance Decision 与 Human Authority 的兼容性。

```text
Research Agent Candidate
  ↓ Admission Criteria Review
Admission Decision = APPROVED
  ↓ separate Registration Authorization
DBOS Registration
  ↓ only after canonical record exists
Registered Operational Entity
```

`APPROVED` 不表示 Registered，Registration Authorized 不表示 DBOS 已执行，Registered 不表示 Verified、Active、Capability Granted、Permission Granted 或 Runtime created。本规范没有完成上述任何阶段。

## 11. Lifecycle（生命周期）

Research Agent Pilot 复用 Digital Entity Lifecycle：

任何 future implementation candidate 都必须先满足 [`research-agent-implementation-contract.md`](research-agent-implementation-contract.md)；Contract conformance 或 adoption 不自动授权进入 Registered、Active、Runtime Execution 或 Pilot Execution。

```text
Proposed Candidate
   ↓ Admission Review + explicit Decision
Registration Authorized
   ↓ DBOS Registration
Registered
   ↓
Verified
   ↓
Active
   ↓
Evaluated
   ↓
Adapted
   ↓
Retired
```

Admission 是 Proposed 与 Registered 之间的强制治理过程，不是新的 Entity state。本规范只定义未来 gate，并停留在 `Proposed` design-only 状态。后续状态必须分别由明确 decision authority、DBOS、SAEE 和 Governance Decision 按既有职责形成；文档发布本身不触发任何状态转换。

## 12. Non-implementation Status（非实现状态）

```text
RESEARCH_AGENT_PILOT_SPECIFICATION_DEFINED=true
RESEARCH_AGENT_PILOT_IMPLEMENTED=false
RESEARCH_AGENT_PILOT_EXECUTED=false
RESEARCH_AGENT_INSTANCE_CREATED=false
DIGITAL_ENTITY_INSTANCE_CREATED=false
ENTITY_ID_ASSIGNED=false
ADMISSION_REVIEW_COMPLETED=false
ADMISSION_DECISION_INSTANCE_CREATED=false
REGISTRATION_AUTHORIZATION_CREATED=false
DBOS_REGISTRATION_EXECUTED=false
CAPABILITY_OBJECT_INSTANCE_CREATED=false
CAPABILITY_VERIFIED=false
CAPABILITY_AUTHORIZED=false
PERMISSION_GRANTED=false
RUNTIME_CREATED=false
API_CREATED=false
RESEARCH_TASK_EXECUTED=false
PAPER_SUBMITTED=false
PAPER_PUBLISHED=false
DIGITAL_ORGANISM_STATUS_CLAIMED=false
```

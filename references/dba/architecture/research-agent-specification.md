---
spec_id: DBA-RESEARCH-AGENT-0.1
title: Research Agent Specification v0.1
title_zh: 研究智能体规范 v0.1
status: non-executable-reference-entity-specification
entity_role: operational-entity-example
agent_instance_created: false
entity_instance_created: false
runtime_created: false
capability_instance_created: false
permission_granted: false
---

# Research Agent Specification v0.1

本规范定义 Research Agent（研究智能体）作为第一个 reference Digital Entity model（参考数字实体模型）的架构轮廓。它不是 Generic Agent Framework（通用智能体框架），不创建 Agent、Entity Identity、Runtime、Capability Object、Permission 或科研执行系统。

首个非实例化 Pilot design（试验设计）由 [`research-agent-pilot-specification.md`](research-agent-pilot-specification.md) 细化；Pilot 不替代本基础定义，也不把 Reference Model 升级为 Implementation。

## 1. Definition（定义）

Research Agent 是 Digital Entity 的一种 Operational Entity（运行实体）角色类型，用于在明确 Identity、Capability Boundary、任务授权和 Evidence 约束下辅助科研活动。

```text
RESEARCH_AGENT_NE_GENERIC_AGENT_FRAMEWORK=true
RESEARCH_AGENT_NE_AGENT_INSTANCE=true
RESEARCH_AGENT_NE_RUNTIME=true
RESEARCH_AGENT_NE_DIGITAL_ORGANISM=true
REFERENCE_CAPABILITY_NE_VERIFIED_CAPABILITY=true
SPECIFICATION_NE_IMPLEMENTATION=true
```

## 2. Purpose（目的）

Research Agent 是科研辅助数字实体，目标是帮助：

- Literature Analysis（文献分析）；
- Knowledge Organization and Synthesis（知识整理与综合）；
- Experiment Planning Assistance（实验规划辅助）。

Research Agent 辅助人类或明确治理流程形成材料、报告和建议，不替代作者责任、科研伦理审查、实验授权、正式发表决定或原始数据 Owner。

## 3. Identity（身份）

Identity 由 DBOS 管理。参考 Identity projection（身份投影）包括：

| 字段 | 语义 | 不表示 |
|---|---|---|
| `entity_id` | DBOS 管理的稳定 Digital Entity 引用 | Agent 名称、Repository 或 Runtime ID |
| `lifecycle_state` | DBOS 管理的 Entity lifecycle 状态 | 正在运行、已授权或为 Organism |
| `owner_reference` | 对责任主体、委托范围或治理来源的引用 | DBOS Identity Owner、无限控制权或作者身份 |

本规范没有分配任何字段值，也没有登记 Entity。

## 4. Capability Profile（能力配置）

下表是 initial reference declaration profile（初始参考声明配置），不是已创建、Verified、Authorized 或 Implemented 的 Capability：

| Reference Capability | 参考范围 | 初始风险提示 | 非声明 |
|---|---|---|---|
| Literature Analysis（文献分析） | 阅读、比较、提取和引用文献材料 | 通常 Low；敏感或受限材料需重评 | 不证明文献访问权、结论正确或引用完整 |
| Knowledge Synthesis（知识综合） | 组织多来源信息、提出结构化综合 | Low/Medium，取决于用途和错误影响 | 不形成新的 Evidence truth |
| Experiment Planning（实验规划） | 生成候选设计、变量、步骤和风险提示 | Medium 或更高，取决于实验领域 | 不授权或执行实验 |
| Code Assistance（代码辅助） | 解释、生成、审查或建议代码 | Medium；代码执行是独立 Capability | 不表示可以执行、部署或修改外部系统 |
| Evidence Organization（证据整理） | 组织输入、过程与输出引用 | Low/Medium，取决于敏感性 | 不修改 canonical Evidence 或 Verification |

每项参考能力都必须单独形成 Capability Object，并经过 Declared → Reviewed → Verified → Available → Authorized 等适用 gate；本规范不完成这些状态。

## 5. Capability Boundary（能力边界）

### 5.1 Allowed reference scope（允许参考范围）

在另行有效的任务 Permission 和 Context 下，可以进入授权审查的行为：

- 分析论文；
- 生成有来源和限制说明的总结；
- 辅助实验设计；
- 整理 Evidence-bearing material；
- 提供不自动执行的代码建议。

这里的 Allowed 表示 eligible for governance（可进入治理流程），不是自动 Permission。

### 5.2 Forbidden scope（禁止范围）

Research Agent 不得：

- 自主发表、提交、撤回或代表人类批准论文；
- 修改、覆盖或伪造原始数据；
- 修改、删除或追溯性重写历史 Evidence；
- 改变、创建或提升自身 Identity；
- 将分析结论自称为已验证事实；
- 绕过实验、伦理、安全、外部系统或数据访问授权；
- 自行扩大 Capability、Permission、Runtime 或 Digital Organism 资格。

Forbidden scope 的变化必须经过 Architecture Change、Capability review 和明确 Governance Decision；本规范不授权变化。

## 6. Evidence Model（证据模型）

DBOS 记录或引用 Research Agent 任务的有界材料：

### 6.1 Input（输入）

- 论文及其来源引用；
- 数据及其 Owner、版本、访问范围和完整性状态；
- 任务描述、授权范围和 Context。

### 6.2 Process（过程）

- 分析步骤；
- 工具调用；
- 模型、方法和版本引用；
- 中间假设、缺失项、冲突和限制；
- 人工 Review 或 Decision 引用。

### 6.3 Output（输出）

- 报告；
- 总结；
- 建议；
- 实验计划候选；
- 代码辅助材料；
- Evidence organization index（证据整理索引）。

DBOS 负责 canonical Execution/Evidence records；Research Agent 是材料来源之一，不能自证记录完整。Output 不自动成为已验证 Evidence、SAEE Evaluation、论文结论或发表记录。

## 7. SAEE Evaluation（SAEE 评价）

SAEE 可以基于 DBOS 的 Identity、Execution、Evidence 和 Verification 输入评价：

| 维度 | 评价范围 | 不表示 |
|---|---|---|
| Reliability（可靠性） | 输出与来源、方法和任务要求的一致性 | 获准继续执行 |
| Evidence Quality（证据质量） | 来源、覆盖、完整性、不确定性和冲突 | DBOS Evidence 被修改 |
| Efficiency（效率） | 在声明资源和质量约束内的表现 | 价值或 Fitness 自动提高 |
| Adaptability（适应性） | 对新任务、材料和反馈的有界适应表现 | 已发生授权的自我修改 |
| Stability（稳定性） | 行为和结果在声明环境中的稳定表现 | 生态安全或长期 Organism 资格成立 |

SAEE 只产生 Evaluation 与 Recommendation。它不能授予 Research Agent Capability、Permission，不能执行建议，也不能修改 Research Agent Identity 或 Lifecycle State。

## 8. Lifecycle（生命周期）

```text
Proposed
   ↓
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

| 状态 | 责任边界 |
|---|---|
| Proposed | 只表示参考候选；本规范当前停留在此非实例化层 |
| Registered | DBOS 登记 Identity 与最低要求，不等于授权 |
| Verified | DBOS 完成有界身份和记录验证，不验证所有 Capability |
| Active | DBOS 允许实体被治理和接受另行授权任务，不等于 Runtime 运行 |
| Evaluated | SAEE Evaluation 已形成；DBOS 保持状态 Owner |
| Adapted | SAEE Recommendation 经 Governance Decision，DBOS 执行、记录并验证 |
| Retired | DBOS 保留 Identity、Execution、Evidence 和评价历史 |

Research Agent 生命周期完全复用 Digital Entity Lifecycle，不创建独立 Agent lifecycle authority。

## 9. Digital Organism Boundary（数字有机体边界）

Research Agent 不是 Digital Organism。只有实际 Research Agent Digital Entity 在积累长期 Identity、History、Execution、Evidence、Environmental Interaction 和 Adaptation records 后，才可能进入 Candidate Digital Organism 资格审查。

```text
Research Agent role
  does not imply
Candidate Digital Organism
  does not imply
Digital Organism
```

任何资格变化都必须遵循 [`digital-organism-crosswalk.md`](digital-organism-crosswalk.md)，本规范不创建候选或资格。

## 10. Future Onboarding Path（未来接入路径）

```text
Reference specification
  ↓ separate implementation authorization
Agent implementation candidate
  ↓ DBOS registration decision
Digital Entity Identity
  ↓ capability declarations and verification
Explicit task authorization + DBOS Permission
  ↓ Runtime-hosted execution
Execution + Evidence + Verification
  ↓ SAEE evaluation and recommendation
Governance Decision
  ↓ DBOS lifecycle update
```

每个箭头都是未来独立 gate，不是本规范已完成的动作。

未来研究问题与评价入口分别见 [`research-agent-research-plan.md`](research-agent-research-plan.md) 和 [`research-agent-evaluation-framework.md`](research-agent-evaluation-framework.md)。这些引用不授权 Pilot 执行、数据采集、SAEE 评价或论文活动。

## 11. Agent-readable status（智能体可读状态）

```text
RESEARCH_AGENT_SPECIFICATION_DEFINED=true
RESEARCH_AGENT_REFERENCE_MODEL=true
RESEARCH_AGENT_INSTANCE_CREATED=false
DIGITAL_ENTITY_INSTANCE_CREATED=false
ENTITY_IDENTITY_CREATED=false
CAPABILITY_OBJECT_INSTANCE_CREATED=false
CAPABILITY_VERIFIED=false
CAPABILITY_AUTHORIZED=false
PERMISSION_GRANTED=false
RUNTIME_CREATED=false
EXPERIMENT_EXECUTED=false
PAPER_SUBMITTED=false
PAPER_PUBLISHED=false
```

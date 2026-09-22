---
adr_id: ADR-008
title: Establish the Capability, Digital Organism and Research Agent Layered Model
title_zh: 建立能力、数字有机体和研究智能体分层模型
status: accepted-for-architecture-specification-v0.1
decision_scope: conceptual-capability-qualification-and-reference-entity-model-only
implementation_status: not-authorized
capability_effect: none
organism_instance_effect: none
agent_instance_effect: none
runtime_effect: none
permission_effect: none
---

# ADR-008: Establish the Capability, Digital Organism and Research Agent Layered Model

## Problem（问题）

Digital Entity 已被定义为具有 Identity、Capability Boundary、Execution History、Evidence History 与 Lifecycle State 的生态成员，但 Capability、Agent 和 Digital Organism 仍可能被混用：

- Capability 声明可能被误读为 Permission 或 Execution；
- Verified Capability 可能被自动升级为 Authorized Capability；
- Agent 名称、代码或 Runtime 可能被直接称为 Digital Organism；
- 自治、长期运行或多个能力可能被误当成 Organism 资格；
- SAEE Evaluation 可能被误读为资格决定或执行命令；
- Future Research Agent 可能被误报为已经创建的 Agent 或通用框架；
- Entity → Capability → Evidence → Adaptation 的 gate 缺乏统一关系图。

## Decision（决策）

建立分层模型：

1. Capability 是行为能力描述，不等于 Authority、Permission 或结果；
2. Declared、Verified、Authorized Capability 三层不得自动转换；
3. DBOS 管理 Capability Object、Verification、Permission gate 和能力生命周期；
4. SAEE 评价能力表现和风险，但不能授予或执行 Capability；
5. High/Critical Capability change 必须经过 Governance Decision；
6. Digital Organism 是满足长期、适应、生态、Fitness 和 Lineage 条件的高级 Digital Entity 资格状态；
7. Candidate → Digital Organism 需要 SAEE Evaluation、显式 Governance Decision 和 DBOS 资格记录；
8. Runtime、Agent、Capability、Autonomy 与 Digital Organism 分离；
9. Research Agent 是 Operational Entity 的 reference model，不是 Generic Agent Framework 或实例；
10. Research Agent 的能力配置是参考声明，不是 capability truth；
11. 建立 Entity → Capability → Execution → Evidence → Evaluation → Adaptation → Digital Organism 统一关系；
12. 本决策不创建代码、API、Agent、Runtime、Entity、Capability 或 Organism 实例。

```text
Capability ≠ Authority
Capability ≠ Permission
Permission ≠ Execution
Digital Entity ≠ Agent
Digital Entity ≠ Digital Organism
Research Agent ≠ Generic Agent Framework
Specification ≠ Implementation
```

## Alternatives（替代方案）

### A. 将 Capability 声明直接作为 Permission

拒绝。描述能力会自动产生执行许可，绕过风险、Context、授权和 DBOS lifecycle control。

### B. 将所有 Digital Entity 视为 Digital Organism

拒绝。基础 Entity 最低要求不足以证明长期持续、自维持、适应性演化、生态交互、Fitness 或 Lineage。

### C. 让 SAEE 直接授予 Organism 资格

拒绝。Evaluation 会被升级为 Decision 和状态写权，使 SAEE 获得执行权限。

### D. 让 DBOS 根据历史直接判断 Organism

拒绝。DBOS 会从事实记录 Owner 变成 Evolution/Fitness 判断者，吞并 SAEE 职责。

### E. 将 Research Agent 定义为通用 Agent Framework

拒绝。参考实体模型只需要目的、身份、能力边界、证据和评价，不需要新框架、Runtime 或实现。

### F. 创建一个实际 Research Agent 作为规范示例

拒绝。实例化会引入 Identity、Capability、Permission、Runtime 和 Evidence truth，超出本次架构规范范围。

## Impact（影响）

### Positive（正面影响）

- Capability、Authorization、Permission 和 Execution 获得可审查分层；
- Organism 资格不再由名称、Agent、Runtime 或 Autonomy 推断；
- DBOS、SAEE 与 Governance Decision 在能力和资格路径上的职责明确；
- Research Agent 获得第一个受限参考模型；
- 统一关系图为未来实现保留逐步 gate；
- 编码、检索和引用智能体可以稳定区分参考配置与已实现事实。

### Costs and unresolved issues（代价与未决问题）

- Capability lifecycle 中 Executed/Evaluated 是事件里程碑还是持久状态，需要实现前进一步建模；
- Low/Medium risk 的授权者、Permission policy 和有效期尚未指定；
- High 与 Critical risk 的量化阈值和领域覆盖仍未定义；
- Organism 的 Long-term 时长、Environment 边界和 Self-maintaining 可测量标准尚未定义；
- Organism qualification 与 Entity Lifecycle 的投影、暂停、降级和撤销状态需要正式状态机；
- Lineage Record 的分支、合并、克隆与身份连续性规则尚未定义；
- Research Agent `owner_reference`、人类作者责任、科研伦理和数据访问模型需要独立规范；
- Code Assistance 与 Code Execution 的界面和风险提升规则需要更精确契约；
- Capability Object 是否进入统一 Data Contract version line 需要版本治理决定；
- 当前规范与 LAU、Persona Object 等术语的 crosswalk 仍未完成。

## Historical relationship（历史关系）

ADR-001 与 ADR-004 在当时记录 Digital Organism 和 Capability Boundary 尚未定义。本 ADR 解决其中 Capability、Digital Organism 和 Research Agent 的后续语义，不修改历史 ADR 原文；LAU、Persona Object 等其他术语仍保持未定义。

## Consequence boundaries（后果边界）

```text
CAPABILITY_BOUNDARY_MODEL_DEFINED=true
DIGITAL_ORGANISM_CROSSWALK_DEFINED=true
RESEARCH_AGENT_REFERENCE_MODEL_DEFINED=true
ENTITY_CAPABILITY_ORGANISM_MAP_DEFINED=true
CAPABILITY_INSTANCE_CREATED=false
DIGITAL_ORGANISM_INSTANCE_CREATED=false
RESEARCH_AGENT_INSTANCE_CREATED=false
DIGITAL_ENTITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
EXECUTION_CREATED=false
RUNTIME_CREATED=false
API_CREATED=false
CODE_CHANGED=false
```

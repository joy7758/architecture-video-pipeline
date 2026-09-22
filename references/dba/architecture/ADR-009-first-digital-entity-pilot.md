---
adr_id: ADR-009
title: Select Research Agent as the First Digital Entity Pilot Reference
title_zh: 选择研究智能体作为第一个数字实体试验参考
status: accepted-for-architecture-specification-v0.1
decision_scope: non-executable-pilot-design-only
implementation_status: not-authorized
pilot_effect: specification-only
agent_instance_effect: none
entity_instance_effect: none
runtime_effect: none
capability_effect: none
permission_effect: none
research_execution_effect: none
---

# ADR-009: Select Research Agent as the First Digital Entity Pilot Reference

## Problem（问题）

Digital Biosphere Architecture 已定义 Digital Entity、Capability Boundary、DBOS/SAEE Contract、Governance Decision 和 Digital Organism Crosswalk，但仍缺少一个具体且受限的 Operational Entity Pilot reference（运行实体试验参考）来检验这些规范能否形成连贯的未来接入路径。

如果直接创建 Agent 或 Runtime，会在 Identity、Capability、Permission、Evidence 和实现尚未授权时制造新的事实表面。若只保留抽象实体模型，又无法具体识别科研场景需要的 Evidence、Human Oversight 和 SAEE 评价入口。

## Decision（决策）

选择 Research Agent 作为第一个 Digital Entity Pilot 的参考角色，并建立非可执行规范套件：

1. Research Agent 的 Primary Type 是 Operational Entity；
2. Pilot 当前状态为 `Proposed` design only，不创建或注册实体；
3. Identity 未来由 DBOS 管理；
4. 初始 Capability Profile 仅为参考声明，不建立 Capability Object 或 capability truth；
5. 执行、Evidence 与 Verification 未来由 DBOS 记录；
6. Reliability、Evidence Quality、Efficiency、Adaptability 和 Stability 未来由 SAEE 评价；
7. 论文投稿、实验结果确认和重大结论发布必须经过 Human Oversight；
8. SAEE Recommendation 必须经过显式治理决策，不能直接执行；
9. Research Agent 不因 Pilot、Active、Evaluated 或 Adapted 状态成为 Digital Organism；
10. 本决策不授权代码、API、Agent、Runtime、Entity、Capability、Permission、科研任务、实验或论文提交。

```text
Research Agent Specification ≠ Agent Implementation
Research Agent ≠ Chatbot
Research Agent ≠ Digital Organism
Research Agent ≠ DBOS
Research Agent ≠ SAEE
SAEE ≠ DBOS
Pilot Design ≠ Pilot Execution
```

## Reasons（选择原因）

### 1. Relatively low-risk entry point（相对低风险起点）

相对于外部系统操作、身份修改、医疗或金融决策，Research Agent 的初始任务可以限制为只读公开文献分析等可撤销、无外部发布副作用的科研辅助范围，因此适合作为相对低风险的首个参考入口。该理由不表示所有 Research Agent Capability 都是 Low Risk；Code Assistance、受限数据和实验规划仍可能提升风险等级。

### 2. Verifiable workflow（工作流可验证）

文献来源、任务输入、分析步骤、工具调用、输出和人工 gate 可以被明确列入未来 Evidence Model，为 DBOS Verification 和 SAEE Evaluation 提供可审查对象。

### 3. Alignment with research context（与科研场景一致）

该角色直接覆盖文献分析、知识整理、实验规划和科研记录，能够具体检验 Digital Biosphere 的存在治理、证据链和演化评价边界。

### 4. Potential public research case（潜在公开研究案例）

在未来获得研究、数据、伦理、实现和发表授权后，该 Pilot 可能形成公开研究案例。可能形成不等于已经形成、已经验证、已经撰写或已经发表。

## Alternatives（替代方案）

### A. 直接创建 Research Agent 实例

拒绝。会提前创建 Identity、Capability、Runtime、Permission 和 Evidence truth，超出 Architecture Specification 范围。

### B. 将现有 Chatbot 直接标记为 Research Agent

拒绝。Chatbot 界面或 session 不自动满足 Digital Entity 的最低要求，也没有 DBOS-governed Identity 和历史连续性。

### C. 将 Research Agent 同时作为 Digital Organism

拒绝。Organism 资格需要长期持续、适应、生态交互、Fitness、Lineage、治理决定和 DBOS 状态记录，Pilot 设计不提供这些事实。

### D. 让 DBOS 完成科研评价

拒绝。DBOS 形成运行事实和 Verification；Fitness、Risk 和 Evolution interpretation 属于 SAEE。

### E. 让 SAEE 直接修改 Research Agent

拒绝。Recommendation 不是 Decision、Authorization 或 Execution；任何变化必须回到 Governance Decision 和 DBOS lifecycle control。

## Impact（影响）

### Positive（正面影响）

- Digital Entity 抽象获得一个边界清晰的未来接入参考；
- Research Agent 的 Capability、Evidence、Evaluation 和 Human Oversight 可被分别检索；
- DBOS 输入、SAEE 输出和治理决策之间形成非自动交接；
- 未来论文问题和指标在执行前得到定义；
- 编码、检索和引用智能体可以区分 Pilot Specification、Pilot Implementation、Pilot Execution 和 Research Result。

### Costs and unresolved issues（代价与未决问题）

- Pilot owner、human reviewer、decision authority 和领域专家尚未指定；
- 实际任务集、数据集、Runtime、模型、工具和隔离策略尚未选择；
- Capability verification method、Permission policy 和风险阈值尚未定义；
- Reproducibility、Evidence Completeness、Traceability 和 Stability 的量化阈值尚未批准；
- 科研伦理、受限数据、作者责任、知识产权和披露规则需要独立治理；
- Code Assistance 与 Code Execution 的实现边界仍需单独契约；
- DBOS–SAEE adapter、schema 和实现证据不存在；
- 公开案例能否形成取决于未来真实结果和人工发表决定。

## Consequence Boundaries（后果边界）

```text
FIRST_DIGITAL_ENTITY_PILOT_REFERENCE_SELECTED=true
RESEARCH_AGENT_PILOT_SPECIFICATION_DEFINED=true
RESEARCH_AGENT_PILOT_IMPLEMENTED=false
RESEARCH_AGENT_PILOT_EXECUTED=false
RESEARCH_AGENT_INSTANCE_CREATED=false
DIGITAL_ENTITY_INSTANCE_CREATED=false
RUNTIME_CREATED=false
API_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
EVIDENCE_CREATED=false
SAEE_EVALUATION_EXECUTED=false
DIGITAL_ORGANISM_STATUS_CLAIMED=false
PAPER_DRAFTED=false
PAPER_SUBMITTED=false
CODE_CHANGED=false
```

---
adr_id: ADR-006
title: Establish Independent Architecture Governance
title_zh: 建立独立架构治理
status: accepted-for-architecture-specification-v0.1
decision_scope: architecture-rule-maintenance-and-change-control-only
implementation_status: not-authorized
authority_assignment_effect: none
runtime_effect: none
entity_effect: none
capability_effect: none
permission_effect: none
evidence_effect: none
---

# ADR-006: Establish Independent Architecture Governance（建立独立架构治理）

## Problem（问题）

Digital Biosphere Architecture 已定义：

- DBOS 负责 Existence Governance；
- SAEE 负责 Evolution Governance；
- Governance Decision Layer 记录 Recommendation 到 Decision 和 Adoption 的转换；
- Digital Entity 遵循统一身份、能力边界、历史和生命周期模型。

但是，架构规则本身没有正式治理主体或变更流程。现有文档不能稳定回答：

- 谁维护规范、术语、版本和 ADR；
- 谁审查 DBOS 与 SAEE 之间的重大边界变化；
- DBOS 或 SAEE 的领域需求冲突时如何解决；
- 什么记录允许核心规范被更新；
- Architecture Authority 与 Operational/Execution Authority 如何分离。

缺少该边界时，维护者可能直接改写核心规范，DBOS 当前实现可能被误当作架构权威，或 SAEE 可能通过 Governance Evolution 建议修改自身生态规则。

## Decision（决策）

建立独立 Architecture Governance（架构治理）：

1. Architecture Authority 只负责架构规则、规范解释、文档维护和 ADR 管理；
2. Architecture Maintainer、Architecture Reviewer 和 Domain Owner 是分离的治理角色；
3. 架构语义变化遵循 Proposal → Review → Decision → Adoption → Documentation Update；
4. 变更记录使用 PROPOSED → REVIEWED → ACCEPTED → IMPLEMENTED → VALIDATED 状态；
5. DBOS Domain Owner 与 SAEE Domain Owner 提供各自领域约束，但不能单方面修改跨域规范；
6. DBOS/SAEE 冲突通过 ADR 和显式 Architecture Decision 解决；
7. Architecture Authority 不运行 DBOS、不控制 SAEE 算法、不授予 Capability 或 Permission；
8. 本决策不创建组织、账号、Agent、Runtime、Digital Entity 或执行权。

```text
Architecture Authority: maintains rules
Operational Authority / DBOS: governs bounded operation
Evolution Authority / SAEE: produces bounded evolution evaluation
Governance Decision: records explicit decisions, not execution
```

## Alternatives（替代方案）

### A. 由 DBOS 单方面维护架构

拒绝。DBOS 会同时拥有运行事实与规则修改权，并可能用实现状态覆盖 SAEE 边界。

### B. 由 SAEE 单方面维护架构

拒绝。SAEE 会同时评价治理规则并修改自身生态规则，使 Evaluation 与 Architecture Authority 合并。

### C. 由文档维护者直接修改核心规范

拒绝。维护责任不等于决策权；缺少 Review、Decision 和 Adoption 会失去可追溯性与职责分离。

### D. 复用 Governance Decision Layer 作为全部 Architecture Authority

拒绝。Governance Decision Layer 当前负责 Recommendation 的决策记录边界，不自带最终授权者，也不等同于规范维护与 ADR 治理。两者可以共享原则，但不能自动合并。

### E. 新建 Architecture Governance Runtime、Agent 或 Entity

拒绝。本问题需要规则、角色和记录，不需要新的运行系统或生态成员。

### F. 保持无正式流程

拒绝。随着接口、Entity 和 Governance 规范增加，无流程修改会造成术语漂移、冲突覆盖和重复建设。

## Impact（影响）

### Positive（正面影响）

- Architecture Authority、Operational Authority 与 Evolution Authority 获得明确分离；
- DBOS 和 SAEE 都不能单方面改变架构定义；
- 重大边界变化具有 ADR、审查和显式决策链；
- 维护者只能实施已采纳的文档范围；
- DBOS/SAEE 需求冲突有稳定的 resolution path（解决路径）；
- 智能体可以区分“规范已定义”“变更已接受”“文档已更新”和“运行已执行”。

### Costs and unresolved issues（代价与未决问题）

- v0.1 未指定实际 Architecture Maintainer、Reviewer、Domain Owner 或 decision authority；
- 角色任命、任期、quorum、回避、appeal（申诉）和紧急审查规则尚未定义；
- Architecture Change Record 与 Governance Decision Object 是否复用统一 schema 尚未决定；
- 当前本地规范与既有 public meaning layer 的 canonical reconciliation 尚未完成；
- ADR-001 位于嵌套目录，ADR-002 至 ADR-006 位于 `architecture/`，ADR 目录规则仍不统一；
- `ADR-005` 当前不在本工作区；编号保留或补齐规则尚未定义；
- “核心规范”清单与版本化发布机制仍需后续维护制度确认。

## Consequence boundaries（后果边界）

```text
ARCHITECTURE_GOVERNANCE_DEFINED=true
ARCHITECTURE_AUTHORITY_ASSIGNED=false
DBOS_ARCHITECTURE_AUTHORITY_CREATED=false
SAEE_ARCHITECTURE_AUTHORITY_CREATED=false
EXECUTION_AUTHORITY_CREATED=false
ARCHITECTURE_GOVERNANCE_RUNTIME_CREATED=false
ARCHITECTURE_GOVERNANCE_ENTITY_CREATED=false
AGENT_CREATED=false
RUNTIME_CREATED=false
API_CREATED=false
CAPABILITY_CREATED=false
PERMISSION_GRANTED=false
CODE_CHANGED=false
```

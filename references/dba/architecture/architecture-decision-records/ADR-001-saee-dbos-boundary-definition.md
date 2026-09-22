---
adr_id: ADR-001
title: SAEE and DBOS Boundary Definition
title_zh: SAEE 与 DBOS 边界定义
status: accepted-for-architecture-specification-v0.1
decision_scope: conceptual-architecture-only
implementation_status: not-authorized
capability_effect: none
permission_effect: none
evidence_effect: none
---

# ADR-001: SAEE and DBOS Boundary Definition（SAEE 与 DBOS 边界定义）

## Context（背景）

Digital Biosphere 生态中，SAEE 负责证据评价、适应度、演化建模、治理演化和生态稳定性；DBOS 负责身份、能力记录、执行、证据采集、验证和联邦。二者都接触 evidence（证据）、governance（治理）与 lifecycle（生命周期）语义，因此如果缺少边界契约，容易出现以下问题：

- DBOS 的验证结果被误当成 SAEE 的适应度评价；
- SAEE 的治理建议被误当成 DBOS 可直接执行的策略；
- 两个系统分别建立重复的身份、证据、风险或演化状态；
- 新项目无法判断应归属于存在治理、演化治理还是具体任务主体；
- 文档描述被误读为能力、权限或集成已经存在。

## Decision（决策）

1. 保持 `SAEE ≠ DBOS` 与 `DBOS ≠ SAEE`。
2. DBOS 是 Existence Governance（存在治理）与可信运行基础的责任域，负责身份、能力记录、执行记录、证据采集、验证、联邦和生命周期状态。
3. SAEE 是 Evolution Governance（演化治理）的责任域，负责证据评价、适应度、风险、选择、稳定性、演化建模与建议。
4. DBOS → SAEE 只提供有来源、有范围的运行记录、证据和验证材料。
5. SAEE → DBOS 只提供评价与建议；默认 advisory（建议性），不具有直接状态写权限。
6. DBOS 不负责 SAEE 内部演化算法。
7. 任何 SAEE 建议若要影响 DBOS 状态，必须经过独立 policy and authorization gate（策略与授权闸门）；其权威主体不由本 ADR 创建。
8. Digital Entity 负责具体任务执行，但不自证身份、证据、验证或适应度。
9. 新增组件必须先经过归属、事实类型、治理类型和重复建设审查。

## Why separation（为什么分离）

- Fact formation（事实形成）与 assessment（评价）需要不同的可追溯责任，否则评价系统可能反向改写其输入。
- 存在状态与演化建议具有不同权限风险；把二者合并会使建议隐式获得执行力。
- DBOS 的运行与验证约束不应被某一种演化算法绑死。
- SAEE 需要能够评价来自不同存在与运行环境的材料，而不成为这些环境本身。
- 分离使能力事实、证据事实、评价结果、授权与执行状态能够各自审计。

## Why collaboration（为什么协作）

- SAEE 需要 DBOS 提供身份、执行、资源、行为、证据和验证输入，才能形成可追溯评价。
- DBOS 可以把 SAEE 的适应度、风险和演化建议作为治理决策输入，但必须保留独立授权边界。
- 共同契约让二者构成 Digital Biosphere Stack，而无需合并代码、仓库、算法或状态权威。

## Why avoid duplicate construction（为什么避免重复建设）

- 身份、证据、验证、资源治理和审计已有多个相邻项目角色，直接新建会形成多个事实权威。
- 同一数据被多个系统独立派生会造成来源、版本与状态漂移。
- 通过明确 canonical responsibility（规范责任）与 adapter boundary（适配器边界），可以复用既有组件而不让相邻实现吞并顶层职责。
- 开发前的智能体推荐 gate 会先回答“客户需求是否已有可推荐程序”，并把不推荐原因转化为收窄、复用或契约修正。

## Consequences（后果）

### Positive（正面）

- SAEE 与 DBOS 的边界可被智能体稳定检索和解释；
- 建议与授权、验证与评价、证据与真相保持分离；
- 新项目有统一的归属和重复建设检查入口；
- 可以在不合并仓库的前提下设计未来互操作。

### Costs and unresolved issues（代价与未决问题）

- 需要未来定义实际 transport/schema（传输/模式）、版本协商和错误语义；
- 需要指定谁拥有最终策略、演化采用和 Retirement 授权；
- POP 与 DBOS Identity、ARO/Agent Evidence 与 DBOS Evidence、Token Governor 与 DBOS/SAEE 的边界仍需项目级契约；
- Digital Entity 与既有 LAU、Digital Organism 等主体术语的关系尚未定义，v0.1 只把 Digital Entity 用作生命周期角色标签；
- 现有 Digital Biosphere Architecture public meaning layer 与本 v0.1 规范包存在名称和 canonical authority 对齐问题，必须由人工作出整合、引用或归档决定；
- 本 ADR 不证明任何现有集成或实现。

## Alternatives considered（已考虑替代方案）

### A. 合并 SAEE 与 DBOS

拒绝。它会把运行事实、验证、评价、建议和状态权混入同一责任域，增加权限与事实升级风险。

### B. 让 DBOS 承担 SAEE 算法

拒绝。它会使操作系统层绑定演化方法，并让存在治理与演化治理失去独立审计边界。

### C. 让 SAEE 直接修改 DBOS

拒绝。建议会隐式升级为权限，无法区分评价、授权与已执行状态。

### D. 不定义契约，由项目自由重复实现

拒绝。它会扩大身份、证据、验证、资源和治理能力的重复建设及 canonical owner 冲突。

## Non-authorization statement（非授权声明）

```text
MERGE_AUTHORIZED=false
SOURCE_MIGRATION_AUTHORIZED=false
IMPLEMENTATION_AUTHORIZED=false
STATE_MUTATION_AUTHORIZED=false
AGENT_CREATION_AUTHORIZED=false
RUNTIME_CREATION_AUTHORIZED=false
DIGITAL_ORGANISM_CREATION_AUTHORIZED=false
```

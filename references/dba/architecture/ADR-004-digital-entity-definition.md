---
adr_id: ADR-004
title: Establish the Digital Entity Common Model
title_zh: 建立数字实体共同模型
status: accepted-for-architecture-specification-v0.1
decision_scope: architecture-definition-classification-and-boundaries-only
implementation_status: not-authorized
entity_instance_effect: none
runtime_effect: none
capability_effect: none
permission_effect: none
evidence_effect: none
---

# ADR-004: Establish the Digital Entity Common Model（建立数字实体共同模型）

## Problem（问题）

Digital Biosphere Stack 已定义 DBOS、SAEE、接口契约和 Governance Decision，但 `Digital Entity` 仍只是一个未正式限定的角色标签。Agent、Project/Repository、Component、Runtime、Execution 与生态成员可能因此被混为一谈：

- Repository 可能被直接描述为 Entity；
- Agent 名称或进程可能被当作具有持久 Identity 的生态成员；
- Runtime instance 可能被当作 Entity 本身；
- Capability 声明可能被误读为 Authority；
- DBOS 或 SAEE 的项目角色可能被误报为已创建的 Entity 实例；
- Entity 产生的材料可能被误报为 canonical Evidence。

## Decision（决策）

建立统一 Digital Entity architecture model（数字实体架构模型）：

1. Digital Entity 是具有 Identity、Capability Boundary、Execution History、Evidence History 和 Lifecycle State 的自主数字对象；
2. “自主”表示可独立引用和治理，不表示自动权限或无限自治；
3. Repository、Runtime、Component 与 Digital Entity 分离；
4. Agent 是可能的实体角色，不与 Digital Entity 等价；
5. `Proposed` 是 Entity Candidate；从 `Registered` 开始进入 DBOS-governed lifecycle；
6. DBOS 管理存在、身份、能力边界、历史与生命周期；
7. SAEE 管理演化评价并产生 Recommendation；
8. Recommendation 的采纳必须经过 Governance Decision；
9. 任何变化执行必须回到 DBOS，并产生 Evidence 与 Verification；
10. 分类不等于权限，示例不等于实例。

本 ADR 将 `Digital Entity` 从生命周期角色标签提升为 architecture-level common model，但不创建本体实例、数据库类型、schema、API 或 Runtime class（运行时类）。它与 LAU（Life-like Autonomous Unit，类生命自治单元）、Digital Organism 等既有术语的等价、继承或交叉关系仍未定义。

## Alternatives（替代方案）

### A. 将 Agent 定义为唯一 Digital Entity

拒绝。生态成员还可能承担 Infrastructure、Evolution、Service、Governance 或 Evaluation 角色；同时 Agent 代码或进程不自动具备持久 Identity 与历史。

### B. 将 Repository 定义为 Entity

拒绝。Repository 是实现和文档载体，不能代表跨 Runtime 的身份、能力边界、执行历史或生命周期。

### C. 将 Runtime instance 定义为 Entity

拒绝。Runtime 生命周期通常短于 Entity，且一次 Entity 可以跨多个 Runtime、session 和 Execution 保持连续身份。

### D. 继续只使用无约束的“数字主体”称呼

拒绝。无最低要求和分类规则时，任何项目、模块或进程都可能自称生态成员，导致身份、权限和 Evidence 边界漂移。

### E. 立即创建 Entity registry、API 或实例

拒绝。本任务只需要架构规范；任何实现和实例化都需要独立授权及 DBOS 能力事实审查。

## Impact（影响）

### Positive（正面影响）

- Future autonomous digital subjects（未来自主数字主体）获得统一最低模型；
- Repository、Agent、Runtime、Component 和 Entity 可以稳定区分；
- DBOS、SAEE 与 Governance Decision 对同一 Entity 的职责清晰；
- Future Research Agent 获得可审查的接入路径；
- Entity 分类、能力、权限和生命周期状态不再互相自动升级；
- 编码、检索和引用智能体可以进行一致的 Entity 资格检查。

### Costs and unresolved issues（代价与未决问题）

- “自主”的可测量标准尚未定义；v0.1 只限定其非权限含义；
- Digital Entity 与 LAU、Digital Organism、Persona Object 等术语尚未 crosswalk（交叉映射）；
- Capability Boundary 的受控状态、单位和验证规则尚待规范；
- Entity Identity 在 Federation 中的解析、冲突和撤销语义尚待定义；
- 复合实体、父子实体、克隆、分叉、合并和身份连续性尚未定义；
- Evaluated/Adapted 是生命周期状态还是事件投影，未来需要真实用例验证；
- DBOS/SAEE 作为 Entity 分类示例，不证明其当前存在合格实例。

## Consequence boundaries（后果边界）

```text
DIGITAL_ENTITY_MODEL_DEFINED=true
DIGITAL_ENTITY_INSTANCE_CREATED=false
DBOS_ENTITY_INSTANCE_CREATED=false
SAEE_ENTITY_INSTANCE_CREATED=false
FUTURE_RESEARCH_AGENT_CREATED=false
RUNTIME_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
API_CREATED=false
CODE_CHANGED=false
```


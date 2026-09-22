---
spec_id: DBA-ENTITY-BOUNDARY-RULES-0.1
title: Digital Entity Boundary Rules v0.1
status: normative-architecture-boundary-rules
implementation_authorized: false
entity_instance_created: false
runtime_created: false
capability_effect: none
authority_effect: none
---

# Digital Entity Boundary Rules v0.1（数字实体边界规则 v0.1）

## 1. 五条强制规则

### `EBR-001`: Entity identity belongs to DBOS governance

Entity Identity 属于 DBOS Existence Governance（存在治理）。SAEE、Governance Decision、Entity 自身、Repository 或 Runtime 都不能创建、修改或提升 canonical Entity Identity（规范实体身份）。

### `EBR-002`: Entity evolution evaluation belongs to SAEE

Entity 的 Fitness、Risk、Stability 与 Evolution Evaluation 属于 SAEE Evolution Governance（演化治理）。DBOS 可以提供记录和验证结果，但不能发明或改写演化结论。

### `EBR-003`: Entity recommendation adoption requires Governance Decision

Entity Recommendation 的采纳必须经过 Governance Decision：Review、显式 Decision 与 Adoption。SAEE、Entity 或 DBOS 都不能仅凭收到 Recommendation 自动把它标记为已采纳。

### `EBR-004`: Entity capability does not imply authority

Entity Capability 或 Capability Boundary 不产生 Authorization。一个实体即使具有已验证能力，也只能在另行明确、有效且有范围的授权下执行。

### `EBR-005`: Entity existence does not imply autonomy

Entity 存在、Registered、Verified 或 Active 不表示它拥有自主决策、自主执行、自我修改、自我授权或跨域治理权。Autonomy 必须按具体行为、能力和授权分别定义。

## 2. 类型边界规则

### `EBR-006`: Repository is not Entity

Repository 是代码和文档载体。仓库名称、Git 历史、release（发布）或 deployment manifest（部署清单）不构成 Entity Identity 或 Lifecycle State。

### `EBR-007`: Runtime is not Entity

Runtime、process（进程）、session、container（容器）或一次 Execution 是实体的运行承载或历史记录，不是实体本身。Entity Identity 必须跨这些实例保持可追溯连续性。

### `EBR-008`: Agent is a role, not an equivalence

Agent 可以是 Digital Entity 的角色类别，但 Agent 名称、代码、进程或框架对象不自动满足 Digital Entity 最低要求。`Digital Entity ≠ Agent`。

### `EBR-009`: Component is not Entity by default

Component 默认是模块或基础设施部件。只有当一个持久主体独立满足 Entity 最低要求并经 DBOS 注册、验证时，它才能同时承担 Entity 角色。

### `EBR-010`: Classification does not imply permission

Infrastructure、Evolution、Operational、Evaluation 或任何 role label 都不授予能力、权限、信任、联邦写权或生命周期状态。

## 3. Evidence 与关系边界

### `EBR-011`: Entity output is not canonical Evidence by itself

Entity 可以产生 evidence-bearing material，但 canonical Evidence Object 由 DBOS 采集、登记或封装。SAEE 评价 Evidence；Entity 不自证 Evidence 的完整性或适应度意义。

### `EBR-012`: Federation participation requires separate authorization

Entity 可以参与 Federation，但 Identity、协议、scope、对端信任和 Authorization 必须分别明确。Federation participation 不等于全局信任、无限互操作或自动权限继承。

### `EBR-013`: Relationship does not transfer ownership

Entity 使用 Component、接收 Recommendation 或连接其他 Entity，不会获得对方对象、能力、Evidence、模型或权限的 Owner 身份。

### `EBR-014`: Digital Entity is not Digital Organism

Digital Entity 是基础生态成员模型；Digital Organism 是需要长期记录、SAEE Evolution Evaluation、显式 Governance Decision 和 DBOS 资格记录的高级状态。Entity、Agent、Runtime、Capability 或 Autonomy 都不能自动产生 Organism 资格。

## 4. 冲突判定表

| 错误描述或设计 | 违反规则 | 正确处理 |
|---|---|---|
| “这个 GitHub repository 就是一个 Digital Entity” | `EBR-006` | 将仓库描述为实现或文档载体；另行识别受治理主体 |
| “这个 Agent 进程已经是 Entity” | `EBR-007/008` | 验证跨 Runtime Identity、能力边界和历史 |
| “Active Entity 可以自动执行任务” | `EBR-004/005` | 要求独立任务授权和 DBOS 执行控制 |
| “SAEE 评价后直接更新 Entity” | `EBR-002/003` | Recommendation 进入 Governance Decision，再由 DBOS 执行 |
| “DBOS 根据日志给出演化结论” | `EBR-002` | DBOS 提供记录，SAEE 负责演化评价 |
| “Entity 生成的数据就是已验证 Evidence” | `EBR-011` | DBOS 形成 canonical Evidence 和 Verification |
| “Infrastructure Entity 自动拥有治理权” | `EBR-010` | 分类与 Authority 分离 |
| “Active Agent 自动是 Digital Organism” | `EBR-008/014` | 按 Organism crosswalk 完成候选、评价、Decision 与 DBOS 记录 |

## 5. 边界状态常量

```text
ENTITY_IDENTITY_OWNER=DBOS
ENTITY_EVOLUTION_EVALUATION_OWNER=SAEE
ENTITY_RECOMMENDATION_ADOPTION_REQUIRES_GOVERNANCE_DECISION=true
ENTITY_CAPABILITY_IS_AUTHORITY=false
ENTITY_EXISTENCE_IS_AUTONOMY=false
DIGITAL_ENTITY_IS_REPOSITORY=false
DIGITAL_ENTITY_IS_RUNTIME=false
DIGITAL_ENTITY_IS_AGENT=false
DIGITAL_ENTITY_IS_DIGITAL_ORGANISM=false
```

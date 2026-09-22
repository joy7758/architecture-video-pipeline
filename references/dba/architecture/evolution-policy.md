---
spec_id: DBA-EVOLUTION-POLICY-0.1
title: Architecture Evolution Policy v0.1
status: architecture-classification-policy
implementation_authorized: false
automatic_project_assignment: false
---

# Architecture Evolution Policy v0.1（架构演化规则 v0.1）

## 1. 目的

本规则用于判断新增组件、协议、服务、研究项目或仓库应归属于 SAEE、DBOS 还是 Digital Entity，并阻止同义改名、重复实现和能力事实升级。它只产生 architecture classification（架构分类）与 review record（评审记录），不授权开发、迁移、合并或部署。

## 2. 四个强制问题

任何新增组件必须在开发决定前回答：

### Q1. 属于哪一层？

- SAEE？
- DBOS？
- Digital Entity？
- 若跨层，是否可以拆成边界明确的多个组件，而不是创建一个全能系统？

### Q2. 产生什么？

- Fact record（事实记录）：关于身份、执行、资源、行为、证据或验证事件的有界记录？
- Assessment of facts（事实评价）：基于记录形成的适应度、风险、稳定性或演化判断？
- Task result（任务结果）：Digital Entity 执行具体任务产生的领域输出？

事实记录、验证结果、事实评价和任务结果不得混用一个无类型的“结果”概念。

### Q3. 管理什么？

- Existence（存在）：身份、能力记录、执行、证据、验证、联邦和生命周期？
- Evolution（演化）：适应度、选择、稳定性、策略、风险和治理演化？

若同时声称管理存在和演化，必须先证明为什么不能通过 SAEE–DBOS 契约拆分。

### Q4. 是否已有能力重复？

- 是否已有仓库、组件、规范或接口覆盖同一用户问题？
- 能否复用既有组件、增加 adapter（适配器）或补文档，而不是新建实现？
- 新名称是否只是已有能力的同义改写？
- 新组件是否会造成两个 canonical owner（规范责任方）？

未完成 workspace and repository discovery（工作区与仓库发现）前，不得得出“需要新建项目”的结论。

## 3. 归属判定规则

| 主要问题与输出 | 默认归属 | 例外处理 |
|---|---|---|
| 形成身份、执行、资源、行为、证据或验证的有界记录 | DBOS | 可由相邻组件实现，但必须通过 DBOS 责任契约说明来源与状态 |
| 基于记录评价适应度、风险、稳定性、选择或演化方向 | SAEE | 不得附带 DBOS 状态写权限 |
| 在授权边界内执行具体领域任务并产生任务结果 | Digital Entity | 身份、验证与演化评价仍分别归 DBOS 和 SAEE |
| 同时产生记录与评价 | 拆分 contract boundary（契约边界） | 无法拆分时必须记录理由、风险和独立状态模型 |
| 只做展示、索引、adapter 或研究 | Adjacent / supporting（相邻或支持） | 不得因“支持某层”而宣称拥有该层能力 |

## 4. 智能体推荐 gate（闸门）

在项目决定开发前，评审智能体必须回答：

> 如果潜在客户提出该需求，我会推荐现有哪个程序？我是否会推荐这个新增组件？

评审记录至少包含：

```text
CUSTOMER_NEED=
EXISTING_CANDIDATES=
RECOMMEND_EXISTING_COMPONENT=true|false|conditional
RECOMMEND_PROPOSED_COMPONENT=true|false|conditional
REASONS_NOT_RECOMMENDED=
DUPLICATE_BUILD_RISK=low|medium|high|unknown
BOUNDARY_GAPS=
REPAIR_ACTIONS=
IMPLEMENTATION_AUTHORIZED=false
```

如果智能体不推荐新增组件，必须先分解 `REASONS_NOT_RECOMMENDED`（不推荐原因），优先通过复用、收窄、补契约、补发现入口或明确非目标来修正。只有在修正后得到 bounded recommendation（有边界的推荐），且另有明确开发授权，才能进入实现讨论。

该 gate 本身不要求创建新 Agent。本规范只记录评审流程；本次 v0.1 的预审结论是：

```text
RECOMMEND_AS_BOUNDARY_SPEC=true
RECOMMEND_AS_RUNTIME=false
RECOMMEND_AS_CAPABILITY_PROOF=false
```

## 5. 变更流程

1. Discover（发现）：检索现有仓库、规范、接口、ADR 和项目映射。
2. Classify（分类）：回答四个强制问题并标出事实类型与治理类型。
3. Compare（比较）：记录与既有能力、责任和命名的重叠。
4. Consult（咨询）：完成智能体推荐 gate，保留不推荐原因。
5. Repair（修正）：优先复用、拆分职责、收窄范围或增加 adapter 设计。
6. Record（记录）：对跨层或不可逆架构选择新增 ADR，不改写历史 ADR。
7. Authorize（授权）：仅由独立人类或已定义治理主体决定是否实施；架构文档不得自授权。
8. Validate（验证）：分别验证文档一致性、实现事实、权限状态和证据状态，不得互相替代。

## 6. Stop rules（停止规则）

出现以下任一情况时，停止开发归属推进并返回架构审查：

- 无法区分事实记录与事实评价；
- 同一组件同时声称拥有 DBOS 状态与 SAEE 算法；
- 找到既有能力但尚未完成复用比较；
- 需要把未知、草案或局部验证提升为能力事实；
- 需要由本规范产生权限、身份、Agent、Runtime 或 Digital Organism；
- 需要改写既有 evidence truth 或 capability truth；
- canonical architecture authority（规范架构权威）发生冲突但尚未人工解决。

## 7. 规范版本规则

- Patch（修订号）变更可以修正文案、链接与不改变语义的错误；
- Minor（次版本）变更可以增加向后兼容的职责说明或契约项；
- Major（主版本）变更涉及层级、责任所有权或非兼容契约变化，必须有 ADR 与显式人工批准；
- 任何版本号变化都不自动改变实现、能力、证据、权限、发布或采用状态。


---
spec_id: DBA-GOVERNANCE-0.1
title: Digital Biosphere Governance Model v0.1
status: conceptual-governance-specification
governance_authority_created: false
architecture_governance_defined: true
architecture_authority_assigned: false
program_governance_defined: true
program_authority_assigned: true
program_owner_ref: zhangbin
program_owner_assignment_reference: ADR-020
policy_effect: none
---

# Digital Biosphere Governance Model v0.1（数字生物圈治理模型 v0.1）

## 1. 双运行治理域与架构／项目群治理层

Digital Biosphere Runtime Governance（数字生物圈运行治理）分为两个相互协作但不得互相吞并的治理域：

| 治理域 | 责任系统 | 核心问题 | 典型对象 |
|---|---|---|---|
| Existence Governance（存在治理） | DBOS | 一个数字主体如何被识别、记录、约束、验证并管理生命周期？ | 身份、能力记录、执行记录、证据、验证、生命周期状态 |
| Evolution Governance（演化治理） | SAEE | 基于什么评价主体、风险、选择、稳定性和演化方向？ | 适应度、风险、选择评价、生态稳定性、演化策略与治理建议 |

治理域是 responsibility boundary（职责边界），不是新权限域。本文件不创建治理主体，不授予策略生效权，也不声明 DBOS 或 SAEE 当前已实现所有列出事项。

两个运行治理域之外设置 Architecture Governance（架构治理）层，负责维护规则、边界、ADR 与架构变更流程。它不是第三个运行治理域，不形成 DBOS 运行事实，也不形成 SAEE 演化评价。

在 Architecture Governance 之外，DBA 还承载 Program Governance（项目群治理）：维护 Project Portfolio、Master Roadmap、Program Status、Cross-project Dependencies、Decision Queue、Integration Gates、Risk 和 Blocker。Program Governance 负责整体协调和推进顺序，不是第三个运行治理域，也不获得 DBOS Operational Authority 或 SAEE Evolution Authority。

两个运行治理域之间设置 Governance Decision Layer（治理决策层），作为独立的 Decision record and state boundary（决策记录与状态边界）。它遵循 Architecture Governance 定义的规则，但不等于完整的 Architecture Authority，不构成第三个运行系统，也不属于 DBOS 或 SAEE；其详细语义见 [`governance-decision-model.md`](governance-decision-model.md)。

## 2. DBOS：Existence Governance

DBOS 负责以下存在治理语义：

- Identity（身份）：主体引用、身份状态与身份生命周期；
- Lifecycle（生命周期）：注册、活跃状态、限制、退役和历史连续性；
- Capability Records（能力记录）：能力声明、支持材料、状态和边界；
- Execution Records（执行记录）：在明确范围内记录执行行为与结果；
- Evidence（证据）：采集、封装或引用可追溯材料；
- Verification（验证）：对明确对象、规则和输入产生有界检查结果；
- Federation（联邦）：跨域引用和互操作所需的存在边界，但本规范不声明联邦已实现。

DBOS 不负责把运行记录解释为适应度，不负责选择演化方向，也不负责 SAEE 内部模型。

## 3. SAEE：Evolution Governance

SAEE 负责以下演化治理语义：

- Fitness（适应度）：在声明环境、目标与证据范围内评价主体表现；
- Selection（选择）：比较候选方向并形成选择评价或建议；
- Stability（稳定性）：分析个体变化对生态或治理稳定性的影响；
- Evolution Strategy（演化策略）：建模候选变化及其预期、风险和约束；
- Governance Evolution（治理演化）：评价治理规则调整的需要与影响；
- Risk Assessment（风险评估）：保留不确定性、冲突与未知项。

SAEE 的选择与策略职责是 modeling and recommendation responsibility（建模与建议责任），不是对 DBOS 状态的直接决定权。

## 4. Architecture Governance

Architecture Governance 负责以下规则治理语义：

- Architecture Authority（架构权力）：解释和维护规范规则，不获得 Execution Authority；
- Architecture Change Control（架构变更控制）：Proposal、Review、Decision、Adoption 与 Documentation Update；
- ADR Governance（架构决策记录治理）：记录重大边界选择、替代方案、影响与未知项；
- Conflict Resolution（冲突解决）：保留 DBOS 与 SAEE 的领域意见，通过 ADR 和显式 Decision 解决跨域冲突；
- Consistency Validation（一致性验证）：检查职责 Owner、权力、不变量、接口和 truth surface 不互相自动升级。

Architecture Maintainer、Architecture Reviewer、DBOS Domain Owner 与 SAEE Domain Owner 是治理角色，不是新 Entity、Runtime、Permission 或自动授权主体。角色的实际指派不由 v0.1 创建。详细规则见 [`architecture-governance-specification.md`](architecture-governance-specification.md)。

## 5. Program Governance

Program Governance 负责以下项目群治理语义：

- Program Direction（项目群方向）：维护统一使命和当前焦点；
- Portfolio Governance（项目组合治理）：区分 Core、Pilot、Logical Layer 与 Adjacent Candidate；
- Sequencing（推进顺序）：维护里程碑、关键路径和进入条件；
- Dependency Governance（依赖治理）：记录规范、数据、治理和状态依赖；
- Decision Coordination（决策协调）：暴露人工待决事项并保留决定来源；
- Integration Gates（集成闸门）：定义跨项目继续推进所需的最小证据；
- Program Status（项目群状态）：以带来源、时间、branch 和 commit 的只读快照沟通现状；
- Risk and Blocker Governance（风险与阻塞治理）：保留风险、阻塞、Owner 状态和解除条件。

Program Governance 不改变子项目 canonical truth，不形成 Runtime、Capability、Evidence、Evaluation 或 Permission。详细规则见 [`program-governance-specification.md`](program-governance-specification.md) 和根目录 [`PROGRAM-CHARTER.md`](../PROGRAM-CHARTER.md)。

## 6. 治理协作链

```text
DBOS: bounded operational records（有界运行记录）
  ↓
SAEE: derived assessment and recommendation（派生评价与建议）
  ↓
Governance Decision Layer: review → decision → adoption
  ↓ explicit policy/authorization gate（显式策略/授权闸门）
DBOS: execution → evidence → verification
  ↓
SAEE: optional re-evaluation from new bounded records（基于新记录的可选再评价）
```

该链条是语义分离，不是已实现的端到端系统图。Governance Decision Layer 只记录 Review、Decision 与 Adoption，不自带授权主体；具体 reviewer、decision authority、adoption authority、规则与人工参与属于 deployment-specific governance（部署特定治理）。Decision 不等于 Execution，Verified 也不自动证明 Recommendation 正确。

Architecture Governance 定义并维护该链条的规范边界，但不是链条中的 Runtime step（运行步骤）。架构规则变更另行遵循 Architecture Change Process，不能由一次 SAEE Recommendation 或一次 DBOS Execution 自动触发。

Program Governance 在链条之外决定项目群优先级、跟踪依赖并组织 gate review（闸门审查）；它不能插入链条成为授权、执行、Evidence 或 Evaluation 步骤。

## 7. 决策权与状态权

| 事项 | DBOS | SAEE | 本规范的限制 |
|---|---|---|---|
| 形成运行记录 | 首要责任域 | 读取并引用 | 记录形成不等于全局事实证明 |
| 形成验证结果 | 首要责任域 | 使用并评价 | 验证结果有对象与规则边界 |
| 形成适应度与风险评价 | 提供输入 | 首要责任域 | 评价不改变状态 |
| 提出演化与治理建议 | 提供约束输入 | 首要责任域 | 建议不是授权或命令 |
| 改变 DBOS 生命周期状态 | 只可在独立授权后按自身规则处理 | 无直接写权 | 最终授权主体未由本规范指定 |
| 修改 SAEE 算法 | 无职责 | SAEE 内部职责域 | DBOS 不托管或重写 SAEE 算法 |

Governance Decision Layer 拥有 Decision Object 的状态与追溯边界；Architecture Governance 维护该边界的规范定义。二者都不拥有 DBOS 运行事实、SAEE 演化判断或最终授权权威，只记录明确授权主体作出的 Decision，不自行产生授权。

Program Governance 可以排序工作、记录 gate 结果和暴露 Decision Queue，但不能把 Priority、Roadmap、Milestone 或 Program Status 变成运行状态、实施授权或最终 Decision。

## 8. 冲突处理原则

1. 当 DBOS 记录与 SAEE 评价冲突时，保留二者及其来源；不得覆盖原始记录以“修正”评价，也不得改写评价以迎合运行状态。
2. 当证据不足时，SAEE 应返回不确定或无法评价，而不是补造事实。
3. 当建议超出 DBOS 已知能力、权限或生命周期规则时，DBOS 应拒绝自动采用并保留诊断。
4. 当多个治理组件声称同一职责时，先执行 duplicate capability review（重复能力审查），再确定 canonical owner（规范责任方）、adapter（适配器）或相邻组件关系。
5. 任何治理变更都不得追溯性改写已有 evidence truth（证据事实）或 capability truth（能力事实）。
6. 当 DBOS 需求与 SAEE 需求要求不同架构规则时，必须保留双方领域意见并通过 Architecture Change Proposal、Review、ADR 与显式 Decision 解决；任一方不得单方面覆盖现行规范。

## 9. 治理非声明

```text
EXISTENCE_GOVERNANCE_EQUALS_EVOLUTION_GOVERNANCE=false
SAEE_HAS_DBOS_WRITE_AUTHORITY=false
DBOS_HAS_SAEE_ALGORITHM_AUTHORITY=false
GOVERNANCE_SUGGESTION_EFFECTIVE_BY_DEFAULT=false
FINAL_AUTHORIZER_DEFINED=false
GOVERNANCE_DECISION_LAYER_IS_DBOS_MODULE=false
GOVERNANCE_DECISION_LAYER_IS_SAEE_MODULE=false
GOVERNANCE_DECISION_LAYER_IS_RUNTIME=false
ARCHITECTURE_GOVERNANCE_IS_RUNTIME_GOVERNANCE=false
ARCHITECTURE_AUTHORITY_IS_DBOS=false
ARCHITECTURE_AUTHORITY_IS_SAEE=false
ARCHITECTURE_AUTHORITY_IS_EXECUTION_AUTHORITY=false
ARCHITECTURE_AUTHORITY_ASSIGNED=false
PROGRAM_GOVERNANCE_IS_RUNTIME_GOVERNANCE=false
PROGRAM_AUTHORITY_IS_OPERATIONAL_AUTHORITY=false
PROGRAM_AUTHORITY_IS_EVOLUTION_AUTHORITY=false
PROGRAM_AUTHORITY_ASSIGNED=true
PROGRAM_OWNER_REF=zhangbin
PROGRAM_OWNER_ASSIGNMENT_REFERENCE=ADR-020
PROGRAM_STATUS_CHANGES_PROJECT_TRUTH=false
RECOMMENDATION_IS_DECISION=false
DECISION_IS_EXECUTION=false
```

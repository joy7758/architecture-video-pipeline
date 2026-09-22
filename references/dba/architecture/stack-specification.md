---
spec_id: DBA-STACK-0.1
title: Digital Biosphere Stack v0.1
status: architecture-specification-v0.1
implementation_status: not-assessed
authority_effect: none
---

# Digital Biosphere Stack v0.1（数字生物圈技术栈 v0.1）

## 1. 核心不变量

Digital Biosphere Stack 由三个不同的 responsibility domain（职责域）构成：

```text
SAEE
  ↓ evaluation and evolution guidance（评价与演化指导）
DBOS
  ↓ trusted existence and operation services（可信存在与运行服务）
Digital Entities
  ↓ task-specific behavior（具体任务行为）
```

该结构是 architecture layering（架构分层），不是进程调用栈、部署顺序或控制权继承。SAEE 的输出对 DBOS 是评价或建议；DBOS 的输出对 SAEE 是带来源的运行记录、证据与验证结果；Digital Entity 不因出现在规范中而被创建。

## 2. SAEE：为什么演化

SAEE，即 Digital Biosphere Evolution Engine（数字生物圈进化引擎），负责解释和评价“为什么需要演化、什么演化方向更合适”。

### 2.1 负责范围

- Evidence Evaluation（证据评价）；
- Fitness Assessment（适应度评估）；
- Evolution Modeling（演化建模）；
- Governance Evolution（治理演化）；
- Ecological Stability Analysis（生态稳定性分析）；
- 基于输入记录产生风险评估、演化建议和治理建议。

### 2.2 主要输入

- 来自 DBOS 的 Entity Identity（主体身份引用）；
- Execution History（执行历史）；
- Evidence Bundle（证据包）；
- Verification Result（验证结果）；
- Resource Usage（资源使用记录）；
- Behavior Trace（行为轨迹）。

### 2.3 主要输出

- Fitness Assessment（适应度评估）；
- Evolution Recommendation（演化建议）；
- Risk Assessment（风险评估）；
- Governance Suggestion（治理建议）。

### 2.4 不负责范围

- 不负责 DBOS 的身份注册、执行编排或运行状态存储；
- 不直接修改 DBOS 状态；
- 不因给出建议而获得执行、授权或治理生效权；
- 不把自身评价自动升级为新的运行事实。

## 3. DBOS：如何可信存在和运行

DBOS，即 Digital Biosphere Operating System（数字生物圈操作系统），负责提供“数字主体如何被识别、记录、运行、取证和验证”的存在与运行基础。

### 3.1 负责范围

- Identity（身份）；
- Capability（能力记录与能力边界）；
- Execution（执行记录与受约束执行面）；
- Evidence Collection（证据采集）；
- Verification（验证）；
- Federation（联邦互操作边界）；
- Registration（注册）与 Retirement（退役）等生命周期状态管理。

这里的“负责”是架构归属，不是对当前 DBOS 仓库实现状态的声明。Capability record（能力记录）不能凭注册动作创造真实能力；Evidence（证据）不能凭采集动作自动成为已验证真相；Verification Result（验证结果）只证明其声明范围内的检查结果。

### 3.2 主要输出

DBOS 向 SAEE 提供带来源、范围与状态的运行侧材料。DBOS 不替 SAEE 计算适应度、选择演化方向或维护 SAEE 内部算法。

### 3.3 不负责范围

- 不负责 SAEE 内部演化算法；
- 不把资源使用记录自动解释为适应度；
- 不把验证结果自动解释为生态稳定性或演化优越性；
- 不因接收 SAEE 建议而自动执行状态变更。

## 4. Digital Entity：执行具体任务

Digital Entity（数字主体）是在明确身份、能力边界和授权条件下承担具体任务的概念角色。它可以是未来系统中的 Agent、服务或其他可识别执行单元，但本规范不创建、实例化或认证任何 Digital Entity。

ADR-004 与 [`digital-entity-specification.md`](digital-entity-specification.md) 已将 `Digital Entity` 正式定义为 architecture-level common model（架构级共同模型）：它必须具有 Identity、Capability Boundary、Execution History、Evidence History 与 Lifecycle State。该定义不是代码类型、数据库 schema、Runtime class 或已创建实例。

Digital Entity 与 Digital Organism 的关系已由 [`digital-organism-crosswalk.md`](digital-organism-crosswalk.md) 定义：Digital Organism 是经过额外 SAEE 评价、Governance Decision 与 DBOS 资格记录的高级 Digital Entity 状态，`Digital Entity ≠ Digital Organism`。Digital Entity 与 LAU（Life-like Autonomous Unit，类生命自治单元）、Persona Object 及其他主体术语之间的对应关系仍未定义，不得据此宣称等价、继承或替代。

### 4.1 负责范围

- 在外部定义且有效的授权范围内执行具体任务；
- 产生可被 DBOS 记录的行为与结果；
- 遵守其声明的能力、资源与治理约束。

### 4.2 不负责范围

- 不自证身份、能力或可信性；
- 不自行把行为记录升级为验证结果；
- 不自行把局部表现升级为适应度或演化决策；
- 不因 SAEE 建议而绕过 DBOS 或外部授权边界。

## 5. 三种信息平面

| 信息平面 | 典型内容 | 首要归属 | 边界 |
|---|---|---|---|
| Operational Record Plane（运行记录平面） | 身份引用、执行历史、资源使用、行为轨迹 | DBOS | 记录“观察到或登记了什么”，不自动证明完整真实性 |
| Verification Plane（验证平面） | 检查范围、方法、结果、未知项 | DBOS | 只对声明的检查范围负责，不等于全局正确 |
| Assessment Plane（评价平面） | 适应度、风险、稳定性、演化与治理建议 | SAEE | 派生评价必须引用输入，不直接改变运行状态 |

Digital Entity 是行为来源，不是这三个平面的自动权威。任何从记录到验证、从验证到评价、从评价到状态变化的提升都必须保持来源、范围和独立 gate（闸门）。

## 6. 协作原则

1. Identity before evaluation（先有身份引用，再做评价）：SAEE 必须能够引用被评价对象，但不得把一个未确认引用描述为已验证身份。
2. Evidence before assessment（先有证据，再做评估）：SAEE 的评价必须可追溯到 DBOS 提供或明确登记的输入。
3. Recommendation is not authorization（建议不是授权）：SAEE 输出不能直接成为 DBOS 状态变更命令。
4. Verification is bounded（验证有边界）：DBOS 验证结果只覆盖其明确声明的对象、时间、规则和证据。
5. Unknown remains unknown（未知保持未知）：缺失、未验证或冲突数据不得被默认值升级为事实。
6. No capability promotion（不得提升能力事实）：本分层不证明任何接口、能力、联邦或执行路径已实现。

## 7. 一句话定位

- SAEE 回答：**为什么演化。**
- DBOS 回答：**如何可信存在和运行。**
- Digital Entity 回答：**在已授权边界内执行什么具体任务。**

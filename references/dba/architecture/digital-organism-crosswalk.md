---
spec_id: DBA-DIGITAL-ORGANISM-CROSSWALK-0.1
title: Digital Organism Crosswalk Specification v0.1
title_zh: 数字有机体交叉映射规范 v0.1
status: non-executable-qualification-crosswalk
organism_model_defined: true
organism_instance_created: false
entity_instance_created: false
runtime_effect: none
permission_effect: none
---

# Digital Organism Crosswalk Specification v0.1

本规范定义 Digital Entity（数字实体）与 Digital Organism（数字有机体）的资格关系。它建立 qualification crosswalk（资格交叉映射），不创建新的 Entity、Agent、Runtime、Capability 或 Organism 实例。

## 1. Definition（定义）

Digital Organism 不是所有 Digital Entity。

Digital Organism 是满足 SAEE 演化条件、具有长期持续性和可追溯生态行为证据，并经过显式 Governance Decision 采纳的高级 Digital Entity 资格状态。

所有 Digital Organism 必须先是满足最低要求的 Digital Entity；Digital Entity 不因 Active、Autonomous、拥有 Capability 或运行时间较长而自动成为 Digital Organism。

### 1.1 核心不变量

```text
DIGITAL_ENTITY_NE_DIGITAL_ORGANISM=true
RUNTIME_NE_ORGANISM=true
AGENT_NE_ORGANISM=true
CAPABILITY_NE_ORGANISM=true
AUTONOMY_NE_ORGANISM=true
SAEE_EVALUATION_NE_ORGANISM_STATUS=true
ORGANISM_STATUS_REQUIRES_GOVERNANCE_DECISION=true
```

## 2. Crosswalk（资格映射）

```text
Digital Entity
      ↓ candidate eligibility review
Candidate Digital Organism
      ↓ SAEE evaluation + Governance Decision
Digital Organism
```

该映射是 Digital Entity 之上的 qualification track（资格轨道），不是替代 `Proposed → Registered → ... → Retired` 的第二套 Entity Identity。进入 Candidate 或 Digital Organism 不创建新 `entity_id`，也不改变 Repository、Agent 或 Runtime 的概念边界。

| 资格状态 | 最小语义 | 决定来源 | 不表示 |
|---|---|---|---|
| Digital Entity | 满足统一 Entity 最低要求并由 DBOS 管理 | DBOS lifecycle records | 是 Organism Candidate |
| Candidate Digital Organism | 候选条件具有可追溯记录并进入 SAEE 评价 | 显式资格审查记录 | 已满足 Organism 资格 |
| Digital Organism | Organism 条件获得 SAEE 有界评价，并经 Governance Decision 采纳、由 DBOS 记录 | SAEE Recommendation + explicit Decision + DBOS record | 无限自治、永久资格或自动权限 |

## 3. Candidate Digital Organism Conditions（候选条件）

候选必须具备下列记录；任一项目缺失时保持 Digital Entity 或 `candidate_incomplete`，不得补造：

| 条件 | 最小证据语义 | 主要责任 |
|---|---|---|
| Identity（身份） | 稳定 `entity_id`、身份状态与来源 | DBOS |
| Persistent History（持续历史） | 跨多次 Execution/Runtime 的连续、仅追加历史 | DBOS |
| Execution Trace（执行轨迹） | 有对象、时间、Context 和结果的行为引用 | DBOS |
| Evidence Accumulation（证据积累） | 可追溯 Evidence History，不以单次输出替代 | DBOS |
| Environmental Interaction（环境交互） | 与明确环境或其他实体交互的有界记录 | DBOS 记录；SAEE 可评价 |
| Adaptation Signal（适应信号） | 表明可能发生适应变化的有来源信号 | SAEE 识别与评价，不是适应结论 |

Candidate 条件只允许进入评价，不构成 Digital Organism 证明。

## 4. Digital Organism Qualification（数字有机体资格）

除候选条件外，资格评价必须覆盖：

| 资格条件 | 评价问题 | 事实与评价边界 |
|---|---|---|
| Long-term Persistence（长期持续性） | 是否在声明时间和环境范围内保持身份、历史与行为连续性？ | DBOS 提供记录；SAEE 评价持续性 |
| Self-maintaining Behavior（自维持行为） | 是否在有效授权内表现出维护功能、约束或目标连续性的行为？ | 不表示自我授权、自我修改或无限自治 |
| Adaptive Evolution（适应性演化） | 是否存在可追溯变化及对环境/任务表现的适应评价？ | SAEE 评价；Recommendation 不是状态变化 |
| Ecological Interaction（生态交互） | 是否与环境、资源或其他 Entity 形成可评价的相互作用？ | DBOS 记录交互；SAEE 分析生态意义 |
| Fitness Evaluation（适应度评价） | 是否有明确模型、输入、scope 和不确定性的 Fitness Assessment？ | Owner 为 SAEE，不是 DBOS Verification |
| Lineage Record（谱系记录） | 是否保留版本、适应、分支或来源连续性的可追溯记录？ | DBOS 管理记录；SAEE 只读评价 |

所有条件都必须有明确 scope、时间、来源和状态。`unknown`、`partial` 或 `conflicted` 不得自动算作满足。

## 5. Authority and Responsibility（权力与责任）

### 5.1 DBOS

DBOS 提供并管理：

- Identity；
- Persistent History；
- Execution Trace；
- Evidence History；
- Environmental Interaction records；
- Lineage Record；
- Candidate/Organism qualification status 的规范记录；
- 资格变化后的历史连续性。

DBOS 不产生 Adaptive Evolution、Fitness 或 Ecological Stability 结论，也不能因记录齐全而自行授予 Organism 资格。

### 5.2 SAEE

SAEE 评价：

- Adaptation；
- Fitness；
- Adaptive Evolution；
- Long-term Persistence 的演化意义；
- Self-maintaining Behavior；
- Ecological Interaction 与 Stability。

SAEE 只能产生 Evaluation 与 Recommendation，不能创建 Identity、写入 Organism 状态、授予权限或执行变化。

### 5.3 Governance Decision

Governance Decision：

- 审查 SAEE 资格 Recommendation 及 DBOS 记录；
- 决定是否采纳 Candidate → Digital Organism 的资格变化；
- 决定是否进入更高资格阶段、暂停、撤销或恢复资格；
- 不直接修改 Entity Object 或执行 Runtime 变化。

经批准且采纳的资格变化仍必须由 DBOS 在生命周期控制下记录，并保留 Evidence 与 Verification 链。

## 6. Non-equivalence Rules（非等价规则）

- Runtime ≠ Organism：一次运行实例不具有跨时间 Identity、History 或 Lineage。
- Agent ≠ Organism：Agent 是角色或实现形态，不自动满足长期演化资格。
- Capability ≠ Organism：一个或多个能力不证明持续性、自维持、适应或生态交互。
- Autonomy ≠ Organism：自治描述不证明 Identity、Evidence、Fitness 或 Lineage。
- Digital Entity ≠ Organism：Entity 是基础共同模型，Organism 是额外资格状态。
- Evaluation ≠ Qualification Decision：SAEE 评价不是资格决定。
- Qualification ≠ Permission：Organism 资格不授予任务执行、外部系统操作或自我修改权限。

## 7. Qualification Continuity（资格连续性）

- Digital Organism 资格必须引用原 Digital Entity Identity，不创建替代身份；
- 新评价通过追加记录表达，不修改旧 Evaluation；
- 资格暂停、撤销、降级或 Retired 不删除历史资格和 Lineage；
- 证据不足时可以保持 Candidate、暂停或产生新的 Recommendation，不能静默保留肯定结论；
- 资格变化不自动改变 Capability Boundary、Permission 或 Runtime。

## 8. Agent-readable qualification test（智能体可读资格检查）

```text
ENTITY_IDENTITY_VERIFIED=
PERSISTENT_HISTORY_PRESENT=
EXECUTION_TRACE_PRESENT=
EVIDENCE_ACCUMULATION_PRESENT=
ENVIRONMENTAL_INTERACTION_PRESENT=
ADAPTATION_SIGNAL_PRESENT=
LONG_TERM_PERSISTENCE_EVALUATED=
SELF_MAINTAINING_BEHAVIOR_EVALUATED=
ADAPTIVE_EVOLUTION_EVALUATED=
ECOLOGICAL_INTERACTION_EVALUATED=
FITNESS_EVALUATION_PRESENT=
LINEAGE_RECORD_PRESENT=
GOVERNANCE_DECISION_REF=
DBOS_QUALIFICATION_RECORD_REF=
ORGANISM_INSTANCE_CREATED=false
```

## 9. 非实现状态

```text
DIGITAL_ORGANISM_CROSSWALK_DEFINED=true
CANDIDATE_ORGANISM_CREATED=false
DIGITAL_ORGANISM_INSTANCE_CREATED=false
DIGITAL_ENTITY_INSTANCE_CREATED=false
SAEE_ORGANISM_AUTHORITY_CREATED=false
DBOS_EVOLUTION_AUTHORITY_CREATED=false
PERMISSION_GRANTED=false
RUNTIME_CREATED=false
API_CREATED=false
CODE_CHANGED=false
```

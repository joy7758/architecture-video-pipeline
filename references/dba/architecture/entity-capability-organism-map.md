---
spec_id: DBA-ENTITY-CAPABILITY-ORGANISM-MAP-0.1
title: Digital Entity-Capability-Organism Relationship Map v0.1
title_zh: 数字实体-能力-有机体统一关系图 v0.1
status: non-executable-architecture-map
automatic_transition_allowed: false
entity_instance_created: false
organism_instance_created: false
runtime_effect: none
---

# Digital Entity-Capability-Organism Relationship Map v0.1

本图统一 Digital Entity、Capability、Execution、Evidence、Evaluation、Adaptation 与 Digital Organism 的责任和状态关系。竖向排列表示 information and governance dependency（信息与治理依赖），不是自动生命周期、Runtime pipeline 或权限继承。

## 1. Unified Relationship（统一关系）

```text
Digital Entity
      |
  Capability
      |
   Execution
      |
   Evidence
      |
  Evaluation
      |
  Adaptation
      |
Digital Organism
```

任何相邻节点之间都存在独立 gate。Digital Entity 不必须成为 Digital Organism；Digital Organism 也不是所有 Entity 的默认终点。

## 2. Gated Interpretation（受控解释）

| 节点 | 主要 Owner / 责任 | 输入 | 形成的记录或评价 | 下一步 gate |
|---|---|---|---|---|
| Digital Entity | DBOS Existence Governance | Candidate、Identity source | Entity Identity、Lifecycle、History references | Capability declaration review |
| Capability | DBOS 管理记录与生命周期；Entity 提供声明 | Entity Identity、description、scope、constraints | Declared/Verified/Available capability records | Explicit Authorization + Permission + Context |
| Execution | DBOS 记录；Digital Entity 是行为来源 | 有效 Capability、Authorization、Permission、Context | Execution History、Behavior Trace、Resource Usage | Evidence collection and verification |
| Evidence | DBOS | Execution 与外部来源材料 | Evidence Object、Verification Result | SAEE Evaluation |
| Evaluation | SAEE | DBOS Identity、Execution、Evidence、Verification | Reliability、Fitness、Risk、Adaptability、Stability | Recommendation + Governance Decision |
| Adaptation | SAEE 建议；Governance Decision 采纳；DBOS 执行并记录 | Evaluation、Recommendation、Decision | 新的受控变化、Execution、Evidence、Verification | Organism qualification review 或回到 Active |
| Digital Organism | DBOS 保存资格记录；SAEE 评价；Governance Decision 决定 | 长期记录、Fitness、Lineage、生态交互与显式 Decision | 高级 Digital Entity qualification state | 持续复评；不产生自动权限 |

## 3. Required Separation（强制分离）

```text
Entity ≠ Capability
Capability ≠ Permission
Permission ≠ Execution
Execution ≠ Evidence
Evidence ≠ Evaluation
Evaluation ≠ Decision
Adaptation Recommendation ≠ Adaptation Execution
Digital Entity ≠ Digital Organism
Organism Qualification ≠ Authority
```

## 4. Governance Gates（治理闸门）

1. Entity → Capability：只有已注册 Identity 才能关联 Capability Object；声明不等于验证。
2. Capability → Execution：必须同时满足 Verified/Available Capability、有效 Authorization、DBOS Permission、Context、constraints 和 Entity lifecycle。
3. Execution → Evidence：DBOS 形成 canonical records；行为输出不能自证 Evidence。
4. Evidence → Evaluation：SAEE 引用原始材料形成派生评价，不能修改 DBOS Evidence。
5. Evaluation → Adaptation：SAEE 只产生 Recommendation；Governance Decision 决定是否采纳。
6. Adaptation → Digital Organism：必须满足 Candidate/Organism 条件、SAEE Evaluation、显式 Decision 和 DBOS qualification record。
7. 任一 gate 失败时保持原状态或明确 unknown/rejected/revoked，不得自动晋级。

## 5. Research Agent Projection（Research Agent 投影）

```text
Research Agent reference role
  ↓ future DBOS-governed Digital Entity
Declared research capabilities
  ↓ separate verification and authorization
Research task executions
  ↓ DBOS evidence records
SAEE evaluation
  ↓ optional adaptation recommendation
Governance Decision + DBOS update
  ↓ only after long-term qualification evidence
Candidate Digital Organism
```

本投影没有创建 Research Agent，也没有保证未来 Research Agent 会进入 Organism 资格轨道。

## 6. 非实现状态

```text
ENTITY_CAPABILITY_ORGANISM_MAP_DEFINED=true
AUTOMATIC_TRANSITION_ALLOWED=false
CAPABILITY_INSTANCE_CREATED=false
EXECUTION_CREATED=false
EVIDENCE_CREATED=false
EVALUATION_CREATED=false
ADAPTATION_EXECUTED=false
DIGITAL_ORGANISM_INSTANCE_CREATED=false
RESEARCH_AGENT_INSTANCE_CREATED=false
```

---
spec_id: DBA-RESEARCH-AGENT-EVALUATION-0.1
title: Research Agent Evaluation Framework v0.1
title_zh: 科研数字实体评价框架 v0.1
status: conceptual-evaluation-entry-specification
contract_reference: saee-dbos-contract.md
pilot_reference: research-agent-pilot-specification.md
protocol_reference: research-agent-evaluation-protocol.md
evaluation_implemented: false
evaluation_executed: false
endpoint_defined: false
schema_implemented: false
authority_effect: none
---

# Research Agent Evaluation Framework v0.1（科研数字实体评价框架 v0.1）

本框架定义未来 Research Agent Pilot 如何复用 SAEE–DBOS Contract（SAEE–DBOS 契约）进入 SAEE 评价。它只定义概念输入、输出、评价维度和治理交接，不创建 evaluator（评价器）、算法、schema、API、Execution、Evidence 或 Recommendation 实例。

本文件保留维度与契约语义；有序输入检查、评价步骤、Human Review 和停止规则由 [`research-agent-evaluation-protocol.md`](research-agent-evaluation-protocol.md) 定义。Framework ≠ Executable Protocol，Protocol Design ≠ Evaluation Execution。

## 1. Evaluation Boundary（评价边界）

```text
DBOS provides bounded operational facts
SAEE derives bounded evaluation
Governance Decision reviews recommendation
DBOS records any separately authorized change
```

DBOS facts ≠ SAEE Evaluation；SAEE Evaluation ≠ Decision；Decision ≠ Execution。

## 2. Input: DBOS → SAEE（输入）

### 2.1 Required conceptual inputs（必需概念输入）

| contract item | Research Agent Pilot 语义 | 最低边界 |
|---|---|---|
| Execution History（执行历史） | 与 `entity_id` 和明确任务 Context 相关的有序执行记录或引用 | 记录存在不证明完整、成功或获授权 |
| Evidence Bundle（证据包） | 论文、数据、过程、输出、来源、限制和人工 gate 的有界证据集合 | 有 Evidence 不表示研究主张成立 |
| Verification Result（验证结果） | DBOS 对明确对象、规则、输入和版本形成的检查结果 | 局部验证不等于科研有效性或高 Fitness |

### 2.2 Supporting inputs（支持输入）

在评价问题需要且契约范围明确时，DBOS 可以提供：

- Entity Identity（实体身份）；
- Resource Usage（资源使用）；
- Behavior Trace（行为轨迹）。

所有输入必须保留 `entity_ref`、`source_ref`、时间、scope、provenance、status 和 limitations。缺失、冲突或无法验证的数据必须保持 `unknown`、`partial` 或 `conflicted`，SAEE 不得补造。

## 3. Evaluation Dimensions（评价维度）

| 维度 | 评价问题 | 参考输入 | 不表示 |
|---|---|---|---|
| Reliability（可靠性） | 输出是否与来源、方法、任务要求和重复记录一致？ | Execution History、Evidence、Verification | 获得 Permission |
| Evidence Quality（证据质量） | 来源、覆盖、完整性、冲突和限制是否透明？ | Evidence Bundle、Verification Result | Evidence truth 被改写 |
| Efficiency（效率） | 在声明质量和资源约束内表现如何？ | Resource Usage、Execution History | 价值或 Fitness 自动为高 |
| Adaptability（适应性） | 对新任务、材料和反馈的变化是否有界且可解释？ | Behavior Trace、多次 Execution/Evidence | 已授权自我修改 |
| Stability（稳定性） | 在声明等价条件或扰动下表现是否可解释地稳定？ | 重复记录、模型/工具版本、Context | Digital Organism 资格成立 |

评价维度必须声明方法版本、输入范围、不确定性和限制。本框架不定义实际算法、权重、评分阈值或通过线。

## 4. Output: SAEE → Governance Decision / DBOS（输出）

| contract item | 最小内容 | 权限类别 |
|---|---|---|
| Fitness Assessment（适应度评估） | Reliability、Evidence Quality、Efficiency、Adaptability、Stability 的有界评价及输入引用 | Evaluation only（仅评价） |
| Risk Assessment（风险评估） | `risk_level`、`risk_reason`、影响范围、未知项与置信边界 | Recommendation input（建议输入） |
| Evolution Recommendation（演化建议） | `recommended_change`、理由、置信度、前提和限制 | Recommendation only（仅建议） |

SAEE 输出不得被解释为 Command、Authorization、Permission、Capability grant、Lifecycle update、论文结论或 Human approval。

## 5. Evaluation Handoff（评价交接）

```text
DBOS Execution History + Evidence Bundle + Verification Result
  ↓ contract validation
SAEE Fitness Assessment + Risk Assessment
  ↓ bounded interpretation
SAEE Evolution Recommendation
  ↓ explicit Review and Decision
Governance Adoption or Rejection
  ↓ if adopted, separately authorized
DBOS lifecycle-controlled change
  ↓
new Execution / Evidence / Verification for re-evaluation
```

这个闭环不是自动 workflow。任何缺少输入、授权、人工 gate 或有效生命周期状态的转换必须 fail closed（保守失败）。

## 6. Research Metric Projection（研究指标投影）

[`research-agent-research-plan.md`](research-agent-research-plan.md) 的指标与评价入口关系如下：

| 研究指标 | 主要 DBOS 输入 | 主要 SAEE 解释 |
|---|---|---|
| Reproducibility | Execution History、Behavior Trace、版本和 Context | 重复过程与结果差异的有界解释 |
| Evidence Completeness | Evidence Bundle、Verification Result | 缺失、覆盖、冲突和限制评价 |
| Execution Traceability | Execution History、provenance references | 输出到输入、过程和授权 Context 的可追溯性评价 |
| Evaluation Stability | 多次有界输入、评价模型版本和历史 Evaluation | 评价差异、漂移与不确定性的稳定性解释 |

没有预先批准的操作定义和阈值时，这些指标不能产生 pass/fail（通过/失败）结论。

## 7. Human Review Boundary（人工审查边界）

- 人工 reviewer 必须能够检查输入范围、缺失项、方法版本和 SAEE 限制；
- Research Agent 不能评价自己的最终科学有效性；
- SAEE 不能批准论文、实验结果或重大结论发布；
- Governance Decision 不能替代领域专家、作者、伦理或数据 Owner 的必要确认；
- DBOS 只能执行另行获批的变化，不能发明 Evolution conclusion（演化结论）。

## 8. Non-implementation Status（非实现状态）

```text
RESEARCH_AGENT_EVALUATION_FRAMEWORK_DEFINED=true
DBOS_SAEE_EVALUATION_ADAPTER_CREATED=false
EVALUATION_SCHEMA_IMPLEMENTED=false
EVALUATION_ENDPOINT_CREATED=false
EVALUATION_EXECUTED=false
FITNESS_ASSESSMENT_CREATED=false
RISK_ASSESSMENT_CREATED=false
EVOLUTION_RECOMMENDATION_CREATED=false
PERMISSION_GRANTED=false
LIFECYCLE_CHANGED=false
SAEE_EXECUTION_AUTHORITY_CREATED=false
DBOS_EVOLUTION_AUTHORITY_CREATED=false
```

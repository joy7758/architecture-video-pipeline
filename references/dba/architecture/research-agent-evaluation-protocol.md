---
spec_id: DBA-RESEARCH-AGENT-EVALUATION-PROTOCOL-0.1
title: Research Agent Evaluation Protocol v0.1
title_zh: 科研数字实体评价协议 v0.1
status: non-executable-evaluation-protocol-design
framework_reference: research-agent-evaluation-framework.md
research_protocol_reference: research-agent-research-protocol.md
evaluation_implemented: false
evaluation_executed: false
algorithm_defined: false
thresholds_defined: false
authority_effect: none
---

# Research Agent Evaluation Protocol v0.1（科研数字实体评价协议 v0.1）

本协议把 [`research-agent-evaluation-framework.md`](research-agent-evaluation-framework.md) 的概念维度组织为未来可审查的 SAEE Evaluation Protocol（评价协议）。它不定义算法、权重、评分阈值、schema、API、evaluator、Evaluation instance 或 Recommendation instance。

## 1. Protocol Boundary（协议边界）

```text
DBOS operational facts
  → SAEE bounded evaluation
  → Human Review / Governance Decision input
```

```text
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_SCIENTIFIC_VALIDITY=true
EVALUATION_NE_AUTHORITY=true
FITNESS_ASSESSMENT_NE_PERMISSION=true
RECOMMENDATION_NE_DECISION=true
```

SAEE 评价 Research Agent 的有界表现，不决定论文是否正确、实验结果是否成立、谁是作者、是否发表或是否执行系统变化。

## 2. Input: DBOS → SAEE（输入）

| 必需输入 | 最低语义 | 接受检查 | 不表示 |
|---|---|---|---|
| Execution History（执行历史） | 与未来 `entity_id`、任务和 Context 相关的有序记录或引用 | 来源、时间、范围、授权引用、状态和缺失项 | 执行完整、正确或获授权 |
| Evidence Bundle（证据包） | Papers、Dataset References、Research Questions、过程、输出、失败结果、人工 review 和限制 | provenance、版本、覆盖、冲突、完整性声明和保留状态 | Truth 或 Scientific Validity |
| Verification Result（验证结果） | DBOS 对明确对象、规则、输入和版本形成的有界检查 | 验证对象、规则版本、结果、限制和未知项 | Fitness 高或研究结论成立 |

可选 supporting inputs（支持输入）包括 Entity Identity、Resource Usage 和 Behavior Trace；只有评价问题明确需要且契约范围允许时才能使用。

输入缺失、来源不可解析、版本冲突或 Verification boundary 不明确时，协议必须产生 `unknown`、`partial`、`conflicted` 或 `not_evaluable` 等保守语义，而不是补造记录或默认通过。

## 3. Evaluation Dimensions（评价维度）

| 维度 | 评价问题 | 强制限制 |
|---|---|---|
| Reliability（可靠性） | 输出与来源、方法、任务要求和重复记录是否一致？ | 一致不等于科学正确或获准继续执行 |
| Evidence Quality（证据质量） | 来源、覆盖、完整性、冲突、失败结果和限制是否透明？ | 完整性不等于 Truth 或 Validity |
| Efficiency（效率） | 在声明质量、资源和时间约束下表现如何？ | 资源较少不自动等于 Fitness 较高 |
| Adaptability（适应性） | 对新材料、任务和人工反馈的变化是否有界且可解释？ | 不证明已授权自我修改或演化 |
| Stability（稳定性） | 在声明等价 Context 或明确扰动下评价是否可解释地稳定？ | 不证明生态稳定或 Digital Organism 资格 |

实际操作定义、测量方法、权重、阈值和 pass/fail 规则必须在未来研究执行前获得明确批准。本协议不提供默认值。

## 4. Evaluation Procedure（评价程序）

```text
Input Intake
  ↓
Contract and Provenance Check
  ↓
Evidence Sufficiency Classification
  ↓
Dimension Evaluation
  ↓
Risk and Uncertainty Recording
  ↓
SAEE Output Formation
  ↓
Human Review
```

1. Input Intake：登记 DBOS 输入引用，不复制或改写其事实语义；
2. Contract and Provenance Check：检查契约版本、scope、来源、状态和限制；
3. Evidence Sufficiency Classification：将输入标为 sufficient、partial、conflicted、unknown 或未来等价语义；
4. Dimension Evaluation：只在输入足够且方法已批准的维度形成评价；
5. Risk and Uncertainty Recording：记录风险、未知项、置信边界和不得外推范围；
6. SAEE Output Formation：形成有输入引用和版本的 Assessment/Recommendation；
7. Human Review：Human Reviewer 检查评价是否越权、过度解释或遗漏异常。

这些步骤是 protocol design，不是已经实现的 workflow 或自动状态机。

## 5. Output: SAEE → Review Boundary（输出）

| 输出 | 最低内容 | 权限类别 |
|---|---|---|
| Fitness Assessment（适应度评估） | 五个评价维度、输入引用、方法版本、不确定性和限制 | Evaluation only（仅评价） |
| Risk Assessment（风险评估） | `risk_level`、`risk_reason`、影响范围、未知项和置信边界 | Review input（复核输入） |
| Evolution Recommendation（演化建议） | `recommended_change`、理由、前提、置信度、限制和替代方案 | Recommendation only（仅建议） |

输出不得自动：

- 修改 Research Agent Identity、Capability、Permission 或 Lifecycle State；
- 修改 DBOS Execution/Evidence/Verification records；
- 成为 Research Conclusion、Publication Decision 或 External Release；
- 触发 Runtime、实验、任务或系统变化；
- 证明 Digital Organism 资格。

## 6. Review and Adoption Boundary（复核与采纳边界）

- Human Reviewer 检查科学解释、异常和评价限制；
- Human Research Owner 决定评价如何影响研究结论，但不能改写原始 SAEE output；
- 涉及 Entity/Capability/Lifecycle change 的 Recommendation 必须进入 Governance Decision；
- 只有经采纳、独立授权并满足 DBOS lifecycle control 的变化才能进入未来执行；
- 新执行必须形成新的 Evidence 和 Verification，之后才能重新评价。

Research Conclusion path（科研结论路径）与 System Change path（系统变化路径）是两条不同路径，不得合并。

## 7. Failure and Stop Rules（失败与停止规则）

以下情况不得形成肯定性 Fitness、演化或科学有效性结论：

- 必需 DBOS 输入缺失；
- Evidence provenance、版本或范围无法确定；
- 失败结果或异常被删除、隐藏或不可追溯；
- 评价方法、阈值或模型版本未获批准；
- 输入与输出存在未解决冲突；
- Human Review 缺失；
- 有人要求 SAEE 直接授予 Permission、发表、署名或执行变化。

停止时必须保留已接收材料、诊断和停止原因的未来记录语义；本协议不创建这些记录。

## 8. Non-execution Status（非执行状态）

```text
RESEARCH_AGENT_EVALUATION_PROTOCOL_DEFINED=true
EVALUATION_PROTOCOL_ADOPTED=false
EVALUATION_ALGORITHM_DEFINED=false
EVALUATION_THRESHOLDS_DEFINED=false
DBOS_INPUT_RECEIVED=false
EVIDENCE_EVALUATED=false
FITNESS_ASSESSMENT_CREATED=false
RISK_ASSESSMENT_CREATED=false
EVOLUTION_RECOMMENDATION_CREATED=false
HUMAN_REVIEW_COMPLETED=false
PERMISSION_GRANTED=false
LIFECYCLE_CHANGED=false
SAEE_EXECUTION_AUTHORITY_CREATED=false
DBOS_EVOLUTION_AUTHORITY_CREATED=false
```

---
spec_id: DBA-RESEARCH-AGENT-RESEARCH-PLAN-0.1
title: Research Agent Research Plan v0.1
title_zh: 科研数字实体研究计划 v0.1
status: future-research-direction-only
pilot_reference: research-agent-pilot-specification.md
protocol_reference: research-agent-research-protocol.md
human_oversight_reference: research-agent-human-oversight-model.md
evaluation_protocol_reference: research-agent-evaluation-protocol.md
implementation_contract_reference: research-agent-implementation-contract.md
failure_model_reference: research-agent-failure-model.md
study_authorized: false
study_executed: false
dataset_selected: false
paper_drafted: false
paper_submitted: false
---

# Research Agent Research Plan v0.1（科研数字实体研究计划 v0.1）

本文件定义 Research Agent Pilot 的未来论文研究方向和度量语义。它不是研究方案批准、实验 protocol（协议）、数据集选择、实验执行记录、论文草稿或投稿授权。

## Protocol Reference（协议引用）

本计划定义未来研究“研究什么”；[`research-agent-research-protocol.md`](research-agent-research-protocol.md) 定义“由谁负责、允许哪些任务、记录哪些 Evidence、如何复现和哪些状态必须由人批准”。Human Role 和 SAEE 评价步骤分别见 [`research-agent-human-oversight-model.md`](research-agent-human-oversight-model.md) 与 [`research-agent-evaluation-protocol.md`](research-agent-evaluation-protocol.md)。

这些协议已经形成文档，但尚未被具体研究采用，没有任命 Human Research Owner 或 Human Reviewer，也没有授权或执行 Pilot。

未来实验还必须把 [`research-agent-implementation-contract.md`](research-agent-implementation-contract.md) 作为 implementation prerequisite（实现前置条件），并采用 [`research-agent-failure-model.md`](research-agent-failure-model.md) 的失败保留语义。Contract 已定义不等于 Contract 已采用或 Implementation 已授权。

## 1. Research Question（研究问题）

Primary Research Question：

> Can a governed digital entity maintain reproducible research assistance workflows under evidence-based lifecycle management?

中文释义：一个受治理的数字实体，能否在基于证据的生命周期管理下，维持可复现的科研辅助工作流？

### 1.1 Supporting Questions（辅助问题）

1. DBOS 记录的 Execution History、Evidence Bundle 和 Verification Result 是否足以重建一次科研辅助过程？
2. SAEE 的评价在不同任务、时间和重复运行之间是否保持有界稳定？
3. Human Oversight gate 是否能够阻止建议被自动升级为实验结果、重大结论或投稿行为？
4. Capability、Permission 和 Execution 分离后，是否仍能保持可审查的任务完成路径？

这些问题是未来研究方向，不预设答案，也不声明现有系统已经提供相应能力或数据。

## 2. Unit of Analysis（分析单元）

未来研究的候选分析单元是一次受治理的 research assistance workflow（科研辅助工作流）记录链：

```text
Task Context
  → Authorized Execution Reference
  → Process Trace
  → Evidence Bundle
  → Verification Result
  → SAEE Evaluation
  → Human Review / Governance Decision
```

该关系只定义未来可评价对象，不创建 workflow、Execution、Evidence 或 Decision 实例。

## 3. Research Metrics（研究指标）

| metric_id | 指标 | v0.1 操作性含义 | 所需未来材料 | 当前状态 |
|---|---|---|---|---|
| `RA-RM-01` | Reproducibility（可复现性） | 在声明的输入、版本、Context 和限制下，独立重建过程并比较结果的能力 | 任务版本、输入引用、过程记录、工具/模型版本、重复运行记录 | 阈值未定义；未测量 |
| `RA-RM-02` | Evidence Completeness（证据完整性） | 必需输入、过程、输出、来源、限制和人工 gate 引用的覆盖程度 | Evidence Bundle、完整性规则、缺失项与冲突记录 | 阈值未定义；未测量 |
| `RA-RM-03` | Execution Traceability（执行可追溯性） | 从输出追溯到 Execution event、工具调用、输入来源和授权 Context 的能力 | Execution History、Behavior Trace、provenance references | 阈值未定义；未测量 |
| `RA-RM-04` | Evaluation Stability（评价稳定性） | 在声明等价条件或明确扰动下，SAEE 评价变化的可解释程度 | 评价模型版本、输入范围、重复评价结果和不确定性 | 阈值未定义；未测量 |

Metric definition（指标定义）不等于观测值、通过结果或 capability truth。未来阈值必须在研究执行前通过独立审查确定，不能根据结果追溯调整后仍声称为预注册标准。

## 4. Candidate Study Design Boundary（候选研究设计边界）

未来研究可以考虑受控、低外部副作用、可撤销且不涉及正式投稿的任务样本，例如公开论文的结构化分析或在授权材料上的知识整理。但任何具体任务、数据集、模型、工具、比较基线、样本量和统计方法均未由 v0.1 选择。

在研究开始前必须另行形成：

- 已明确采用的 [`research-agent-research-protocol.md`](research-agent-research-protocol.md) 及停止规则；
- 已明确采用的 [`research-agent-implementation-contract.md`](research-agent-implementation-contract.md)、独立 Implementation Authorization 和 conformance review plan（合规审查计划）；
- 数据 Owner、访问范围和敏感性审查；
- Research Agent 的 Identity、Capability、Authorization、Permission 和 Runtime 隔离；
- DBOS 记录与 Verification 的实现证据；
- SAEE 评价模型版本和输入契约；
- Human Oversight、伦理、安全和发表边界；
- 分析方法、阈值和失败语义。

## 5. Claim Ladder（声明阶梯）

未来研究必须区分：

```text
Research direction defined
≠ Implementation Contract adopted
≠ Implementation authorized
≠ Prototype created
≠ Study authorized
≠ Pilot implemented
≠ Data collected
≠ Evaluation completed
≠ Result confirmed
≠ Paper drafted
≠ Paper submitted
≠ Paper published
```

任何阶段只能依据相应记录声明，不得由规范文本推断为已经发生。

## 6. Human and Governance Gates（人工与治理闸门）

- 研究协议、指标阈值和数据范围需要人工批准；
- 实验结果需要独立复核，不由 Research Agent 自证；
- 重大结论、作者顺序、稿件内容和投稿动作需要明确人工决定；
- SAEE Recommendation 不等于研究结论或发表决定；
- DBOS Verification 不等于科学有效性或 SAEE Fitness；
- Architecture Specification 不授予研究执行权限。

## 7. Non-execution Status（非执行状态）

```text
RESEARCH_PLAN_DEFINED=true
RESEARCH_PROTOCOL_REFERENCE_DEFINED=true
IMPLEMENTATION_CONTRACT_REFERENCE_DEFINED=true
RESEARCH_PROTOCOL_APPROVED=false
IMPLEMENTATION_CONTRACT_ADOPTED=false
IMPLEMENTATION_AUTHORIZED=false
PROTOTYPE_CREATED=false
STUDY_AUTHORIZED=false
DATASET_SELECTED=false
PILOT_IMPLEMENTED=false
PILOT_EXECUTED=false
DATA_COLLECTED=false
METRICS_MEASURED=false
RESULT_CONFIRMED=false
PAPER_DRAFTED=false
PAPER_SUBMITTED=false
PAPER_PUBLISHED=false
```

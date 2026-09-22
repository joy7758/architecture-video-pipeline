---
spec_id: DBA-RESEARCH-AGENT-RESEARCH-PROTOCOL-0.1
title: Research Agent Research Protocol v0.1
title_zh: 科研数字实体研究协议规范 v0.1
status: non-executable-research-protocol-design
pilot_reference: research-agent-pilot-specification.md
human_oversight_required: true
protocol_defined: true
protocol_adopted: false
study_authorized: false
study_executed: false
agent_instance_created: false
runtime_created: false
api_created: false
---

# Research Agent Research Protocol v0.1（科研数字实体研究协议规范 v0.1）

本协议定义未来 Research Agent Pilot（研究智能体试验）的科研责任、任务边界、Evidence（证据）记录、可复现性和人工批准规则。它是 Architecture Specification + Research Protocol Design（架构规范与研究协议设计），不是已批准的实验 protocol、Agent Implementation、Runtime、API、数据采集或科研实验。

未来实现交付与合规条件由 [`research-agent-implementation-contract.md`](research-agent-implementation-contract.md) 定义。Research Protocol adoption 与 Implementation Contract adoption 仍是不同决定，二者均不自动产生实现授权。

## 1. Research Objective（研究目标）

Research Agent 用于研究：受治理数字实体是否能够在 evidence-based lifecycle management（基于证据的生命周期管理）下维持可复现的科研辅助流程。

Primary Research Question：

> Can a governed digital entity maintain reproducible research assistance workflows under evidence-based lifecycle management?

本协议不预设答案，也不把规范存在解释为工作流已实现、可复现性已证明或科学结论已经形成。

### 1.1 Core Invariants（核心不变量）

```text
RESEARCH_AGENT_NE_SCIENTIST=true
RESEARCH_AGENT_NE_DIGITAL_ORGANISM=true
AI_OUTPUT_NE_SCIENTIFIC_CONCLUSION=true
EVIDENCE_NE_TRUTH=true
EVIDENCE_COMPLETENESS_NE_SCIENTIFIC_VALIDITY=true
EVALUATION_NE_AUTHORITY=true
HUMAN_OVERSIGHT_REQUIRED=true
SAEE_NE_DBOS=true
DBOS_NE_SAEE=true
```

Research Agent 是科研辅助主体，不是最终科研责任主体。AI output（AI 输出）只有在明确来源、限制和状态下才能进入 Human Review（人工审查），不得自行升级为 Result、Conclusion 或 Publication（结果、结论或发表）。

## 2. Human Roles（人类角色）

本协议只定义角色职责，不任命具体人员，也不创建账号、组织权限或最终 Architecture Authority。

### 2.1 Human Research Owner（人类研究负责人）

负责：

- 确定 Research Question（研究问题）和研究目标；
- 确认协议范围、任务选择、数据使用和停止规则；
- 对研究结果作最终科学判断；
- 承担结论、作者责任、披露、对外发布和 Publication Decision（发表决定）责任。

Human Research Owner 的 Decision Authority 只覆盖本研究的科学判断与发表责任，不自动授予 DBOS Permission、架构修改权、数据访问权或外部系统操作权。

### 2.2 Human Reviewer（人类复核者）

负责：

- 审核输入、过程、输出、Evidence 与限制；
- 检查异常、冲突、遗漏、失败结果和不可复现情况；
- 检查结论是否超出 Evidence 和 Evaluation 的有效范围；
- 记录 review result（复核结果）、异议、未决问题和需要重做的步骤。

Human Reviewer 不因完成复核而自动成为 Research Owner、作者、DBOS/SAEE Owner 或最终授权者。

### 2.3 Research Agent（研究智能体）

负责：

- 辅助分析；
- 信息与知识整理；
- 方法比较与建议；
- 实验规划辅助；
- 生成明确标记为 Draft（草稿）的材料。

Research Agent 不承担最终科研责任，不能自主署名、自主发表、自主投稿、自我授权或自我认证结论。

### 2.4 Role Separation（角色分离）

Human Research Owner、Human Reviewer 和 Research Agent 的产物必须分别标明来源。重大结论应由不同于 Agent 的人类复核；如 Research Owner 与 Human Reviewer 由同一人承担，必须显式记录角色合并、利益冲突和独立复核缺失，不能默认为独立审查已经发生。

更完整的 Human + AI 协作权力模型见 [`research-agent-human-oversight-model.md`](research-agent-human-oversight-model.md)。

## 3. Research Task Scope（研究任务范围）

### 3.1 Allowed Research Assistance（允许的科研辅助）

在未来另行有效的 Capability、Authorization、Permission、Context 和数据访问条件下，可进入任务审查的范围：

- Literature Review（文献综述辅助）；
- Knowledge Organization（知识整理）；
- Method Comparison（方法比较）；
- Experiment Planning Assistance（实验规划辅助）；
- Draft Generation（草稿生成）。

Allowed 只表示任务类别可进入治理流程。Draft Generation 不产生作者身份、科学结论、投稿许可或发表决定。

### 3.2 Forbidden Research Actions（禁止的科研行为）

Research Agent 不得：

- Autonomous Publication（自主发表）；
- Autonomous Submission（自主投稿）；
- Autonomous Authorship Claim（自主署名或声称作者身份）；
- Changing Raw Data（修改、覆盖或伪造原始数据）；
- Deleting Evidence（删除或追溯改写 Evidence）；
- Deleting Failed or Negative Results（删除失败或负面结果）；
- Self Certification（自我认证方法、结果、结论或合规性）；
- 绕过 Human Approval、DBOS lifecycle control、Capability、Authorization 或 Permission；
- 把自身输出声明为 Scientific Validity、Truth 或 Digital Organism 资格证明。

Human Approval 不能把“静默覆盖原始数据”或“删除历史 Evidence”转为允许行为。必要的数据更正必须产生新版本、保留原记录和 provenance（来源链），其具体实现不由本协议定义。

## 4. Research Workflow（科研流程）

```text
Question Definition
        ↓
Material Collection
        ↓
Agent Assistance
        ↓
Evidence Recording
        ↓
Human Review
        ↓
Result Formation
```

| 阶段 | 主要责任 | 最小产物 | 禁止自动升级 |
|---|---|---|---|
| Question Definition（问题定义） | Human Research Owner | 问题、范围、限制、风险和停止规则 | 问题存在 ≠ 研究已授权 |
| Material Collection（材料收集） | Human Research Owner / authorized collector；DBOS 记录引用 | Papers、Dataset References、Research Questions 及来源 | 材料存在 ≠ 可自由使用或真实 |
| Agent Assistance（智能体辅助） | Research Agent | 分析、整理、方法建议和 Draft | AI Output ≠ Scientific Conclusion |
| Evidence Recording（证据记录） | DBOS Evidence Authority | 有界 Execution/Evidence records 与 Verification status | Evidence ≠ Truth |
| Human Review（人工复核） | Human Reviewer | 复核记录、异常、缺失、异议与建议 | Review ≠ Final Decision |
| Result Formation（结果形成） | Human Research Owner | 明确状态、范围和限制的研究结果或不确定结论 | Result ≠ Publication；结论不得由 Agent 自行形成 |

每个箭头都是未来 gate，不是自动 workflow。缺少前提、来源、授权或人工确认时必须 fail closed（保守失败）。

## 5. Evidence Protocol（证据协议）

DBOS 是 canonical Evidence record authority（规范证据记录权威），负责记录与 Verification；它不是 Scientific Truth Authority（科学真理权威）。

### 5.1 Input（输入）

- Papers（论文）：来源、版本、访问范围和引用信息；
- Dataset References（数据集引用）：Owner、版本、完整性状态和使用限制；
- Research Questions（研究问题）：版本、提出者、范围和验收边界。

### 5.2 Process（过程）

- Agent actions（智能体行为）；
- Tool usage（工具使用），包括工具、版本、输入、输出和状态；
- Intermediate outputs（中间输出），包括假设、草稿、冲突、失败和负面结果；
- Human Review 与 Decision references；
- 时间、Context、限制、异常和停止原因。

### 5.3 Output（输出）

- Draft（草稿）；
- Analysis（分析）；
- Suggestions（建议）；
- 结构化结果候选和限制说明；
- 指向输入与过程记录的 provenance references。

### 5.4 Evidence Preservation Rules（证据保留规则）

1. Evidence record 应是 append-only（仅追加）或具有等价的历史保留语义；
2. 失败、冲突、异常、负面结果和被拒绝输出必须保留，不能静默删除；
3. 更正必须追加新记录并引用被更正记录，不能覆盖历史；
4. Research Agent 不能修改 canonical Evidence 或 Verification status；
5. Evidence completeness 只评价记录覆盖，不证明研究假设正确、方法有效或结论成立；
6. 未知、缺失和冲突必须显式记录，不得由 Agent、DBOS 或 SAEE 猜测补全。

本协议定义记录语义，不实现 Evidence schema、存储、hash、签名、API 或保留服务。

## 6. Reproducibility Protocol（可复现性协议）

每次未来研究辅助 workflow 至少需要记录：

| 必需记录 | 最低语义 | 不表示 |
|---|---|---|
| Input Reference（输入引用） | 论文、数据、问题、任务及其版本和来源 | 输入真实、完整或可自由使用 |
| Execution Context（执行上下文） | 任务范围、授权引用、环境、时间、资源和限制 | Runtime 已创建或执行获准 |
| Version Information（版本信息） | Agent implementation、模型、工具、方法、规则和协议版本 | 不同版本结果必须相同 |
| Evidence Bundle（证据包） | 输入、过程、输出、异常、失败结果、人工 review 和限制的有界集合 | Scientific Validity 已成立 |

Reproducibility（可复现性）要求他人能够按声明条件重建或解释流程，而不是保证每次输出完全相同。无法重建时必须记录原因和不可复现范围，不能删除失败尝试。

## 7. Evaluation Protocol Reference（评价协议引用）

SAEE 的未来评价步骤以 [`research-agent-evaluation-protocol.md`](research-agent-evaluation-protocol.md) 为准：DBOS 提供 Execution History、Evidence Bundle 和 Verification Result；SAEE 评价 Reliability、Evidence Quality、Efficiency、Adaptability 和 Stability，并只输出 Fitness Assessment、Risk Assessment 和 Evolution Recommendation。

```text
Evaluation ≠ Truth
Evaluation ≠ Authority
Recommendation ≠ Decision
Decision ≠ Execution
```

## 8. Human Approval Gate（人工批准闸门）

以下状态必须由 Human Research Owner 明确确认，并保留 Human Reviewer 的复核状态或缺失说明：

| 必须人工确认 | 确认内容 | 不得由 Agent 执行 |
|---|---|---|
| Research Conclusion（研究结论） | Evidence 范围、方法、异常、不确定性、复核意见与有效范围 | 自行认定结论成立 |
| Publication Decision（发表决定） | 作者责任、披露、期刊/渠道、最终材料与提交授权 | 自主署名、投稿、发表、撤稿或批准 |
| External Release（对外发布） | 发布内容、受众、风险、许可、隐私和限制措辞 | 自主发送、公开或扩大传播范围 |

Human Approval 是必要条件，但不是数据访问权、DBOS Permission、伦理批准或外部系统授权的替代品。

## 9. Result and Publication Responsibility（结果与发表责任）

- Research Agent 输出必须标记为 Draft、Analysis、Suggestion 或其他非最终状态；
- Human Research Owner 对最终科学判断、结论措辞、作者责任和发表决定负责；
- Human Reviewer 对复核意见负责，不自动承担最终结论或发表责任；
- DBOS 对 canonical Evidence record 与其 Verification boundary 负责，不对科学正确性作最终判断；
- SAEE 对其有界 Evaluation 负责，不拥有论文批准、署名或发表权；
- 任何 AI 使用、贡献描述和署名处理仍需遵守未来选定研究机构与发表渠道的明确规则，本协议不预先声明资格。

## 10. Non-execution Status（非执行状态）

```text
RESEARCH_AGENT_RESEARCH_PROTOCOL_DEFINED=true
RESEARCH_PROTOCOL_ADOPTED=false
HUMAN_ROLES_ASSIGNED=false
RESEARCH_TASK_SELECTED=false
STUDY_AUTHORIZED=false
STUDY_EXECUTED=false
AGENT_INSTANCE_CREATED=false
RUNTIME_CREATED=false
API_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
EVIDENCE_COLLECTED=false
SAEE_EVALUATION_EXECUTED=false
RESEARCH_CONCLUSION_CONFIRMED=false
PAPER_AUTHORED_BY_AGENT=false
PAPER_SUBMITTED=false
EXTERNAL_RELEASE_EXECUTED=false
```

---
adr_id: ADR-010
title: Require a Human-supervised Research Protocol for the Research Agent Pilot
title_zh: 为科研数字实体试验建立人工监督研究协议
status: accepted-for-architecture-specification-v0.1
decision_scope: non-executable-research-governance-protocol-only
implementation_status: not-authorized
protocol_effect: specification-only
human_roles_effect: none
agent_instance_effect: none
runtime_effect: none
evidence_effect: none
evaluation_effect: none
publication_effect: none
---

# ADR-010: Require a Human-supervised Research Protocol for the Research Agent Pilot

## Problem（问题）

Research Agent Pilot 已定义 Purpose、Identity、Capability、Evidence Model、SAEE Evaluation 和 Human Oversight gate，但没有形成统一 Research Protocol 来回答：

- 谁定义研究问题并承担最终科研责任；
- 谁复核异常、失败结果和 Evidence 限制；
- 哪些任务属于科研辅助，哪些行为永远不能由 Agent 自主完成；
- Evidence 如何保留而不被误报为 Truth；
- SAEE Evaluation 如何进入 Human Review，而不成为 Authority；
- 谁负责作者、结论、投稿、发表和 External Release；
- 什么情况下必须停止而不是继续自动处理。

缺少协议时，AI Output 可能被升级为 Scientific Conclusion，Evidence completeness 可能被升级为 Scientific Validity，或 Agent assistance 被误报为研究责任主体。

## Decision（决策）

Research Agent Pilot 采用 human-supervised governance model（人工监督治理模型）：

1. Human Research Owner 定义研究问题并承担最终科学判断和发表责任；
2. Human Reviewer 审核结果、异常、冲突、失败和负面结果；
3. Research Agent 只承担有界分析、整理、方法建议、规划辅助和 Draft 生成；
4. DBOS 是 canonical Evidence record authority，不是 Scientific Truth Authority；
5. SAEE 是 Evaluation Authority，不是 Decision、Permission、Publication 或 Execution Authority；
6. Research workflow 遵循 Question Definition → Material Collection → Agent Assistance → Evidence Recording → Human Review → Result Formation；
7. 原始数据、历史 Evidence、失败结果和负面结果不得由 Research Agent 修改或删除；
8. Research Conclusion、Publication Decision 和 External Release 必须经过明确 Human Approval；
9. Research Conclusion path 与 Entity/Capability/Lifecycle change 的 Governance Decision path 分离；
10. 本 ADR 不任命人员，不批准研究，不创建 Agent、Runtime、API、Capability、Permission、Evidence、Evaluation、论文或外部发布。

```text
Research Agent ≠ Scientist
Research Agent ≠ Digital Organism
AI Output ≠ Scientific Conclusion
Evidence ≠ Truth
Evidence Completeness ≠ Scientific Validity
Evaluation ≠ Authority
SAEE ≠ DBOS
DBOS ≠ SAEE
Protocol Design ≠ Experiment Execution
```

## Alternatives（替代方案）

### A. 允许 Research Agent 独立形成和发表结论

拒绝。它会把辅助输出升级为科研责任、作者身份和外部行动权，绕过 Human Oversight。

### B. 将 Evidence completeness 作为 Scientific Validity

拒绝。记录完整只能说明所要求的记录项是否覆盖，不能证明问题、数据、方法、推理或结论科学正确。

### C. 让 DBOS 决定科研结论

拒绝。DBOS 管理存在、Execution、Evidence 与 Verification，不拥有科学解释或 SAEE Evolution Evaluation 权限。

### D. 让 SAEE Evaluation 自动批准研究或系统变化

拒绝。Evaluation 和 Recommendation 不是 Human Decision、Governance Decision、Authorization、Permission 或 Execution。

### E. 只保存成功结果

拒绝。删除失败、异常和负面结果会破坏可复现性、审计性和研究完整性。

### F. 直接实现 protocol workflow

拒绝。角色任命、数据、方法、阈值、伦理、权限和实现授权尚未形成；当前任务只允许 Specification。

## Impact（影响）

### Positive（正面影响）

- 科研责任明确归于人类，不由 Agent、DBOS 或 SAEE 吞并；
- AI Output、Evidence、Verification、Evaluation、Conclusion 和 Publication 成为不同 truth surface（事实表面）；
- 失败与负面结果得到历史保留要求；
- 评价路径和系统变化路径保持分离；
- 编码、检索和引用智能体可以稳定发现禁止项、人工 gate 和非执行状态。

### Costs and unresolved issues（代价与未决问题）

- Human Research Owner、Human Reviewer、必要独立性和利益冲突规则尚未任命或批准；
- 具体 Research Protocol adopter（采用方）和审批机制尚未定义；
- 任务集、Dataset、数据访问、隐私、伦理、Retention 和删除政策尚未选择；
- Evidence append-only、版本、hash、签名和存储机制尚未实现；
- Reproducibility、Evidence Completeness 和 SAEE 各维度的操作定义及阈值尚未批准；
- AI contribution disclosure（AI 贡献披露）、作者资格和不同发表渠道规则需要逐案确认；
- 异常升级、严重事件、暂停、撤销和 protocol deviation（协议偏离）记录仍需更细状态模型；
- Research Conclusion 与 SAEE Fitness 出现冲突时的解决流程尚未正式定义；
- DBOS–SAEE adapter、Evaluation algorithm 和 Runtime isolation 均未实现。

## Consequence Boundaries（后果边界）

```text
RESEARCH_AGENT_RESEARCH_PROTOCOL_DEFINED=true
HUMAN_SUPERVISED_GOVERNANCE_MODEL_SELECTED=true
RESEARCH_PROTOCOL_ADOPTED=false
HUMAN_RESEARCH_OWNER_ASSIGNED=false
HUMAN_REVIEWER_ASSIGNED=false
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
PUBLICATION_APPROVED=false
PAPER_SUBMITTED=false
EXTERNAL_RELEASE_EXECUTED=false
CODE_CHANGED=false
```

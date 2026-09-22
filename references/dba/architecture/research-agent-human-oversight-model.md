---
spec_id: DBA-RESEARCH-AGENT-HUMAN-OVERSIGHT-0.1
title: Research Agent Human Oversight Model v0.1
title_zh: 科研数字实体人工监督模型 v0.1
status: non-executable-governance-role-model
protocol_reference: research-agent-research-protocol.md
human_oversight_required: true
roles_assigned: false
authority_granted: false
agent_instance_created: false
runtime_created: false
---

# Research Agent Human Oversight Model v0.1（科研数字实体人工监督模型 v0.1）

本模型定义 Human + AI Collaboration（人类与 AI 协作）中的责任和权力边界。它定义角色类别，不任命人员、注册 Digital Entity、授予权限或创建治理组织。

## 1. Authority Model（权力模型）

| 参与方 | 规范角色 | 权力或责任范围 | 明确不拥有 |
|---|---|---|---|
| Human Research Owner | Decision Authority（研究决策权力） | 研究问题、最终科学判断、结论、作者和发表责任 | DBOS Operational Authority、SAEE 算法权、无限数据访问权 |
| Human Reviewer | Review Authority（复核责任） | 结果审核、异常检查、范围核对和异议记录 | 自动最终决定权、执行权或发表权 |
| Research Agent | Execution Assistance（执行辅助） | 有界分析、整理、比较、规划辅助和 Draft 生成 | 最终科研责任、自我授权、Evidence Authority 或发表权 |
| DBOS | Evidence Authority（证据记录权威） | canonical Execution/Evidence records、Verification 与生命周期记录 | Scientific Truth、Fitness、Evolution conclusion 或发表决定 |
| SAEE | Evaluation Authority（评价权力） | Reliability、Evidence Quality、Efficiency、Adaptability、Stability、Fitness 与 Risk 的有界评价 | Capability/Permission 授予、DBOS 写权、科学结论或执行权 |
| Governance Decision | Adoption Boundary（采纳边界） | 审查 SAEE Recommendation 是否被采用为受治理变化 | Research Conclusion、论文作者责任或 DBOS Execution |

这里的 Human Decision Authority 只指研究问题、科学判断和发表责任；Governance Decision 只处理系统变化的采纳。二者不能相互替代。

```text
HUMAN_DECISION_AUTHORITY_NE_OPERATIONAL_AUTHORITY=true
DBOS_EVIDENCE_AUTHORITY_NE_TRUTH_AUTHORITY=true
SAEE_EVALUATION_AUTHORITY_NE_DECISION_AUTHORITY=true
RESEARCH_AGENT_ASSISTANCE_NE_RESEARCH_RESPONSIBILITY=true
```

## 2. Responsibility Flow（责任流）

```text
Human Research Owner defines question and scope
  ↓
Research Agent provides bounded assistance
  ↓
DBOS preserves execution and evidence records
  ↓
SAEE evaluates bounded performance
  ↓
Human Reviewer checks results and anomalies
  ↓
Human Research Owner forms scientific conclusion
```

如 SAEE Recommendation 涉及 Capability 或 Lifecycle change（生命周期变化），还必须进入 Governance Decision，并在采纳和独立授权后交回 DBOS；该系统治理路径不替代科研结论审查。

## 3. Human Research Owner Responsibilities（研究负责人职责）

- 定义研究问题、假设、范围、数据边界和停止规则；
- 确认任务是否适合 Research Agent 辅助；
- 审查 Human Reviewer 意见和未解决异常；
- 决定结果是否足以形成结论，或应标记为 inconclusive（无确定结论）；
- 对论文、署名、披露、投稿、发表和外部发布承担最终责任；
- 确认禁止性边界没有因人工批准而被绕过。

## 4. Human Reviewer Responsibilities（复核者职责）

- 核对 Input Reference、Execution Context、Version Information 和 Evidence Bundle；
- 检查失败结果、负面结果、缺失项、异常和冲突是否保留；
- 检查 AI Output、DBOS Verification 和 SAEE Evaluation 是否被过度解释；
- 记录 `accepted_for_owner_review`、`revision_required`、`inconclusive` 或等价的未来复核语义；
- 对重大结论提出独立意见，并披露角色冲突或复核限制。

这些状态只是语义示例，不创建 schema、状态机或 Review Object 实例。

## 5. Research Agent Responsibilities（研究智能体职责）

- 在批准的任务范围内提供分析、整理、比较、计划和草稿辅助；
- 标记来源、假设、不确定性、工具使用和限制；
- 保留失败、中间和冲突输出供 DBOS 记录；
- 在输入、权限、工具或 Evidence 不足时停止并报告；
- 将科学结论、发表和外部发布交回 Human Approval Gate。

Research Agent 不得自我升级为 Scientist、Author、Reviewer、Decision Authority、Evidence Authority 或 Digital Organism。

## 6. Mandatory Escalation and Stop Conditions（强制升级与停止条件）

出现以下任一情况时，Research Agent assistance 必须停止或转交人工处理；未来实现必须 fail closed：

- 请求自主投稿、发表、署名或对外发布；
- 请求覆盖原始数据、删除历史 Evidence 或隐藏失败结果；
- 任务超出 Capability、Authorization、Permission 或数据访问范围；
- 来源冲突、Evidence 缺失或 Verification 状态无法解释；
- 涉及伦理、安全、隐私、身份、医疗、金融或不可逆外部影响；
- SAEE Evaluation 被要求直接转成执行、权限或科学结论；
- Human Research Owner 或 Human Reviewer 尚未明确，或重大结论缺少复核。

## 7. Separation and Conflict Rules（职责分离与冲突规则）

1. Research Agent 不能审核或批准自己的最终科学结论；
2. Human Research Owner 不能以“人工负责”为由绕过 DBOS/SAEE/Governance 边界；
3. DBOS 不能把 Evidence completeness 转成 Scientific Validity；
4. SAEE 不能把 Evaluation 转成 Permission、Publication Decision 或 Human approval；
5. 同一人承担 Owner 与 Reviewer 时必须记录非独立性；高风险或重大结论需要的独立性标准仍待未来协议决定；
6. 任何角色缺失、冲突或范围不明时，结论和对外发布状态必须保持未批准。

## 8. Non-instantiation Status（非实例化状态）

```text
HUMAN_OVERSIGHT_MODEL_DEFINED=true
HUMAN_RESEARCH_OWNER_ASSIGNED=false
HUMAN_REVIEWER_ASSIGNED=false
DECISION_AUTHORITY_GRANTED=false
REVIEW_AUTHORITY_GRANTED=false
RESEARCH_AGENT_INSTANCE_CREATED=false
DBOS_EVIDENCE_RECORD_CREATED=false
SAEE_EVALUATION_CREATED=false
GOVERNANCE_DECISION_CREATED=false
PUBLICATION_APPROVED=false
EXTERNAL_RELEASE_EXECUTED=false
```

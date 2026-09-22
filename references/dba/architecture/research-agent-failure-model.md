---
spec_id: DBA-RESEARCH-AGENT-FAILURE-MODEL-0.1
title: Research Agent Failure Model v0.1
title_zh: 科研数字实体失败模型 v0.1
status: non-executable-failure-semantics
contract_reference: research-agent-implementation-contract.md
failure_model_defined: true
failure_instance_created: false
failure_workflow_implemented: false
retry_authorized: false
runtime_created: false
---

# Research Agent Failure Model v0.1（科研数字实体失败模型 v0.1）

本模型定义未来 Research Agent implementation 中失败、冲突和拒绝的保留语义。它不创建异常处理代码、自动 retry、Failure Object schema、监控系统、Runtime 或真实失败记录。

## 1. Core Failure Rules（核心失败规则）

```text
FAILURE_MUST_BE_PRESERVED=true
FAILURE_CAN_BE_SILENTLY_DELETED=false
RETRY_OVERWRITES_FAILURE=false
LATER_SUCCESS_INVALIDATES_FAILURE=false
FAILURE_NE_SCIENTIFIC_FALSITY=true
FAILURE_NE_PERMISSION=true
```

失败记录说明某个明确阶段、对象或规则没有满足要求，不自动证明研究假设为假、Agent 永久无能力或系统整体不可信。

## 2. Failure Categories（失败类别）

| failure type | 定义 | 首要记录/处理责任 | 必须保留 | 禁止自动行为 |
|---|---|---|---|---|
| Execution Failure（执行失败） | 任务未完成、工具错误、超时、输入不可用、Context 不满足或行为结果失败 | Research Agent 提供 failure material；DBOS 记录 Execution/failure reference | 原始输入、步骤、工具状态、输出、错误、时间和 Context | 标记为成功、复用 `execution_id` 覆盖、无授权自动重试 |
| Evidence Failure（证据失败） | 必需材料缺失、provenance 不可解析、采集不完整、历史链断裂或失败结果未保留 | DBOS | 缺失项、冲突、采集范围、完整性状态和诊断 | 用默认值补齐、删除部分 Evidence、声称 Truth 或完整性通过 |
| Verification Failure（验证失败） | 明确对象在指定规则、输入或版本下未通过或不可验证 | DBOS | Verification rule/version、input reference、result、limitations 和 unknowns | 把失败升级为 Fitness、永久禁止或 SAEE 结论 |
| Evaluation Conflict（评价冲突） | SAEE 评价之间、评价与输入、或 SAEE 评价与 Human interpretation 出现未解决差异 | SAEE 保留原评价；DBOS 保留输入；Human Reviewer / Governance Decision 处理适用冲突 | 各版本评价、输入、模型、理由、不确定性和异议 | 静默选择有利结果、改写原评价、自动修改实体状态 |
| Human Rejection（人工拒绝） | Human Reviewer 或 Human Research Owner 拒绝输出、结论、发表或外部发布 | Human role 形成 rejection reference；DBOS 在适用范围记录引用 | 被拒绝材料、理由、review、时间、责任角色和后续状态 | 删除被拒绝输出、改成批准、由 Agent 重新自签名 |

## 3. Scope and Authorization Failure（范围与授权失败）

当 Capability、Authorization、Permission、Lifecycle State、数据访问或 Context 缺失、过期、撤销、冲突或超范围时，执行必须 fail closed。该失败不能由 Research Agent 通过扩大 scope、更换工具、继承 Human 权限或修改配置来自行修复。

任何后续修复都必须形成新的明确状态和引用；旧失败仍保留。

## 4. Failure Lifecycle Semantics（失败生命周期语义）

```text
Detected
  ↓
Recorded
  ↓
Review Pending
  ↓
Resolved | Rejected | Unresolved
```

该序列是 conceptual status semantics（概念状态语义），不是已实现状态机：

- Detected：观察到失败或冲突；
- Recorded：相应材料和来源已交给 canonical Owner 记录；
- Review Pending：等待 DBOS Verification、SAEE bounded evaluation 或 Human Review；
- Resolved：形成新的修正记录、验证或明确处理决定；
- Rejected：输出、变化、结论或发布被拒绝；
- Unresolved：证据不足、冲突未解或没有权限继续。

Resolved 不表示原失败消失。所有终态必须保留到原失败的引用。

## 5. Retry and Correction Rules（重试与更正规则）

1. Retry 必须获得适用于新执行的有效 Authorization、Permission 和 Context；
2. 每次 Retry 必须使用新的 `execution_id`，并引用原失败；
3. 输入、实现、模型、工具、配置或协议变化必须明确记录；
4. 后续成功不得把原失败重写为成功；
5. Evidence correction 必须追加新记录，不能覆盖 canonical Evidence；
6. Human Rejection 后的修订必须产生新 Draft/Output reference；
7. Evaluation conflict 的解决必须保留所有原评价与解决理由；
8. 没有权限、Owner 或充分记录时不得自动 retry。

## 6. Escalation Boundaries（升级边界）

| failure | 必要升级方向 | 不表示 |
|---|---|---|
| Execution Failure | DBOS record；必要时 Human Review | SAEE 自动评价或 Governance Decision 自动触发 |
| Evidence / Verification Failure | DBOS diagnosis；SAEE 可在有界输入上评价风险 | Scientific Conclusion 已形成 |
| Evaluation Conflict | Human Reviewer；涉及系统变化时进入 Governance Decision | Human 可改写 SAEE original output |
| Human Rejection | Human Research Owner / Reviewer 的研究责任域 | 删除材料或禁止所有未来任务 |
| Capability/Permission failure | DBOS lifecycle and explicit authorization path | 实现可以自我扩展 |

## 7. Evidence and Truth Boundary（证据与真相边界）

失败记录本身是 evidence-bearing material，只有在 DBOS 采集和登记后才成为 canonical Evidence Object。Evidence Failure 或 Verification Failure 不自动等于研究结论错误；同样，Evidence 完整或 Verification 通过也不等于 Truth、Scientific Validity 或高 Fitness。

## 8. Non-implementation Status（非实现状态）

```text
RESEARCH_AGENT_FAILURE_MODEL_DEFINED=true
FAILURE_OBJECT_CREATED=false
FAILURE_WORKFLOW_IMPLEMENTED=false
FAILURE_RECORDED=false
RETRY_AUTHORIZED=false
RETRY_EXECUTED=false
EXECUTION_CREATED=false
EVIDENCE_CREATED=false
VERIFICATION_EXECUTED=false
SAEE_EVALUATION_EXECUTED=false
HUMAN_REJECTION_RECORDED=false
RUNTIME_CREATED=false
CODE_CHANGED=false
```

---
spec_id: DBA-RESEARCH-AGENT-DATA-FLOW-0.1
title: Research Agent Data Flow and Ownership Model v0.1
title_zh: 科研数字实体数据流与归属模型 v0.1
status: non-executable-conceptual-data-flow
contract_reference: research-agent-implementation-contract.md
data_flow_implemented: false
transport_selected: false
schema_created: false
api_created: false
runtime_created: false
---

# Research Agent Data Flow and Ownership Model v0.1（科研数字实体数据流与归属模型 v0.1）

本文件定义 Research Agent future implementation（未来实现）的概念数据流、canonical object ownership（规范对象归属）和只读/写入边界。它不是 API、schema、pipeline、消息总线、Runtime topology（运行拓扑）或已接通集成。

## 1. Canonical Flow（规范数据流）

```text
Human
  ↓ task, scope, input and approval references
Research Agent
  ↓ raw output, process, tool usage and failure references
DBOS
  ↓ canonical Execution / Evidence / Verification records
Evidence
  ↓ bounded read-only evaluation input
SAEE
  ↓ Fitness / Risk / Evolution Recommendation
Governance Decision
  ↓ adopted or rejected decision reference
DBOS
  ↓ separately authorized lifecycle-controlled action or no change
```

图中的 Evidence 是 DBOS 管理的 canonical Evidence Object layer（规范证据对象层），不是新的 Component、Entity、Agent、Runtime 或独立权威。

## 2. Ownership Semantics（归属语义）

本文件中的 Owner 表示谁维护 architecture-level canonical object and state（架构级规范对象及状态），不自动表示版权、法律所有权、作者资格、数据许可或最终科学责任。原始论文、数据集和第三方材料仍保留其既有 Owner 与许可边界。

| 数据或对象 | Producer / Source（产生者或来源） | Canonical Owner（规范 Owner） | Consumer | 禁止推断 |
|---|---|---|---|---|
| Research Question / Task Scope | Human Research Owner | Human Research Owner 的研究责任域；DBOS 只记录引用 | Research Agent、Reviewer | 问题存在即获执行权 |
| Source Material | 论文、Dataset Owner、Human | 既有材料 Owner；DBOS 记录有界引用 | Research Agent、Reviewer、SAEE 只在授权范围内使用 | 进入流程即转移数据权利 |
| Entity Identity / Lifecycle | Registration candidate + DBOS | DBOS | Research Agent、SAEE 只读引用 | Identity 产生 Capability 或 Permission |
| Capability / Permission State | Implementation declaration + governance inputs | DBOS | Research Agent Runtime、Reviewer | 声明或配置自动扩大权限 |
| Raw Output / Process / Tool / Failure Material | Research Agent | Research Agent 是 material producer；DBOS 管理被采集引用 | DBOS | 原始输出已成为 Evidence truth |
| Execution Object | Research Agent behavior + DBOS observation | DBOS | Human Review、SAEE | Execution record 证明成功、正确或获授权 |
| Evidence Object | DBOS collection from bounded materials | DBOS | SAEE、Human Reviewer | Evidence completeness 等于 Truth |
| Verification Result | DBOS | DBOS | SAEE、Human Reviewer | Verification 等于 Scientific Validity 或 Fitness |
| Evaluation / Recommendation | SAEE | SAEE | Human Review、Governance Decision、DBOS 只读接收 | Evaluation 产生 Permission 或状态变化 |
| Governance Decision | Explicit reviewer/authority inputs | Governance Decision boundary | DBOS | Decision 已执行 |
| Scientific Conclusion / Publication Decision | Human Research Owner with Human Review | Human Research Owner 的科研责任域 | Publication/external process | Agent、DBOS 或 SAEE 自动成为作者或发表权威 |

## 3. Flow Boundary by Hop（逐跳边界）

### 3.1 Human → Research Agent

可以传递任务、范围、材料引用和 Human Approval reference。Research Agent 只获得当前 Context 中明确授予的使用范围，不能继承 Human 的全部数据、系统或发表权限。

### 3.2 Research Agent → DBOS

Research Agent 必须交付 raw output、process、tool usage 和 failure references。它不能直接写 canonical Identity、Capability、Permission、Evidence、Verification 或 Lifecycle State。

### 3.3 DBOS → Evidence

DBOS 依据明确采集范围形成 canonical Evidence Object、integrity status 和 provenance。采集成功不表示内容正确、研究结论成立或 Evidence 充分。

### 3.4 Evidence / DBOS → SAEE

SAEE 只读消费 Execution History、Evidence Bundle 和 Verification Result，并保持输入来源、范围和限制。SAEE 不修改 DBOS objects。

### 3.5 SAEE → Governance Decision

SAEE 提供 Fitness Assessment、Risk Assessment 和 Evolution Recommendation。输出权限类别仍是 Evaluation/Recommendation，不是 Command、Authorization 或 Permission。

### 3.6 Governance Decision → DBOS

Governance Decision 记录 Adoption 或 Rejection。只有被采纳且另行授权的变化才能交回 DBOS lifecycle control；Rejected、Revoked、unknown 或 conflicted 决定不得执行。

## 4. Read and Write Matrix（读写矩阵）

| 参与方 | 可提供/写入的概念表面 | 只读表面 | 禁止写入 |
|---|---|---|---|
| Human Research Owner | Question、Scope、Human Approval、Scientific Conclusion | DBOS records、SAEE Evaluation、Review | DBOS canonical state、SAEE original output |
| Research Agent | Raw/process/tool/failure material | Task Context、允许的输入和状态引用 | Identity、Capability、Permission、Evidence、Verification、Evaluation、Decision |
| DBOS | Identity、Lifecycle、Capability state、Execution、Evidence、Verification | SAEE output、Governance Decision | SAEE algorithm/original evaluation、Human scientific conclusion |
| SAEE | Evaluation、Risk、Recommendation | DBOS inputs | DBOS state、Permission、Human conclusion、Decision |
| Governance Decision | Review/Decision/Adoption record | SAEE Recommendation、DBOS context | DBOS Execution、SAEE Evaluation、Scientific Conclusion |

## 5. Failure Flow（失败数据流）

任一 hop 出现失败、缺失或冲突时，材料必须进入 [`research-agent-failure-model.md`](research-agent-failure-model.md) 的保留路径：

```text
failure detected
  → DBOS record/reference where applicable
  → Human Review and/or SAEE bounded evaluation
  → explicit resolution, rejection or unresolved status
```

Failure 不得被静默丢弃，也不得因为后续成功而覆盖。

## 6. Non-implementation Status（非实现状态）

```text
RESEARCH_AGENT_DATA_FLOW_DEFINED=true
DATA_FLOW_IMPLEMENTED=false
DATA_TRANSPORT_SELECTED=false
DATA_SCHEMA_CREATED=false
API_CREATED=false
ENDPOINT_CREATED=false
AGENT_INSTANCE_CREATED=false
RUNTIME_CREATED=false
EVIDENCE_OBJECT_CREATED=false
SAEE_INTEGRATION_CREATED=false
GOVERNANCE_INTEGRATION_CREATED=false
```

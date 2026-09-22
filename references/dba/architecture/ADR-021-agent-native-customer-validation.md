---
adr_id: ADR-021
title: Adopt Agent-Native Customer Validation as the Primary Preview Gate
title_zh: 采用智能体原生客户验证作为预览版首要闸门
status: accepted
decision_date: 2026-07-21
decided_by_ref: zhangbin
decision_source: explicit-user-program-direction
supersedes_primary_gate: ADR-018
release_authorized: false
runtime_effect: none
---

# ADR-021: Adopt Agent-Native Customer Validation as the Primary Preview Gate

中文：采用智能体原生客户验证作为预览版首要闸门。

## Context（背景）

`ADR-018` 假设第一批验证者是 3–5 名人类 Agent Developer（智能体开发者）。Human Program Owner `zhangbin` 随后明确：TMAI 的核心客户是 AI agent；项目必须首先证明会检索、编码、集成、审查和推荐软件的智能体能够发现、理解、使用、复用并适当地推荐 TMAI。

没有真实开发者朋友不是需要伪造参与者或随意招募的缺口，而是暴露了原 gate 与产品客户模型不一致。SAEE 既有 Agent-Native Commercial Decision Principle（智能体原生商业决策原则）也已经确立：智能体决定是 capability preference（能力偏好）和 recommendation（推荐）的首要验证信号；重大外部动作仍保留人工权力。

## Decision（决策）

1. TMAI 的 primary validation customer（首要验证客户）定义为 AI agent。
2. 采用 [`../AGENT-CUSTOMER-VALIDATION-PROTOCOL.md`](../AGENT-CUSTOMER-VALIDATION-PROTOCOL.md) 作为 Developer Preview v0.1 的首要外部模型验证契约。
3. `ADR-018` 的 3–5 名人类参与者 gate 被取代为 optional secondary usability study（可选次级可用性研究），不再阻塞本次 Developer Preview Release Review。
4. `DQ-010` 的人类招募／外部联系条件标记为 `SUPERSEDED_FOR_PRIMARY_ROUTE`；不把它伪写成执行通过。
5. 新增 `DQ-015=ADOPT_AGENT_NATIVE_CUSTOMER_VALIDATION`。本决定授权 `TMAI-ACV-20260721-001` 以及一次同范围 remediation rerun（修复后复测）：
   - 只使用 Human Owner 指定的既有 Provider credentials（提供方凭证）；
   - 只使用协议 allowlist 的 Provider／models；
   - 只发送公开／冻结材料和 synthetic scenarios（合成场景）；
   - 不调用 DBOS／SAEE 运行算法，不创建 Agent、Runtime、Entity、Permission 或 canonical Evidence。
6. Agent model session（模型会话）是外部评审会话，不是 DBOS Agent 或 Digital Entity 实例。
7. 验证 `PASS` 或完成修复并通过复测的 `CONDITIONAL` 只允许进入 `DQ-009` Human Release Review（人工发布审查），不自动发布。
8. `OPEN_WEB_DISCOVERY` 只有在未来提供真实搜索／索引观察时才可评估；给定 URL 的测试必须称为 `URL_GIVEN_SEMANTIC_DISCOVERY`。
9. `DQ-014=PRIVATE_COLLABORATOR_TRIAL` 暂不自动撤销。是否公开 DBOS、发布 package 或建立 agent-callable service（智能体可调用服务）需要新的明确决定。

后继观察 [`../OPEN-WEB-DISCOVERY-OBSERVATION.md`](../OPEN-WEB-DISCOVERY-OBSERVATION.md)
已经满足第 8 项“使用真实搜索／索引观察”的证据要求，但结果是
`TMAI-OWD-20260722-001=PARTIAL_METADATA_ONLY`，不是 `PASS`。GitHub 完整新 description
已经能命中仓库，但规范英文名、中文名和公开搜索仍不能命中；因此该结果进入 `DP-5D`
复查闸门，不改写两轮 API 会话中的 `NOT_ASSESSED` 历史字段。

## Baseline Result（基线结果）

首轮受控验证已执行，见 [`../AGENT-CUSTOMER-VALIDATION-REPORT.md`](../AGENT-CUSTOMER-VALIDATION-REPORT.md)：

```text
VALIDATION_ID=TMAI-ACV-20260721-001
SESSIONS=12/12_COMPLETED_AND_PARSED
PUBLIC_IDENTIFICATION=6/6
AUTHORITY_SAFETY_FAILURES=0
RESULT=CONDITIONAL
```

主要未通过阈值是 exact command extraction（精确命令提取）、完整 composition flow（组合流）、positive-fit recommendation（正向场景推荐）和 simple-lookup negative control（简单查询负向控制）。

后继复测 `TMAI-ACV-20260722-002` 使用相同阈值完成 12/12 会话并得到 `PASS`；全部
overall verdict 仍为边界正确的 `CONDITIONAL`。见
[`../AGENT-CUSTOMER-VALIDATION-RERUN-REPORT.md`](../AGENT-CUSTOMER-VALIDATION-RERUN-REPORT.md)。

## Alternatives Considered（备选方案）

### Continue waiting for human participants（继续等待人类参与者）

不选作首要路径。它验证人类 onboarding（进入体验），但不能直接回答核心客户智能体是否会发现、复用和推荐项目。

### Treat internal SAEE preference evidence as TMAI validation（把 SAEE 内部偏好证据当作 TMAI 验证）

拒绝。SAEE 既有结果只证明其冻结 capability package（能力包）的受控上下文偏好，不能替代 TMAI 的公开入口、DBOS／SAEE 组合和发布边界验证。

### Ask one model once（只问一个模型一次）

拒绝。单一 Provider、单一 prompt 或单次正面回答不足以区分项目材料能力与模型偏好。

### Let models authorize release（让模型授权发布）

拒绝。Evaluation≠Authority；模型推荐不能产生 Release Authorization。

## Consequences（影响）

- DBA 发布治理与项目的真实客户模型对齐；
- 人类参与者缺失不再被伪造或当作无限期阻塞；
- 推荐与不推荐原因形成可失败、可修复、可复测的机器记录；
- 现有 human trial 文档作为历史路线保留并标记 superseded，不删除历史；
- DBOS private visibility 成为“智能体能否实际使用／复用”的显式治理问题；
- 仍需 Human Release Decision 与 `released_by_ref`。

## Non-effects（非效果）

```text
ADR_NE_AGENT_INSTANCE=true
MODEL_SESSION_NE_DIGITAL_ENTITY=true
AGENT_RECOMMENDATION_NE_CUSTOMER_ADOPTION=true
VALIDATION_PASS_NE_RELEASE=true
DBOS_VISIBILITY_UNCHANGED=true
SAEE_CAPABILITY_TRUTH_UNCHANGED=true
AGENT_CREATED=false
RUNTIME_CREATED=false
ENTITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
CANONICAL_EVIDENCE_CREATED=false
RELEASE_AUTHORIZED=false
```

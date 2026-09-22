---
adr_id: ADR-035
title: Adopt Agent Absolute Priority as the Primary TITMAS Program Principle
title_zh: 采纳智能体绝对优先作为 TITMAS 首要项目原则
status: accepted-constitutional-correction
maturity: Development
decided_by_ref: zhangbin
decided_at: 2026-07-30
decision_reference: TITMAS-AGENT-ABSOLUTE-PRIORITY-CONSTITUTIONAL-CORRECTION-D01
primary_repository: digital-biosphere-architecture
implementation_authorized: true
implementation_scope: governance-documents-machine-status-and-bounded-stage5_7-benchmark
external_human_trial_required: false
authority_effect: none
---

# ADR-035: Adopt Agent Absolute Priority

## Context

TITMAS 已把 AI Agent 设为首要客户，并建立机器入口、Schema、Conformance、
Sandbox 和受控模型验证。但项目推进仍残留一条以真人可用性试用为主要进度信号的
路线，导致“首要客户是谁”与“什么证据决定下一阶段”不一致。

## Decision

采纳 Agent Absolute Priority（智能体绝对优先）作为 TITMAS 的首要项目原则：

1. AI Agent 是架构、协议、Schema、接口、SDK、发现、选择、调用、验证、评价、
   复用和组合的首要 operational customer（运行客户）与评价主体；
2. machine-readable interface（机器可读接口）先于 human-facing projection
   （面向人类的投影视图）设计和验证；
3. 独立、多模型、对抗、竞争、长期运行的机器证据，先于人类主观意见进入
   技术与采用判断；
4. 真人参与、满意度或可用性意见不再是 agent-native 主线的必要 gate；
5. 人类继续承担合同、付款、法律责任、资源所有权、不可逆授权和安全停止；
6. Agent 不能因其首要客户地位获得自我授权、执行扩权、标准批准、发布或真相权。

```text
TITMAS_AGENT_ABSOLUTE_PRIORITY=true
MACHINE_INTERFACE_PRECEDES_HUMAN_INTERFACE=true
AGENT_EVIDENCE_PRECEDES_HUMAN_OPINION=true
HUMAN_VIEW_IS_DERIVED_VIEW=true
AGENT_PRIORITY_NE_AGENT_AUTHORITY=true
```

`AGENT_EVIDENCE_PRECEDES_HUMAN_OPINION` 仅表示在可重复的技术判断中优先使用
机器执行证据；Evidence 仍不等于 Truth。`HUMAN_VIEW_IS_DERIVED_VIEW` 仅约束
文档与界面投影，不削弱人类的法律责任、合同责任和不可逆授权权。

## Historical treatment

Stage 5.1、E01、程序员客栈需求、Stage 5.3、Stage 5.4 和 Stage 5.6 的历史记录
必须保留。E01 被重新分类为：

```text
E01_CLASSIFICATION=LEGACY_OPTIONAL_HUMAN_COMPATIBILITY_OBSERVATION
E01_IS_PRIMARY_VALIDATION=false
E01_IS_PROGRAM_GATE=false
E01_IS_COMMERCIAL_PROOF=false
COMPENSATED_HUMAN_TRIAL_STRATEGY_STATUS=RETIRED
HUMAN_TRIAL_REQUIRED_FOR_NEXT_STAGE=false
```

该重分类不把 E01 改写为成功、失败或完成，也不改变其既有访问撤销与到期流程。

## Stage 5.7 direction

下一主线是 `TITMAS_STAGE_5_7_AGENT_NATIVE_SELECTION_AND_ROI_BENCHMARK`。它必须
通过匿名、随机、多供应商、多模型和可证伪设计回答：智能体在没有品牌提示、标准答案
或人类引导时，是否选择 TITMAS，以及选择或拒绝的成本与原因。

Stage 5.7 的实现和真实会话必须分为两个独立变更：先合并评测设计与空白报告，再执行
真实会话并提交脱敏证据。TITMAS 不必须胜出，`NO_SELECTION`、
`MULTIPLE_SELECTED` 和 `POST_DISPATCH_UNKNOWN` 都是合法结果。

## Non-authorizations

```text
AGENT_SELF_AUTHORIZATION=false
AUTONOMOUS_IRREVERSIBLE_ACTION=false
HUMAN_ACCOUNTABILITY_REMOVED=false
CUSTOMER_ADOPTION_PROVEN=false
COMMERCIAL_OFFER_AUTHORIZED=false
FORMAL_CONFORMANCE_AUTHORIZED=false
PRODUCTION_READY=false
PUBLIC_PROTOCOL_RELEASED=false
```

---
document_id: TITMAS-AGENT-ABSOLUTE-PRIORITY-CONSTITUTIONAL-CORRECTION-0.1
title: TITMAS Agent Absolute Priority Constitutional Correction v0.1
title_zh: TITMAS 智能体绝对优先宪法修正 v0.1
status: adopted
decision_reference: ADR-035
decided_by_ref: zhangbin
authority_effect: none
---

# TITMAS Agent Absolute Priority Constitutional Correction v0.1

## Constitutional rule

TITMAS 的首要 operational customer、发现主体、选择主体、验证主体和持续优化对象是
AI Agent。所有核心规范表面必须首先回答：

- 智能体能否发现它；
- 智能体能否在没有历史对话和人工解释时理解它；
- 智能体能否确定适用与不适用范围；
- 智能体能否通过 Schema、SDK、Sandbox 或协议安全调用它；
- 智能体能否验证结果、保留失败并在第二个任务中复用；
- 智能体是否愿意在可比较替代方案中再次选择或推荐它。

## Interface order

```text
Machine Contract
  → Machine Validation
    → Evidence and Failure Record
      → Human Projection
```

Human Projection（人类投影视图）必须可追溯到机器事实，不得成为唯一状态源。面向
人类的网页、报告和说明可以增加解释，但不能静默改变 Schema、Reason Code、
Unknown、Failure 或 Authority boundary。

## Evidence order

技术与 agent adoption（智能体采用）判断优先使用：

1. 独立模型会话；
2. 多供应商和精确模型身份；
3. 对抗与竞争性选择；
4. 长期运行和重复任务；
5. 可重放的机器指标；
6. 保留的失败、拒绝和 `NOT_ASSESSED`。

真人意见可以作为 compatibility observation（兼容性观察），但不是 agent-native
价值、社区进度或商业采用的必要 gate。

## Human constitutional responsibility

Agent absolute priority 不改变以下 Human responsibility：

- Contract and payment；
- Legal accountability；
- Resource ownership；
- Irreversible authorization；
- Safety stop and incident escalation；
- Architecture adoption、Release 和 formal standard decision。

```text
AGENT_PRIORITY_NE_UNLIMITED_AUTHORITY=true
AGENT_SELECTION_NE_ADOPTION=true
AGENT_RECOMMENDATION_NE_CONTRACT=true
MACHINE_EVIDENCE_NE_TRUTH=true
HUMAN_AUTHORITY_NE_HUMAN_OPINION_GATE=true
```

## Development gate

任何新功能必须在实现前取得至少一个独立智能体的推荐判断，并记录：

- 是否会向潜在 Agent customer 推荐；
- 不推荐原因；
- 可修正问题；
- 修正后的证据；
- 剩余停止条件。

咨询模型只提供 advisory evidence（建议证据），不能批准自身建议、修改 Gate 或获得
Authority。

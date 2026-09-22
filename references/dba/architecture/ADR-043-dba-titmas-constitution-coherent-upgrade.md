---
adr_id: ADR-043
title: DBA and TITMAS constitutional coherence for unified entry and DCell modules
title_zh: DBA与TITMAS统一入口和DCell模块宪法一致性
status: accepted
decision_id: DBA-TITMAS-CONSTITUTION-COHERENT-UPGRADE-v0.1
decided_by_ref: zhangbin
decision_source: human-directed-codex-goal
human_content_approval_recorded: true
human_final_decision_recorded: true
adoption_authorized: true
adoption_effect_trigger: canonical-main-merge-of-pr-142
authorized_content_head: 440d0163aea1577437a2a9c6737a37e0af47663a
candidate_branch_authority_effect: none
proposed_at: 2026-08-13
implementation_authorized: false
merge_authorized: true
release_or_deployment_authorized: false
---

# ADR-043: DBA and TITMAS Constitutional Coherence

## Context

DBA 已有组合式规模、动态注意力、执行上下文连续性和商业私有基础设施边界；TITMAS 已有
四产品、Observer 入口、Agent-first 与私有核心边界。DCell 相关叙事尚缺父子宪法继承、
模块最小契约、权限交集、组合重新评价和产品非扩张的统一机器表达。

若直接把“统一入口”实现为一个全局 Gateway，或把 DCell 当作自由激活的 Skill，会与
ADR-032、DBOS/SAEE 边界、Capability/Permission 分离及 C-01 四产品冻结冲突。

## Accepted decision

1. 以版本化修正案扩展，不改写历史宪法和已接受 ADR；
2. 建立父级原则机器契约、TITMAS 子级机器契约和 DCell 模块治理 Profile；
3. 将统一入口定义为逻辑机器契约，不定义全局强制或物理单一 Gateway；
4. 将执法保留为各规范 Owner 接入点的分布式有界行为；
5. 将 DCell 定义为 skill-like selection + cell-grade governance；
6. 保留 Gate、Receipt、Audit、Health 四产品，Observer 与 DCell 均不增加产品数；
7. 在 canonical merge 前保持候选分支 `authority_effect=NONE`；合并进入 canonical
   `main` 后，按照本 ADR 的 Human Decision 生效。

## Alternatives considered

### Directly edit the adopted constitutions

Rejected. 直接覆盖会破坏版本历史并模糊候选与已采纳事实。

### Build a global TITMAS controller

Rejected. 它会重复 Gateway、OPA/OPAL、Runtime 或 Agent framework 能力，并形成隐藏的
Authority aggregation。

### Treat DCell as a renamed skill

Rejected. 普通技能描述不足以表达 Permission intersection、Evidence、side effect、
lifecycle、composition accountability 和 change revalidation。

### Versioned parent-child contracts

Accepted. 该方案保持历史、所有权和产品边界，同时让 Agent 可以验证继承与冲突。

## Consequences

- 新 TITMAS / DCell 提案必须先证明父级一致性与复用审计；
- 模块组合变化必须重新核验，不允许自动继承 PASS；
- 统一入口的实现仍需未来单独授权和真实环境验证；
- 外部项目只能作为兼容或采纳候选，不能因本 ADR 自动成为依赖。

## Final adoption decision and canonical merge activation

Human Owner `zhangbin` 已完成最终内容审查并正式采纳本宪法方向。采纳内容绑定
`440d0163aea1577437a2a9c6737a37e0af47663a`；后续一次收口提交只允许记录本决定、
canonical merge 触发条件、测试和报告同步，不得改变实质原则。

采纳前要求的两项语义修正已经完成：

1. Permission（权限）必须是所有适用约束的交集；Human approval 只在策略、风险等级、
   行动类别或显式升级要求时适用，不能被写成每次行动的无条件约束；
2. 全球基础宪法不得硬编码 `zh-CN`；Human readback 必须使用显式 principal/market locale，
   中国市场 Profile 继续默认简体中文。

本 Human Decision 在候选分支上不产生规范 Authority。当本决定与对应修正案通过 PR #142
合并并可从 canonical `refs/heads/main` 到达时，采纳自动正式生效；不需要第二个合并后
采纳 PR。Human Owner 是 Authority，Git merge 只是已授权决定的生效条件，不是 Authority
来源。生效不授权 Runtime、DCell Library、统一入口、网站、部署、发布或生产运行。

```text
ADR_043_STATUS=ACCEPTED
HUMAN_DECISION_RECORDED=true
HUMAN_DECIDED_BY_REF=zhangbin
HUMAN_DECISION_SOURCE=HUMAN_DIRECTED_CODEX_GOAL
HUMAN_CONTENT_APPROVAL_RECORDED=true
HUMAN_FINAL_DECISION_RECORDED=true
CANDIDATE_APPROVED_BY_HUMAN=true
ADOPTION_AUTHORIZED=true
AUTHORIZED_CONTENT_HEAD=440d0163aea1577437a2a9c6737a37e0af47663a
ADOPTION_EFFECT_TRIGGER=CANONICAL_MAIN_MERGE_OF_PR_142
CANONICAL_REF=refs/heads/main
PRE_MERGE_AUTHORITY_EFFECT=PENDING_CANONICAL_MERGE
POST_MERGE_AUTHORITY_EFFECT=ADOPTED_AND_EFFECTIVE
CONSTITUTION_EFFECTIVE_WHEN_REACHABLE_FROM_CANONICAL_MAIN=true
IMPLEMENTATION_AUTHORIZED=false
MERGE_AUTHORIZED=true
RELEASE_AUTHORIZED=false
DEPLOYMENT_AUTHORIZED=false
```

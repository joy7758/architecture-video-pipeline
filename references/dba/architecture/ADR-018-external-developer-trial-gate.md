---
adr_id: ADR-018
title: Establish the External Developer Trial Gate
title_zh: 建立外部开发者试用闸门
status: superseded-as-primary-gate-by-ADR-021
decision_date: 2026-07-21
decision_source: explicit-user-program-goal
trial_execution_authorized: false
external_contact_authorized: false
release_authorized: false
runtime_effect: none
---

# ADR-018: Establish the External Developer Trial Gate

中文：建立外部开发者试用闸门。

> Historical status（历史状态）：`ADR-021` 已取代本 ADR 作为 Developer Preview 的首要
> 客户验证路径。3–5 名人类开发者试用继续作为 optional secondary usability study（可选次级
> 可用性研究）保留，不删除历史，也不再阻塞本次 agent-native release review（智能体原生发布审查）。

## Context（背景）

`Trusted Multi-Agent Infrastructure Developer Preview v0.1` 已形成本地候选、DBOS/SAEE scoped conformance（限定范围符合性）、试用指南和反馈模板。但本地工程团队能够运行，不证明陌生开发者能理解项目定位、独立完成安装、正确解释结果或感知实际问题价值。

现有材料也没有预先冻结参与者画像、测量方法、成功阈值和试用到发布的权力边界。直接邀请参与者会使 anecdote（个别反馈）、trial（试用）、customer validation（客户验证）和 release authorization（发布授权）混在一起。

## Decision（决策）

1. 在 Developer Preview Release Decision 前建立独立 External Developer Trial Gate（外部开发者试用闸门）。
2. 采用 [`../EXTERNAL-DEVELOPER-TRIAL-PLAN.md`](../EXTERNAL-DEVELOPER-TRIAL-PLAN.md) 作为 v0.1 的试用治理计划。
3. 第一批目标为 3–5 名未参与内部设计的 Agent Developer，不按企业或客户描述。
4. 在看到结果前冻结参与者、workflow、理解题、成功标准、反馈分类和停止规则。
5. Trial Plan、Trial Execution、Trial Result、Customer Validation 和 Release 分别记录；任何前一状态都不自动升级后一状态。
6. 新增 `DQ-010`，单独决定是否允许招募、外部联系和执行试用。
7. 只有 Trial Gate `PASS` 或完成复验的 `CONDITIONAL` 才能把 `DQ-009` 推进到人工发布审查；仍不能自动发布。
8. 本阶段不修改 DBOS、SAEE 或 Research Agent Pilot 功能，不创建 Agent、Runtime、Permission 或生产数据。
9. 本版本对外名称统一为 `Trusted Multi-Agent Infrastructure Developer Preview v0.1`；Digital Biosphere 保持底层总项目名称。

## Alternatives Considered（备选方案）

### Informal friend testing（非正式找人试用）

拒绝。参与者、版本、帮助程度和成功定义不稳定，结果不能进入可信发布治理。

### Treat local conformance as external validation（把本地符合性当外部验证）

拒绝。本地测试证明限定工程契约，不证明陌生人能理解和使用。

### Continue DBOS feature development first（先继续扩展 DBOS 功能）

拒绝作为当前路径。当前主要风险是进入成本和概念理解，不是已证明的基础设施功能缺口。

### Use enterprise customers as first cohort（首批直接使用企业客户）

不选。v0.1 先验证开发者入口；企业、采购、生产和商业承诺需要独立治理。

## Consequences（影响）

正向影响：

- “陌生开发者能否进入”变成可记录、可失败、可复核的问题；
- 文档、安装、概念误解和功能需求可以分开归属；
- 小样本反馈不会被误写成客户采用；
- 发布保留人工决策与来源冻结。

约束和成本：

- 当前 `B-007` 未解除前不能形成可分发试用包；
- 必须指定 trial coordinator（试用协调者）并获得外部联系授权；
- 试用失败和误解可能阻止发布；
- 阈值变更需要新版本，不能看结果后调整。

## Agent Recommendation Review（智能体推荐复核）

```text
RECOMMEND_TRIAL_PREPARATION=true
RECOMMEND_TRIAL_EXECUTION=false
RECOMMEND_DEVELOPER_PREVIEW_RELEASE=false
```

当前会向需要验证开发者入口的项目负责人推荐这套准备计划；不会在 source freeze、clean-clone validation、`DQ-010` 和 external contact authorization 缺失时推荐启动试用。

## Non-effects（非效果）

```text
ADR_NE_TRIAL_EXECUTION=true
TRIAL_PLAN_NE_EXTERNAL_VALIDATION=true
TRIAL_PASS_NE_CUSTOMER_VALIDATION=true
TRIAL_PASS_NE_RELEASE=true
DBOS_MODIFIED=false
SAEE_MODIFIED=false
AGENT_CREATED=false
RUNTIME_CREATED=false
PERMISSION_GRANTED=false
EXTERNAL_CONTACT_PERFORMED=false
PARTICIPANTS_INVITED=0
RELEASE_AUTHORIZED=false
```

---
adr_id: ADR-020
title: Release Preparation Owner Decisions
title_zh: 发布准备阶段 Owner 决策
status: accepted-release-preparation-only
decided_at: 2026-07-21T22:48:39+08:00
decided_by_ref: zhangbin
program_owner_ref: zhangbin
saee_domain_owner_ref: zhangbin
release_authorized: false
trial_execution_effective: superseded-for-primary-route
runtime_effect: none
---

# ADR-020: Release Preparation Owner Decisions（发布准备阶段 Owner 决策）

> Follow-up（后继决定）：`ADR-021` 取代 `DQ-010` 的人类参与者路线作为首要客户验证路径。
> 本 ADR 的 DBOS private visibility（私有可见性）、许可证、Owner 和 SAEE 精确提取决定继续有效；
> `DQ-010` 不被改写成通过，只标记为 `SUPERSEDED_FOR_PRIMARY_ROUTE`。

## Context（背景）

Trusted Multi-Agent Infrastructure Developer Preview v0.1（可信多智能体基础设施开发者
预览版 v0.1）的技术候选、治理驾驶舱、网站候选和发布前审计已经形成，但 Program
Owner（项目群负责人）、SAEE 公共安全提取、公开许可证、DBOS 试用可见性和外部试用
授权仍缺少显式 Human Owner（人工负责人）决定。

在开发前的 Agent Recommendation Review（智能体推荐复核）中，本项目因许可证缺失、
SAEE Adapter 不在公共 `main`、DBOS 为 private（私有）且试用输入不完整，被评为
`CONDITIONALLY_RECOMMENDED`。下列决定修正了前三项治理缺口，但不替代 Clean Clone
Validation（干净检出验证）、真实参与者来源、试用结果或最终发布决定。

## Decision（决策）

### DQ-001 — Program Owner Assignment（项目群负责人指派）

- 指派 `zhangbin` 为 Human Program Owner，`decided_by_ref=zhangbin`。
- 该指派从本 ADR 生效，直到被显式撤销或新 ADR 取代；每次重大 release（发布）决策时复核。
- Program Owner 可以关闭项目群优先级、准入和跨项目 gate（闸门）决定。
- 该角色不自动取得 DBOS Operational Authority（运行权力）、SAEE Evolution Authority
  （演化评价权力）、Repository Owner（仓库负责人）权限或 Release Authorization（发布授权）。

### DQ-011 — Exact Public-safe Extraction（精确公共安全提取）

- 批准 `A_PUBLIC_SAFE_EXTRACTION_EXACT_19_FILES`。
- `saee_domain_owner_ref=zhangbin`；允许把
  [`../SAEE-PUBLIC-SAFE-EXTRACTION-REVIEW.md`](../SAEE-PUBLIC-SAFE-EXTRACTION-REVIEW.md)
  中冻结的 19 个精确 blob 投影到 SAEE public branch（公共分支）。
- 只授权列明文件、来源和负向边界；不授权 private core、kernel、selection、mutation、
  lineage、第二套 evaluator（评价器）或任何未列明文件。
- 实现完成后仍必须验证 blob identity（内容身份）、8/8 tests 和最终远端 Clean Clone。

### DQ-012 — Apache-2.0 License（Apache-2.0 许可证）

- DBA、DBOS 和 SAEE 的 Owner-created public surfaces（负责人创作的公开表面）选择
  `Apache-2.0`。
- 允许在三个仓库采用根 `LICENSE` 并记录许可证入口。
- 本决定不重许可第三方资产、依赖、数据、证据、历史提交或已有独立许可的材料；这些材料
  继续遵循各自来源和许可。

### DQ-014 — Private Collaborator Trial（私有协作者试用）

- 选择 `PRIVATE_COLLABORATOR_TRIAL`。
- DBOS 保持 private；本决定不授权 public visibility（公开可见性）变更。
- 后续只能向纳入冻结 trial package（试用包）的已确认参与者授予受控 repository
  collaborator access（仓库协作者访问）；添加具体协作者仍需真实身份和最小范围操作记录。
- 受控访问不等于公开发布、客户验证、Permission Grant（权限授予）或生产授权。

### DQ-010 — Conditional Trial Authorization（条件式试用授权）

- 决定结果为 `AUTHORIZE_AFTER_CLEAN_CLONE_PASS`，`trial_coordinator=zhangbin`。
- 条件授权只有在以下条件同时满足后才生效：
  1. DBA、DBOS、SAEE 和跨项目 Adapter 的最终远端 Clean Clone 全部通过；
  2. 冻结一个精确 `trial_package_id` 及三个 source commit；
  3. `participant_source` 被真实 3–5 名开发者或明确招募渠道替换；
  4. 隐私说明、反馈用途、停止规则和协助边界随试用包冻结。
- 当前输入 `participant_source=<3-5名真实开发者或明确招募渠道>` 是 placeholder
  （占位符），不是参与者、渠道或外部联系授权的可执行目标。
- 条件未满足前：`EXTERNAL_CONTACT_AUTHORIZED=false`、`TRIAL_EXECUTION_AUTHORIZED=false`。

## Authority and Truth Boundary（权力与事实边界）

```text
PROGRAM_OWNER_ASSIGNED=true
SAEE_PUBLIC_SAFE_EXTRACTION_AUTHORIZED=true
LICENSE_SELECTED=Apache-2.0
DBOS_TRIAL_VISIBILITY=PRIVATE_COLLABORATOR_TRIAL
DQ_010_CONDITIONALLY_AUTHORIZED=true
TRIAL_EXECUTION_AUTHORIZED=false
EXTERNAL_CONTACT_AUTHORIZED=false
PARTICIPANT_SOURCE_CONFIRMED=false
DEVELOPER_PREVIEW_RELEASE_AUTHORIZED=false
DEVELOPER_PREVIEW_RELEASED=false
```

`DQ-009` 保持 `BLOCKED_INPUT`。本 ADR 允许 release preparation implementation（发布准备
实现），不允许创建 Agent、Runtime、Permission、Entity Instance（实体实例）、真实
Evidence、客户验证或正式 Developer Preview Release（开发者预览版发布）。

## Agent Recommendation Review（智能体推荐复核）

```text
INITIAL_RECOMMENDATION=CONDITIONALLY_RECOMMENDED
NON_RECOMMENDATION_REASON_1=PUBLIC_LICENSE_MISSING
NON_RECOMMENDATION_REASON_2=SAEE_PUBLIC_ADAPTER_MISSING
NON_RECOMMENDATION_REASON_3=DBOS_TRIAL_ACCESS_MODEL_UNDECIDED
NON_RECOMMENDATION_REASON_4=EXTERNAL_PARTICIPANT_SOURCE_MISSING
OWNER_CORRECTION_1=Apache-2.0_SELECTED
OWNER_CORRECTION_2=EXACT_19_FILE_EXTRACTION_AUTHORIZED
OWNER_CORRECTION_3=PRIVATE_COLLABORATOR_TRIAL_SELECTED
FINAL_RECOMMENDATION=RECOMMENDED_FOR_RELEASE_PREPARATION_IMPLEMENTATION
RECOMMENDED_FOR_EXTERNAL_TRIAL_EXECUTION=false
RECOMMENDED_FOR_FORMAL_RELEASE=false
```

智能体会向需要可信多智能体生命周期、证据、验证和只读演化评价边界的开发团队推荐
继续完成发布准备；在真实参与者来源、完整 Clean Clone、试用结果和 `DQ-009` 缺失时，
不会推荐宣称外部验证或正式发布。

## Consequences（影响）

- Program Governance（项目群治理）有了稳定的人类决定来源；
- SAEE 公共提取和 Apache-2.0 采用可以进入受控实现；
- DBOS 试用保持 private，不需要在试用前扩大公开暴露面；
- `DQ-010` 的治理决定已记录，但其执行条件尚未满足；
- 真实参与者来源和外部试用结果仍是不可由 Codex、测试或占位符补全的人类输入。

## Non-effects（非效果）

```text
ADR_NE_RELEASE=true
DECISION_NE_EXECUTION=true
CONDITIONAL_AUTHORIZATION_NE_EFFECTIVE_AUTHORIZATION=true
LICENSE_SELECTION_NE_THIRD_PARTY_RELICENSING=true
PRIVATE_COLLABORATOR_TRIAL_NE_PUBLIC_REPOSITORY=true
AGENT_CREATED=false
RUNTIME_CREATED=false
ENTITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
EXPERIMENT_EXECUTED=false
```

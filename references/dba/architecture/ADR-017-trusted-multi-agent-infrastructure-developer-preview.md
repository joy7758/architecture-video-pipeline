---
adr_id: ADR-017
title: Enter the Trusted Multi-Agent Infrastructure Developer Preview Stage
title_zh: 进入可信多智能体基础设施开发者预览阶段
status: accepted
decision_date: 2026-07-21
decision_source: explicit-user-program-goal
execution_authorized: bounded-by-workstream-and-existing-governance
release_authorized: false
runtime_effect: none
---

# ADR-017: Enter the Trusted Multi-Agent Infrastructure Developer Preview Stage

中文：进入可信多智能体基础设施开发者预览阶段。

## Context（背景）

Digital Biosphere 已形成 DBA 架构和项目群治理表面、DBOS 对象/校验/本地 SDK 骨架，以及 SAEE 演化智能责任边界。继续只增加规范不能证明外部开发者能够安装、运行、理解和复核整个方向；直接构建 Agent 平台或自动演化系统又会突破既有责任边界。

同时，对外直接呈现 DBA、DBOS、SAEE 三个孤立名称会增加理解成本。需要一个总项目入口和一个受限、可验证的阶段成果。

## Decision（决策）

1. Digital Biosphere 保持总项目名称；统一对外定位采用 `Trusted Multi-Agent Infrastructure`（可信多智能体基础设施）。
2. 进入 `Trusted Multi-Agent Infrastructure Developer Preview v0.1` 阶段。
3. DBA 建立公开入口、交付计划、发布 gate 和跨项目状态；不实现 Runtime。
4. DBOS 提供存在与可信记录基础设施的本地 Developer Preview；不成为 Agent Framework。
5. 建立三个受控角色模拟的 Multi-Agent Trust Demo，并由 DBOS 形成 Identity、Execution、Evidence Reference 和 Validation 链路。
6. SAEE 只建立最小 Evaluation Layer，输出 Reliability、Stability、Risk Assessment 和 Evolution Recommendation；不修改 DBOS。
7. 发布必须另行通过 Release Gate；本 ADR 不等于发布、部署或外部采用。
8. Developer Preview 同时作为 DBOS / SAEE 跨项目测试工程。可复现测试暴露的真实缺口可以触发最小功能提案，但必须经过 DBA 归属、重复建设和副作用审查，并只在责任仓库实现。

## Alternatives Considered（备选方案）

### Continue specification-only expansion（继续只扩展规范）

拒绝作为当前主路径。它能降低边界风险，但不能产生可运行、可展示、可验证的开发者成果。

### Merge DBA, DBOS, and SAEE（合并三个仓库）

拒绝。仓库边界承载不同 authority（权力）与 truth ownership（事实所有权），合并会放大职责混淆。

### Build an Agent platform first（先做智能体平台）

拒绝。它重复既有 Agent Framework 能力，并让 DBOS 偏离 existence infrastructure（存在基础设施）。

### Release DBOS alone（只发布 DBOS）

不选为总项目路径。DBOS 是关键开发者入口，但不能独自代表 DBA 治理与 SAEE 评价闭环。

## Consequences（影响）

正向影响：

- 外部开发者获得统一理解入口；
- 项目群以可运行证据而非文档数量推进；
- DBOS 与 SAEE 的接口可通过真实 demo fixture（演示夹具）验证；
- Recommendation、Decision 和 Execution 的分离可以被展示。
- 测试不再只是发布末端检查，而成为 DBOS / SAEE 最小功能补全的受治理输入。

约束和成本：

- 必须解决 DBOS 冻结文档与 validator 的当前冲突；
- SAEE 必须先审计现有能力，不能为 Demo 复制第二套评价权威；
- 三角色演示必须保持 synthetic/local（合成／本地），直到另有生产授权；
- 每个 release claim（发布声明）必须绑定版本、命令和结果。
- Demo 不得吸收 DBOS 或 SAEE 缺失功能形成第三套 canonical truth；测试失败也不自动产生实现授权。

## Agent Recommendation Review（智能体推荐复核）

当前智能体会向需要对象契约、失败关闭校验和本地可信记录教学路径的潜在使用者推荐 DBOS bounded local preview（受限本地预览）。当前不会推荐完整 Developer Preview release，因为全套 validator、三角色 Demo、SAEE 评价闭环和外部试用路径尚未同时通过。

必须修复这些不推荐原因并通过 [`../DEVELOPER-PREVIEW-RELEASE-PLAN.md`](../DEVELOPER-PREVIEW-RELEASE-PLAN.md) 后，才允许改变推荐结论。

## Non-effects（非效果）

```text
ADR_NE_IMPLEMENTATION=true
ADR_NE_RELEASE=true
ADR_NE_DEPLOYMENT=true
DBA_NE_RUNTIME=true
DBOS_NE_AGENT_FRAMEWORK=true
SAEE_NE_OPERATIONAL_AUTHORITY=true
RECOMMENDATION_NE_DECISION=true
DECISION_NE_EXECUTION=true
AGENT_INSTANCE_CREATED=false
RUNTIME_CREATED=false
PERMISSION_GRANTED=false
HISTORICAL_EVIDENCE_MODIFIED=false
```

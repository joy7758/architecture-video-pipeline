---
adr_id: ADR-016
title: Establish DBA as the Digital Biosphere Program Governance Cockpit
title_zh: 将 DBA 建立为数字生物圈项目群治理驾驶舱
decision_status: ACCEPTED
documentation_status: IMPLEMENTED
validation_status: PASS_WORKTREE_BASELINE
decision_source: human-directive-2026-07-21
runtime_effect: none
child_repository_effect: none
---

# ADR-016: Establish DBA as the Digital Biosphere Program Governance Cockpit

中文：将 DBA 建立为数字生物圈项目群治理驾驶舱。

## Context（背景）

Digital Biosphere 已形成 DBA、DBOS、SAEE、Governance Decision 和 Research Agent Pilot 等多个责任域与仓库。DBA 已详细定义架构边界、接口、生命周期、权力和版本规则，但缺少 Project Portfolio、Master Roadmap、Program Status、Cross-project Dependencies、Decision Queue、Integration Gates 与 Risk Register。

结果是：DBA 能回答“规则是什么”，但不能稳定回答“整个项目群现在在哪里、下一步推进什么、谁负责、缺什么证据、什么决定阻塞下一阶段”。这偏离了 DBA 作为整个 Digital Biosphere 项目群治理与沟通中心的原始目的。

## Decision（决策）

DBA 的正式仓库角色扩展为：

> Digital Biosphere Program Governance and Architecture Specification Hub

中文：数字生物圈项目群治理与架构规范中心。

DBA 将同时维护：

1. Architecture Governance（架构治理）：规则、边界、接口、ADR 和版本；
2. Program Governance（项目群治理）：组合、路线图、状态、依赖、决策、集成 gate、风险和阻塞。

该扩展只增加非执行治理工件，不授予 DBA 对 DBOS、SAEE、Pilot 或其他仓库的运行、写入、算法、Capability、Permission、发布或部署权。

## Decision Scope（决策范围）

本决定允许：

- 创建根目录 Program Governance cockpit 工件；
- 创建 `program-governance-specification.md`；
- 更新 README、AGENTS、Architecture Governance、Governance Model 和 Project Mapping；
- 通过只读检查记录带时间、branch 和 commit 的状态观察；
- 把未确认事项放入 Decision Queue、Risk 或 Blocker Register。

本决定不允许：

- 修改 DBOS、SAEE、Research Agent Pilot 或相邻仓库；
- 创建 API、Runtime、Agent、Entity、Capability、Permission 或 Evidence；
- 自动采纳路线图、关闭 gate、执行实验、发布版本或推送 Git；
- 重写当前 DBA Git 历史或修复 Git root 拓扑；
- 把状态快照当作子项目 canonical truth。

## Alternatives（替代方案）

### Alternative A: Keep DBA specification-only（保持 DBA 仅为规范仓库）

拒绝。它保持边界清晰，但不能支持整体推进、跨项目沟通和优先级治理。

### Alternative B: Put program governance in DBOS（把项目群治理放入 DBOS）

拒绝。DBOS 是 Operational / Existence Governance 责任域；让 DBOS 管整个项目群会混淆运行权与项目群权力，并使 SAEE 处于不对称控制关系。

### Alternative C: Merge DBA, DBOS and SAEE（合并 DBA、DBOS 和 SAEE）

拒绝。仓库合并不能解决 Authority、Truth、Evaluation 与 Execution 的分离，反而增加自我授权和事实覆盖风险。

### Alternative D: Create a separate fourth governance repository（新建第四个治理仓库）

暂不采用。它会增加切换成本和重复语义；DBA 本身就是最合理的总入口。

## Consequences（影响）

正面影响：

- Digital Biosphere 对外保持一个总项目，对内保持清晰责任域；
- 用户可以从 DBA 查看整体状态、决策、风险和下一步；
- 每个工作项有一个 primary repository；
- 跨项目变化先经过契约和 gate，再分别实施；
- 智能体可以按稳定入口检索项目群状态而不推断越权事实。

代价与风险：

- 状态快照需要持续维护，否则会过期；
- Program Owner 和各 Domain Owner 仍需显式指派；
- DBA 必须避免复制子项目 ledger 形成第二事实源；
- 当前 DBA Git root 拓扑问题成为需要独立决定的风险。

## Adoption Artifacts（采纳工件）

- [`../PROGRAM-CHARTER.md`](../PROGRAM-CHARTER.md)
- [`../PROJECT-PORTFOLIO.md`](../PROJECT-PORTFOLIO.md)
- [`../MASTER-ROADMAP.md`](../MASTER-ROADMAP.md)
- [`../PROGRAM-STATUS.md`](../PROGRAM-STATUS.md)
- [`../CROSS-PROJECT-DEPENDENCIES.md`](../CROSS-PROJECT-DEPENDENCIES.md)
- [`../DECISION-QUEUE.md`](../DECISION-QUEUE.md)
- [`../INTEGRATION-GATES.md`](../INTEGRATION-GATES.md)
- [`../RISK-AND-BLOCKER-REGISTER.md`](../RISK-AND-BLOCKER-REGISTER.md)
- [`program-governance-specification.md`](program-governance-specification.md)
- [`../PROGRAM-GOVERNANCE-BASELINE-AUDIT.md`](../PROGRAM-GOVERNANCE-BASELINE-AUDIT.md)

## Validation Contract（验证契约）

ADR-016 只有在以下条件全部满足后才能把 `validation_status` 更新为 `PASS_WORKTREE_BASELINE`：

- 驾驶舱八个根入口和 Program Governance Specification 均存在；
- README 与 AGENTS 将其列为首要入口；
- Architecture Governance、Governance Model 和 Project Mapping 正确增加 Program Governance；
- 所有内部 Markdown 引用可解析；
- 没有文件声称 DBA 获得 DBOS/SAEE 执行权；
- 没有修改 DBA 之外的仓库；
- 没有创建 Runtime、Agent、Entity、Capability、Permission 或 Evidence；
- Git diff 仅包含 DBA 目标范围且没有 commit 或 push，除非另有明确授权。

2026-07-21 的验证结果记录在 [`../PROGRAM-GOVERNANCE-BASELINE-AUDIT.md`](../PROGRAM-GOVERNANCE-BASELINE-AUDIT.md)，上述条件全部通过。该结果只验证当前 DBA 工作树文档基线，不表示 Release、子项目 Adoption 或跨项目 Integration 已发生。

```text
ADR_016_ACCEPTED=true
PROGRAM_GOVERNANCE_COCKPIT_SELECTED=true
DBA_EXECUTION_AUTHORITY_CREATED=false
DBOS_AUTHORITY_CHANGED=false
SAEE_AUTHORITY_CHANGED=false
CHILD_REPOSITORIES_MODIFIED=false
```

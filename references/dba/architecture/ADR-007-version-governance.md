---
adr_id: ADR-007
title: Establish Architecture Version and Release Governance
title_zh: 建立架构版本与发布治理
status: accepted-for-architecture-specification-v0.1
decision_scope: architecture-version-release-compatibility-and-history-only
implementation_status: not-authorized
release_effect: none
adoption_effect: none
runtime_effect: none
entity_effect: none
capability_effect: none
permission_effect: none
---

# ADR-007: Establish Architecture Version and Release Governance（建立架构版本与发布治理）

## Problem（问题）

Architecture Governance、Architecture Change Process 和 ADR 已经规定架构如何提出、审查、接受与更新，但没有正式回答：

- Architecture、Interface、Data Contract 与 Lifecycle Model 如何独立版本化；
- 已接受规范如何形成 Current Release；
- 版本何时冻结，发布后能否原地修改；
- Backward/Forward Compatibility 如何声明；
- Breaking Change 何时需要 Major Version 和 Migration Requirement；
- Release 如何与 Adoption、Implementation 和 Deployment 分离；
- Deprecated 与 Archived 版本如何保留历史。

缺少版本治理时，文档版本可能被误报为代码实现，Release 可能被误报为 Deployment，后继版本可能静默删除旧语义，或者 DBOS/SAEE 被自动升级到未采用的规范。

## Decision（决策）

建立独立 Version and Release Governance（版本与发布治理）：

1. 定义 Architecture、Interface、Data Contract 和 Lifecycle Model 四类版本；
2. 版本生命周期为 Draft → Reviewed → Accepted → Current → Deprecated → Archived；
3. Review Freeze 与 Release Freeze 阻止已审查或已发布内容被静默改写；
4. 每个非编辑性版本必须声明 Backward Compatibility、Forward Compatibility、Breaking Change 和 Migration Requirement；
5. Breaking Change 必须使用 Major Version、ADR 和显式 Architecture Decision；
6. 发布遵循 Release Proposal → Review → Decision → Release → Adoption；
7. Release ≠ Deployment，Release ≠ Adoption，Adoption ≠ Implementation；
8. Adoption 必须由每个采用方通过显式 Decision 记录；
9. Deprecated ≠ Deleted，历史 Version、Release、ADR 和 Adoption 引用必须保留；
10. 本 ADR 不创建版本服务、Release、Adoption、实现、部署或 Runtime 状态。

```text
Version = normative specification state
Release = published normative record
Adoption = explicit scoped governance choice
Implementation = separately evidenced software state
Deployment = separately authorized operational state
```

## Alternatives（替代方案）

### A. 用 Git commit、tag 或目录名代替版本治理

拒绝。存储标识不能表达审查、接受、兼容、废弃、采用和权力来源；本规范也不选择具体发布载体。

### B. 将 Architecture Version 与 Runtime Version 绑定

拒绝。规范变化会被错误升级为运行变化，并绕过 DBOS 生命周期与独立部署授权。

### C. 发布后自动采用

拒绝。Release 只形成规范记录；不同项目、系统和治理范围必须独立决定是否采用。

### D. 默认 Minor Version 向后兼容

拒绝。特别是 `v0.x` 阶段，数字号不能替代逐项 Compatibility Declaration。

### E. 用删除处理 Deprecated Version

拒绝。删除会破坏 ADR、Decision、Evidence、Adoption 和历史解释链。

### F. 允许 Maintainer 同时提出、批准和发布

拒绝。维护职责不自动成为 Architecture Decision Authority；实际职责分离规则仍需治理制度定义。

## Impact（影响）

### Positive（正面影响）

- Version、Release、Adoption、Implementation 和 Deployment 获得独立状态；
- 四类规范可以独立演进并通过 manifest 明确组合；
- 兼容与迁移从隐含假设变成显式审查对象；
- Current、Deprecated 和 Archived 具有可追溯状态；
- 发布内容冻结，历史版本不被静默覆盖；
- 编码、检索和引用智能体能够避免把规范发布误报为 Runtime 升级。

### Costs and unresolved issues（代价与未决问题）

- 实际 Version Authority、Release Publisher、Adopter 和 quorum 尚未指定；
- Version/Release/Adoption Record 的序列化格式和存储位置尚未定义；
- 版本完整性是否使用 hash、签名、Git tag、archive 或其他机制尚未选择；
- 多个 compatibility line 是否允许同时标为 Current，需要按 scope 制定更精确规则；
- Adoption registry（采用登记表）及 adopter 通知机制尚未定义；
- Deprecated 到 Archived 的时间、支持窗口和退出条件尚未统一；
- Architecture Change Record、Version Record、Release Record 与 Governance Decision Object 的共同标识和引用规则尚未定义；
- 当前规范与既有 public meaning layer 的 canonical release 关系仍需人工对齐；
- ADR 目录不统一且 `ADR-005` 缺失的问题仍未解决。

## Consequence boundaries（后果边界）

```text
VERSION_GOVERNANCE_DEFINED=true
VERSION_AUTHORITY_ASSIGNED=false
ARCHITECTURE_RELEASE_CREATED=false
VERSION_ADOPTION_RECORDED=false
IMPLEMENTATION_CHANGED=false
DEPLOYMENT_CHANGED=false
RUNTIME_VERSION_CHANGED=false
HISTORICAL_VERSION_DELETED=false
API_CREATED=false
AGENT_CREATED=false
RUNTIME_CREATED=false
ENTITY_CREATED=false
CODE_CHANGED=false
```

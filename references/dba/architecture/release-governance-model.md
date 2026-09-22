---
spec_id: DBA-RELEASE-GOVERNANCE-MODEL-0.1
title: Digital Biosphere Architecture Release Governance Model v0.1
title_zh: 数字生物圈架构发布治理模型 v0.1
status: non-executable-release-governance-specification
release_created: false
deployment_created: false
adoption_created: false
release_authority_assigned: false
runtime_effect: none
implementation_effect: none
---

# Digital Biosphere Architecture Release Governance Model v0.1

本模型定义已接受的 Architecture Version 如何形成可引用的规范发布，并由采用方通过独立决定选择采用。Release（发布）是规范状态与记录，不是软件 Deployment（部署）。

## 1. 核心不变量

```text
RELEASE_NE_DEPLOYMENT=true
RELEASE_NE_IMPLEMENTATION=true
RELEASE_DECISION_NE_RELEASE=true
RELEASE_NE_ADOPTION=true
ADOPTION_NE_DEPLOYMENT=true
ADOPTION_REQUIRES_EXPLICIT_DECISION=true
```

## 2. Release Lifecycle（发布生命周期）

```text
Release Proposal
       ↓
Review
       ↓
Decision
  ↙          ↘
Rejected     Approved
                  ↓
               Release
                  ↓
               Adoption
```

| 阶段 | 最小记录 | 状态边界 |
|---|---|---|
| Release Proposal（发布提案） | Accepted Version、冻结内容、scope、清单、兼容声明、ADR 与变更引用 | 提案不表示批准、发布或采用 |
| Review（审查） | 内容一致性、版本组合、兼容性、废弃影响、非实现声明和历史保留检查 | Review 不等于 Decision |
| Decision（决策） | approved、rejected 或 deferred，以及明确 decision source | Approved 不等于 Release |
| Release（发布） | Release Record、发布清单、稳定引用、时间和 Current scope | Release 不等于 Deployment、Implementation 或 Adoption |
| Adoption（采用） | 每个采用方独立的 Adoption Decision、scope 和版本引用 | Adoption 不等于代码升级、迁移完成或部署 |

Rejected Release Proposal 必须保留；若重新发布，应创建新的候选记录，不得改写旧决定。

## 3. Release Proposal（发布提案）

Release Proposal 至少包含：

| 字段 | 语义 |
|---|---|
| `release_proposal_id` | 发布提案的稳定引用 |
| `version_ref` | 必须指向 Accepted Version |
| `release_scope` | 发布覆盖的规范范围和 compatibility line |
| `manifest` | Architecture、Interface、Data Contract、Lifecycle Model Version 的组合 |
| `frozen_content_refs` | 供审查和决定的稳定内容引用 |
| `change_refs` / `adr_refs` | 变更与重大决策来源 |
| `compatibility_declaration` | Backward、Forward、Breaking 和 Migration 状态 |
| `deprecation_actions` | 本发布计划废弃的旧版本；没有时显式为 none |
| `limitations` | 未实现、未知、未采用和未部署状态 |

Release Proposal 不创建 tag、GitHub Release、archive、DOI、软件包或部署动作。

## 4. Review（发布审查）

Architecture Reviewer 必须检查：

1. Version 已处于 Accepted，且内容与接受范围一致；
2. Release Manifest 中每个版本引用可解析；
3. 兼容性和 Migration Requirement 已显式声明；
4. Breaking Change 已有 ADR 和 Major Version；
5. Deprecated 版本不会被删除或静默改写；
6. Release 文案没有声称 Implementation、Deployment、Runtime support 或 Adoption；
7. Architecture Authority、Operational Authority 与 Evolution Authority 仍保持分离；
8. Review Freeze 后没有未重新审查的语义变化。

受影响的 DBOS/SAEE Domain Owner 可以提供领域意见，但不能单方面批准或拒绝 Architecture Release。

## 5. Decision（发布决策）

Release Decision 必须引用：

- 被审查的固定 Release Proposal；
- decision result、scope、理由和 `decided_by_ref`；
- 未决问题、条件和废弃影响；
- 是否允许 Maintainer 执行 Release 记录动作。

`approved` 只允许进入 Release，不证明 Release 已发生。v0.1 不指定实际 Architecture Decision Authority。

## 6. Release（规范发布）

Release 由明确指定的 Architecture Maintainer 或 release publisher 在 Approved Decision 范围内记录。Release Record 至少包含：

| 字段 | 语义 |
|---|---|
| `release_id` | 发布记录稳定引用 |
| `release_version_ref` | 已发布 Version Record |
| `release_manifest` | 冻结的版本组合与规范引用 |
| `decision_ref` | Approved Release Decision |
| `released_at` | 规范发布时间，不是部署时间 |
| `current_scope` | 此发布成为 Current 的明确范围 |
| `supersedes_release` | 被替代发布；没有时显式为空 |
| `deprecation_refs` | 与本发布关联的废弃记录 |
| `implementation_status` | 默认 `not_assessed` 或 `not_implemented`，不能由发布推断 |
| `deployment_status` | 默认 `not_assessed`；架构发布不能改写 |
| `adoption_refs` | 采用后追加引用；发布时可以为空 |

本模型不指定发布载体、tag、archive、签名或 URL。Current Version 必须有 Release Record，但 Release Record 不创建 Runtime Version。

## 7. Release Freeze（发布冻结）

- Release Decision 必须指向冻结候选；
- Release 后的 manifest 和规范内容不可原地修改；
- 非语义勘误必须追加 Errata 引用；
- 语义修正必须创建新 Version 和 Release；
- 发布错误不能通过删除 Release 解决，应使用 Deprecated、Superseded 或 Errata 记录；
- Archived Release 继续保持稳定引用。

## 8. Adoption（版本采用）

Adoption 是采用方对某个 Release 的 scoped normative choice（有范围规范选择），不是系统升级。每个 Adoption Record 至少包含：

| 字段 | 语义 |
|---|---|
| `adoption_id` | 采用记录稳定引用 |
| `adopter_ref` | 采用主体或治理边界的明确引用 |
| `release_ref` / `version_ref` | 被采用的发布和版本 |
| `scope` | 采用覆盖的规范、项目或治理活动 |
| `decision_ref` | 显式 Adoption Decision |
| `compatibility_and_migration` | 兼容条件与迁移要求 |
| `effective_normative_date` | 规范采用生效时间，不是部署时间 |
| `supersedes_adoption` | 被替代的采用记录 |
| `implementation_status` | 独立状态，默认 unknown/not_assessed |
| `deployment_status` | 独立状态，默认 unknown/not_assessed |

Release publisher、Architecture Maintainer、DBOS 或 SAEE 都不能通过发布动作替采用方作出 Adoption Decision。采用方是否实现、迁移或部署需要新的授权和证据。

## 9. Failed, Superseded and Deprecated Release

- Approved 但未 Release：保留 Decision，不声称发布完成；
- Release 后发现问题：形成 Errata、Deprecation Proposal 或新 Release，不删除原记录；
- Superseded：表示存在后继 Release，不自动等于 Deprecated；
- Deprecated：需要独立废弃决定，不终止既有 Adoption；
- Adoption rollback（采用回退）：需要新 Adoption Decision，不能重写原采用记录；
- Archived：保留 Release、Version、ADR、Compatibility 和 Adoption 引用。

## 10. Agent-readable release status（智能体可读发布状态）

```text
RELEASE_PROPOSAL_CREATED=false
RELEASE_REVIEWED=false
RELEASE_APPROVED=false
ARCHITECTURE_RELEASE_CREATED=false
VERSION_CURRENT_RECORDED=false
VERSION_ADOPTION_RECORDED=false
IMPLEMENTATION_CHANGED=false
DEPLOYMENT_CHANGED=false
RUNTIME_VERSION_CHANGED=false
```

以上是本规范自身的非执行状态，不是未来 Release Record 的固定值域。

## 11. 非实现边界

本模型不创建 Release Service、API、Registry、签名系统、Git tag、GitHub Release、Runtime、Agent、Entity 或部署流程。

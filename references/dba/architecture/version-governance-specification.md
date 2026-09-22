---
spec_id: DBA-VERSION-GOVERNANCE-0.1
title: Digital Biosphere Architecture Version Governance Specification v0.1
title_zh: 数字生物圈架构版本治理规范 v0.1
status: non-executable-version-governance-specification
version_authority_assigned: false
release_created: false
adoption_created: false
implementation_effect: none
runtime_effect: none
entity_effect: none
permission_effect: none
---

# Digital Biosphere Architecture Version Governance Specification v0.1

本规范定义 Digital Biosphere Architecture（数字生物圈架构）如何标识、审查、接受、发布、冻结、废弃和归档规范版本。它治理的是 normative specification state（规范状态），不是代码、Runtime、部署或运行采用状态。

## 1. 核心不变量

```text
VERSION_NE_IMPLEMENTATION=true
ARCHITECTURE_VERSION_NE_RUNTIME_VERSION=true
RELEASE_NE_DEPLOYMENT=true
ADOPTION_REQUIRES_EXPLICIT_DECISION=true
BACKWARD_COMPATIBILITY_MUST_BE_DECLARED=true
DEPRECATED_NE_DELETED=true
VERSION_NUMBER_GRANTS_AUTHORITY=false
```

1. Version ≠ Implementation：版本号表示规范状态，不证明代码已支持、接口已实现或能力已存在。
2. Architecture Version ≠ Runtime Version：架构版本变化不自动改变 DBOS、SAEE、Digital Entity 或 Runtime 状态。
3. Adoption requires explicit decision：发布版本不自动被任何系统、项目或治理域采用。
4. Backward Compatibility must be declared：没有明确兼容声明时，兼容状态必须保持 `unknown`。
5. Deprecated ≠ Deleted：废弃版本继续保留其内容、状态、来源、决策和替代关系。

## 2. Version Types（版本类型）

不同版本类型独立编号。一个类型变化不自动提升其他类型；Architecture Release Manifest（架构发布清单）必须声明一次发布包含的具体版本组合。

| 版本类型 | 规范对象 | 最小范围 | 不表示 |
|---|---|---|---|
| Architecture Version（架构版本） | Digital Biosphere Stack 的总体规则、层级、权力和治理基线 | 被纳入基线的规范文件及 ADR 集合 | DBOS/SAEE 实现或部署采用了该基线 |
| Interface Version（接口版本） | SAEE ↔ DBOS 的字段、方向、状态和权限边界 | 指定接口 profile（接口配置） | API、endpoint 或 runtime handshake 已存在 |
| Data Contract Version（数据契约版本） | Entity、Execution、Evidence、Evaluation、Recommendation、Decision 等对象语义与 Owner | 指定对象集合和字段语义 | schema 已序列化或数据库已迁移 |
| Lifecycle Model Version（生命周期模型版本） | Entity、Decision 及其他已规范生命周期的状态与转换 | 指定状态机、转换 gate 和 Owner | Runtime 状态已迁移或实例已改变 |

### 2.1 组合规则

- Architecture Version 可以引用一个或多个 Interface、Data Contract 和 Lifecycle Model Version；
- 引用表示规范依赖，不表示实现依赖已经满足；
- 每个引用必须保留版本类型、版本号、范围和兼容性状态；
- 若组合中存在 `unknown` 或 `incompatible`，Release Proposal 必须显式记录限制，不能默认兼容；
- 同一版本类型可以存在多个 compatibility line（兼容线），但 `Current` 必须声明 scope（范围），不得声称无范围的“全局最新”。

## 3. Version Identifier（版本标识）

规范版本采用 `vMAJOR.MINOR[.PATCH]`：

- Major（主版本）：改变架构边界、Owner、权力、不变量或其他 breaking semantics（破坏性语义）；
- Minor（次版本）：增加经声明向后兼容的规范内容；
- Patch（修订版本）：只修正文案、链接、格式或不改变语义的错误。

`v0.x` 属于早期规范阶段，版本号本身不提供兼容保证。每次变更仍必须提供 Compatibility Declaration（兼容声明）。Draft、Reviewed、Accepted 等是版本状态，不应通过在版本号中隐藏状态来替代治理记录。

## 4. Version Record（版本记录）

每个版本至少应具有以下可追溯语义：

| 字段 | 语义 |
|---|---|
| `version_id` | 版本记录的稳定引用 |
| `version_type` | architecture、interface、data_contract 或 lifecycle_model |
| `version_number` | `vMAJOR.MINOR[.PATCH]` 标识 |
| `scope` | 该版本覆盖的规范对象和边界 |
| `status` | Draft、Reviewed、Accepted、Current、Deprecated 或 Archived |
| `included_spec_refs` | 被该版本包含或引用的规范 |
| `change_refs` | 对 Architecture Change Record 的引用 |
| `adr_refs` | 支持重大选择的 ADR 引用 |
| `compatibility_declaration` | 向后、向前、破坏性和迁移状态 |
| `supersedes` | 被本版本替代的版本引用；未知时保持空或 unknown |
| `release_ref` | Release 后对应的 Release Record；此前为空 |
| `deprecated_by` | 废弃决定或后继版本引用；未废弃时为空 |
| `authority_refs` | 提案、审查、批准、废弃或归档的明确记录来源 |
| `limitations` | 不确定性、未覆盖范围和非实现声明 |

该记录是 conceptual data contract（概念数据契约），不定义 API、文件格式、数据库或自动版本服务。

## 5. Version Lifecycle（版本生命周期）

```text
Draft
  ↓
Reviewed
  ↓
Accepted
  ↓
Current
  ↓
Deprecated
  ↓
Archived

Side states:
Rejected
Withdrawn
Superseded-before-release
```

| 状态 | 最小条件 | 规范效力 | 不表示 |
|---|---|---|---|
| Draft（草案） | 已有版本提案、范围和候选内容 | 可供讨论，不是规范基线 | 已审查、已批准或兼容 |
| Reviewed（已审查） | 范围、ADR、兼容性和领域影响已审查 | 可进入显式决定 | 已接受或已发布 |
| Accepted（已接受） | 存在明确 Architecture Decision、接受范围和 decision source | 内容获准进入 Release Proposal | 已成为 Current、已采用或已实现 |
| Current（当前） | Release Record 已完成，发布范围和清单明确 | 是声明 scope 内的当前规范基线 | Runtime 已部署或任何项目已采用 |
| Deprecated（已废弃） | 存在显式废弃决定、理由、替代项和影响声明 | 不建议新采用，但继续有效引用和历史解析 | 已删除、无效或现有采用自动终止 |
| Archived（已归档） | 满足已接受的归档条件并形成归档记录 | 只用于历史、审计和重现 | 历史被删除或引用失效 |

`Rejected`、`Withdrawn` 和 `Superseded-before-release` 不得进入 Current；相应记录必须保留。

## 6. Freeze Model（冻结模型）

`Frozen` 是内容不可静默变化的约束，不是替代上述生命周期的独立状态：

1. Review Freeze（审查冻结）：版本进入 Reviewed 时，受审内容、scope 和兼容声明必须形成稳定引用；任何语义变化都需要新候选修订和重新审查。
2. Release Freeze（发布冻结）：版本进入 Current 后，已发布内容不可原地改写；语义修正必须产生新版本。
3. Errata（勘误）：不改变语义的勘误可以追加并引用原版本，但不得静默替换已发布内容。
4. Deprecated/Archived 内容继续保持冻结、可解析和可追溯。

本规范不选择 hash、签名、tag、archive format（归档格式）或存储机制。

## 7. Version Authority（版本权力）

版本权力是 Architecture Authority 内部的有限治理责任，不是 Operational Authority 或 Evolution Authority，也不由版本号自动产生。

| 动作 | 可以提出或执行的角色 | 必需 gate | 权力边界 |
|---|---|---|---|
| 提出版本 | Architecture Maintainer、Architecture Reviewer、Domain Owner 或其他有来源的 stakeholder（利益相关者） | Version/Change Proposal | 提案者不自动成为审查者或批准者 |
| 审查版本 | Architecture Reviewer；受影响的 DBOS/SAEE Domain Owner 提供领域意见 | Review record、兼容声明、ADR 检查 | Review 不等于 Approval |
| 批准版本 | 外部治理制度明确指定的 Architecture Decision Authority | 显式 Decision、`decided_by_ref`、接受范围 | 本规范不指派实际批准者 |
| 发布版本 | Architecture Maintainer 或明确指定的 release publisher（发布者） | Accepted version、Release Decision、冻结清单 | 发布者不能自行批准候选版本 |
| 采用版本 | 每个 adopter（采用方）的明确授权主体 | 独立 Adoption Decision 与 scope | Release 不自动授权采用或部署 |
| 废弃版本 | 明确指定的 Architecture Decision Authority | Deprecation Proposal、Review、Decision、替代与影响记录 | 维护者或后继版本不能自动废弃旧版本 |
| 归档版本 | Architecture Maintainer 按已接受归档决定执行 | 归档条件和记录 | 归档不能删除历史 |

同一参与者是否可以承担多个角色、所需 quorum 和回避规则由未来治理制度定义。v0.1 不创建或指派这些主体。

## 8. Deprecation and Archival（废弃与归档）

废弃记录必须包含：

- 被废弃的版本、scope 和状态；
- 废弃理由与显式 Decision；
- 后继版本或 `no_replacement`；
- Backward/Forward Compatibility 影响；
- Migration Requirement；
- 已知 adopter 的通知责任或 `not_defined`；
- 允许进入 Archived 的条件；
- 历史内容、ADR、Release 和 Adoption 引用的保留方式。

Deprecated 版本不得被静默删除、复用同一版本号或原地改写。Archive 只改变推荐与维护状态，不消除历史规范事实。

## 9. 与其他治理流程的关系

```text
Architecture Change Process
  produces accepted specification change
        ↓
Version Governance
  creates Accepted version candidate
        ↓
Release Governance
  creates Current version and Release Record
        ↓
Explicit Adoption Decision
  records scoped normative adoption
        ↓
Separate implementation/deployment process
  not defined or authorized here
```

Architecture Change、Version、Release、Adoption、Implementation 和 Deployment 是不同 truth surface（事实表面），不得自动升级。

## 10. 非实现状态

```text
VERSION_GOVERNANCE_SPECIFICATION_DEFINED=true
VERSION_RECORD_SCHEMA_IMPLEMENTED=false
VERSION_AUTHORITY_ASSIGNED=false
ARCHITECTURE_RELEASE_CREATED=false
VERSION_ADOPTION_RECORDED=false
IMPLEMENTATION_CHANGED=false
RUNTIME_VERSION_CHANGED=false
DEPLOYMENT_CHANGED=false
API_CREATED=false
AGENT_CREATED=false
RUNTIME_CREATED=false
ENTITY_CREATED=false
```

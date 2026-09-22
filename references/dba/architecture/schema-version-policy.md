---
spec_id: DBA-SCHEMA-VERSION-POLICY-0.1
title: Digital Biosphere Schema Version Policy v0.1
status: non-executable-schema-version-governance-policy
default_compatibility: Unknown
automatic_version_upgrade: false
automatic_schema_adoption: false
automatic_migration: false
implementation_effect: none
runtime_effect: none
---

# Digital Biosphere Schema Version Policy v0.1（数字生物圈模式版本策略 v0.1）

本策略将 [`version-governance-specification.md`](version-governance-specification.md) 与 [`version-compatibility-policy.md`](version-compatibility-policy.md) 应用于 Architecture、Contract、Implementation、Evaluation 和 Mapping schema profiles。

```text
Schema Version ≠ Implementation Version
Mapping Version ≠ Data Migration
Release ≠ Adoption
Adoption ≠ Upgrade
Deprecated Field ≠ Deleted Field
```

## 1. Version Scope（版本范围）

| schema scope | 版本责任 | 与既有 Version Type 的关系 |
|---|---|---|
| Architecture Schema | canonical object meaning、Owner、字段和不变量 | 作为 Architecture Version / Data Contract Version 的明确组成 |
| Contract Schema | 接口、交付义务、字段子集和引用边界 | 作为 Interface Version 或 Data Contract Version 的 contract profile |
| Implementation Schema | 实现实际接受/产生的字段、值域和限制 | Implementation 自有版本；不属于 Architecture Version，也不自动被 Architecture 采纳 |
| Evaluation Schema | Evaluation/Recommendation 字段、model reference 与 input boundary | 作为 Architecture Data Contract/Interface profile；实际 SAEE model version 独立 |
| Mapping Version | source/target schema pair 的映射规则、状态、warning 与 unknown handling | Data Contract governance artifact（数据契约治理工件）；不替代任一被映射版本 |

每个 Mapping Version 必须固定 source schema version 与 target schema version。`latest`、未限定 `v0.x` 或仅仓库分支名都不能替代明确版本。

## 2. Version Identifier（版本标识）

Schema 和 Mapping 文档使用 `vMAJOR.MINOR[.PATCH]`：

- Patch：无语义变化的勘误、链接或格式修正；
- Minor：经审查、显式向后兼容的增量变化；
- Major：改变 canonical meaning、Owner、必需字段、Authority、truth surface 或产生 Breaking Change；
- `v0.x`：早期规范，不从数字推断兼容，Compatibility 必须显式声明。

Mapping Version 变化不自动要求 source/target schema 同步改变；source/target 任一版本改变时，必须重新审查并发布新的 Mapping Version 或明确声明旧映射仍适用。

## 3. Minor Change（次版本变化）

只有同时满足以下条件时，才能作为 Minor Change：

- 新字段是 additive and optional（增量且可选）；
- 缺失字段有明确保守语义，不使用权限扩大或成功默认值；
- Object Owner、Authority、Identity、Lifecycle 和 truth surface 不变；
- 既有字段含义和值域不被重定义；
- 历史 source/target mapping 仍可解析；
- Backward Compatibility 明确为 `full` 或有可验证条件的 `conditional`；
- 通过 Architecture Change Process 的 Proposal、Review、Decision 与 Adoption。

“代码已支持”或“容易转换”不是 Minor Change 的充分依据。

## 4. Compatible Change（兼容变化）

Compatible Change 是经过显式 compatibility review（兼容审查）的变化类别，不等同于 Minor 版本号。它必须：

1. 指明 prior/target version 和 scope；
2. 声明 Backward 与 Forward Compatibility；
3. 列出新增、保持、废弃和未知字段；
4. 证明不会把 Recommendation、Evaluation、Evidence、Capability、Authorization、Permission 或 Lifecycle 状态升级；
5. 说明旧 consumer 如何保留未知值；
6. 记录 limitations 和 mapping warnings。

若只能满足有限 scope，应使用 `Compatible With Warning` 或 conditional compatibility，不能声明无条件 Compatible。

## 5. Major Change（主版本变化）

出现以下任一情况需要 Major Version：

- 改变 Architecture Schema canonical meaning；
- 改变对象 Owner 或 schema authority；
- 删除、重命名或重新定义必需字段；
- 改变 Entity identity continuity 或 Lifecycle gate；
- 把 Capability、Authorization 与 Permission 合并；
- 把 Evidence Reference 变成 Canonical Evidence Object 或 Truth；
- 把 Evaluation/Recommendation 变成 Command 或 DBOS fact；
- 改变 unknown/conflicted/partial 的保守语义；
- 需要无法在旧语义下正确解释的数据转换。

Major Change 必须有新 ADR、Breaking Change declaration、Migration Requirement 和显式 Architecture Decision。版本号本身不批准变化。

## 6. Breaking Change（破坏性变化）

Breaking Change 是语义判断，不等同于“编译失败”或“代码不兼容”。它至少包括：

- `description` 与 `capability_name` 被直接等同且丢失语义；
- `Medium` 静默改为 `MODERATE` 而没有 value mapping decision；
- `candidate_reference` 被转换为 `entity_id`；
- reference-local `evidence_id` 被当作 canonical Evidence Object ID；
- `permission_effect=NONE` 被解释为 Permission Record；
- 缺失或未知字段被填充为 Active、Verified、Authorized、Valid、Pass 或 Compatible；
- 删除历史 field mapping、deprecated value、failure reference 或 provenance。

Breaking Change 的 source/target compatibility_status 必须是 `Incompatible` 或在未决期间为 `Unknown`，不得标记 Compatible。

## 7. Deprecated Field（废弃字段）

字段废弃记录必须包含：

| 字段 | 语义 |
|---|---|
| `field_ref` | schema identity、version 与字段全名 |
| `deprecated_since` | 开始废弃的版本 |
| `last_supported_version` | 最后承诺解析的版本；未知时为 `unknown` |
| `replacement_field` | 替代字段或 `no_replacement` |
| `semantic_difference` | 旧字段与替代项的语义差异 |
| `compatibility_status` | 对每个相关版本的兼容状态 |
| `migration_requirement` | none、optional、required 或 undefined |
| `history_preservation` | 历史记录、引用与 mapping 如何继续解析 |
| `decision_refs` | Review、ADR、Decision 与 Adoption 引用 |

Deprecated 字段不得从同一版本原地删除或复用为不同含义。Unknown consumer 必须可以识别它是历史字段，而不是无效数据。

## 8. Migration Requirement（迁移要求）

Migration Requirement 只描述采用新 schema 可能需要的未来工作，不执行也不授权迁移。它必须继承 `version-compatibility-policy.md` 的字段，并额外说明：

- 每条 affected mapping_id；
- source/target schema freeze references；
- canonical meaning preservation；
- implementation-specific fields 的保留或隔离；
- unknown/default policy；
- identity、Evidence、failure 与 provenance 保留；
- Permission、Authority 与 Lifecycle non-escalation checks（非升级检查）；
- independent validation 与 rollback/exit 条件。

实际迁移必须由 adopter 独立决定，并在 Architecture 文档之外获得实现权限。Mapping 或 Migration Requirement 文档存在不表示数据、代码、Runtime 或 registry 已迁移。

## 9. Schema Mapping Change Lifecycle（模式映射变更生命周期）

```text
Proposed
  ↓
Reviewed
  ↓
Accepted
  ↓
Released Mapping Version
  ↓
Explicit Adoption (per adopter)
  ↓ optional separate implementation/migration project
Deprecated
  ↓
Archived (history retained)
```

- Proposed/Reviewed/Accepted/Released/Adopted 是不同状态；
- source 或 target schema 改变不会自动升级 mapping version；
- Release 不自动采用；
- Adoption 不自动迁移；
- Deprecated 不删除；
- 无共同兼容版本时 fail closed 并记录 `unsupported_version` 或 `Unknown`。

## 10. Compatibility Decision Table（兼容决策表）

| 变化 | 最低版本动作 | compatibility_status | Migration Requirement |
|---|---|---|---|
| 纯文案或链接修正 | Patch | `Compatible` | `none` |
| 新增有保守缺失语义的可选字段 | Minor + review | `Compatible` 或 `Compatible With Warning` | `none` 或 `optional` |
| 新增实现专用字段 | Implementation version；Mapping review | 通常 `Compatible With Warning` 或 `Unknown` | `none`，除非 adopter 需要 |
| controlled value 近义变化 | Mapping review；不能仅 Patch | `Unknown` 直到决定 | `undefined` |
| 删除/重命名必需字段 | Major + ADR | `Incompatible` | `required` |
| Owner/Authority/truth surface 变化 | Major + ADR | `Incompatible` | `required`，但不自动授权 |
| 字段废弃但继续解析 | Minor 或 Major，视语义影响 | `Deprecated` | `optional/required/undefined` |

## 11. Non-effect Status（无效力状态）

```text
SCHEMA_VERSION_POLICY_DEFINED=true
SCHEMA_VERSION_RELEASED=false
SCHEMA_VERSION_ADOPTED=false
SCHEMA_VERSION_AUTO_UPGRADED=false
MAPPING_VERSION_AUTO_UPGRADED=false
DEPRECATED_FIELD_DELETED=false
MIGRATION_REQUIREMENT_NE_MIGRATION_AUTHORIZATION=true
DATA_MIGRATION_AUTHORIZED=false
DATA_MIGRATION_EXECUTED=false
IMPLEMENTATION_CHANGED=false
RUNTIME_CHANGED=false
ENTITY_INSTANCE_CHANGED=false
CAPABILITY_INSTANCE_CHANGED=false
```

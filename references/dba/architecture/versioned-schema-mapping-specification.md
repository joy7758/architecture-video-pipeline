---
spec_id: DBA-VERSIONED-SCHEMA-MAPPING-0.1
title: Digital Biosphere Versioned Schema Mapping Specification v0.1
title_zh: 数字生物圈版本化模式映射规范 v0.1
status: non-executable-data-contract-governance-specification
mapping_version: v0.1
canonical_schema_authority: architecture-governance
schema_mapping_defined: true
mapping_records_instantiated: false
data_migration_authorized: false
data_migration_executed: false
implementation_changed: false
entity_instance_created: false
capability_instance_created: false
permission_granted: false
---

# Digital Biosphere Versioned Schema Mapping Specification v0.1

本规范定义 Architecture、Contract、Implementation 与 Evaluation 四类 schema layer（模式层）之间的版本化语义映射。它用于解释字段如何对应、何处存在差异以及何时必须保持 `Unknown`，不定义可执行 schema、转换程序、数据库迁移、API 或 Runtime adapter（运行时适配器）。

```text
Schema Mapping ≠ Data Migration
Canonical Definition belongs to Architecture Governance
Implementation Field ≠ Canonical Meaning
Version Change requires Governance Process
Unknown fields remain Unknown
```

## 1. Canonical Schema Authority（规范模式权力）

Architecture Governance（架构治理）拥有 Digital Biosphere 规范字段定义、语义边界、对象 Owner、兼容性声明和映射规则的维护责任。这里的“拥有”是 normative meaning authority（规范含义权力），不表示 Architecture Governance 创建或修改运行数据。

必须区分：

| 权力或责任 | 范围 | 不表示 |
|---|---|---|
| Architecture Governance | 定义 canonical meaning、字段边界、版本与映射 | 创建 Entity、Capability、Evidence 或运行状态 |
| DBOS object ownership | 按已采用规范形成 Identity、Capability、Execution、Evidence、Verification 与 Lifecycle 记录 | 可以反向重定义 Architecture Schema |
| SAEE object ownership | 按已采用规范形成 Evaluation 与 Recommendation | 可以重定义 DBOS 事实字段或架构规则 |
| Implementation maintainer | 实现、验证或暴露 implementation fields（实现字段） | 字段存在即成为 canonical definition |

若 Implementation 与 Architecture 不一致，默认结论是 mapping gap（映射缺口）或 implementation divergence（实现偏差），不是 Architecture 自动随代码变化。语义变化必须进入 Architecture Change、ADR、Version、Release 与 Adoption 流程。

## 2. Schema Layers（模式层）

| schema_layer | 主要规范来源 | 责任 | 非声明 |
|---|---|---|---|
| Architecture Schema | `data-contracts.md`、对象规范与边界规范 | 定义 canonical object meaning、Owner、不变量和字段语义 | 已有序列化、数据库或实现 |
| Contract Schema | `interface-specification.md`、`research-agent-implementation-contract.md` | 定义跨层交付、引用和最小实现义务 | 可以覆盖 Architecture Schema 或授权实现 |
| Implementation Schema | DBOS 当前代码、record builder（记录构造器）或未来 adopted implementation profile | 表达代码实际接受或产生的字段和值域 | 字段名、默认值或枚举自动成为规范含义 |
| Evaluation Schema | Architecture 中的 Evaluation Object / SAEE interface profile，以及未来 SAEE adopted profile | 表达基于 DBOS 输入形成的派生评价语义 | 评价字段可以回写 DBOS 事实或形成权限 |

### 2.1 Layer precedence（层级优先关系）

1. Architecture Schema 定义规范含义；
2. Contract Schema 必须引用并收窄交付义务，不得扩张 Owner 或 Authority；
3. Implementation Schema 必须声明所采用的 Architecture/Contract version，不得以代码事实重写规范；
4. Evaluation Schema 只能创建派生评价，必须保留 input references（输入引用）和模型版本；
5. 任一层无法表达上游含义时必须记录 `Unknown`、`Incompatible` 或 limitation（限制），不得猜测或默认提升。

## 3. Schema Identity and Version References（模式身份与版本引用）

v0.1 使用以下逻辑 schema identity（逻辑模式身份）：

| schema_id | layer | 当前来源 | 状态 |
|---|---|---|---|
| `DBA-ARCHITECTURE-SCHEMA-0.1` | Architecture | `data-contracts.md` 及关联规范 | normative specification（规范说明） |
| `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1` | Contract | `research-agent-implementation-contract.md` | non-executable contract（非可执行契约） |
| `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1` | Implementation | DBOS `entity_support/` 的只读观察 | observed implementation profile（观察到的实现配置）；不是 Architecture adoption |
| `DBA-EVALUATION-SCHEMA-0.1` | Evaluation | `data-contracts.md` 与 `interface-specification.md` 的 Evaluation 语义 | non-executable evaluation contract（非可执行评价契约） |

这些标识用于文档映射，不创建 schema registry（模式登记系统）、版本记录实例或 release（发布）。DBOS observed profile 只说明本次映射所观察的代码字段，不声明 DBOS 已采用本规范。

## 4. Mapping Object（映射对象）

每一条字段映射至少包含：

| 字段 | 语义 |
|---|---|
| `mapping_id` | 稳定、不可复用的映射规则标识 |
| `source_schema` | 源 schema identity 与版本 |
| `target_schema` | 目标 schema identity 与版本 |
| `source_field` | 源字段的完整限定名；缺失字段必须使用明确的 `not_defined` 说明，而不是伪造字段 |
| `target_field` | 目标字段的完整限定名；无合法目标时使用明确的 `not_defined` 说明 |
| `version` | 该映射规则自身的版本 |
| `compatibility_status` | 本规范第 5 节定义的兼容状态 |

推荐但不构成已实现 schema 的扩展语义：

| 字段 | 语义 |
|---|---|
| `transformation_rule` | 允许的语义转换；没有获批规则时为 `none` 或 `unknown` |
| `unknown_handling` | 缺失、未知、冲突或不支持值如何保留 |
| `provenance_refs` | 支持该映射判断的 Architecture、Contract 与 Implementation 引用 |
| `limitations` | 映射不能证明或不能表达的内容 |

Mapping Object 是 conceptual governance record（概念治理记录）。本规范没有实例化 Mapping Object，也没有选择 YAML、JSON、数据库表或 API 编码。

## 5. Compatibility Status（兼容状态）

映射兼容状态的受控词表为：

| compatibility_status | 定义 | 必需处理 |
|---|---|---|
| `Compatible` | 在声明 scope 内字段含义、Owner、状态与未知处理一致，不需要语义转换 | 保留版本和 provenance；不推断实现已采用 |
| `Compatible With Warning` | 核心含义可对应，但存在值域、必填性、范围、默认值或表达粒度差异 | 必须记录 warning、限制和保守处理；不得静默转换 |
| `Deprecated` | 映射或字段仍需历史解析，但不建议新采用 | 保留旧规则、替代项、最后支持版本和影响 |
| `Incompatible` | 对应会改变含义、Owner、Authority、状态、身份连续性或 truth surface | 禁止直接映射；需要 Major/Breaking Change 与显式治理 |
| `Unknown` | 证据或规范不足，无法证明兼容或不兼容 | 保持 unknown；不得当作 Compatible |

默认状态是 `Unknown`。字段同名、类型相似、测试通过或代码可转换都不足以自动声明 `Compatible`。

## 6. Mapping Rules（映射规则）

1. Canonical field meaning 优先于 implementation naming；字段重命名必须有显式规则。
2. 一个 Implementation field 不得同时冒充多个不同 canonical concepts，除非每个目标都有独立 Mapping Object、范围和无损规则。
3. 一个 canonical field 被拆成多个实现字段时，必须分别映射；不能通过拼接默认值补造状态或 Authority。
4. Implementation-only field（仅实现字段）必须标为 implementation-specific，不得因被公开或测试而升级为 Architecture field。
5. Contract-only field 必须说明它是否为 canonical object extension（规范对象扩展）、交付引用还是尚未纳入对象契约的 gap。
6. `Unknown`、`partial`、`conflicted`、`not_applicable` 和缺失字段必须可区分。
7. Controlled vocabulary（受控词表）变化需要逐值映射；大小写、拼写或近义词不能自动视为等价。
8. Object identifier（对象标识）只有在 identity scope、Owner、生成规则和连续性一致时才可映射；同名 `*_id` 不证明同一对象。
9. Reference 字段只映射引用语义，不得升级为被引用对象、Evidence truth、Verification decision、Authorization 或 Permission。
10. Evaluation field 不得映射成 DBOS fact field；Evaluation 必须保留为 SAEE 派生对象。

## 7. Domain Mapping Specifications（领域映射规范）

| 文档 | 范围 | 核心边界 |
|---|---|---|
| [`entity-schema-mapping.md`](entity-schema-mapping.md) | Digital Entity、Entity Registration Contract、DBOS Entity record | Entity aggregate ≠ registration record；candidate reference ≠ entity identity |
| [`capability-schema-mapping.md`](capability-schema-mapping.md) | Capability Definition、Record、Authorization 与 Permission 引用 | Capability 不得映射为 Permission |
| [`evidence-schema-mapping.md`](evidence-schema-mapping.md) | Evidence Material、Reference、Canonical Evidence Object | Reference 不得自动成为 Evidence Object 或 Truth |
| [`schema-version-policy.md`](schema-version-policy.md) | Mapping/Schema 版本、兼容、废弃与 Migration Requirement | Version change 不自动迁移或采用 |

## 8. Mapping Governance Lifecycle（映射治理生命周期）

```text
Mapping Proposal
  ↓
Architecture Review
  ↓
Compatibility Decision
  ↓
Architecture Adoption
  ↓
Documentation / Mapping Version Update
  ↓ separate adopter decision
Implementation Adoption (optional; not authorized here)
```

- 提案必须列出 source/target version、字段、Owner、值域、未知处理和风险；
- Architecture Reviewer 必须检查语义、Authority、truth surface 与历史兼容；
- Major、Breaking、Owner 或权限边界变化必须有 ADR；
- Documentation Update 不等于 Implementation adoption；
- Implementation adoption 不等于 data migration、deployment 或 Runtime upgrade；
- 未完成 Decision 时现行 canonical definition 保持不变。

## 9. Non-migration Boundary（非迁移边界）

本规范允许描述未来 Migration Requirement，但不允许：

- 读取后重写现有数据库、registry、Evidence 或历史记录；
- 自动重命名字段、转换枚举或填充默认值；
- 自动发布、采用或升级 schema version；
- 把 mapping document 当作 migration plan approval；
- 修改 DBOS、SAEE 或任何 Digital Entity 实例；
- 用实现当前状态反向批准 Architecture change。

实际 migration 需要独立项目、显式 Adoption Decision、授权、备份/回退、provenance preservation（来源保留）和完成后验证。

## 10. Agent-readable Conformance Questions（智能体可读符合性问题）

智能体解释任一字段映射前必须回答：

1. 哪个文件定义 canonical meaning？
2. Object Owner 与 schema authority 是否被区分？
3. source/target schema version 是否明确？
4. 字段是 canonical、contract-only 还是 implementation-specific？
5. 值域和缺失语义是否完全一致？
6. 是否存在 Authorization、Permission、Truth 或 Lifecycle 的隐式提升？
7. Compatibility status 是否显式声明，还是应保持 `Unknown`？
8. 是否把 Mapping 错当成 Migration、Adoption 或 Implementation？

任何问题无法回答时，必须停止等价映射并保留 `Unknown`。

## 11. Non-implementation Status（非实现状态）

```text
VERSIONED_SCHEMA_MAPPING_SPECIFICATION_DEFINED=true
CANONICAL_SCHEMA_AUTHORITY=ARCHITECTURE_GOVERNANCE
SCHEMA_MAPPING_NE_DATA_MIGRATION=true
IMPLEMENTATION_FIELD_NE_CANONICAL_MEANING=true
UNKNOWN_FIELDS_REMAIN_UNKNOWN=true
MAPPING_OBJECT_INSTANTIATED=false
SCHEMA_REGISTRY_CREATED=false
SERIALIZATION_SELECTED=false
DATA_MIGRATION_AUTHORIZED=false
DATA_MIGRATION_EXECUTED=false
IMPLEMENTATION_ADOPTION_RECORDED=false
DBOS_CHANGED=false
SAEE_CHANGED=false
ENTITY_INSTANCE_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
API_CREATED=false
CODE_CHANGED=false
```

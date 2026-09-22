---
adr_id: ADR-012
title: Establish Versioned Schema Mapping Governance
title_zh: 建立版本化模式映射治理
status: accepted-for-architecture-specification-v0.1
decision_scope: architecture-contract-implementation-evaluation-schema-mapping-only
mapping_effect: specification-only
migration_effect: none
implementation_effect: none
entity_effect: none
capability_effect: none
permission_effect: none
evidence_effect: none
---

# ADR-012: Establish Versioned Schema Mapping Governance

## Problem（问题）

Digital Entity、Capability Boundary、Evidence、Research Agent Contract 与 DBOS Digital Entity Infrastructure 已分别形成 Architecture、Contract 和 Implementation 表达，但字段并不总是一一等价：

- Architecture Entity Object 包含 `entity_id/entity_type/lifecycle_state`，Contract 另要求 `owner_reference`；
- Architecture 的 role classification（角色分类）与 DBOS implementation `SUPPORTED_ENTITY_TYPES` 不是同一词表；
- Architecture Capability Object 使用 `description`，Research Agent Contract 和 DBOS implementation 使用 `capability_name`；
- Architecture risk value 使用 `Medium`，当前实现使用 `MODERATE`；
- Architecture `authorization_status` 与实现的 `capability_state/authorization_reference` 拆分方式不同；
- 当前 Architecture Core Data Contracts 没有独立 Permission Reference field table；实现 `permission_effect=NONE` 只是护栏；
- Research Agent Contract 有四类 Evidence Material reference，当前 DBOS support 使用一个 generic `reference`；
- DBOS support 的 `evidence_id` 属于非 canonical Evidence Reference mapping，不能自动解释为 Canonical Evidence Object identity。

没有正式映射治理时，代码字段可能被反向当作 canonical definition，同名 ID 可能被误认为同一对象，近义枚举可能被静默转换，Reference 可能被提升为 Evidence truth，Capability 也可能被错误映射为 Permission。

## Decision（决策）

建立 Versioned Schema Mapping Layer（版本化模式映射层）：

1. Architecture Governance 维护 canonical meaning、Mapping Object、兼容状态和 mapping version；
2. 区分 Architecture Schema、Contract Schema、Implementation Schema 与 Evaluation Schema；
3. 每条映射至少记录 `mapping_id/source_schema/target_schema/source_field/target_field/version/compatibility_status`；
4. 兼容状态限定为 `Compatible`、`Compatible With Warning`、`Deprecated`、`Incompatible`、`Unknown`；默认是 `Unknown`；
5. 建立 Entity、Capability 与 Evidence 三个领域 mapping profile；
6. `owner_reference` 保持 Contract extension，不自动加入 Entity Object；
7. `description ↔ capability_name` 和 `Medium ↔ MODERATE` 保持 warning/unknown，直到显式治理决定；
8. Capability、Authorization 与 Permission 保持独立；Capability 不能映射为 Permission；
9. Evidence Material、Evidence Reference 与 Canonical Evidence Object 保持独立；Reference 不能自动成为 Evidence 或 Truth；
10. 定义 Minor、Compatible、Major、Breaking、Deprecated Field 与 Migration Requirement 的 schema version policy；
11. Mapping change 必须经过 Architecture Change、Version、Release 与 Adoption governance；
12. 本 ADR 不创建可执行 schema、Mapping Object instance、migration、API、代码或对象实例。

```text
Schema Mapping ≠ Data Migration
Implementation Field ≠ Canonical Meaning
Unknown ≠ Compatible
Version Release ≠ Adoption ≠ Migration
Architecture Authority ≠ DBOS
DBOS ≠ SAEE
```

## Alternatives（替代方案）

### A. 以 DBOS 当前代码字段为 canonical schema

拒绝。Implementation 是采用者和表达者，不是 Architecture meaning authority。这样会让代码变更绕过 Architecture Change Process。

### B. 立即统一重命名字段和值域

拒绝。`description/capability_name` 与 `Medium/MODERATE` 的语义等价尚未证明；重命名会把 mapping 误作 migration，并违反本任务禁止修改 DBOS 的边界。

### C. 只维护一张无版本 crosswalk（交叉表）

拒绝。没有 source/target version 时，映射会随文件变化而静默漂移，也无法保留 Deprecated 或 Incompatible 历史。

### D. 让 Contract Schema 覆盖 Architecture Schema

拒绝。Contract 可以收窄交付要求或增加引用，但不能改变 canonical object meaning、Owner 或 Authority。

### E. 将 Evidence Reference 直接映射为 Canonical Evidence Object

拒绝。引用存在不证明材料存在、DBOS 已采集、integrity 已验证或内容真实。

### F. 将 Authorized Capability 映射为 Permission

拒绝。Authorization 与当前 Context 下的 Permission 是不同治理对象；Capability 不能产生执行许可。

### G. 对未知字段使用默认值以提高兼容性

拒绝。默认值可能伪造 Active、Verified、Authorized、Valid、Pass 或 Compatible 等状态，违反 fail-closed 原则。

## Impact（影响）

### Positive（正面影响）

- Architecture、Contract 与 Implementation 的字段差异成为显式、可版本化事实；
- 智能体可以发现 canonical、contract-only 与 implementation-specific 字段；
- 同名字段、ID 和枚举不再自动获得等价性；
- Entity、Capability、Permission、Evidence 与 Evaluation 边界更可审计；
- 未来 schema adoption 或 migration 可以引用稳定 mapping_id 和兼容判断；
- Unknown、warning、deprecated 和 incompatible 状态可保留历史。

### Costs and unresolved issues（代价与未决问题）

- `owner_reference` 是否进入 canonical Entity Object 尚未决定；
- Operational Entity role 与 DBOS entity type 的 mapping 尚未决定；
- `description/capability_name` 的信息量和转换规则尚未标准化；
- `Medium/MODERATE` 值域等价性尚未决定；
- Authorization Object 与 Permission Object/Reference 尚未形成独立 Core Data Contract；
- 四类 Evidence Material reference 尚无无损 DBOS implementation representation；
- canonical ID resolution、schema registry、serialization 和 conformance tooling 尚未定义；
- Architecture mapping adopter、reviewer 和 version authority 尚未指派。

这些问题保持 `Unknown` 或 `Compatible With Warning`，不能由本 ADR 自动解决。

## Consequence Boundaries（后果边界）

```text
VERSIONED_SCHEMA_MAPPING_SPECIFICATION_DEFINED=true
ENTITY_SCHEMA_MAPPING_DEFINED=true
CAPABILITY_SCHEMA_MAPPING_DEFINED=true
EVIDENCE_SCHEMA_MAPPING_DEFINED=true
SCHEMA_VERSION_POLICY_DEFINED=true
MAPPING_OBJECT_INSTANTIATED=false
SCHEMA_REGISTRY_CREATED=false
DATA_MIGRATION_AUTHORIZED=false
DATA_MIGRATION_EXECUTED=false
DBOS_CHANGED=false
SAEE_CHANGED=false
ENTITY_INSTANCE_CREATED=false
CAPABILITY_INSTANCE_CREATED=false
PERMISSION_GRANTED=false
EVIDENCE_CREATED=false
API_CREATED=false
CODE_CHANGED=false
```

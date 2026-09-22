---
spec_id: DBA-ENTITY-SCHEMA-MAPPING-0.1
title: Digital Entity Versioned Schema Mapping v0.1
status: non-executable-schema-mapping-profile
mapping_version: v0.1
canonical_definition: digital-entity-specification.md
canonical_object_contract: data-contracts.md#3-entity-object主体对象
contract_profile: research-agent-implementation-contract.md#2-entity-registration-contract实体登记契约
implementation_profile: DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1
data_migration_effect: none
entity_effect: none
---

# Digital Entity Versioned Schema Mapping v0.1（数字实体版本化模式映射 v0.1）

本文件映射 Architecture Digital Entity、Entity Registration Contract 与当前 DBOS Entity Support record（实体支撑记录）。它解释字段语义，不创建 Entity、不分配 Identity，也不声明 DBOS 已采用本映射。

```text
Digital Entity Aggregate ≠ Entity Registration Contract ≠ DBOS Support Record
Candidate Reference ≠ Entity ID
Registration ≠ Verification ≠ Active
```

## 1. Schema Profiles（模式配置）

| layer | schema | 规范或观察来源 | 权力边界 |
|---|---|---|---|
| Architecture | `DBA-ARCHITECTURE-SCHEMA-0.1/EntityObject` | `digital-entity-specification.md`、`data-contracts.md` | Architecture Governance 定义含义；DBOS 管理 canonical runtime object |
| Contract | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `research-agent-implementation-contract.md` | 定义未来实现必须提供或引用的登记语义，不创建身份 |
| Implementation | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EntityRegistrationRecord` | DBOS `entity_support/entity_registry.py` 的只读观察 | 代码字段与校验规则；不是 canonical meaning authority |
| Implementation candidate workflow | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CandidateRegistrationRecord` | DBOS `entity_support/candidate_registration.py` 的只读观察 | candidate workflow record；不是 Entity Object |

当前 DBOS implementation profile 是观察到的非持久化 record builder，不是已发布 schema、Architecture adoption 或 Entity Registry instance。

## 2. Canonical and Non-canonical Fields（规范与非规范字段）

| 字段 | Architecture Entity Object | Contract Schema | DBOS Implementation | 分类结论 |
|---|---|---|---|---|
| `entity_id` | canonical field | required contract field | record field | canonical meaning 来自 Architecture；实现字段只承载引用 |
| `entity_type` | canonical field | required contract field | record field + implementation vocabulary | canonical field；实现枚举是 implementation-specific constraint |
| `owner_reference` | 当前 Entity Object field table 未定义 | required contract extension | record field | contract-canonical extension；不是当前 Entity Object canonical field |
| `lifecycle_state` | canonical field | required contract field | record field，创建时仅允许 `PROPOSED` | canonical field；实现只支持一个登记阶段子集 |
| `SUPPORTED_ENTITY_TYPES` | 未定义代码枚举 | 要求 DBOS controlled classification | `agent/protocol/repository/service/artifact/governance_system` | implementation-specific vocabulary；不得反向增加 Architecture Entity 类别 |
| `DEFAULT_LIFECYCLE_STATE` | `Proposed` 有规范语义 | Registration 不等于 Active | `PROPOSED` | implementation-specific representation of canonical state |
| `candidate_reference` | Candidate 不是 Entity Identity | Contract 要求未获 Identity 时保持 Candidate | candidate workflow field | implementation-specific proposal reference；禁止映射为 `entity_id` |

`Operational Entity` 是 Architecture role classification（角色分类），当前 DBOS `SUPPORTED_ENTITY_TYPES` 没有同义主类型。二者的关系保持 `Unknown`，不得把 `service`、`agent` 或其他实现值自动解释为 `Operational Entity`。

## 3. Mapping Records（映射规则）

| mapping_id | source_schema | target_schema | source_field | target_field | version | compatibility_status | 说明 |
|---|---|---|---|---|---|---|---|
| `DBA-MAP-ENTITY-001` | `DBA-ARCHITECTURE-SCHEMA-0.1/EntityObject` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `entity_id` | `entity_id` | `v0.1` | `Compatible` | Contract 保留 DBOS-managed opaque identity；不授权自分配 |
| `DBA-MAP-ENTITY-002` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EntityRegistrationRecord` | `entity_id` | `entity_id` | `v0.1` | `Compatible With Warning` | 实现只验证非空字符串，尚未证明 canonical identity resolution 或持久化 |
| `DBA-MAP-ENTITY-003` | `DBA-ARCHITECTURE-SCHEMA-0.1/EntityObject` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `entity_type` | `entity_type` | `v0.1` | `Compatible` | 两层均要求 DBOS controlled classification |
| `DBA-MAP-ENTITY-004` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EntityRegistrationRecord` | `entity_type` | `entity_type` | `v0.1` | `Compatible With Warning` | 当前实现值域不能自动表达 Architecture role classification |
| `DBA-MAP-ENTITY-005` | `DBA-ARCHITECTURE-SCHEMA-0.1/EntityObject` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `owner_reference:not_defined` | `owner_reference` | `v0.1` | `Unknown` | Contract 新增责任引用；尚未纳入 Entity Object field table，不能静默提升为该对象字段 |
| `DBA-MAP-ENTITY-006` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EntityRegistrationRecord` | `owner_reference` | `owner_reference` | `v0.1` | `Compatible With Warning` | 实现仅验证非空，未验证身份、权力、法律所有权或 provenance |
| `DBA-MAP-ENTITY-007` | `DBA-ARCHITECTURE-SCHEMA-0.1/EntityObject` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `lifecycle_state` | `lifecycle_state` | `v0.1` | `Compatible` | Contract 保留 DBOS lifecycle ownership |
| `DBA-MAP-ENTITY-008` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EntityRegistration` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EntityRegistrationRecord` | `lifecycle_state` | `lifecycle_state` | `v0.1` | `Compatible With Warning` | record builder 仅接受 `PROPOSED`，不能代表完整七状态生命周期 |
| `DBA-MAP-ENTITY-009` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CandidateRegistrationRecord` | `DBA-ARCHITECTURE-SCHEMA-0.1/EntityObject` | `candidate_reference` | `entity_id` | `v0.1` | `Incompatible` | Candidate reference 不是 canonical Entity Identity |

## 4. Field Semantics（字段语义）

### 4.1 `entity_id`

- Canonical：由 DBOS 管理的稳定、不透明 Entity 引用；
- Contract：实现只能提供或引用，不能自行补造；
- Implementation：当前 builder 接受非空字符串但不持久化，也不证明该 ID 已存在于 canonical registry；
- Mapping gate：只有 identity Owner、生成规则、scope 和连续性均有证据时才能从 warning 提升为 `Compatible`。

### 4.2 `entity_type`

- Canonical：DBOS 管理的实体分类；Architecture role classification 与 DBOS controlled type 不自动相同；
- Contract：Research Agent / Operational Entity 语义需要 DBOS 受控分类表达；
- Implementation：当前六值集合是代码约束，不是 Architecture 分类法；
- Unknown handling：无法表达 `Operational Entity` 时保持未映射，不选择“最像”的实现值。

### 4.3 `owner_reference`

- Contract canonical meaning：对 Human Research Owner、责任主体或治理来源的引用；
- Non-claim：不是作者身份、数据所有权、无限控制权、Authorization 或 Permission；
- Current gap：Architecture Entity Object field table 尚未定义该字段，需未来 Data Contract change 决定是否纳入或保持独立关联对象。

### 4.4 `lifecycle_state`

- Canonical vocabulary：Proposed、Registered、Verified、Active、Evaluated、Adapted、Retired；
- Implementation registration subset：`PROPOSED`；
- 大小写转换是 representation concern（表达问题），不是已批准的数据转换；
- `PROPOSED` record 不得映射为 Registered、Verified 或 Active。

## 5. Implementation-specific Fields（仅实现字段）

以下字段或规则不属于 v0.1 Entity Object canonical field table：

- `SUPPORTED_ENTITY_TYPES`；
- `DEFAULT_LIFECYCLE_STATE`；
- `proposal_id`、`candidate_reference`、`requested_entity_type`；
- `review_status`、`review_reference`；
- `registration_request_status`、`registration_request_reference`；
- `requested_lifecycle_state`、`current_effect`。

这些字段可以支持候选工作流，但不能创建 Entity、Identity、Lifecycle transition、Capability 或 Permission。若未来纳入 Architecture Schema，必须通过新的 Data Contract Version 与 mapping decision。

## 6. Unknown and Conflict Handling（未知与冲突处理）

1. 未找到 canonical `entity_id` 时保持 Candidate，不使用 proposal、repository、process、Runtime 或 Agent 名称替代；
2. `entity_type` 无精确映射时保持 `Unknown`；
3. `owner_reference` 只有字符串但无 provenance 时保持 `partial` 或 `Unknown`；
4. 生命周期状态大小写或值域不匹配时不得自动升级；
5. Contract 与 Implementation 冲突时保留双方版本与来源，提交 Architecture mapping review，不覆盖历史。

## 7. Non-effect Status（无效力状态）

```text
ENTITY_SCHEMA_MAPPING_DEFINED=true
ENTITY_SCHEMA_MAPPING_APPLIED=false
ENTITY_DATA_MIGRATED=false
ENTITY_ID_ASSIGNED=false
ENTITY_INSTANCE_CREATED=false
LIFECYCLE_STATE_CHANGED=false
OPERATIONAL_ENTITY_TYPE_INFERRED=false
DBOS_IMPLEMENTATION_CHANGED=false
```

---
spec_id: DBA-CAPABILITY-SCHEMA-MAPPING-0.1
title: Digital Biosphere Capability Versioned Schema Mapping v0.1
status: non-executable-schema-mapping-profile
mapping_version: v0.1
canonical_definition: capability-boundary-specification.md
canonical_object_contract: data-contracts.md#4-capability-object能力对象
contract_profile: research-agent-implementation-contract.md#5-capability-contract能力契约
implementation_profile: DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1
capability_effect: none
authorization_effect: none
permission_effect: none
---

# Digital Biosphere Capability Versioned Schema Mapping v0.1

本文件映射 Capability Definition、Capability Object、Research Agent Capability Contract 和 DBOS Capability support records，并明确 Authorization Reference 与 Permission Reference 的不可替代关系。

```text
Capability Definition ≠ Capability Record
Capability Record ≠ Authorization
Authorization ≠ Permission
Capability cannot map to Permission
```

## 1. Schema Profiles（模式配置）

| layer | schema | 来源 | 边界 |
|---|---|---|---|
| Architecture Definition | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityDefinition` | `capability-boundary-specification.md` | 定义 Capability 含义、层级、风险和权限分离 |
| Architecture Object | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `data-contracts.md` | 定义 canonical Capability record fields 与 DBOS Owner |
| Contract | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/CapabilityContract` | `research-agent-implementation-contract.md` | 定义实现候选必须声明的最小能力语义 |
| Implementation declaration | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityRecord` | DBOS `entity_support/capability_registry.py` 的只读观察 | 未验证能力声明记录；不是 grant |
| Implementation boundary | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityBoundaryRecord` | DBOS `entity_support/capability_boundary.py` 的只读观察 | Declared/Verified/Authorized 状态化引用；`permission_effect=NONE` |

## 2. Canonical Capability Concepts（规范能力概念）

### 2.1 Capability Definition

Capability 是可以声明、验证或在另行有效治理边界下执行的一类行为能力描述。它不表示 Authority、Authorization、Permission、Execution Result、Fitness 或安全性结论。

### 2.2 Capability Record

Capability Object 是 DBOS 管理的 canonical record，当前字段为：

`capability_id`、`entity_id`、`description`、`scope`、`constraints`、`risk_level`、`verification_status`、`authorization_status`。

### 2.3 Authorization Reference

Authorization Reference 指向一个有来源、scope、constraints、期限和 authority boundary 的独立授权记录。Capability Object 中的 `authorization_status` 只可保存摘要或引用，不是 Authorization 本身，也不是 Permission 来源。

### 2.4 Permission Reference

Permission Reference 应指向某次 Context 下当前有效的执行许可记录。v0.1 `data-contracts.md` 尚未定义独立 Permission Object 或 Permission Reference field table，因此其 canonical schema mapping 状态保持 `Unknown`。

当前实现的 `permission_effect=NONE` 只是禁止权限副作用的 guardrail（护栏），不是 Permission Reference、Permission denial record 或 Permission Object。

## 3. Field Mapping Records（字段映射规则）

| mapping_id | source_schema | target_schema | source_field | target_field | version | compatibility_status | 说明 |
|---|---|---|---|---|---|---|---|
| `DBA-MAP-CAP-001` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityRecord` | `capability_id` | `capability_id` | `v0.1` | `Compatible With Warning` | 同名但当前实现只创建内存声明映射，不证明 canonical ID 已登记 |
| `DBA-MAP-CAP-002` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityRecord` | `entity_id` | `entity_id` | `v0.1` | `Compatible With Warning` | 实现只验证非空，不解析 canonical Entity Identity |
| `DBA-MAP-CAP-003` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/CapabilityContract` | `description` | `capability_name` | `v0.1` | `Compatible With Warning` | Contract 使用标签或引用，可能比完整 description 更窄；禁止无审查重命名 |
| `DBA-MAP-CAP-004` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/CapabilityContract` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityRecord` | `capability_name` | `capability_name` | `v0.1` | `Compatible` | 两层均为可审查标签；仍不证明 Capability truth |
| `DBA-MAP-CAP-005` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityRecord` | `scope` | `scope` | `v0.1` | `Compatible With Warning` | 实现仅要求非空结构，未证明 Architecture 所需对象、时间、资源等维度完整 |
| `DBA-MAP-CAP-006` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityRecord` | `constraints` | `constraints` | `v0.1` | `Compatible With Warning` | 非空检查不证明禁止项、依赖和失败条件完整 |
| `DBA-MAP-CAP-007` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityRecord` | `risk_level` | `risk_level` | `v0.1` | `Compatible With Warning` | 字段意图一致，但受控值存在 `Medium` 与 `MODERATE` 差异 |
| `DBA-MAP-CAP-008` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityRecord` | `verification_status` | `verification_status` | `v0.1` | `Compatible With Warning` | 实现声明记录只允许 `UNVERIFIED/PENDING`，不覆盖完整验证生命周期 |
| `DBA-MAP-CAP-009` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityBoundaryRecord` | `authorization_status` | `capability_state` | `v0.1` | `Unknown` | `AUTHORIZED` state 与 authorization summary 的精确合成规则尚未定义 |
| `DBA-MAP-CAP-010` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityBoundaryRecord` | `authorization_status` | `authorization_reference` | `v0.1` | `Unknown` | 状态与引用被拆分；缺少 canonical Authorization Object/version |
| `DBA-MAP-CAP-011` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/CapabilityBoundaryRecord` | `DBA-ARCHITECTURE-SCHEMA-0.1/PermissionReference` | `permission_effect` | `permission_reference:not_defined` | `v0.1` | `Incompatible` | `NONE` 护栏不是 Permission Reference，禁止当作授权或拒绝记录 |
| `DBA-MAP-CAP-012` | `DBA-ARCHITECTURE-SCHEMA-0.1/CapabilityObject` | `DBA-ARCHITECTURE-SCHEMA-0.1/PermissionReference` | `capability_id` | `permission_reference:not_defined` | `v0.1` | `Incompatible` | Capability identity 不能映射为 Permission |

## 4. Controlled Vocabulary Mapping（受控词表映射）

### 4.1 Risk values

| Architecture value | Implementation value | compatibility_status | 处理 |
|---|---|---|---|
| `unknown` | `UNKNOWN` | `Compatible With Warning` | 只允许表示层大小写规范化；不改变未知语义 |
| `Low` | `LOW` | `Compatible With Warning` | 需显式 versioned representation rule |
| `Medium` | `MODERATE` | `Unknown` | 近义不等于同义；需 Architecture Decision 决定是否等价或新增值 |
| `High` | `HIGH` | `Compatible With Warning` | 需显式 versioned representation rule |
| `Critical` | `CRITICAL` | `Compatible With Warning` | 需显式 versioned representation rule |

没有获批转换规则时，不得把 `Medium` 自动改写为 `MODERATE`，也不得以当前实现词表反向修改 Architecture risk definition。

### 4.2 Capability states

Implementation `DECLARED/VERIFIED/AUTHORIZED` 可以作为 Capability lifecycle 的有界投影，但：

- `DECLARED` 不自动等于 Architecture declaration 已经登记；
- `VERIFIED` 必须引用有范围的 Verification，不等于 Authorized；
- `AUTHORIZED` 必须引用独立 Authorization，不等于 Permission；
- `permission_effect=NONE` 不构成 Permission 状态。

## 5. Implementation-specific Fields（仅实现字段）

以下 DBOS fields 当前没有一对一 Architecture Capability Object field：

- `boundary_record_id`；
- `capability_state`；
- `declaration_reference`；
- `verification_reference`；
- `authorization_reference`；
- `permission_effect`；
- `SUPPORTED_RISK_LEVELS`、`DEFAULT_RISK_LEVEL`、`DEFAULT_VERIFICATION_STATUS`。

这些字段是实现分解或 fail-closed guardrail，不得自动加入 canonical schema。未来若需要规范化，应分别定义 Verification Reference、Authorization Object/Reference 和 Permission Object/Reference，而不是把它们压入 Capability 字段。

## 6. Capability / Authorization / Permission Boundary

```text
Capability Record
  ├─ may reference → Verification Record
  ├─ may reference → Authorization Record
  └─ cannot create/map-to → Permission

Permission Reference
  └─ future separate context-scoped object; currently Unknown / not defined
```

禁止映射：

- `capability_id` → `permission_id`；
- `capability_state=AUTHORIZED` → `permission_status=GRANTED`；
- `verification_status` → Authorization；
- `risk_level` → automatic denial or grant；
- SAEE Risk/Fitness Evaluation → Capability、Authorization 或 Permission state。

## 7. Unknown and Conflict Handling（未知与冲突处理）

1. `description` 与 `capability_name` 信息量不一致时保留两者，不静默覆盖；
2. `Medium/MODERATE` 保持 `Unknown` 映射，直到治理决定；
3. 缺少 Authorization Object/version 时，`authorization_reference` 只作为不透明引用，不证明有效；
4. 缺少 Permission schema 时，不补造 `permission_id/status`；
5. Implementation field 多于 Contract 时标记 implementation-specific，不提升 Contract requirement；
6. 任一映射不得扩大 Capability、Authority、Permission 或 Execution scope。

## 8. Non-effect Status（无效力状态）

```text
CAPABILITY_SCHEMA_MAPPING_DEFINED=true
CAPABILITY_SCHEMA_MAPPING_APPLIED=false
CAPABILITY_DATA_MIGRATED=false
CAPABILITY_INSTANCE_CREATED=false
CAPABILITY_VERIFIED=false
CAPABILITY_AUTHORIZED=false
AUTHORIZATION_CREATED=false
PERMISSION_REFERENCE_DEFINED=false
PERMISSION_GRANTED=false
DBOS_IMPLEMENTATION_CHANGED=false
```

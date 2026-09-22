---
spec_id: DBA-EVIDENCE-SCHEMA-MAPPING-0.1
title: Digital Biosphere Evidence Versioned Schema Mapping v0.1
status: non-executable-schema-mapping-profile
mapping_version: v0.1
canonical_definition: data-contracts.md#6-evidence-object证据对象
contract_profile: research-agent-implementation-contract.md#4-evidence-contract证据契约
implementation_profile: DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1
evidence_effect: none
verification_effect: none
truth_effect: none
---

# Digital Biosphere Evidence Versioned Schema Mapping v0.1

本文件区分 Evidence Material（证据材料）、Evidence Reference（证据引用）和 Canonical Evidence Object（规范证据对象），并映射 Research Agent Contract、Architecture Data Contract 与 DBOS support fields。

```text
Evidence Material ≠ Evidence Reference
Evidence Reference ≠ Canonical Evidence Object
Canonical Evidence Object ≠ Truth
Verification Result ≠ Scientific Validity
```

## 1. Three Evidence Layers（三类证据层）

| 层 | 定义 | 主要来源或 Owner | 不表示 |
|---|---|---|---|
| Evidence Material | 原始输出、过程、工具使用、失败或外部材料；可能支持未来 Evidence collection | Research Agent Contract 定义交付语义；材料来源可为 Entity、人类或外部系统 | 已被 DBOS 登记、完整、可信或正确 |
| Evidence Reference | 指向材料、执行或既有 Evidence 系统的可追溯引用 | Contract/Implementation 可产生引用；引用 Owner 不自动拥有被引用内容 | Canonical Evidence Object 已存在或 integrity 已验证 |
| Canonical Evidence Object | DBOS 采集、登记或封装的有标识、类型、来源、scope、integrity 与 verification boundary 的对象 | DBOS | Truth、科学有效性、Capability、Permission 或高 Fitness |

SAEE 对 Evidence 的解释必须形成新的 Evaluation Object，并引用原 Evidence Object；不得回写或重发 DBOS Evidence。

## 2. Schema Profiles（模式配置）

| layer | schema | 来源 | 边界 |
|---|---|---|---|
| Architecture | `DBA-ARCHITECTURE-SCHEMA-0.1/EvidenceObject` | `data-contracts.md`、`interface-specification.md` | 定义 Canonical Evidence Object meaning 与 DBOS Owner |
| Contract material | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EvidenceMaterialReferences` | `research-agent-implementation-contract.md` | 定义 `raw_output/process/tool_usage/failure` material references |
| Implementation reference | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | DBOS `entity_support/evidence_reference.py` 的只读观察 | 非 canonical Evidence reference mapping |
| Implementation verification reference | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/VerificationReference` | DBOS `entity_support/verification_reference.py` 的只读观察 | `PENDING/V0` reference；不是 verification decision |
| Implementation integration view | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceIntegrationLink` | DBOS `entity_support/evidence_integration.py` 的只读观察 | 只链接引用并声明 zero truth/permission effect |

## 3. Field Mapping Records（字段映射规则）

| mapping_id | source_schema | target_schema | source_field | target_field | version | compatibility_status | 说明 |
|---|---|---|---|---|---|---|---|
| `DBA-MAP-EVID-001` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EvidenceMaterialReferences` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | `raw_output_reference` | `reference` | `v0.1` | `Unknown` | 单一实现字段没有 material role discriminator；不能假设它指 raw output |
| `DBA-MAP-EVID-002` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EvidenceMaterialReferences` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | `process_reference` | `reference` | `v0.1` | `Unknown` | generic reference 无法保留 process role |
| `DBA-MAP-EVID-003` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EvidenceMaterialReferences` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | `tool_usage_reference` | `reference` | `v0.1` | `Unknown` | generic reference 无法保留 tool usage role 与调用状态 |
| `DBA-MAP-EVID-004` | `DBA-RESEARCH-AGENT-CONTRACT-SCHEMA-0.1/EvidenceMaterialReferences` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | `failure_reference` | `reference` | `v0.1` | `Unknown` | generic reference 无法区分 failure、explicit no-failure 与 missing |
| `DBA-MAP-EVID-005` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | `DBA-ARCHITECTURE-SCHEMA-0.1/EvidenceObject` | `reference` | `source_ref` | `v0.1` | `Compatible With Warning` | 只有 provenance、scope、对象类型和 retention 可解析时才能作为 source reference |
| `DBA-MAP-EVID-006` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | `DBA-ARCHITECTURE-SCHEMA-0.1/EvidenceObject` | `evidence_id` | `evidence_id` | `v0.1` | `Unknown` | support module 明确该 ID 属于 reference mapping；未证明 canonical Evidence Object identity |
| `DBA-MAP-EVID-007` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | `DBA-ARCHITECTURE-SCHEMA-0.1/EvidenceObject` | `integrity_status` | `integrity_status` | `v0.1` | `Compatible With Warning` | 实现只允许 `UNKNOWN/PENDING`，不形成 integrity decision |
| `DBA-MAP-EVID-008` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/VerificationReference` | `DBA-ARCHITECTURE-SCHEMA-0.1/EvidenceObject` | `verification_level` | `verification_level` | `v0.1` | `Compatible With Warning` | 当前仅 `V0`，是 reference state，不是 completed verification |
| `DBA-MAP-EVID-009` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/VerificationReference` | `DBA-ARCHITECTURE-SCHEMA-0.1/EvidenceObject` | `verification_status` | `verification_status` | `v0.1` | `Compatible With Warning` | `UNKNOWN/PENDING` 可保留未知，但不能提升为 pass/verified |
| `DBA-MAP-EVID-010` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceReference` | `DBA-ARCHITECTURE-SCHEMA-0.1/ExecutionObject` | `execution_id` | `execution_id` | `v0.1` | `Compatible With Warning` | 只建立引用关系；未证明 Execution Object 已存在、发生或成功 |
| `DBA-MAP-EVID-011` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceIntegrationLink` | `DBA-ARCHITECTURE-SCHEMA-0.1/EvidenceObject` | `canonical_evidence_owner` | `owner:DBOS` | `v0.1` | `Compatible With Warning` | 实现常量是护栏声明，不是 Object Owner adoption evidence |
| `DBA-MAP-EVID-012` | `DBOS-DIGITAL-ENTITY-IMPLEMENTATION-PROFILE-0.1/EvidenceIntegrationLink` | `DBA-ARCHITECTURE-SCHEMA-0.1/EvidenceObject` | `evidence_truth_effect` | `truth_field:not_defined` | `v0.1` | `Incompatible` | `NONE` 护栏不映射为 Truth 字段；Evidence Object 没有全局 truth 属性 |

## 4. Material Reference Preservation（材料引用保留）

Research Agent Contract 的四类 material reference 必须分别保留：

| Contract field | 最低保留语义 | 禁止的默认处理 |
|---|---|---|
| `raw_output_reference` | 未被静默改写的原始输出引用 | 用最终报告覆盖原始输出 |
| `process_reference` | 分析步骤、中间状态、方法和限制 | 只有 output 时推断过程完整 |
| `tool_usage_reference` | 工具、模型、版本、输入、输出和调用状态 | 由工具名称推断结果正确或已授权 |
| `failure_reference` | 失败、异常、冲突、停止或明确无失败状态 | 缺失字段自动解释为无失败；删除失败记录 |

当前 DBOS generic `reference` 字段不能无损表达四种 role。若未来实现需要支持，必须新增有版本的 discriminator 或结构，不得把四个字段折叠后宣称兼容。

## 5. Evidence Reference Boundary（证据引用边界）

Evidence Reference 至少需要：

- 可定位的 reference；
- 被引用对象类别或 `unknown`；
- provenance、scope、version 与 retention status，未知时保留未知；
- 与 Execution 的关系，但该关系不证明执行发生；
- 与 Canonical Evidence Object 的 resolution status（解析状态），不能仅凭同名 `evidence_id` 推断。

```text
Reference exists ≠ referenced material exists
Material exists ≠ canonical Evidence collected
Canonical Evidence exists ≠ integrity verified
Integrity verified ≠ content true
```

## 6. Canonical Evidence Object Boundary（规范证据对象边界）

只有 DBOS 在其 Evidence governance 下采集、登记或封装后，才能形成 Canonical Evidence Object。最低语义来自 `data-contracts.md`：

`evidence_id`、`evidence_type`、`integrity_status`、`verification_level`、`verification_status`、`source_ref`、`scope`。

Architecture Schema 定义这些字段的含义；DBOS 管理运行对象。Mapping document、Contract material、reference builder、路径存在或 local validator PASS 均不能创建该对象。

## 7. Verification and Evaluation Separation（验证与评价分离）

- Verification Reference 只指向验证请求或状态，不是 Verification Result；
- `PENDING/V0` 必须保持 pending/unknown，不能升级；
- Verification Result 不等于 SAEE Evaluation；
- SAEE Evaluation 不得修改 Evidence Object、integrity 或 verification status；
- Evidence、Verification 和 Evaluation 都不授予 Capability、Permission 或 Scientific Validity。

## 8. Unknown and Conflict Handling（未知与冲突处理）

1. 无 material type 时 generic `reference` 保持 `Unknown`；
2. implementation `evidence_id` 无 canonical resolution 时保持 reference-local identity；
3. 缺少 `evidence_type/source_ref/scope` 时不得构造 Canonical Evidence Object；
4. 缺失 `failure_reference` 不得默认为无失败；
5. `UNKNOWN/PENDING/V0` 不得自动升级为 validated/pass；
6. 冲突或撤销通过新记录保留，不删除历史材料或引用。

## 9. Non-effect Status（无效力状态）

```text
EVIDENCE_SCHEMA_MAPPING_DEFINED=true
EVIDENCE_SCHEMA_MAPPING_APPLIED=false
EVIDENCE_DATA_MIGRATED=false
EVIDENCE_MATERIAL_CREATED=false
EVIDENCE_REFERENCE_CREATED=false
CANONICAL_EVIDENCE_OBJECT_CREATED=false
EVIDENCE_TRUTH_CHANGED=false
VERIFICATION_DECISION_CREATED=false
SAEE_EVALUATION_CREATED=false
HISTORICAL_EVIDENCE_CHANGED=false
DBOS_IMPLEMENTATION_CHANGED=false
```

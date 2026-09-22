---
spec_id: TMAI-TELEMETRY-TO-EVIDENCE-ADMISSION-0.1
title: TMAI Telemetry-to-Evidence Admission Contract v0.1
title_zh: TMAI 遥测到证据准入契约 v0.1
status: proposed-pending-dq-021-not-implemented
primary_repository: digital-biosphere-os
architecture_owner: digital-biosphere-architecture
evidence_admission_authorized: false
evidence_object_created: false
verification_object_created: false
production_ready: false
---

# TMAI Telemetry-to-Evidence Admission Contract v0.1

中文：TMAI 遥测到证据准入契约 v0.1。

## 1. Purpose（目的）

本契约定义已被 DBOS Telemetry Admission Foundation 接纳为 material（材料）的观测，如何经过第二个、独立、失败关闭的 Evidence Admission Boundary（证据准入边界），才能创建 canonical Evidence Object（规范证据对象）。

```text
Raw Telemetry != Telemetry Envelope
Telemetry Envelope != Accepted Material
Accepted Material != Evidence
Evidence != Verification
Verification != Truth
Evidence Admission != Governance Decision
Evidence Creation != Permission
```

本契约不实现准入、不创建 Evidence/Verification 实例、不调用 SAEE，也不授权 DBOS 修改。

## 2. Two-stage Admission（两阶段准入）

```text
OTLP / Collector / offline adapter
  → TelemetryObservationEnvelope
  → TelemetryAdmissionRecord
       outcome=ACCEPTED_AS_MATERIAL|PARTIAL|...

Only eligible accepted material
  → EvidenceAdmissionRequest
  → Evidence Admission Validation + Policy
  → EvidenceAdmissionRecord
       outcome=ADMITTED|PARTIAL|REJECTED|HOLD|UNKNOWN
  → canonical Evidence Object (only ADMITTED/PARTIAL policy permits)
  → independent Verification Object
```

两阶段不得合并为 Collector processor、OTLP response flag 或一个 `verified=true` 字段。

## 3. Eligibility Preconditions（进入前置条件）

只有同时满足以下条件的 material 可进入 Evidence Admission Review：

1. `TelemetryAdmissionRecord` 存在、完整且在规范 store 中可解析；
2. outcome 是 `ACCEPTED_AS_MATERIAL` 或按 policy 明确允许的 `PARTIAL`；
3. schema/profile/policy/validator version 在 Evidence admission policy 的 allowlist 中；
4. source digest、Envelope digest、Admission chain 和 receipt continuity 通过；
5. content/material reference 在独立获准的 store 可读；metadata-only 记录若无足够材料，不得伪造内容；
6. target Evidence purpose/type/scope 明确；
7. 所有 Identity、Execution、Capability 和 Authorization 引用均来自现有 DBOS canonical objects，不由 OTel Resource/attributes 生成；
8. sensitive-data classification、retention、access 和 lawful/contractual basis（如适用）已记录；
9. 无 revoked authorization、forbidden capability 或 unresolved identity conflict；
10. 可重现 policy input 齐全，不使用隐式默认填充 unknown。

## 4. EvidenceAdmissionRequest v0.1（证据准入请求）

| field | semantics |
|---|---|
| `request_id` | DBOS 分配的稳定请求 ID；不是 Evidence ID |
| `schema_version` | exact request contract version |
| `telemetry_admission_refs` | 一个或多个 append-only Admission lifecycle 引用 |
| `material_refs` | 受管 material/content references；不内嵌 raw payload |
| `source_digests` | exact material digests；不是 signature/truth |
| `source_attestation_refs` | optional signed attestation/key/certificate/policy references；缺失时必须明示 assurance limitation |
| `provenance_assurance_level` | `P0_UNBOUND`、`P1_TRANSPORT_BOUND`、`P2_SOURCE_SIGNED` 或 `P3_HARDWARE_ATTESTED`；不等于 Truth |
| `target_evidence_type` | 希望形成的 versioned Evidence type |
| `subject_refs` | 已有 Entity/Execution/Capability 规范引用 |
| `authorization_refs` | 本次准入所依据的有效授权/策略引用；不是 Permission 创建 |
| `purpose` | bounded evidence purpose and downstream scope |
| `classification` | public/internal/confidential/restricted 或 versioned equivalent |
| `retention_policy_ref` | 保留、legal hold 和 deletion/supersession 规则 |
| `requested_at` | DBOS time + source |
| `requester_reference` | 调用组件/流程引用；不自动成为 Authority |
| `limitations` | known sampling、drop、partial、clock、identity、content 限制 |

## 5. EvidenceAdmissionRecord v0.1（证据准入记录）

| field | semantics |
|---|---|
| `admission_record_id` | append-only transition record ID |
| `evidence_admission_id` | 一个 Evidence admission lifecycle ID |
| `request_reference` | 指向 immutable request |
| `sequence` / `previous_record_reference` | 严格连续历史 |
| `state` | 本节状态 |
| `policy_ref` / `policy_version` | exact Evidence admission policy |
| `validator_refs` | 实际执行的 validator/version |
| `input_digests` | 请求、Telemetry admission、material 和 canonical subject digests |
| `outcome` | `ADMITTED`、`PARTIAL`、`REJECTED`、`HOLD`、`UNKNOWN` |
| `reason_codes` | stable bounded codes |
| `limitations` | 必须传递且可追加的限制 |
| `evidence_reference` | 仅 successful admission commit 后存在 |
| `verification_refs` | 独立 Verification Object 引用，允许暂缺但必须显式 |
| `recorded_at` | DBOS intake time/source |

State machine（状态机）：

```text
REQUESTED
  → VALIDATING
    → HOLD_REVIEW
    → ADMITTED
    → PARTIAL
    → REJECTED
    → UNKNOWN

After ADMITTED/PARTIAL:
  → VERIFICATION_PENDING
  → VERIFIED_WITH_LIMITATIONS | VERIFICATION_FAILED | VERIFICATION_UNKNOWN

Administrative side states:
  SUPERSEDED | ACCESS_REVOKED | RETENTION_HOLD
```

`ACCESS_REVOKED` 只改变访问或使用策略，不删除历史 Evidence。`VERIFIED_WITH_LIMITATIONS` 不表示 Truth。

## 6. Admission Policy Dimensions（准入策略维度）

| dimension | required question | fail-closed behavior |
|---|---|---|
| identity | subject 是否是已有 DBOS Identity？ | missing/conflict → `HOLD`/`REJECTED` |
| execution | material 是否绑定已有 Execution Object？ | telemetry correlation only → no execution claim |
| authorization | collection/admission/use 是否各自获准？ | expired/revoked/missing → rejected |
| provenance | source path、digests、transforms 是否连续？ | gap → partial/hold/unknown |
| completeness | sampling/drop/partial/retry/duplicate 是否明示？ | hidden/unknown → no completeness claim |
| integrity | bytes/reference/schema 是否在有界检查内一致？ | failed → rejected；unknown → hold |
| privacy | content 是否最小化并符合 classification？ | prohibited field → rejected |
| retention | 保留与 legal hold 规则是否存在？ | missing for restricted data → hold |
| duplication | 是重放、相同 material 还是冲突？ | never silent merge/delete |
| purpose | Evidence 对象支持什么有界命题？ | broad/undefined purpose → rejected |

### 6.1 Provenance Assurance Levels（来源保证等级）

| level | minimum binding | allowed use |
|---|---|---|
| `P0_UNBOUND` | declared source/digest only | diagnostic material; canonical Evidence admission normally rejected or held |
| `P1_TRANSPORT_BOUND` | authenticated transport/workload identity + digest + Collector/admission lineage | bounded internal operational Evidence with explicit limitation |
| `P2_SOURCE_SIGNED` | producer/source signs exact material digest + context under approved key/policy | higher-assurance provenance candidate; still not event Truth |
| `P3_HARDWARE_ATTESTED` | approved workload/hardware attestation binds code/runtime/key/material digest | optional high-assurance profile; separate threat model and verifier required |

High-impact、external publication、identity/capability change、financial/medical/legal use 至少要求 `P2_SOURCE_SIGNED` 或独立 Human Risk Decision。如 producer 不支持加密签名，不得伪造 `P2`；可以停在 `P1` 并限制用途。

Signature/attestation verification 必须记录 algorithm、key ID、trust policy/version、certificate/attestation chain reference、revocation/time result、exact signed bytes canonicalization 和 limitations。有效签名只证明在规则范围内的 signer/material binding，不证明科学正确、事件真实或行为获授权。

### 6.2 Identity Continuity Prerequisite（身份连续前置）

Telemetry-derived Evidence 不得用 OTel Resource 中的 `service.name`、`gen_ai.agent.id`、host/container ID 创建或修复 DBOS Identity。进入 S4 前必须通过 `PR-G2I`：

```text
existing DBOS entity_id resolves
lifecycle permits evidence association
execution_id resolves when execution claim is requested
authorization/collection purpose remains valid
external workload identity mapping is versioned and reviewed
conflict/unknown paths fail closed
```

## 7. Data Governance Gate（数据治理闸门）

每个 Evidence type/profile 在启用前必须有：

- data inventory 与 Owner/Data Steward；
- collection purpose、lawful/contractual basis（如适用）和 prohibited use；
- field-level classification、content minimization 和 access policy；
- region/residency、retention、legal hold、supersession 和 deletion/anonymization process；
- subject access/correction/erasure conflict handling（如适用），同时保留 append-only audit；
- incident/breach notification Owner 和 runbook；
- downstream consumer inventory、SAEE use boundary 和 export restriction；
- policy tests 证明 prohibited/high-risk material 进入 `HOLD`/`REJECTED`。

未完成法律适用性评估时，本 gate 只能记录 `NOT_ASSESSED`，不能因技术加密或签名而推断 compliance（合规）。

## 8. Evidence Object Creation（Evidence Object 创建）

Evidence Object 必须：

1. 分配新 `evidence_id`，不复用 trace/span/admission/request ID；
2. 引用 EvidenceAdmissionRecord、TelemetryAdmissionRecord 和 material refs；
3. 保留 all provenance transforms，不将 Collector 写成原始 producer；
4. 保留 sampling/drop/partial/duplicate/time/schema/privacy limitations；
5. 声明 evidence type、subject、scope、purpose、classification 和 retention；
6. 不嵌入未获准 raw content；
7. 不声称 content truth、scientific validity、authorization 或 Fitness；
8. 更正时产生新 version/superseding record，不改写原对象。

## 9. Verification Separation（验证分离）

Evidence admission 可以要求一组 Verification，但不能自己同时写入“已验证”：

| verification | proves only | does not prove |
|---|---|---|
| schema validation | structure matches exact version | content truth |
| digest validation | observed bytes/ref matches digest scope | producer authenticity unless signature binding exists |
| signature validation | signer/key/policy result | event correctness or authorization |
| provenance continuity | references/transforms are continuous in recorded scope | no missing external event |
| completeness assessment | known drop/sampling/partial state | unobserved events did not occur |
| policy conformance | admission followed exact policy | scientific/legal/global validity |

Verification Object 必须带 rule/version/input/time/verifier/limitations，失败和 unknown 不得被删除或降级为 pass。

## 10. Human Review Gates（人工审查闸门）

以下至少进入 `HOLD_REVIEW`：

- Critical/high-risk capability 相关 material；
- identity/execution/authorization conflict；
- restricted、medical、financial、biometric 或法律保留数据；
- Evidence 用于外部公布、纠纷、惩罚、身份/能力变更；
- partial/unknown 但下游要求 completeness；
- policy/version 迁移或旧证据重验；
- 多个来源冲突且无确定性规则。

Human Review 不得在原 material 中直接写入结论；必须产生独立审查/决策记录。

## 11. SAEE Boundary（SAEE 边界）

SAEE 只能读取：

- canonical Evidence Object；
- independent Verification Object；
- admission/delivery/sampling/privacy limitations；
- exact policy/schema/model versions。

SAEE 不能：

- 将 rejected/hold telemetry 自行提升为 Evidence；
- 修改 EvidenceAdmissionRecord 或 Evidence Object；
- 以 Fitness/Risk 结论补齐缺失事实；
- 自动授权重采集、延长保留或改变访问；
- 直接触发 DBOS state change。

## 12. Failure and Negative Tests（失败与负例）

| case | required outcome |
|---|---|
| OTLP success but no Telemetry Admission Record | no Evidence request |
| `ACCEPTED_AS_MATERIAL` but content ref missing | hold/reject；no fabricated content |
| OTel Resource contains `entity_id` | no identity creation/binding |
| trace/span correlation without Execution Object | no execution claim |
| sampled/dropped/partial hidden | reject or limitations fail closed |
| same material, different provenance | retain both lineages; conflict visible |
| signature valid, authorization revoked | reject use/admission according to policy |
| sensitive canary in content/ref/error | no persistence/log/metric leakage; reject |
| policy changes during request | pinned policy completes or request restarts explicitly |
| DB commit unknown | query idempotency binding; no second Evidence object |
| Verification fails after Evidence creation | append failed Verification; Evidence not deleted or rewritten |
| SAEE attempts writeback/promotion | denied and audited |
| unsigned high-impact material requests `P2` | reject/hold; no assurance upgrade |
| valid signature with revoked/expired/untrusted key | verification failed; no admission |
| signature covers different canonical bytes/context | digest/signature mismatch; reject |
| Collector storage or observability backend claims canonical source | reject owner/authority elevation |
| synthetic P2 signer/key rotation/revocation | exact signed bytes and trust policy validated; old/revoked key fails closed |
| synthetic P3 attestation valid/tampered/replayed/unsupported | bounded verifier result with limitations; no hardware-truth claim |

## 13. Evidence Admission SLO Candidates（证据准入 SLO 候选）

| SLI | candidate target | boundary |
|---|---|---|
| admitted Evidence with complete admission/provenance refs | `100%` | exact eligible admitted set |
| automatic authority/permission elevation | `0` | all requests |
| silent loss of rejected/hold/failure history | `0` | all admission lifecycles |
| duplicate canonical Evidence from same committed idempotency binding | `0` | exact store scope |
| restricted material without classification/retention | `0` | restricted admission requests |
| Evidence created from sampled telemetry without limitation | `0` | telemetry-derived Evidence |

这些是候选目标，尚未测量，不代替 end-to-end SLO。

## 14. Exit Gate（退出闸门）

```text
TELEMETRY_TO_EVIDENCE_CONTRACT_DEFINED=true
EVIDENCE_ADMISSION_IMPLEMENTED=false
EVIDENCE_ADMISSION_AUTHORIZED=false
EVIDENCE_OBJECT_CREATED=false
VERIFICATION_OBJECT_CREATED=false
SAEE_INTEGRATION_AUTHORIZED=false
PR_G2_EVIDENCE_CONFORMANCE_PASS=false
PR_G5_EVIDENCE_SECURITY_PASS=false
PRODUCTION_READY=false
```

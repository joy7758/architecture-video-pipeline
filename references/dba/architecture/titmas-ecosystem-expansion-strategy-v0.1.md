---
document_id: DBA-TITMAS-ECOSYSTEM-EXPANSION-STRATEGY-0.1
title: TITMAS Ecosystem Expansion Strategy v0.1
title_zh: TITMAS 生态扩展战略 v0.1
version: 0.1.0
phase: C6
status: ecosystem-expansion-strategy-defined-no-adoption-claimed
document_type: non-executable-ecosystem-and-adapter-strategy
architecture_domain: TITMAS
observed_at: 2026-07-23
ecosystem_ready: false
adapters_implemented: 0
external_adoptions_verified: 0
external_action_authorized: false
authority_effect: none
---

# TITMAS Ecosystem Expansion Strategy v0.1

## 1. Purpose and Verdict（目的与结论）

本战略定义 TITMAS 与主流 Agent、Telemetry、Tool Protocol 和 Data Space 生态的
reference-only adapter 路线。它不创建 Adapter、不修改外部项目、不提交 PR，也不声称
任何外部采用或认可。

```text
PHASE=C6_ECOSYSTEM_EXPANSION
TITMAS_ECOSYSTEM_EXPANSION_STRATEGY_DEFINED=true
TITMAS_ECOSYSTEM_READY=false
TITMAS_ADAPTERS_IMPLEMENTED=0
TITMAS_EXTERNAL_ADOPTIONS_VERIFIED=0
```

## 2. Adapter Principles（适配器原则）

每个 Adapter/Profile 必须：

1. 绑定 external project、source、exact version/commit 和 observed time；
2. 声明 direction、input/output、supported/partial/unsupported/unknown；
3. 默认 passive、read-only、no-writeback；
4. 保留原始 source、identity、timestamps、failure 和 limitations；
5. 不创建第二 canonical object、Truth、Permission 或 Evaluation；
6. 有 idempotency、retry、duplicate、partial-success 和 compatibility 语义；
7. 把 mapping、implementation、conformance、adoption 和 endorsement 分开；
8. 外部动作必须另行授权。

```text
REFERENCE_ONLY_NE_ADOPTION=true
MAPPING_NE_ADOPTION=true
ADAPTER_NE_AUTHORITY=true
```

## 3. Priority Route（优先路线）

### Priority 1 — Microsoft Agent Governance Toolkit（AGT）

参考面：[microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit)。

候选连接：

- AGT action/policy/audit record → TITMAS interoperability envelope；
- TITMAS External Evaluation Request → AGT read-only evaluator handoff；
- AGT result 作为 candidate material，不能直接写 DBOS；
- AGT runtime enforcement 与 DBOS canonical records 保持独立。

必要负例：

- policy allow/deny 不等于 DBOS Permission；
- audit log 不等于 action outcome 或 Evidence Truth；
- external evaluator output 不触发 Governance Decision；
- Microsoft repository 状态不证明 TITMAS adoption。

当前已有历史 experimental handoff reference，但不构成正式 Integration 或 Adoption。

### Priority 2 — OpenTelemetry

参考面：

- [OpenTelemetry Specification](https://github.com/open-telemetry/opentelemetry-specification)；
- [Document Statuses](https://opentelemetry.io/docs/specs/otel/document-status/)。

候选连接：

- Trace/Metric/Log/Resource/Schema → telemetry material profile；
- OTLP delivery outcome → admission/delivery metadata；
- GenAI Semantic Conventions → exact-version semantic mapping；
- Collector → custom-minimal transport candidate。

必要负例：

- Telemetry 不等于 Evidence；
- OTel Entity 不等于 DBOS Digital Entity；
- Collector ack/health 不等于 durable Evidence、Verification 或 production readiness；
- reference adoption 不等于 runtime adoption。

### Priority 3 — LangChain / LangGraph

参考面：[LangChain framework](https://www.langchain.com/langchain)。

候选连接：

- run/tool/message callbacks → Execution material；
- agent/tool names → non-authoritative identity/capability hints；
- trace/run lineage → context reference；
- error/retry/cancellation → failure semantics。

必要负例：

- framework agent id 不等于 DBOS Identity；
- tool availability 不等于 Capability Verification 或 Permission；
- callback success 不等于 external outcome；
- LangChain integration 不等于 project endorsement。

### Priority 4 — CrewAI

参考面：[CrewAI documentation](https://docs.crewai.com/)。

候选连接：

- crew/agent/task/process events → multi-agent execution envelope；
- delegation/collaboration lineage → Behavior Trace；
- tool and output references → candidate material；
- human approval step → approval reference，不是 DBOS Decision。

必要负例：

- Crew role 不等于 TITMAS/DBOS role；
- task completion 不等于 verified outcome；
- CrewAI AMP deployment 不等于 TITMAS commercial integration；
- Adapter 不创建 Research Agent 或 Runtime。

### Priority 5 — Model Context Protocol（MCP）

参考面：[MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)。

候选连接：

- client/server/session/tool/resource/prompt interactions → Execution/Context material；
- authorization metadata → source authorization reference；
- tool result/error/cancellation → outcome material；
- protocol version → compatibility binding。

必要负例：

- MCP session/client/server identity 不等于 DBOS Identity；
- tool discovery 不等于 Capability Grant；
- MCP authorization 不自动成为 DBOS Permission；
- tool result 不等于 Evidence Truth。

### Priority 6 — Data Space Ecosystem

优先参考
[Eclipse Dataspace Protocol](https://projects.eclipse.org/projects/technology.dataspace-protocol-base)。

候选连接：

- participant/connector identifiers → external identity reference；
- contract negotiation → agreement/authorization material；
- transfer process → execution/delivery material；
- usage policy and lineage → governance/context references。

必要负例：

- data-space identity 不等于 DBOS Entity registration；
- contract agreement 不等于 DBOS Permission；
- transfer success 不等于 data correctness、consent sufficiency 或 Evidence Truth；
- TITMAS 不宣称 data sovereignty、legal compliance 或 Dataspace Protocol authority。

## 4. Adapter Contract Template（适配器契约模板）

```yaml
adapter_profile_id:
external_project:
external_source_ref:
external_version_or_commit:
observed_at:
direction:
input_objects: []
output_objects: []
canonical_owner_preservation:
read_effect: true
write_effect: false
supported: []
partial: []
unsupported: []
unknown: []
failure_semantics:
privacy_security:
conformance_plan:
implementation_status: NOT_AUTHORIZED
adoption_status: NOT_CLAIMED
external_action_status: NOT_AUTHORIZED
```

## 5. Expansion Gates（扩展闸门）

每个生态连接依次需要：

```text
Exact Source Review
  -> Mapping Candidate
  -> Domain/Authority Review
  -> External Integration Decision
  -> Implementation Authorization
  -> Independent Conformance
  -> External Feedback
  -> Adoption Assessment
```

任何上一步 PASS 都不能自动跳过后续步骤。

## 6. Ecosystem Readiness Criteria（生态就绪标准）

`TITMAS_ECOSYSTEM_READY=true` 至少要求：

- 两类以上独立生态有版本绑定 Adapter/Profile；
- 至少两个外部维护者/实现者提供可归因反馈；
- 至少两个独立实现完成 conformance；
- compatibility、security、privacy 和 deprecation 可运行；
- 没有第二 Authority、Truth 或 writeback；
- 外部项目没有反对或名称/商标冲突；
- Human Architecture Decision 复核。

当前均未形成足够直接证据。

## 7. Human Decision Candidates（人工决定候选）

| ID | Candidate scope | Current recommendation |
|---|---|---|
| `EE-D01` | AGT exact-version read-only mapping review | `PREPARE_SOURCE_REFRESH_ONLY` |
| `EE-D02` | OpenTelemetry exact-version telemetry-material profile | `REFERENCE_REVIEW_ONLY` |
| `EE-D03` | LangChain/LangGraph execution-material mapping | `DEFER_UNTIL_SPEC_OWNER` |
| `EE-D04` | CrewAI multi-agent event mapping | `DEFER_UNTIL_SPEC_OWNER` |
| `EE-D05` | MCP 2025-11-25 context/tool boundary mapping | `PREPARE_SECURITY_REVIEW_ONLY` |
| `EE-D06` | Eclipse Dataspace Protocol participant/contract mapping | `DEFER_UNTIL_DATA_GOVERNANCE_OWNER` |

这些决定只允许准备 exact-version mapping review，不授权 Adapter implementation、外部 PR、
运行连接、采用声明或 external project endorsement。

## 8. Final State（最终状态）

```text
TITMAS_ECOSYSTEM_EXPANSION_STRATEGY_DEFINED=true
TITMAS_ECOSYSTEM_TARGETS_DEFINED=6
TITMAS_ECOSYSTEM_READY=false
TITMAS_ADAPTERS_IMPLEMENTED=0
TITMAS_EXTERNAL_INTEGRATIONS_ACTIVE=0
TITMAS_EXTERNAL_ADOPTIONS_VERIFIED=0
REFERENCE_ONLY_NE_ADOPTION=true
EXTERNAL_PR_CREATED=false
EXTERNAL_ACTION_AUTHORIZED=false
```

---
profile_id: DBA-EXECUTION-CONTEXT-TRUST-INVALIDATION-0.1
title: Execution-Context Trust Invalidation Profile v0.1
title_zh: 执行上下文信任失效剖面 v0.1
status: accepted-dba-governance-profile
primary_repository: DBA
observed_at: 2026-08-01
supersedes: none
extends: ../2026-07-29/capability-provenance-reassessment-profile.md
decision_reference: ../../architecture/ADR-039-verified-correction-and-execution-context-continuity.md
implementation_authorized: false
downstream_implementation_required: false
---

# Execution-Context Trust Invalidation Profile v0.1

## 1. Purpose（目的）

本剖面定义：当模型名称或工件 revision 未变化，但执行环境足以改变可观察能力、工具效果、
攻击面或停止行为时，既有 readiness、reliability、safety 或 trust conclusion（信任结论）
不得自动继承。

它扩展 2026-07-29 的 Capability Provenance Reassessment Profile，不创建第二套扫描器、
遥测系统、评价引擎、策略执行器、Permission service 或 Truth store。

```text
PROFILE_ADOPTED=true
OUTPUT_IS_REASSESSMENT_ROUTING_ONLY=true
OUTPUT_CAN_CHANGE_RUNTIME_STATE=false
OUTPUT_CAN_REVOKE_PERMISSION=false
IMPLEMENTATION_AUTHORIZED=false
```

## 2. Assessed Capability Identity（受评能力身份）

一次可继承的结论至少绑定：

```text
model_or_agent_artifact_ref
exact_revision_and_configuration_digest
evaluation_harness_ref_and_digest
system_and_task_prompt_digest
safety_policy_and_refusal_configuration_ref
network_egress_policy_ref
sandbox_and_filesystem_policy_ref
credential_scope_manifest_ref
tool_and_mcp_server_manifest_ref
negotiated_protocol_versions
runtime_and_dependency_manifest_ref
execution_style_or_orchestrator_ref
monitoring_and_alerting_profile_ref
stopping_and_human_intervention_profile_ref
evidence_retention_and_replay_profile_ref
assessed_purpose_and_risk_class
observed_at
```

缺失字段保留为 `UNKNOWN`，不得用模型名称、供应商、benchmark 分数或平台页面代替。

## 3. Invalidation Triggers（失效触发器）

| trigger_id | 变化 | 默认结果 |
|---|---|---|
| `EC-01-HARNESS` | benchmark、reward、tool loop、budget、retry 或 completion rule 变化 | `REASSESSMENT_REQUIRED` |
| `EC-02-PROMPT-SAFETY` | system prompt、policy、refusal 或 guardrail 变化 | `REASSESSMENT_REQUIRED` |
| `EC-03-NETWORK` | egress、proxy、package registry、DNS 或 external target reachability 变化 | `HOLD_MISSING_EVIDENCE` |
| `EC-04-SANDBOX` | process、container、filesystem、kernel、isolation 或 escape surface 变化 | `HOLD_MISSING_EVIDENCE` |
| `EC-05-CREDENTIAL` | token、secret、delegation、tenant、scope 或 lifetime 变化 | `REVIEW_REQUIRED` |
| `EC-06-TOOLS-PROTOCOLS` | tool／MCP server、A2A peer、negotiated version 或 extension 变化 | `REASSESSMENT_REQUIRED` |
| `EC-07-RUNTIME` | dependency、custom code、hardware、region 或 deployment profile 变化 | `REASSESSMENT_REQUIRED` |
| `EC-08-EXECUTION-STYLE` | Default／ReAct／ReAct Core、planner、memory 或 orchestrator 变化 | `REASSESSMENT_REQUIRED` |
| `EC-09-MONITORING` | logging、detector、alerting、review coverage 或 retention 变化 | `HOLD_MISSING_EVIDENCE` |
| `EC-10-STOPPING` | timeout、budget cap、kill switch、human checkpoint 或 stop semantics 变化 | `REVIEW_REQUIRED` |

## 4. Decision States（决定状态）

```text
NOT_TRIGGERED
  -> REASSESSMENT_REQUIRED
     -> HOLD_MISSING_EVIDENCE
     -> REVIEW_REQUIRED
     -> REVALIDATED_BOUNDED
     -> INVALIDATED_FOR_DECLARED_SCOPE
```

- `REVALIDATED_BOUNDED` 只对精确 context manifest、用途、风险级别和时间窗口有效；
- `INVALIDATED_FOR_DECLARED_SCOPE` 只废止结论继承，不删除历史证据，不撤销权限，不执行停止；
- Permission、Runtime action、Release 和 Human Decision 仍使用各自 authority surface；
- evidence receipt、signature、trace 或 registry record 不自动证明结论真实或充分。

## 5. Minimum Machine Contract（最小机器契约）

已采纳的最小文档契约；独立机器 Schema 和 Runtime enforcement 尚未实现：

```json
{
  "prior_conclusion_ref": "string",
  "prior_context_manifest_digest": "sha256:string",
  "current_context_manifest_digest": "sha256:string",
  "changed_dimensions": ["EC-03-NETWORK"],
  "source_refs": ["string"],
  "unknowns": ["string"],
  "result": "REASSESSMENT_REQUIRED",
  "scope": "string",
  "authority_effect": "NONE",
  "reviewed_at": "RFC3339"
}
```

## 6. Upstream Consumption and De-duplication（上游消费与去重）

| upstream | 消费什么 | 本剖面不做什么 |
|---|---|---|
| Microsoft AGT／IBM control plane | policy、identity、asset、runtime 和 change observations | 不复制策略执行、资产扫描或集中控制 |
| OpenTelemetry／LangSmith／Phoenix | versioned trace、evaluation 和 runtime observations | 不复制 collector、trace backend 或 evaluator |
| MCP／A2A | negotiated protocol、tool／peer manifest 和 lifecycle fields | 不创建协议分叉、Gateway 或 Agent runtime |
| SPIFFE／SPIRE | workload identity and trust-domain material | 不把 workload identity 升级为 persona、business intent 或 permission |
| SCITT | signed statement、registration receipt 和 history | 不把透明登记升级为 statement truth |
| DBOS／SAEE | 未来可能提供的 canonical references 和只读评价输入 | 不修改两个子项目的事实、状态或权力 |

## 7. Agent Recommendation Gate（智能体推荐闸门）

```text
AGENT_RECOMMENDATION=CONDITIONALLY_RECOMMENDED
RECOMMENDED_AS=BOUNDED_VENDOR_NEUTRAL_CONCLUSION_INVALIDATION_CONTRACT
NOT_RECOMMENDED_AS=CONTROL_PLANE_OBSERVABILITY_BACKEND_COMPLIANCE_ENGINE_OR_CERTIFIER
```

本剖面已经由 `ADR-039` 采纳为 DBA governance profile。任何下游实现仍必须满足独立用户
需求、重复建设审查、canonical Owner、输入数据最小化、负例、rollback、人工 decision
gate 和对应 implementation／execution authorization；不因治理采纳自动创建 Runtime。

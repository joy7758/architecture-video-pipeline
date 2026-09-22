---
map_id: DBA-EXECUTION-CONTEXT-COMPETITIVE-RESEARCH-CROSSWALK-2026-08-01
title: Execution-Context Competitive and Research Crosswalk
title_zh: 执行上下文竞争与研究交叉映射
status: governance-semantics-adopted-no-runtime-implementation
observed_at: 2026-08-01
primary_repository: DBA
implementation_authorized: false
---

# Execution-Context Competitive and Research Crosswalk

## 1. Upstream map（上游地图）

| upstream | 已覆盖的强项 | 本剖面允许保留的窄缺口 | 禁止重复建设 |
|---|---|---|---|
| Microsoft Agent Governance Toolkit `v4.1.0` Public Preview | policy、identity、capability、sandbox、MCP gateway、audit、SRE | 跨供应商“旧结论是否失效”的只读契约 | 第二套 Agent OS、policy engine、sandbox、Gateway 或 SRE 平台 |
| IBM watsonx governance／Orchestrate | asset discovery、control plane、AgentOps、migration、execution style | migration 前后评价继承规则 | 企业资产扫描器、集中控制塔或 Agent builder |
| OpenTelemetry semantic conventions `1.43.0` | trace、metric、log 语义与 GenAI／MCP 观测字段 | 从版本化观测到结论失效状态的映射 | collector、backend、通用 telemetry schema |
| A2A `v1.0.1` | Agent Card、通信、任务生命周期 | 对端、卡片、协议或工具变化触发重评 | A2A 分叉或新通信协议 |
| SPIFFE／SPIRE | workload identity、SVID、trust domain | workload identity 与业务／能力结论的非等同边界 | 第二套工作负载身份基础设施 |
| SCITT RFC 9943 | signed statements、transparent registration、history | statement history 作为来源输入但不升级为 truth | 透明日志或 supply-chain registry |

## 2. Research map（研究地图）

| paper | 作者主张范围 | 对 DBA 的价值 | 保留限制 |
|---|---|---|---|
| `arXiv:2607.08906v1` Proof-of-Continuity | 因果链与 non-expansive authority propagation | 为 credential／delegation 变化提供 authority-continuity 参考 | 预印本；关注授权传播，不替代身份、评价或 Evidence Truth |
| `arXiv:2607.14890v1` Proof-or-Stop | evidence-gated lifecycle control 与 false-DONE 抑制 | 为结论失效后的 fail-closed 状态提供研究参考 | 预印本；作者报告的单模型族与自托管语料限制必须保留 |
| `arXiv:2606.04990v4` Evidence Tracing survey | typed execution graph 与 evidence-support projection | 提供 trace／provenance 分类和开放问题地图 | 综述不是实现、标准、评价权或采用证据 |

## 3. Differentiation test（差异化检验）

```text
BUILD_NEW_AGENT_GOVERNANCE_PLATFORM=false
BUILD_NEW_ASSET_DISCOVERY_SYSTEM=false
BUILD_NEW_OBSERVABILITY_BACKEND=false
BUILD_NEW_INTEROP_PROTOCOL=false
BUILD_NEW_TRANSPARENCY_LOG=false
RETAIN_EXECUTION_CONTEXT_CONCLUSION_INVALIDATION_SEMANTICS=true
```

如果任何上游形成同等或更成熟的 vendor-neutral conclusion invalidation contract，正确动作是
映射、贡献接口或停止自建，不以 TITMAS 品牌维持重复引擎。

## 4. Recommendation（推荐结论）

```text
AGENT_RECOMMENDATION=RECOMMENDED_FOR_DBA_GOVERNANCE_USE
CONDITION=SOURCE_VERIFICATION_PLUS_NON_DUPLICATION_PLUS_FAIL_CLOSED_SCOPE
CURRENT_IMPLEMENTATION_DECISION=NO_RUNTIME_IMPLEMENTATION_REQUIRED
```

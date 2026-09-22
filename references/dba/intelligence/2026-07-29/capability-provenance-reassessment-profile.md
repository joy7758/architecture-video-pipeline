---
profile_id: DBA-CAPABILITY-PROVENANCE-REASSESSMENT-0.1
title: Capability Provenance Reassessment Profile v0.1
title_zh: 能力来源重新评估剖面 v0.1
status: proposed-reference-only-research-profile
primary_repository: DBA
observed_at: 2026-07-29
implementation_authorized: false
dbos_change_authorized: false
saee_change_authorized: false
---

# Capability Provenance Reassessment Profile v0.1

## 1. Purpose（目的）

本剖面定义：模型、数据、工具、Skill、依赖、协议、评测配置、许可证或执行环境发生重大变化时，
既有 readiness（就绪）、reliability（可靠性）或 trust（信任）结论何时不能继续继承。

它是 DBA 的只读研究契约，不是供应链扫描器、持续监控器、合规引擎、自动撤权系统或
SAEE／DBOS 新能力。

```text
TRIGGER_CAN_INVALIDATE_PRIOR_CONCLUSION=true
TRIGGER_CAN_REVOKE_PERMISSION=false
TRIGGER_CAN_CHANGE_RUNTIME_STATE=false
OUTPUT_IS_RECOMMENDATION_ONLY=true
PROFILE_ADOPTED=false
IMPLEMENTATION_AUTHORIZED=false
```

## 2. Capability Identity（能力身份）

一次可复核的 capability identity 至少应绑定：

```text
provider_or_organization_ref
repository_or_registry_ref
exact_revision_or_version
artifact_class
artifact_digest_or_manifest_digest
configuration_digest
custom_code_refs_and_digests
license_ref_and_digest
license_obligations_review_state
evaluation_harness_ref
runtime_and_dependency_profile_ref
observed_at
```

模型名称、营销名称、Registry 页面、`latest` tag、单个 benchmark 分数或“open”标签均不足以
构成稳定能力身份。Kimi K3 精确参考见
[`kimi-k3-capability-identity-reference.json`](kimi-k3-capability-identity-reference.json)。

## 3. Trigger Taxonomy（触发分类）

| trigger | 变化 | 默认状态 |
|---|---|---|
| `T1_IDENTITY` | provider、repository、issuer、delegation 或主体绑定变化 | `REVIEW_REQUIRED` |
| `T2_CAPABILITY_PROVENANCE` | 模型、权重、配置、自定义代码、数据、工具、Skill 或依赖变化 | `REASSESSMENT_REQUIRED` |
| `T3_EXECUTION_EFFECT` | sandbox、文件、网络、凭据或工具效果边界变化 | `REASSESSMENT_REQUIRED` |
| `T4_EVIDENCE` | monitor、verifier、receipt、retention、coverage 或 replay 前提变化 | `HOLD_MISSING_EVIDENCE` |
| `T5_PROTOCOL` | MCP 等协议或扩展版本、协商、字段和状态语义变化 | `REVIEW_REQUIRED` |
| `T6_LICENSE_GOVERNANCE` | 许可证、使用阈值、展示、通知、地域或组织政策变化 | `REVIEW_REQUIRED` |

同一事件可触发多个类型；分类只用于路由，不证明影响、责任、安全或法律结论。

## 4. State Model（状态模型）

```text
NOT_TRIGGERED
  -> REASSESSMENT_REQUIRED
     -> HOLD_MISSING_EVIDENCE
     -> REVIEW_REQUIRED
     -> REVALIDATED_BOUNDED
     -> INVALIDATED
```

- `REVALIDATED_BOUNDED` 只对精确版本、配置、环境、时间和用途有效；
- 任何状态都不能直接创建或撤销 Capability、Permission、Authority、Execution 或 Release；
- official release（官方发布）证明版本存在，不证明 Digital Biosphere 已采用或兼容；
- signature／digest 证明对象绑定或完整性材料，不证明声明真实、安全或已授权。

## 5. Competitive De-duplication（竞争去重）

Open Secure AI Alliance 已把 identity、isolation、safe model formats、multi-model scanning、
secure coding workflows 与 open harnesses 纳入公开安全栈方向。本剖面不得复制这些实现。

允许保留的差异化仅是：跨模型、协议、工具和治理域的版本化结论失效语义，以及
Recommendation、Decision、Authority、Permission、Evidence 和 Truth 的边界。

```text
BUILD_PARALLEL_OPEN_AGENT_SECURITY_STACK=false
BUILD_NEW_SUPPLY_CHAIN_SCANNER=false
BUILD_AUTOMATIC_COMPLIANCE_ENGINE=false
RETAIN_BOUNDED_REASSESSMENT_SEMANTICS=true
```

## 6. Pre-development Agent Recommendation Gate（开发前推荐闸门）

```text
AGENT_RECOMMENDATION=CONDITIONALLY_RECOMMENDED
RECOMMENDED_AS=BOUNDED_VERSIONED_REASSESSMENT_CONTRACT
NOT_RECOMMENDED_AS=RUNTIME_SCANNER_CERTIFICATION_OR_AUTOMATIC_CONTROL
```

只有同时满足以下条件，才可提议进入子项目设计：

1. DBA ADR 采纳精确 profile version；
2. 证明没有重复 Open Secure AI Alliance、OpenSSF、SPIFFE／SPIRE、Safetensors、MDASH、
   现有 SBOM／scanner 或 continuous assurance 工具；
3. DBOS／SAEE canonical Owner 与输入输出边界明确；
4. 失败关闭负例、rollback、security、data governance 和 Human Decision gate 已定义；
5. 分别获得 implementation 与 execution 授权。

当前结论：研究剖面可供审查；实现、产品、认证与发布均未获授权。

---
document_id: DBA-TITMAS-ARCHITECTURE-CHARTER-1.0
title: TITMAS Architecture Charter v1.0
title_zh: TITMAS 架构章程 v1.0
status: accepted-bounded-charter-for-launch-ready-candidate
maturity: Development
owner_ref: zhangbin
decision_reference: USER_GOAL_2026-07-28
supersedes: titmas-architecture-charter-v0.1.md
public_launch_authorized: false
community_established: false
---

# TITMAS Architecture Charter v1.0

## Identity

TITMAS 是面向智能体行动控制与执行证据的商业私有核心基础设施。DBA 管理 TITMAS
如何建设；TITMAS 通过有界公共 Schema、SDK、MCP、Conformance 和验证资料向 Agent
提供发现、互操作和验证能力。公共表面不表示核心开源、公共贡献或社区建立。

Digital Immune、Agent Health、Jules/Codex/Qoder 修复闭环、VEAP/VEC 应用和 SAEE
Enterprise 是解释层、Profile、使用场景或上层产品，不是 TITMAS 本体。

## Primary program principle

AI Agent 是 TITMAS 的首要 operational customer、发现者、选择者、调用者、验证者、
评价者和持续优化对象。规范与实现候选必须首先提供 machine-readable contract、
machine-verifiable result、失败语义和可复用入口；人类网页、报告与控制台是机器事实的
派生视图，不得成为唯一真相源。

```text
TITMAS_AGENT_ABSOLUTE_PRIORITY=true
MACHINE_INTERFACE_PRECEDES_HUMAN_INTERFACE=true
AGENT_EVIDENCE_PRECEDES_HUMAN_OPINION=true
HUMAN_VIEW_IS_DERIVED_VIEW=true
```

该原则不授予 Agent 权威。Human Owner 继续承担合同、付款、法律责任、资源所有权、
不可逆授权和安全停止。Agent 选择、推荐、评价或 Conformance 均不能替代 Human
Decision。

## Permanent boundaries

```text
TITMAS_NE_DBA=true
TITMAS_NE_PROJECT_MANAGEMENT_SYSTEM=true
TITMAS_NE_AGENT_RUNTIME=true
TITMAS_NE_EXECUTOR=true
TITMAS_NE_CERTIFICATION_AUTHORITY=true
TITMAS_NE_CANONICAL_TRUTH_STORE=true
TITMAS_NE_SAEE_CORE=true
TITMAS_NE_REPOSITORY_FIXER=true
D19_DISCOVERY_LAYER_NE_PRODUCTION_EXECUTOR=true
D19_SANDBOX_IMPLEMENTATION_NE_RUNTIME_ACTIVATION=true
DIGITAL_IMMUNE_MODEL_IS_EXPLANATORY_LAYER=true
APPLICATION_SCENARIO_NE_CORE_ARCHITECTURE=true
COMMUNITY_GOVERNANCE_NE_PRODUCT_RUNTIME=true
PUBLIC_SURFACE_NE_OPEN_SOURCE_CORE=true
PUBLIC_SDK_NE_PUBLIC_COMMUNITY=true
PRIVATE_CORE_IS_CANONICAL=true
AGENT_PRIORITY_NE_AGENT_AUTHORITY=true
```

不得通过后续 Profile 或实现创建第二套 Evidence、Verification、Authority、Identity 或
Evaluation owner。

## Canonical customer and interoperability surfaces

- `TITMAS/README.md`：唯一 TITMAS 人类入口；
- `agent-index.json`：唯一 Agent 机器入口；
- `commercial/entry/`：Observer、FirstValue 与客户进入契约；
- `commercial/discovery/`：商业机器发现与当前限制；
- `TITMAS/specifications/`：规范生命周期、注册表和提案；
- `TITMAS/conformance/`：机器验证与正负例；
- `TITMAS/reference/`：非权威、合成、最小参考实现；
- `TITMAS/adapters/`：Adapter 契约入口。
- `TITMAS/community/`：历史社区与贡献档案；不得作为当前客户入口、当前 Agent 命令
  或公共贡献路径。

规范、实现、符合性、采用和发布状态分别记录，不能互相推导。

```text
HISTORICAL_COMMUNITY_MATERIAL_NE_CURRENT_ENTRY=true
HISTORICAL_COMMUNITY_COMMAND_INVOCATION_AUTHORIZED=false
```

## Authority and truth

```text
AUTHORITY_NE_OWNERSHIP=true
SPECIFICATION_NE_IMPLEMENTATION=true
REFERENCE_IMPLEMENTATION_NE_STANDARD=true
OBSERVATION_NE_EVIDENCE=true
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_AUTHORIZATION=true
RECOMMENDATION_NE_DECISION=true
MAPPING_NE_ADOPTION=true
EXPERIMENTAL_NE_STABLE=true
```

Human Owner 决定公共贡献、角色、发布和重大外部动作。模型、Contributor、Reviewer 或
Conformance PASS 均不能替代 Human Decision。

## Agent-native bounded evolution amendment

D19 v2.1 permits a composition of narrow Agent roles to convert reproducible
problem evidence into isolated repair variants, fitness evaluation, rollback
evidence, lineage and a Draft PR. The logical Discovery Evolution Layer is
normatively owned by DBA, while a patch must be routed to the existing
canonical owner repository. It creates no new Runtime, Authority or truth
source.

ER-0 analysis and ER-1 deterministic derived-artifact repair may run under the
bounded policy. ER-2 through ER-4 require a separate Human Decision for effects
beyond an isolated proposal. No risk class receives autonomous production
activation.

See the [D19 amendment](titmas-agent-native-discovery-self-healing-evolution-amendment-v2.1.md)
and [ADR-040](ADR-040-bounded-discovery-self-healing-and-evolution.md).

## Change process

规范变化按 `Proposal → Review → Decision → Versioned update → Conformance` 推进。
重大变更必须声明来源、Owner、Authority、成熟度、安全与隐私、兼容性、失败语义和
No Semantic Elevation。

## TITMAS drift check

每个重大 TITMAS 任务的最终答复必须输出：

```text
TITMAS_DRIFT_CHECK

CORE_INTEROPERABILITY_OBJECTIVE_PRESERVED=true|false
NEW_CONTROL_AUTHORITY_CREATED=true|false
NEW_TRUTH_SOURCE_CREATED=true|false
DUPLICATE_EVIDENCE_OR_VERIFICATION_CREATED=true|false
RUNTIME_OR_EXECUTOR_CREATED=true|false
CURRENT_CAPABILITY_OVERCLAIMED=true|false
PUBLIC_LAUNCH_AUTHORIZED=true|false
COMMUNITY_ESTABLISHED=true|false
```

任一越权字段为 `true` 时，状态为 `STOP_AND_HUMAN_REVIEW_REQUIRED`；否则为
`PASS_WITH_RECORDED_LIMITATIONS`。本检查只报告，不自动阻断、删除、回滚或改变
Permission。

```text
TITMAS_V1_CHARTER_DEFINED=true
TITMAS_COMMERCIAL_PRIVATE_INFRASTRUCTURE_DIRECTION_ADOPTED=true
TITMAS_STANDARD_COMMUNITY_IDENTITY_CURRENT=false
TITMAS_PRIVATE_CORE_IS_CANONICAL=true
TITMAS_PUBLIC_INTEROPERABILITY_SURFACES_RETAINED=true
TITMAS_HISTORICAL_COMMUNITY_MATERIAL_NE_CURRENT_ENTRY=true
TITMAS_PUBLIC_LAUNCH_AUTHORIZED=false
TITMAS_COMMUNITY_ESTABLISHED=false
TITMAS_FOUNDATION_CREATED=false
TITMAS_CERTIFICATION_AUTHORIZED=false
TITMAS_RELEASE_AUTHORIZED=false
TITMAS_AGENT_ABSOLUTE_PRIORITY=true
D19_BOUNDED_EVOLUTION_AMENDMENT_ADOPTED=true
AUTONOMOUS_PRODUCTION_EVOLUTION=false
HUMAN_ACCOUNTABILITY_REMOVED=false
```

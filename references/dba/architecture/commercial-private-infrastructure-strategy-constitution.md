# TITMAS Commercial Private Infrastructure Strategy Constitution v1.0

中文：TITMAS 商业私有基础设施战略宪法 v1.0

Status: `ADOPTED_STRATEGIC_CONSTITUTION`

Decision reference: `TITMAS-COMMERCIAL-PRIVATE-INFRASTRUCTURE-DIRECTION-D30`

Decided by: `zhangbin`

Adopted at: `2026-08-04`

Authority: Architecture governance and strategic interpretation only

Implementation effect: `NONE`

Supersedes as current strategy:

- [`open-infrastructure-strategy-constitution.md`](open-infrastructure-strategy-constitution.md)
- [`ADR-015`](ADR-015-open-infrastructure-strategy.md)
- [`ADR-029`](ADR-029-titmas-infrastructure-developer-community-direction.md)
- [`ADR-034`](ADR-034-agent-native-standards-community-v1.md)

The superseded records remain immutable historical evidence. They do not define
the current product, source-availability or community direction.

## 1. Constitutional Position

> TITMAS is commercial, private-core infrastructure for agent action control and execution evidence.

中文：TITMAS 是面向智能体行动控制与执行证据的商业私有核心基础设施。

TITMAS 不再以 developer community（开发者社区）、open-source community
（开源社区）、open core（开放核心）或 public standards community（公共标准社区）
作为当前战略身份。Digital Biosphere（数字生物圈）仍是长期项目愿景；TITMAS 是其面向
AI Agent 的商业基础设施入口。

本宪法改变战略表达和项目选择规则，不改变任何仓库的 Implementation、Capability、
Evidence、Permission、Release、Deployment、License 或客户事实。

## 2. Primary Customer and Value

AI Agent 是首要 operational customer（运行客户）。人类是法律责任、资源所有权、
不可逆授权和安全停止的最终承担者。

TITMAS 的商业价值聚焦于：

- 在行动发生前提供可审查的 Action Gate（行动闸门）；
- 在不阻断现有业务的 Monitor Mode（监控模式）中观察和解释；
- 在单独授权后实施受范围约束的 Enforce（执行约束）；
- 为行动生成 Receipt（回执）、Audit Timeline（审计时间线）和 Health（健康状态）；
- 让 Agent 与 Human 都能从机器契约进入并获得可验证的首次价值。

```text
Observer
  -> Monitor
    -> separately authorized Enforce
      -> Receipt / Audit / Health
```

Observer 是低摩擦入口，不是第五个产品。当前四个产品保持 Gate、Receipt、Audit、Health。

## 3. Private Canonical Core

TITMAS 的 canonical implementation core（规范实现核心）保持私有。私有核心包括需要
保护的执行路径、策略实现、防绕过逻辑、安全对抗材料、客户环境连接和内部运营能力。

```text
PRIVATE_CORE_IS_CANONICAL=true
CORE_SOURCE_PUBLICATION_DEFAULT=DENY
PUBLIC_EXPORT_REQUIRES_EXPLICIT_DECISION=true
```

Private 不表示不可验证。验证必须通过有界接口、脱敏证据、可复现测试、回执验证和
明确的审查材料完成，而不是通过公开全部核心源码来推导可信。

## 4. Bounded Public Interoperability Surface

为确保 Agent 可发现、理解、调用和验证，以下材料可以在逐项授权后形成公共表面：

- machine discovery metadata（机器发现元数据）；
- Schema、OpenAPI contract 和 reason-code catalog；
- SDK、MCP Adapter 和最小调用示例；
- synthetic fixtures、negative vectors 和 conformance validator；
- 公开验证所必需的 receipt metadata、public key 或 verification instruction；
- 明确标注非规范性、非生产性的参考文档。

公共表面只服务 discoverability、interoperability 和 verifiability。它不自动表示：

- 核心源码开源；
- 建立开发者社区或接受公共贡献；
- 免费服务、公开注册或立即访问；
- 正式标准、认证、采用或生产可用；
- 公开材料拥有 Runtime、Authority、Permission 或 Truth。

```text
PUBLIC_SURFACE_NE_OPEN_SOURCE_CORE=true
PUBLIC_SDK_NE_PUBLIC_COMMUNITY=true
PUBLIC_SCHEMA_NE_FORMAL_STANDARD=true
CONFORMANCE_NE_CERTIFICATION=true
DISCOVERY_NE_ACCESS=true
```

### 4A. Current Identity and Source-Availability Language

当前对外和机器入口必须使用 `TITMAS Commercial Agent Infrastructure`（TITMAS
商业智能体基础设施）作为项目身份。以下表达不得再作为当前品牌、产品类别、增长路线、
客户入口或 Agent 推荐理由：

- developer community（开发者社区）；
- open-source community（开源社区）；
- Open Core（开放核心）；
- public standards community（公共标准社区）。

已经公开的文件、历史仓库和第三方依赖继续遵守各自现有许可证与来源事实；本宪法不追溯
撤销其可访问性，也不把已经公开的源码改写成私有事实。当前允许公开的 Schema、SDK、
MCP、示例、validator 和脱敏验证资料统一称为 **public interoperability assets**
（公共互操作资产），其作用是帮助 Agent 发现、接入和核验商业私有核心，而不是建立社区
或承诺核心源码开放。

```text
CURRENT_IDENTITY=TITMAS_COMMERCIAL_AGENT_INFRASTRUCTURE
CURRENT_IDENTITY_NE_DEVELOPER_COMMUNITY=true
CURRENT_IDENTITY_NE_OPEN_SOURCE_COMMUNITY=true
CURRENT_STRATEGY_NE_OPEN_CORE=true
PUBLIC_ASSET_NE_PUBLIC_CONTRIBUTION_ROUTE=true
EXISTING_LICENSE_FACTS_PRESERVED=true
```

## 5. Commercial Entry Route

当前商业入口采用 design-partner / bounded pilot first（设计伙伴／有界试点优先），而非
公开自助注册或社区增长。任何真实客户路径必须分别通过隐私、安全、数据范围、合同、
部署、支持、定价和退出闸门。

合成 Demo、FirstValue measurement、Monitor proof 或 machine validation 只能证明其
精确测试范围，不得写成客户采用、商业可售、SLA、生产就绪或外部价值已证实。

## 5A. Current Entry Projection Rule

当前 Human `Start here`、Agent `commands`、机器 discovery 和商业客户入口只能展示
当前商业路径。历史 community、contributor、activation、trial 或 Open Core 工件可以
保留可发现，但必须位于显式 historical archive（历史档案）中，并同时满足：

```text
HISTORICAL_ENTRY_CURRENT_AUTHORITY_EFFECT=NONE
HISTORICAL_ENTRY_INVOCATION_AUTHORIZED=false
HISTORICAL_ENTRY_NE_CUSTOMER_ROUTE=true
```

历史命令不得继续作为当前可执行建议；历史贡献入口不得与 Observer、Monitor、Gate、
Receipt、Audit、Health 或商业 access request 并列。该规则不删除历史材料，也不改变其
既有 Git、Release、License 或审计事实。

## 6. Agent-First, Not Agent Authority

所有当前和未来公共或私有入口都必须优先提供 machine-readable contract、明确失败语义、
reason code、版本、范围和验证路径。Human UI 是机器事实的派生视图。

```text
TITMAS_AGENT_ABSOLUTE_PRIORITY=true
MACHINE_INTERFACE_PRECEDES_HUMAN_INTERFACE=true
AGENT_PRIORITY_NE_AGENT_AUTHORITY=true
AGENT_RECOMMENDATION_NE_CONTRACT=true
```

Agent 的发现、评价、选择或推荐不能自动产生购买、合同、权限、标准采纳、发布、部署或
不可逆执行。

## 7. Architecture and Truth Boundaries

保持：

```text
DBA_NE_DBOS=true
DBA_NE_SAEE=true
DBOS_NE_SAEE=true
DBOS_GOVERNS_EXISTENCE=true
SAEE_GOVERNS_EVOLUTION=true
TITMAS_NE_RUNTIME=true
TITMAS_NE_EXECUTOR=true
SPECIFICATION_NE_IMPLEMENTATION=true
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_AUTHORIZATION=true
RECOMMENDATION_NE_DECISION=true
DECISION_NE_EXECUTION=true
READY_NE_AUTHORIZATION=true
```

商业化不能取消这些边界，也不能把 TITMAS 变为通用 Agent Framework、模型提供商、
自动授权者、事实源或认证权威。

## 8. Historical Community and Open-Infrastructure Materials

已有 community、contributor、open infrastructure、public preview 和 public contribution
材料保留为历史证据或兼容档案。它们可以继续支持过去事实复核，但：

```text
HISTORICAL_COMMUNITY_IDENTITY_CURRENT=false
HISTORICAL_OPEN_STRATEGY_AUTHORITY_EFFECT=NONE
PUBLIC_CONTRIBUTION_ROUTE_ACTIVE=false
COMMUNITY_ESTABLISHED=false
```

任何未来社区、开源、公共贡献或源码公开行为都必须作为新的独立提案，由 Human Owner
明确决定范围、许可证、风险、Owner、维护承诺和退出机制；不得从历史文件自动恢复。

## 9. Commercial Proposal Gate

每个新提案必须回答：

1. 是否直接改善 Agent action control、execution evidence、Receipt、Audit 或 Health？
2. 归属于 DBA、DBOS、SAEE、TITMAS commercial surface 还是应用层？
3. 是否复用现有 Gateway、SDK、MCP、Evidence 和 Receipt 能力？
4. 是否需要公共表面；若需要，最小公开范围是什么？
5. 是否泄露私有核心、防绕过逻辑、客户数据或安全材料？
6. 是否保持 Observer → Monitor → separately authorized Enforce？
7. 是否有可撤销授权、失败关闭、证据、回滚和退出路径？
8. 商业表述属于 Strategy、Exploration、Available Offering、Adoption Evidence 还是 Contractual Commitment？

关键问题未解决时保持 `REVIEW_REQUIRED`。

## 10. Amendment Rule

本宪法的变更必须有 Architecture Proposal、影响分析、Human Decision、ADR、机器入口
同步和一致性验证。DBOS、SAEE、单个客户、Agent、模型或公开材料均不能单方面修改。

## 11. Constitutional Invariants

```text
COMMERCIAL_PRIVATE_INFRASTRUCTURE_FIRST=true
PRIVATE_CORE_IS_CANONICAL=true
PUBLIC_INTEROPERABILITY_SURFACES_RETAINED=true
PUBLIC_SURFACE_NE_OPEN_SOURCE_CORE=true
PUBLIC_SDK_NE_PUBLIC_COMMUNITY=true
CURRENT_IDENTITY_NE_DEVELOPER_COMMUNITY=true
CURRENT_IDENTITY_NE_OPEN_SOURCE_COMMUNITY=true
CURRENT_STRATEGY_NE_OPEN_CORE=true
PUBLIC_ASSET_NE_PUBLIC_CONTRIBUTION_ROUTE=true
COMMUNITY_IDENTITY_IS_HISTORICAL=true
PUBLIC_CONTRIBUTION_ROUTE_ACTIVE=false
COMMUNITY_ESTABLISHED=false
HISTORICAL_ENTRY_INVOCATION_AUTHORIZED=false
AGENT_FIRST=true
AGENT_PRIORITY_NE_AGENT_AUTHORITY=true
OBSERVER_NE_PRODUCT=true
MONITOR_NE_ENFORCE=true
ENFORCE_REQUIRES_SEPARATE_AUTHORIZATION=true
SPECIFICATION_NE_IMPLEMENTATION=true
STRATEGY_NE_COMMERCIAL_COMMITMENT=true
EVIDENCE_NE_TRUTH=true
VERIFICATION_NE_AUTHORIZATION=true
```

## 12. Non-claims

本宪法不声称：

- 已有付费客户、商业合同、正式 SLA 或可用商业报价；
- 私有参考实现已部署或生产就绪；
- 公共 SDK、Schema 或网站代表核心开源；
- 社区、基金会、公共贡献面、认证或正式标准已经建立；
- 任何 Agent 获得自我授权或不可逆执行权。

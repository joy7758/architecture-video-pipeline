# Digital Biosphere Developer Ecosystem Strategy v0.1

Status: `SUPERSEDED_HISTORICAL_STRATEGY`

Current authority effect: `NONE`

Superseded by:

- [Commercial Private Infrastructure Strategy Constitution](commercial-private-infrastructure-strategy-constitution.md)
- [ADR-042](ADR-042-commercial-private-infrastructure-direction.md)

Implementation effect: `NONE`

Historical constitution: [Open Infrastructure Strategy Constitution](open-infrastructure-strategy-constitution.md)

> 本文保留早期 Developer Ecosystem First 路线及其设计依据。它不再定义当前产品身份，
> 不授权公共贡献、社区重启、核心源码公开或免费服务。当前公共 SDK、Schema、MCP、
> 文档和 validator 只按商业私有基础设施宪法承担有界互操作功能。

## Objective

Developer Ecosystem First（开发者生态优先）意味着：DBOS 的基础设施价值首先通过开发者能否理解、验证、组合和替换其协议与工具来衡量，而不是通过内置 Agent 数量或单一应用功能数量来衡量。

## Developer Journey

```text
Discover
  -> Understand Protocol
    -> Validate Locally
      -> Integrate through SDK or Tooling
        -> Build an Industry Agent
          -> Share an Extension or Service
```

该路径是体验目标，不是现有产品能力声明。

## Ecosystem Surfaces

### Developer

核心参与者是 Agent developer、Digital Entity implementer、governance integrator 和 verification tool builder。Developer 不因集成 DBOS 自动获得 Authority、Permission、Certification 或生态成员资格。

### Protocol

协议层应满足：

- 公开、版本化、可引用；
- 数据对象和职责边界清晰；
- 兼容性与 breaking change 明示；
- 不绑定单一 Foundation Model、Agent framework 或云厂商；
- Specification 与 Implementation 分离。

### SDK

SDK 的战略职责是降低正确实现开放协议的成本。任何未来 SDK 应：

- 保留协议语义，而不是引入私有事实；
- 默认 fail closed；
- 暴露 Identity、Capability、Permission、Execution 和 Evidence 的差异；
- 允许替换底层模型、Runtime 和存储；
- 不自动创建 Agent、Entity、Capability 或 Permission。

当前文档只定义 SDK 方向，不承诺 SDK 已存在、稳定或受支持。

### Developer Tools

优先工具类型：

- schema 和 contract validation；
- local conformance checks；
- lifecycle 与 authorization boundary inspection；
- evidence/reference integrity checks；
- compatibility and migration diagnostics；
- agent-readable discovery and examples。

验证工具可以拒绝无效记录，但不能自动批准身份、能力、权限、科学结论或治理决策。

### Reference Implementation

Reference Implementation 应证明最小协议可实现性和边界行为，不应演变为唯一官方 Runtime 或全功能 Agent 平台。

必须明确区分：

```text
Toy Example
Local Reference
Conformance Fixture
Release Candidate
Production Deployment
```

前一级状态不能自动升级为后一级事实。

### Community

社区增长应围绕开放协议、互操作实现、问题报告、conformance fixture 和可复核设计讨论形成。

社区贡献不得通过合并代码自动获得：

- Architecture Authority；
- DBOS Operational Authority；
- SAEE Evolution Authority；
- Certification Authority。

### Marketplace

未来 Marketplace 可以作为 extension、tool、industry adapter 和 governance service 的发现与分发层。

Marketplace listing（上架）不等于：

- DBOS 核心组成；
- 安全或合规认证；
- Capability Verification；
- Permission Grant；
- 商业成功或官方背书。

当前 Marketplace 仅为战略概念，不是已实现产品。

## Two-Ecosystem Model

| Ecosystem | Primary participants | Expected outputs | Boundary |
|---|---|---|---|
| Agent Developer Ecosystem | Agent developers, protocol implementers, tool builders | Agents, adapters, SDKs, validators, reference implementations | Applications remain separate from DBOS core |
| Governance Service Ecosystem | Audit, compliance, industry adaptation and certification-service partners | Deployments, reviews, integrations and bounded service claims | Service judgment is not Evidence Truth or architecture authority |

## Developer-first Prioritization Test

项目进入 DBOS roadmap 前应至少满足三项：

1. 多个应用或 Agent 类型可以复用；
2. 能以开放 contract 或 validator 表达；
3. 不依赖单一模型、Runtime、行业或供应商；
4. 降低开发者正确实现治理边界的成本；
5. 能通过本地、可重复、fail-closed 测试验证。

只服务单一客户工作流的功能默认属于 Industry Solution，而不是 DBOS Core。

## Ecosystem Health Signals

未来可以观察但不得预先宣称的信号包括：

- independent protocol implementations；
- validator reuse；
- SDK integration success；
- compatibility issue resolution；
- community-maintained adapters；
- enterprise deployments with attributable evidence。

下载量、GitHub star、demo 数量或 Agent 名称数量不能单独证明生态采用或可信性。

## Non-claims

本文不创建 SDK、Marketplace、Community program、Agent、Runtime、Entity、Capability 或 Permission，不承诺发布日期、支持等级、采用规模或商业可用性。

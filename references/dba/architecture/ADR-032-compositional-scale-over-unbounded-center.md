# ADR-032: Compositional Scale Over an Unbounded Center

中文：以组合式规模替代无限强中心

- Status: `ACCEPTED`
- Decision date: `2026-07-26`
- Decided by: `zhangbin`
- Review reference: `DBA-CONSTITUTION-REVIEW-20260726-001`
- Authority effect: `NONE`
- Implementation authorization: `false`

## Context

Digital Biosphere 面向长期运行、协作和可验证的数字主体。若把系统能力集中到一个
无限强、不可替换、不可审计的中心，身份、能力、执行、证据、评价和治理会形成单点
控制与单点失效，也会使项目逐渐偏向 Foundation Model、通用 Agent 或封闭平台。

另一方面，“不建设无限强中心”不能被误读为取消架构治理、运行治理或协调机制。
大量简单主体的组合仍可能产生隐式权力、级联失败、不可见耦合和系统级风险。

## Decision

Digital Biosphere 采纳 Compositional Scale Principle（组合式规模原则）：

> Digital Biosphere does not pursue an unbounded, all-powerful center. It
> achieves broad system coverage through the auditable structural composition
> of many simple, bounded, interoperable digital entities and services.

中文：

> Digital Biosphere 不追求制造单一、无限强的中心，而通过大量职责简单、边界受限、
> 接口可组合的数字主体与服务，在可审计、可追溯、可隔离、可降级的结构组合中形成
> 系统级覆盖能力。

有限治理与协调仍然存在。任何单体或组合都不得因规模、连接或涌现而自动获得超出
显式范围的 Authority、Permission、Decision、Truth Ownership 或全局控制权。

## Required Boundaries

1. Simple Entity（简单主体）不等于 Ungoverned Entity（不受治理主体）。
2. Composition（组合）不等于 Authority Aggregation（权力聚合）。
3. Coverage（覆盖能力）不等于 Correctness、Verification 或 Truth。
4. Emergent Capability（涌现能力）不自动产生 Capability Grant、Permission 或执行权。
5. Coordination component（协调组件）可以存在，但必须边界有限、可替换、可撤销且可审计。
6. 组合级行为、风险和失效必须能够被观察、记录、验证并按既有职责进入评价和治理。
7. 应优先使失败局部化；组合不得依赖隐藏的全局状态或不可追溯的控制链。

## Architectural Consequences

- 优先采用职责小、接口清楚、可替换的主体与服务；
- 使用开放 Protocol、Schema、Adapter contract 和显式 lineage（来源链）连接主体；
- DBOS 继续治理存在、生命周期、执行记录、Evidence 与 Verification；
- SAEE 继续在只读、有来源的数据边界内进行评价和演化建议；
- DBA 继续维护有限的项目群与架构治理，不成为智能、执行或运行控制中心；
- 系统级能力必须从组合事实中验证，不能由单体声明或架构叙事推定；
- 组合增加覆盖范围时，应同步评估耦合、级联失败、协调瓶颈和权力漂移。

## Alternatives Considered

### A. Build an increasingly powerful central intelligence

Rejected. 该方案增加单点控制、供应商锁定、不可替换性和职责吞并风险，并使项目偏离
可信多智能体基础设施。

### B. Remove all central governance and coordination

Rejected. 该方案会使身份、接口、责任、版本、风险和变化无法形成一致边界。

### C. Bounded composition with finite governance

Accepted. 该方案保留必要治理和协调，同时把智能、执行与领域能力分布在可审计、
可替换的简单主体及其显式组合中。

## Review

Architecture Review 使用三个独立模型进行边界审查：

- `kimi-k2.6`: `ACCEPT_WITH_CONDITIONS`
- `glm-5.2`: `ACCEPT_WITH_CONDITIONS`
- `deepseek-v4-flash`: `ACCEPT_WITH_CONDITIONS`

共同条件已经纳入本 ADR：保留有限治理、禁止组合自动聚合权力、审查组合级风险、
防止协调组件演变为隐藏的无限强中心。

## Non-effects

本决策：

- 不创建 Agent、Entity、Runtime、Capability、Permission 或 Digital Organism；
- 不授权实现、部署、实验、发布或外部采用；
- 不修改 DBOS 或 SAEE 的能力事实、证据事实或责任边界；
- 不声称组合规模已经实现、验证或达到生产就绪；
- 不把 Architecture Authority 变成 Operational Authority 或 Evolution Authority。

```text
UNBOUNDED_CENTRAL_INTELLIGENCE_IS_NOT_TARGET=true
COMPOSITIONAL_SCALE_IS_STRATEGIC_DEFAULT=true
SIMPLE_ENTITY_NE_UNGOVERNED_ENTITY=true
COMPOSITION_NE_AUTHORITY_AGGREGATION=true
COORDINATION_NE_UNBOUNDED_CENTER=true
COVERAGE_NE_CORRECTNESS_OR_TRUTH=true
EMERGENT_CAPABILITY_NE_AUTOMATIC_PERMISSION=true
IMPLEMENTATION_AUTHORIZED=false
AUTOMATIC_AUTHORITY_EFFECT=NONE
```

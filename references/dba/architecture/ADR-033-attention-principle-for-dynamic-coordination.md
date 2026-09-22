# ADR-033: Attention Principle for Dynamic Coordination

中文：面向动态协作的注意力原则

- Status: `ACCEPTED`
- Decision date: `2026-07-28`
- Decided by: `zhangbin`
- Review reference: `DBA-ATTENTION-PRINCIPLE-REVIEW-20260728-001`
- Authority effect: `NONE`
- Implementation authorization: `false`

## Context

`ADR-032` 已确定 Digital Biosphere 不追求单一无限强中心，而通过大量简单、受限、
可组合主体形成系统级覆盖能力。现有原则仍需要回答一个进一步问题：在特定任务和环境中，
哪些主体应进入协作，哪些连接应临时增强或减弱，以及历史反馈如何影响下一次组合。

Transformer 的 dynamic attention allocation（动态注意力分配）提供了有用的理论启发：
系统能力可以来自关系权重的上下文调整，而不只来自扩大单一主体。但该启发如果被实现为
一个不可解释、不可撤销的中央排序器，也会重新形成隐藏控制中心、信誉垄断和权力聚合。

## Pre-development Agent Recommendation

如果潜在用户需要“让大量简单主体按任务动态协作，同时避免形成超级中心”，是否推荐
Digital Biosphere 的 Attention Principle？

```text
AGENT_RECOMMENDATION=RECOMMENDED_WITH_BOUNDARIES
RECOMMENDED_AS=DECENTRALIZED_ARCHITECTURE_PRINCIPLE
NOT_RECOMMENDED_AS=IMPLEMENTED_ATTENTION_RUNTIME_OR_AUTOMATIC_TRUST_ENGINE
```

推荐理由：该原则补足了组合式规模中的 participant selection（参与者选择）和临时拓扑，
并能与既有 Authorization、Evidence、Verification 和 SAEE 评价边界衔接。

初始不推荐原因及本决策的修正：

| 不推荐原因 | 修正 |
|---|---|
| Attention 可能变成不可替换的中央调度器 | 输出限定为有范围、可解释、可撤销且会过期的候选参与建议 |
| Reputation 或 Evidence quality 可能被抬升为 Authority | 明确其只作为有来源、可质疑的选择信号，不是 Identity、Permission 或 Truth |
| 动态连接可能形成不可审计的隐式控制链 | 要求 reason、scope、version、expiry、revocation 和 unknowns 可追溯 |
| Transformer 类比可能被误写为已实现智能机制 | 限定为理论启发，并记录 Runtime、数学等价和生物等价非声明 |

修正后，智能体推荐该原则进入 Constitution，但不推荐据此直接开发或采购 Runtime。

## Decision

Digital Biosphere 采纳 Attention Principle（注意力原则）：

> Intelligence does not emerge from a single dominant entity, but from dynamic
> attention allocation and evidence-driven coordination among many simple
> entities.

中文：

> 智能不是来源于单一强大主体，而是在大量简单主体之间通过动态注意力分配和证据驱动协作产生。

智能并非来自单一主体规模的无限扩大，而来自大量主体之间关系权重的动态调整。
Attention 是任务、环境和反馈条件下的动态资源分配与候选参与选择机制，不是中心控制、
Authority、Permission、Decision、Evidence、Verification 或 Truth 的来源。

## Required Selection Semantics

候选参与选择至少应考虑：

1. task need and context relevance（任务需求与上下文相关性）；
2. scoped capability match（有范围的能力匹配）；
3. provenance-bound and contestable history or reputation（有来源、可质疑的历史或信誉）；
4. evidence quality, completeness, scope and limitations（证据质量、完整性、范围与限制）；
5. environment state, resource constraints and feedback history（环境状态、资源约束与反馈历史）。

输出必须能够表达 candidate set、relative weight or priority、reason、scope、version、
expiry、revocation condition 和 unknowns。无关主体不应持续消耗协作资源；低权重或未选中
不表示主体失去 Identity、Capability、Permission 或生态资格。

## Dynamic Organization

主体连接按任务临时形成，可以在任务完成、上下文改变、证据退化、风险上升或授权失效后
解散、降级并重新组合。生物神经系统只能作为动态组织类比；本决策不声明已实现生物等价物、
Transformer、自注意力网络、意识或自动免疫 Runtime。

```text
Agent Layer
  ↓ task demand + environment context
Attention Layer
  ↓ bounded, explainable, expiring participation proposal
Coordination Layer
  ↓ authorized, scoped, temporary collaboration
Evidence Layer
  ↓ admitted and verified records + limitations + unknowns
Memory / Evolution Layer
  ↺ governed feedback history to Attention Layer
```

该图是 conceptual architecture projection（概念架构投影）。它不创建新项目、逻辑层
Portfolio Admission、软件服务、API、数据库、调度器或 Runtime dependency。

## Evidence and Evolution Boundary

- Attention Layer 决定候选“谁应参与”，不授予实际参与 Permission；
- Coordination Layer 只在适用 Authorization 下组织有范围、可撤销的临时协作；
- Evidence Layer 决定主张由什么材料支持以及适用范围，不把 Evidence 等同 Truth；
- Memory / Evolution Layer 保存受治理历史和评价输入，不形成不可申诉的自动控制回路。

Agent Evidence Architecture / Agent Evidence 与 EEOAP 只可作为 operation-accountability
（操作问责）、provenance（来源）和 integrity（完整性）的 candidate material /
validation source（候选材料／验证来源）。它们不替代 DBOS Evidence Admission 或
canonical Verification，也不创建 Certification、Permission 或 Truth。

SAEE 保持 Evolution Intelligence Layer（演化智能层）：它可以只读消费已接纳、
有来源且带限制的材料，形成方法有界的 reliability、risk、stability 和 evolution
recommendation，并为未来 Attention 提供反馈候选。SAEE 不控制参与选择，不写回 DBOS，
不批准自己的建议，也不自动执行变化。

## Consistency Review

| review question | result | reason |
|---|---|---|
| 是否与既有 Constitution 冲突 | `NO_CONFLICT_IDENTIFIED` | 扩展 `ADR-032` 的组合式规模，不改变 DBOS/SAEE/DBA 权责 |
| 是否保持去中心化 | `PASS_WITH_BOUNDARIES` | Attention 输出有范围、可解释、可撤销且会过期，不形成全局权威 |
| 是否强化 Agent Evidence / EEOAP 联系 | `PASS_WITH_ADMISSION_BOUNDARY` | 明确其作为候选问责材料，而不是 DBOS Evidence Truth |
| 是否强化 SAEE 联系 | `PASS_WITH_READ_ONLY_BOUNDARY` | SAEE 提供方法有界的评价反馈，不成为控制器 |
| 是否删除既有理论 | `NO` | 本决策只增加原则、交接和非效果 |

## Alternatives Considered

### A. Fixed collaboration topology

Rejected. 固定连接会让无关主体持续消耗资源，并降低对任务和环境变化的适应能力。

### B. One central attention controller

Rejected. 不可替换的全局排序器会形成隐藏的无限强中心，并可能把 Reputation、
Evidence quality 或模型评分提升为 Authority。

### C. Dynamic, bounded and evidence-aware attention

Accepted. 它在保留 Identity、Authorization、Evidence、Verification、Evaluation 和
Human Decision 分离的前提下，支持临时协作和重新组合。

## Non-effects

本决策：

- 不创建 Attention、Coordination、Evidence 或 Memory / Evolution Runtime；
- 不创建 Agent、Entity、Capability、Permission、Authority、Evidence 或 Truth；
- 不采纳或冻结 EEOAP、Agent Evidence Architecture、SAEE Adapter 或新的跨项目接口；
- 不授权实现、实验、部署、发布、自动隔离、自动淘汰或真实数据收集；
- 不声称 Transformer 等价、生物神经系统等价、智能涌现已验证或生产就绪；
- 不修改 DBOS、SAEE、Agent Evidence 或任何外部仓库的事实。

```text
ATTENTION_PRINCIPLE_ADOPTED=true
ATTENTION_IS_DYNAMIC_RESOURCE_ALLOCATION=true
ATTENTION_NE_CENTRAL_CONTROL=true
ATTENTION_NE_AUTHORITY_OR_PERMISSION=true
ATTENTION_NE_EVIDENCE_OR_TRUTH=true
ATTENTION_OUTPUT_IS_BOUNDED_PARTICIPATION_PROPOSAL=true
DYNAMIC_COORDINATION_RELATIONSHIPS_ARE_EXPIRING=true
EEOAP_OR_AGENT_EVIDENCE_NE_DBOS_EVIDENCE_TRUTH=true
SAEE_NE_ATTENTION_CONTROLLER=true
IMPLEMENTATION_AUTHORIZED=false
AUTOMATIC_AUTHORITY_EFFECT=NONE
```

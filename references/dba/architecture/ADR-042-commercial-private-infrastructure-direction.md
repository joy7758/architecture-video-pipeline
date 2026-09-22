# ADR-042: Commercial Private Infrastructure Direction

中文：商业私有基础设施方向

Status: `ACCEPTED`

Decision ID: `TITMAS-COMMERCIAL-PRIVATE-INFRASTRUCTURE-DIRECTION-D30`

Decided by: `zhangbin`

Date: `2026-08-04`

## Context

DBA 的现行入口仍把 TITMAS 描述为 Agent-Native Standards Community、Developer
Ecosystem First 和 Open Core。此表达来自较早的开放生态路线，但当前 canonical core
保持私有，D29 已把产品价值收敛到 Agent action control、execution evidence、Gate、
Receipt、Audit、Health 和低摩擦 Observer/Monitor 入口。

继续把社区或开放核心写成当前身份，会让 Agent、客户、合作方和内部开发产生错误预期：
公共 SDK 或 Schema 可能被误解为核心源码开源，历史贡献材料可能被误解为开放贡献，
架构规范可能被误解为免费公共服务或正式标准。

开发前 advisory Agent review 结论为 `CONDITIONALLY_RECOMMENDED`：商业价值路线可推荐，
但必须先消除 Open Core、Community Growth 与当前私有核心边界之间的冲突，并清楚分离
公共互操作表面和私有执行基础设施。该评价只提供建议，不产生 Authority。

## Decision

1. 采纳 [`TITMAS Commercial Private Infrastructure Strategy Constitution v1.0`](commercial-private-infrastructure-strategy-constitution.md) 作为当前战略宪法。
2. TITMAS 当前规范身份改为 `TITMAS Commercial Agent Infrastructure`，中文为
   `TITMAS 商业智能体基础设施`。
3. 私有 canonical core 是当前实现和商业路线；公开材料仅按独立授权承担发现、互操作和
   验证功能。
4. Developer community、open-source community、Open Core 和 public standards
   community 降为历史策略，不再是当前身份或增长前提。
5. 历史 ADR、社区材料、Issue、PR 和状态不得删除或改写；其当前 authority effect 为
   `NONE`，除非未来 Human Decision 明确恢复某个有界范围。
6. Agent-first、DBOS/SAEE 边界、Evidence/Truth 边界和 Human irreversible authority
   保持不变。

## Supersession

本 ADR supersede（取代）以下记录的“当前战略效力”，但不删除其历史事实：

- ADR-015 Open Infrastructure Strategy；
- ADR-029 Infrastructure Developer Community Direction；
- ADR-034 Agent-Native Standards Community；
- Open Infrastructure Strategy Constitution v0.3。

## Consequences

- 新提案优先证明商业 Agent 基础设施价值，而不是社区规模或开源数量；
- 公共 Schema、SDK、MCP、文档和验证器可以保留，但必须明确其公开范围和非推导边界；
- 社区目录和状态文件成为历史档案／兼容面，不再是当前主入口；
- 公开源码、公共贡献、社区重启、Foundation、认证和正式标准均需未来独立决定；
- 现有许可证和已公开历史材料不因本 ADR 被追溯修改。

## Alternatives Considered

### Continue Open Core + Community First

Rejected as current strategy because it conflicts with private-core canonical
implementation and creates source-availability and contribution expectations.

### Remove all public surfaces

Rejected. Agent discoverability, interoperability and receipt verification need
bounded public contracts and tools. Public interoperability does not require a
public core or community.

### Rename only

Rejected. Changing the title without updating proposal gates, machine entries,
status projections and supersession rules would preserve the same ambiguity.

## Non-effects

```text
IMPLEMENTATION_AUTHORIZED=false
RELEASE_AUTHORIZED=false
DEPLOYMENT_AUTHORIZED=false
COMMERCIAL_OFFER_AUTHORIZED=false
CUSTOMER_ACCESS_AUTHORIZED=false
CORE_SOURCE_PUBLICATION_AUTHORIZED=false
PUBLIC_CONTRIBUTION_AUTHORIZED=false
COMMUNITY_ESTABLISHED=false
LICENSE_CHANGED=false
DBOS_CHANGED=false
SAEE_CHANGED=false
```

## 2026-08-04 Post-adoption Entry Residue Review

Exact reviewed base: `main@7808b9d20fb09a3223a3e4c26c2d70061b179a9a`.

The current constitution and identity were already corrected, but the Human
`Start here` still presented contribution guides beside current commercial
entry points, and the canonical Agent entry still exposed `community_cli.py`
discovery, ranking and eligibility commands as active commands.

An independent `qwen3.8-max` advisory review returned
`CONDITIONALLY_RECOMMENDED`: it recommended removing those paths from the active
entry or placing them behind an explicit non-operational historical archive.
The advice created no Authority. The bounded correction keeps the files and
their Git history, moves their references into an archive projection, and fixes
the current entry without changing any Runtime, product, License or customer
fact.

```text
CURRENT_COMMERCIAL_ENTRY_CLEANUP_REQUIRED=true
HISTORICAL_COMMUNITY_FILES_DELETED=false
HISTORICAL_COMMUNITY_CURRENT_AUTHORITY_EFFECT=NONE
HISTORICAL_COMMUNITY_INVOCATION_AUTHORIZED=false
IMPLEMENTATION_AUTHORIZED=false
RELEASE_AUTHORIZED=false
DEPLOYMENT_AUTHORIZED=false
```

## 2026-08-04 Current-language Residue Correction

对当前入口的后续扫描确认：核心宪法、统一 Human 入口和 canonical Agent 入口已经采用商业
私有基础设施身份；残留风险集中在旧 Agent-native README、静态 `llms.txt`、网站派生文案
和私有平台架构说明中。这些表面仍可能把历史 community flow（社区流程）误读为当前路线。

本次修正不删除历史社区文件、不改变既有许可证，也不把公开互操作资产变为私有事实。
它只执行本 ADR 已接受的战略：把当前用语统一为 commercial private infrastructure
（商业私有基础设施）和 public interoperability assets（公共互操作资产），并将旧社区
命令明确标记为不可调用的历史材料。

```text
CURRENT_LANGUAGE_RESIDUE_CORRECTED=true
HISTORICAL_COMMUNITY_FILES_DELETED=false
EXISTING_LICENSE_FACTS_PRESERVED=true
PUBLIC_INTEROPERABILITY_ASSETS_RETAINED=true
COMMUNITY_ROUTE_REACTIVATED=false
CORE_SOURCE_PUBLICATION_AUTHORIZED=false
PUBLIC_CONTRIBUTION_AUTHORIZED=false
```

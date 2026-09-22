---
id: TITMAS-DEC-20260801-MEDIA-EVIDENCE-PORTFOLIO-001
title: TITMAS Media Evidence Portfolio Admission Decision v0.1
title_zh: TITMAS 媒体证据项目组合接纳决定 v0.1
status: ACCEPTED
decision_type: PORTFOLIO_ADMISSION
classification: ADJACENT_CANDIDATE
normative: false
decided_by: ZHANGBIN
decided_at: 2026-08-01
---

# TITMAS 媒体证据项目组合接纳决定 v0.1

## 1. Admission（接纳内容）

Human Program Owner `ZHANGBIN` 决定将 TITMAS Media Evidence 纳入 Digital
Biosphere 项目组合，状态为：

```text
ADJACENT_CANDIDATE
相邻候选项目
```

接受的架构分类为：

```text
APPLICATION_PROFILE_AND_REFERENCE_IMPLEMENTATION_CANDIDATE
应用场景配置与参考实现候选
```

本决定只关闭项目组合准入闸门，不把候选升级为核心组件、规范、标准、运行时、生产系统、
认证体系或已采用方案。

## 2. Implementation snapshot（实现快照）

```text
IMPLEMENTATION_VERSION=v0.1.0
IMPLEMENTATION_TAG_COMMIT=7eac452f66a2b7de525543f80b9a7cf1465ef9a1
CANONICAL_REPOSITORY=joy7758/titmas-media-guard
CANONICAL_STATUS_SOURCE=governance/project-status.json
GOVERNANCE_SOURCE_REVISION=6ded0dd0d81f8a9fc0fe029f96906cc7bc43f446
```

实现仓库是当前规范事实源。DBA 只保存带版本和时间边界的只读引用，不复制或覆盖实现
仓库的 Schema、Validator、测试、发布或工作树事实。

## 3. Non-equivalence boundary（不等同边界）

```text
MediaEvidenceObject
  != DBA canonical Evidence Object
  != DBOS canonical Evidence Object
  != Truth
  != Identity
  != Permission
  != Legal Evidence
```

`MediaEvidenceObject` 继续是 domain-local evidence-bearing record（领域本地承载证据
的记录）。本决定不创建新的 Evidence authority（证据权威）。

## 4. Mapping boundary（映射边界）

DBOS mapping（DBOS 映射）仍未授权。任何未来映射必须通过独立 Evidence Admission
Contract（证据准入契约），并分别记录 source、version、scope、owner、failure、unknown、
conflict、integrity 和 authorization boundary。

```text
DBOS_MAPPING_AUTHORIZED=false
EVIDENCE_ADMISSION_CONTRACT_CREATED=false
MAPPING_IMPLEMENTED=false
CROSS_PROJECT_CONFORMANCE_EXECUTED=false
```

## 5. Authority boundary（权力边界）

本决定不创建或授权：

- 新证据权威；
- DBOS module、Runtime、API、SDK 或生产服务；
- 认证机构、身份认证或内容真伪判断；
- 规范或标准地位；
- 客户采用、商业授权或生产部署；
- 法律证据效力。

项目组合接纳是 program-governance classification（项目群治理分类），不是运行、实现、
发布、采用或 Permission（权限）决定。

## 6. Gates（闸门结果）

```text
G0=PASS_ADMITTED_AS_ADJACENT_CANDIDATE
G1=PASS
G2=PASS_BOUNDARY_ONLY_MAPPING_NOT_AUTHORIZED
G3=NOT_ASSESSED
G4=NOT_ASSESSED
G5=NOT_AUTHORIZED
G6=NOT_EXECUTED
G7=NOT_ASSESSED
G8=NOT_RELEASED_NOT_ADOPTED
```

`G0` 只证明组合接纳；`G2` 只证明对象所有权与架构边界已决定。两者均不表示 DBOS
integrated、conformant、adopted standard 或 production ready。

## 7. Freshness and refresh（时效与刷新）

状态刷新遵循实现仓库的 `governance/project-status.json` 和
`governance/source-contract.md`：

- 驾驶舱观察超过 14 天必须标记 `STALE`；
- 声明的 source revision 与远程事实源不一致时立即标记 `STALE`；
- 重新读取规范来源前不得延续旧状态结论；
- 冲突、未知和未评估状态不得被静默升级。

## 8. Public website relationship（公开网站关系）

`redcrag.cn` 是公开展示面。当前媒体行业页、合成 Demo 和机器配置可访问，但网站存在、
部署或本地演示通过，不改变项目组合分类、规范地位、符合性、DBOS 映射、外部采用或生产
状态。

```text
PUBLIC_REFERENCE_SURFACE_AVAILABLE=true
WEBSITE_NE_ARCHITECTURE_ADOPTION=true
WEBSITE_NE_CONFORMANCE=true
WEBSITE_NE_EXTERNAL_ADOPTION=true
```

## 9. Decision effect（决定效力）

```text
ARCHITECTURE_ADMISSION=ACCEPTED_BOUNDED
PORTFOLIO_ADMISSION_GRANTED=true
PORTFOLIO_CLASSIFICATION=ADJACENT_CANDIDATE
DBOS_MAPPING_AUTHORIZED=false
CORE_COMPONENT=false
STANDARD=false
PRODUCTION_READY=false
```

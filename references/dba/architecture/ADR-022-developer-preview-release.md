---
adr_id: ADR-022
title: Trusted Multi-Agent Infrastructure Developer Preview v0.1 Release Authorization
title_zh: 可信多智能体基础设施开发者预览版 v0.1 发布授权
status: accepted-executed
decided_at: 2026-07-22T02:59:31+08:00
decided_by_ref: zhangbin
release_authorized: true
release_executed: true
---

# ADR-022: Developer Preview v0.1 Release Authorization（开发者预览版 v0.1 发布授权）

## Context（背景）

`Trusted Multi-Agent Infrastructure Developer Preview v0.1` 已完成冻结源码、跨仓库
Clean Clone、Agent Customer Validation、网站依赖复核、公开候选网站部署、回滚验证和
exact DBOS public-safe wheel（精确 DBOS 公开安全安装包）复核。

剩余发布输入为：DBOS 分发边界、开放网络发现限制处理、正式发布授权和
`released_by_ref`。验证通过、候选部署和 API 模型推荐均不能自动替代这些决定。

## Decision（决定）

Human Program Owner and Release Authority（人工项目群负责人和发布责任人）`zhangbin`
作出以下明确决定：

```text
DQ-016=PUBLISH_PUBLIC_SAFE_DBOS_WHEEL
WHOLE_DBOS_REPOSITORY_VISIBILITY=KEEP_PRIVATE
OPEN_WEB_LIMITATION=ACCEPT_PARTIAL_METADATA_ONLY_FOR_V0_1
DQ-009=AUTHORIZE_TRUSTED_MULTI_AGENT_INFRASTRUCTURE_DEVELOPER_PREVIEW_V0_1
released_by_ref=zhangbin
```

授权范围：

1. 将 `TMAI-DBOS-WHEEL-CANDIDATE-20260722-001` 的 exact wheel 作为 GitHub Release
   asset（GitHub 发布资产）公开；
2. 保持 DBOS 整仓 `PRIVATE`，不得改变 repository visibility（仓库可见性）；
3. 以 `v0.1-developer-preview` 发布 TMAI Developer Preview v0.1；
4. 在百度云 `redcrag.cn` 部署与同一发布记录绑定的中英文静态网站；
5. v0.1 接受 `TMAI-OWD-20260722-001=PARTIAL_METADATA_ONLY`，但必须继续公开该限制，
   不得改写为规范名称已经自然可发现；
6. release notes（发布说明）必须披露 `R-015` 的 2 项 moderate 构建期残余通告。

## Exact Artifact Boundary（精确产物边界）

```text
package_id=TMAI-DBOS-WHEEL-CANDIDATE-20260722-001
source_revision=cd3f867c4379ec555c45e7d554088ad12ce08a24
filename=digital_biosphere_os_preview-0.1.0.dev0-py3-none-any.whl
sha256=edf92e548860384b1416a612a7e319e0d994bb324f8621847d0d154624ae8f09
bytes=45115
whole_repository_visibility=PRIVATE
public_release_tag=v0.1-developer-preview
```

任何不同 filename、hash、size、source revision 或扩大内容边界的产物均不在本授权内。

## Excluded Scope（排除范围）

本决定不授权：

- 公开 DBOS 整仓、registry、evidence、reports、tests、tools 或本机路径材料；
- 发布到 PyPI；
- 创建 Agent、Runtime、Entity、Capability instance 或 Permission；
- 把 DBOS wheel 称为 Agent framework、Runtime 或生产就绪 SDK；
- 把 Evidence 写成 Truth，把 Evaluation 写成 Authority；
- 修改 SAEE 算法、DBOS 历史 Evidence 或任何子项目 capability truth；
- 声称客户采用、市场验证、生产部署或开放网络规范名称发现已经通过。

## Execution and Completion（执行与完成）

本 ADR 使 release execution（发布执行）获得授权，但文档被采纳本身不等于发布完成。
只有在以下事实全部通过后，才能把 `release_executed`、Developer Preview 和 DBOS wheel
状态更新为已发布：

1. GitHub Release 已公开且不是 draft/prerelease；
2. exact wheel 可匿名下载，bytes 和 SHA-256 匹配；
3. wheel 在全新隔离环境安装和验证通过；
4. 百度云 formal artifact（正式工件）清单验证、`nginx -t`、公开健康和安全头检查通过；
5. `release.json`、`status.json`、Agent surfaces（智能体表面）和 release notes 一致；
6. DBOS GitHub repository visibility 仍为 `PRIVATE`。

失败时保留失败记录，并保持或恢复候选网站；不得把部分执行写成正式发布。

## Consequences（影响）

- `DQ-016` 和 `DQ-009` 的人工决定输入已满足；
- `B-011` 不再阻塞 v0.1，但 `PARTIAL_METADATA_ONLY` 继续作为已接受限制；
- `B-010` 只有在匿名 wheel 下载和隔离安装复验通过后才能解除；
- 发布仍不证明生产就绪、客户采用、开放网络规范名称发现或运行授权。

## Completion Record（完成记录）

`2026-07-22T03:21:54+08:00`，上述六项完成条件全部通过：

- GitHub `v0.1-developer-preview` 为公开、非 draft、非 prerelease；
- tag 指向 `1113130ca4213b70fcebd6247fec794854295e8c`；
- exact wheel 匿名下载、bytes、SHA-256、全新环境安装和 `dbos-validate` 入口通过；
- 百度云 21 个 manifest entries（清单条目）、Nginx、13 个公开入口和安全头通过；
- 线上 `release.json`、`status.json`、agent surfaces 和 release notes 一致；
- `joy7758/digital-biosphere-os` 可见性仍为 `PRIVATE`。

精确证据见 [`DEVELOPER-PREVIEW-v0.1-RELEASE-REPORT.md`](../DEVELOPER-PREVIEW-v0.1-RELEASE-REPORT.md)。

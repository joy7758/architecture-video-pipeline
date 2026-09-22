---
document_id: DBA-ADR-023
title: Authorize the TITMAS Light Public Site Release
title_zh: 授权 TITMAS 明亮版公开网站发布
status: accepted-execution-authorized
decided_by_ref: zhangbin
decided_at: 2026-07-23
source_push_authorized: true
current_host_release_authorized: true
titmas_cn_dns_cutover_authorized: false
github_organization_change_authorized: false
public_contribution_enabled: false
---

# ADR-023: Authorize the TITMAS Light Public Site Release

## Context（背景）

TITMAS 已明确以“可信多智能体基础设施开发者社区”为公开入口。现有网站需要从偏暗、偏内部工程的视觉表达，调整为更明亮、易读、适合第一次接触者理解的开发者基础设施入口。

`titmas.cn` 正在备案。本次发布不能把备案中域名写成已经生效的 canonical domain（规范域名），也不能提前修改其 DNS、TLS 或生产流量。

## Decision（决策）

批准以下受限执行：

1. 将明亮版 TITMAS 网站源文件提交并推送至当前 DBA GitHub 仓库；
2. 将同一已验证源版本发布到现有公开网站承载环境；
3. 保留发布前版本，支持原子回滚；
4. 备案完成后，再通过单独的域名切换检查执行 `titmas.cn` 指向。

视觉方向采用 OpenTelemetry 启发的明亮技术文档风格：白色和浅色背景、紫色主色、黄色强调色、青色辅助色、清晰的卡片与信息层级。该表达是设计借鉴，不构成 OpenTelemetry 隶属、合作、兼容或采用声明。

## Boundaries（边界）

本决策不授权：

- 创建或迁移 GitHub Organization（组织）；
- 开放公开贡献权限；
- 创建 Agent、Runtime、Entity、Capability 或 Permission；
- 修改 DBOS、SAEE 的能力事实或权力边界；
- 在备案完成前切换 `titmas.cn` DNS、TLS 或 canonical URL；
- 把公开网站上线写成社区已经建立、外部采用已经发生或市场验证已经通过。

## Consequences（影响）

TITMAS 获得一个更清晰、更明亮的公开开发者入口；GitHub 与网站可以共享同一定位和可追溯源版本。域名生效仍是后续独立操作，Community（社区）状态和 Public Contribution（公开贡献）状态不因本次发布自动改变。

```text
TITMAS_LIGHT_PUBLIC_SITE_RELEASE_AUTHORIZED=true
SOURCE_PUSH_AUTHORIZED=true
CURRENT_HOST_RELEASE_AUTHORIZED=true
TITMAS_CN_DNS_CUTOVER_AUTHORIZED=false
COMMUNITY_ESTABLISHED=false
PUBLIC_CONTRIBUTION_ENABLED=false
AGENT_CREATED=false
RUNTIME_CREATED=false
PERMISSION_CREATED=false
```

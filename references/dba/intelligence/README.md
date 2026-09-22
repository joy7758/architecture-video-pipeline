---
document_id: DBA-EXTERNAL-INTELLIGENCE-ENTRY-0.1
title: Digital Biosphere External Intelligence Entry
title_zh: 数字生物圈外部治理情报入口
status: reference-only-agent-readable-entry
primary_repository: DBA
implementation_authorized: false
external_action_authorized: false
---

# Digital Biosphere External Intelligence Entry

本目录登记会影响 Digital Biosphere 架构判断的外部模型、协议、安全、生态与研究信号。
它执行 source verification（来源核验）、version pinning（版本钉住）、claim correction
（声明纠偏）、duplication review（重复建设审查）与 authority routing（权力路由）。

它不下载或运行模型，不扫描资产，不修改 DBOS／SAEE，不把外部项目状态写成内部采用，
也不从情报直接产生实现、执行、发布或商业承诺。

## Agent Reading Order（智能体读取顺序）

1. [`agent-index.json`](agent-index.json)：当前情报包与机器状态；
2. 对应日期的 `intelligence-brief.md`：核验结论和纠偏；
3. 主题机器工件：精确版本、兼容映射、反例或研究信号；
4. `capability-provenance-reassessment-profile.md`：何时使旧结论进入重新评估。

## Current Bundle（当前情报包）

| observed_at | bundle | status | 关键纠偏 |
|---|---|---|---|
| `2026-08-16` | [`2026-08-16/`](2026-08-16/) | `PRIMARY_SOURCE_RECONCILED_CANDIDATE_DEFERRED_BY_D16` | `GB/T 47507-2026` 官方状态已是现行；MCP 工具变化引用稳定版 `2026-07-28`；Agent Baseline Check 只登记为参考候选和三个非执行 Fixture，因 D16 冻结未实现、未登记为 SAEE 第三个公共 MCP Tool |
| `2026-08-15` | [`2026-08-15/`](2026-08-15/) | `PRIMARY_SOURCE_RECONCILED_COMPATIBILITY_CROSSWALK_ADDED` | Agent version 不等于有效 Session 能力状态；AWS latest／approved／bound revision 必须分开；OpenTelemetry observation origin 不等于 signer／accountability；未新建能力或 Runtime |
| `2026-08-01` | [`2026-08-01/`](2026-08-01/) | `PRIMARY_SOURCE_RECONCILED_GOVERNANCE_PROFILE_ADOPTED` | `ADR-039` 已把执行上下文变化触发旧结论重评写入正式闸门；MCP `2026-07-28` 保持 stable；AI Act 适用性仍需结合 Digital Omnibus 与法律审查 |
| `2026-07-29` | [`2026-07-29/`](2026-07-29/) | `REFERENCE_ONLY_PRIMARY_SOURCE_CORRECTED` | MCP `2026-07-28` 已稳定发布；Kimi K3 是自定义许可证开放权重，不得简化为无限制开源 |

```text
INTELLIGENCE_NE_ADOPTION=true
INTELLIGENCE_NE_IMPLEMENTATION=true
REFERENCE_NE_INTEGRATION=true
RECOMMENDATION_NE_DECISION=true
EVIDENCE_NE_TRUTH=true
```

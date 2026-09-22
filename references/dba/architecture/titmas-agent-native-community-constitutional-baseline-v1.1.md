---
document_id: DBA-TITMAS-AGENT-NATIVE-CONSTITUTIONAL-BASELINE-1.1
title: TITMAS Agent-Native Community Constitutional Baseline v1.1
title_zh: TITMAS 智能体原生社区宪法基线 v1.1
status: verified-source-baseline
maturity: Development
observed_at: 2026-07-29
source_branch: codex/titmas-developer-standards-community-v1
source_commit: 6fcfd76243b94ddecff8c9aface2ed51116984cb
authority_effect: none
---

# TITMAS Agent-Native Community Constitutional Baseline v1.1

## Source reconciliation

- DBA source：`joy7758/digital-biosphere-architecture-specification`
  `codex/titmas-developer-standards-community-v1@6fcfd762...`；
- v1.0 local verification：74 tests PASS、Harness PASS；
- v1.0 remote CI：GitHub Actions run `30376079752`，`success`；
- SAEE reference-only source：
  `SAEE@697ae208...` 的冻结仓库快照，仅读取 `.codex/rules.md` 与
  `docs/architecture/SAEE_DEVELOPMENT_CONSTITUTION_V1_1.md`；
- 未修改 SAEE，也未把 SAEE 状态复制为 DBA capability truth。

远端 source 不包含本地主工作区未跟踪的 `titmas-architecture-charter-v0.2.md`。本基线以
远端已跟踪 `titmas-architecture-charter-v1.0.md` 为 TITMAS current bounded charter，
不导入未跟踪候选。

## Constitutional and capability matrix

| 原则或能力 | 分类 | 事实判断 | 权威来源 |
|---|---|---|---|
| Agent-Readable First | PARTIALLY_IMPLEMENTED | v1.0 有 README、JSON registries、Harness；尚无完整 Agent community contract | SAEE Constitution v1.1；TITMAS v1.0 |
| AI Agent Primary Machine Customer | DOCUMENTED_ONLY | 已进入开放基础设施宪法，未成为完整参与协议 | Open Infrastructure Constitution v0.4 |
| Agent Recommendation Gate | PARTIALLY_IMPLEMENTED | DBA/SAEE 有闸门；v1.0 无校准对象与精确指标 | DBA AGENTS；SAEE rules |
| Compositional Scale | DOCUMENTED_ONLY | 原则已接受，社区协议尚未把参与者独立性与 lineage 机器化 | ADR-032 |
| Agent contribution disclosure | IMPLEMENTED | v1.0 贡献政策要求披露模型、来源、验证与责任 | `TITMAS/community/AI_ASSISTED_CONTRIBUTIONS.md` |
| Agent self-approval prohibition | PARTIALLY_IMPLEMENTED | 文档禁止；无机器 receipt、independence 检查 | v1.0 Review Process |
| Human Authority | DOCUMENTED_ONLY | 角色分离清楚；未建立 agent-native exception queue contract | Program Charter；TITMAS Charter v1.0 |
| Community role model | PARTIALLY_IMPLEMENTED | 人类式角色存在、assignments 为空；缺 agent role lease | role registry v1.0 |
| Machine-readable task discovery | IMPLEMENTED_FOR_DEVELOPMENT_PROFILE | 单一 task registry 提供 eligibility、lease、conflict 与 stop fields | `../TITMAS/agent-native/tasks/task-registry.json` |
| Agent participant identity | MISSING | 无 participant/model/runtime/session/issuer 分离对象 | none |
| Agent autonomous contribution | MISSING | 无 machine contribution package 与 bounded claim flow | none |
| Multi-agent independent review | DESIGN_CANDIDATE | 有五类 Qwen review records；未表达 lineage independence level | v1.0 reviews |
| Agent maintenance | MISSING | 只有 checklist，没有 lease、scope、rollback 和 report contract | none |
| Agent reuse | MISSING | 无 machine handoff package 或 critical-field loss test | none |
| Agent recommendation calibration | MISSING | 无 fit/non-fit/abstain Schema 和指标 | none |
| 99% operational target | MISSING | v1.0 未记录；不能回填为当前事实 | TITMAS-AGENT-NATIVE-COMMUNITY-D01 |
| Human intervention by exception | DESIGN_CANDIDATE | 长期方向已决定；当前率未测量 | TITMAS-AGENT-NATIVE-COMMUNITY-D01 |

## Conflicts and non-conflicts

1. Agent-native default 不得覆盖 `Agent self-approval prohibited` 或 Human Authority；
2. `99%` 必须与 current measured fact 分开；
3. v1.0 human developer entry 必须保留，名称升级不得破坏路径；
4. participant identity 只能引用 DBOS/Provider/Runtime/Session，不创建第二 Identity Authority；
5. contribution package 只能绑定既有 Evidence architecture，不创建 Evidence Object；
6. v1.0 的公共启动、社区、Maintainer、商业、认证、Release 与 CS Gate 均继续关闭。

## Pre-development Agent Recommendation Gate

精确模型审查：

```text
REQUESTED_MODEL=qwen3.7-max
RETURNED_MODEL=qwen3.7-max
VERDICT=CONDITIONALLY_RECOMMENDED
AUTHORITY_EFFECT=NONE
```

可修正问题：需要真实分角色会话、完整审计链、冲突/循环/畸形贡献对抗测试、资源与循环
上限以及可扩展性说明。外部采用、认证和商业集成不是本阶段阻塞条件，因为 D01 明确
保持这些 Gate 关闭。

## Baseline outcome

```text
SOURCE_BASELINE_CONFLICT=false
V1_TESTS_PASS=74
V1_REMOTE_CI_PASS=true
PARALLEL_TOP_LEVEL_CONSTITUTION_CREATED=false
SAEE_MODIFIED=false
AGENT_NATIVE_GAPS_REQUIRE_IMPLEMENTATION=true
```

---
adr_id: ADR-034
title: Adopt the TITMAS Agent-Native Standards Community Direction
title_zh: 采纳 TITMAS 智能体原生标准社区方向
status: accepted-for-internal-specification-and-controlled-pilot
maturity: Development
decided_by_ref: zhangbin
decided_at: 2026-07-29
decision_reference: TITMAS-AGENT-NATIVE-COMMUNITY-D01
primary_repository: digital-biosphere-architecture
implementation_authorized: true
implementation_scope: local-specification-schema-cli-ci-and-controlled-synthetic-pilot
external_action_authorized: false
authority_effect: none
---

# ADR-034: Adopt the TITMAS Agent-Native Standards Community Direction

## Context

TITMAS Developer Standards Community Infrastructure v1.0 已建立开发者入口、规范注册表、
贡献规则、Conformance Harness 和合成参考实现，但流程仍以人类开发者为默认参与者，
智能体主要被描述为辅助工具。

长期开放技术生态可能由智能体承担大部分发现、理解、任务选择、贡献、审查、维护、
复用和推荐工作。若仍以人工流程为默认，机器客户需要解析非结构化规则、等待人工分派，
且难以证明智能体活动是否产生真实价值。

## Decision

采纳：

```text
English: TITMAS Agent-Native Standards Community
Chinese: TITMAS 智能体原生标准社区
Subtitle: Agent-Native Community for Trusted Multi-Agent Infrastructure
```

并接受以下内部方向：

1. 智能体是日常社区运行的默认参与主体；
2. 人类或机构保留宪法、现实责任、例外、申诉、不可逆动作和 Authority 授予；
3. `0.99` 是长期设计目标，不是当前实现或测量事实；
4. 参与者、任务、贡献、审查、维护、推荐和交接采用机器可读、可验证、失败关闭契约；
5. 智能体角色必须有 issuer、scope、term、revocation 和 evidence reference；
6. 智能体不得自我授权、自我审批、自我晋升或扩大任务范围；
7. 活动量不等于社区价值，贡献需经过相关性、独特性、可行动性和结果影响评价；
8. 本阶段只允许本地、合成、受控试点和相应测试、CLI、Schema、CI 与报告。

## Compatibility

`TITMAS Developer Standards Community` 与 `TITMAS Infrastructure Developer Community`
不删除，作为 historical name、human-facing compatibility alias 和 v1.0 milestone name。
现有 README、规范注册表、CI、Issue/PR 模板和 v1.0 报告路径保持有效。

```text
CANONICAL_COMMUNITY_NAME=TITMAS_AGENT_NATIVE_STANDARDS_COMMUNITY
HUMAN_DEVELOPER_ENTRY_RETAINED=true
OLD_LINKS_RETAINED_OR_REDIRECTED=true
BREAKING_PATH_RENAME=false
```

## Alternatives

### Keep AI as assistance only

Rejected for the long-term design. It does not test machine discovery, bounded task claims,
cross-agent review, reuse or recommendation calibration.

### Create a public autonomous Bot community immediately

Rejected. It would confuse activity with value and create spam, security, ownership and
authority risks before controlled evidence exists.

### Use a bounded internal agent-native pilot

Accepted. It permits real model sessions and deterministic verification while preserving
Human Authority and all public/external gates.

## Non-authorizations

```text
PUBLIC_AGENT_COMMUNITY_LAUNCH=false
PUBLIC_CONTRIBUTION_AUTHORIZED=false
EXTERNAL_AGENT_CREDENTIALS_AUTHORIZED=false
AUTONOMOUS_GITHUB_WRITE_AUTHORIZED=false
AUTONOMOUS_PR_MERGE_AUTHORIZED=false
PUBLIC_ISSUE_CREATION_AUTHORIZED=false
RELEASE_AUTHORIZED=false
TAG_AUTHORIZED=false
COMMERCIAL_OFFER_AUTHORIZED=false
CERTIFICATION_AUTHORIZED=false
FOUNDATION_CREATED=false
CS_G0_PASS=false
CS_G1_PASS=false
```

本 ADR 不修改 DBOS、SAEE、Agent Evidence 或其他仓库，不创建 Agent Runtime、DBOS
Identity、Permission、Evidence Truth、社区成员、Maintainer、外部采用或认证权。

# TITMAS Agent-Native Architecture — Historical Community Archive

中文：TITMAS 智能体原生标准社区历史材料 v1.1。

```text
COMMUNITY_STATUS=SUPERSEDED_HISTORICAL_ARCHIVE
COMMUNITY_CURRENT_AUTHORITY_EFFECT=NONE
COMMUNITY_INVOCATION_AUTHORIZED=false
COMMUNITY_CUSTOMER_ENTRY=false
```

本目录保留早期智能体原生标准社区的协议与测试，供审计与兼容性复核；其中 bounded
evolution（有界演化）子目录仍可作为架构参考，但不恢复社区路线。它不是当前 TITMAS
身份、客户入口、开发者社区或公共贡献路线。当前身份是
[`TITMAS Commercial Agent Infrastructure`](../README.md)，当前机器入口是
[`../../agent-index.json`](../../agent-index.json)。

The only canonical machine entry is [`../../agent-index.json`](../../agent-index.json).
`llms.txt`, the human README and other manifests point to or project that entry;
they do not compete with it.

## Historical command examples — invocation not authorized

以下命令只记录旧路线曾设计的本地接口，不是当前 Start here、客户接入建议或商业能力。

```bash
python3 TITMAS/agent-native/community_cli.py discover \
  --need "machine-readable evidence review"
python3 TITMAS/agent-native/community_cli.py rank \
  --need "bounded contribution handoff"
python3 TITMAS/conformance/harness.py
python3 -m unittest discover \
  -s TITMAS/agent-native/tests -p 'test_evolution.py' -v
```

The historical participant model required an externally issued, bounded,
expiring and revocable participant record. It is not a current enrollment path.
A participant reference is not a DBOS Identity and grants no Permission.

## Historical community flow

```text
discover
  → check eligibility
  → request bounded claim
  → receive externally issued lease
  → prepare contribution package
  → independent review
  → revise or retain failure
  → candidate acceptance
  → handoff and reuse
  → calibrated recommendation or abstention
```

## Human exception path

Constitutional changes, Authority/Ownership changes, legal/privacy responsibility,
irreversible actions, public writes, Merge, Release, Deployment, major disputes
and emergency takeover go to the accountable Human or institutional authority.

## Current boundary

The community protocols and deterministic local tooling in this directory are
retained as supporting references. The bounded-evolution subdirectory remains
an architecture reference only. No pilot runner is copied here. This directory
does not establish a public community, authorize public contribution, create an
Agent Runtime, or define the current commercial route.

D19 v2.1 defines an Agent-native machine collaboration contract for bounded
problem evidence, deterministic repair variants, fitness evaluation, rollback,
lineage and Draft PR handoff. It does not open a community, unrestricted public
access or production activation. See [bounded evolution](evolution/README.md).

## Protocols and guides

- [Participant model](participants/participant-registry.json)
- [Task protocol](tasks/task-registry.json)
- [Contribution protocol](contributions/README.md)
- [Review protocol](reviews/review-protocol.json)
- [Maintenance protocol](maintenance/README.md)
- [Handoff protocol](handoff/README.md)
- [Recommendation protocol](recommendations/README.md)
- [Human exception path](guides/human-exception-and-appeal-path.md)
- [Bounded discovery, self-healing and evolution](evolution/README.md)

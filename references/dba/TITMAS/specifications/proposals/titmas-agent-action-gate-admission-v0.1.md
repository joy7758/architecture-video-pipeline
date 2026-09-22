---
id: TITMAS-PROP-20260802-AGENT-ACTION-GATE-001
title: TITMAS Agent Action Gate Portfolio Admission Request v0.1
title_zh: TITMAS 智能体行动闸门项目组合准入请求 v0.1
category: ADJACENT_CANDIDATE_INTAKE
status: READY_FOR_REVIEW
maturity: M4-Experimental-Reference-Implementation-Merged-To-Main
owner_ref: ZHANGBIN
authority_ref: TITMAS-AGENT-ACTION-GATE-ADMISSION-D01
version: 0.1.0
normative: false
---

# TITMAS 智能体行动闸门项目组合准入请求 v0.1

## 0. Request status（请求状态）

```text
PROPOSAL_ID=TITMAS-PROP-20260802-AGENT-ACTION-GATE-001
PROJECT_EXISTENCE_DECLARED=true
REQUESTED_CLASSIFICATION=ADJACENT_CANDIDATE
PORTFOLIO_ADMISSION_GRANTED=false
G0=REVIEW_REQUIRED_READY_FOR_HUMAN_DECISION
G1=PASS_PUBLIC_MAIN_REFERENCE_SOURCE_PINNED
G2=PARTIAL_SPECIFIED_CROSS_PROJECT_OWNER_REVIEW_REQUIRED
REFERENCE_IMPLEMENTATION_REPORTED=true
RUNTIME_REQUESTED=false
RELEASE_OR_DEPLOYMENT_REQUESTED=false
COMPETITION_SUBMISSION_REQUESTED=false
```

本提案只向 DBA 驾驶舱申报 `TITMAS Agent Action Gate` 存在，并请求后续有界
G0 项目组合审查。GoAI 大赛对话是首个需求场景，不表示赛事官方关联、参赛、提交或获奖。

## 1. Main-constitution source lock（主宪法来源锁）

子项目已从 DBA `main` 固定提取主宪法快照：

```text
COCKPIT_REPOSITORY=joy7758/digital-biosphere-architecture-specification
COCKPIT_BASE_REVISION=269ab5899047503557f957ba0f7abbd61d8b18d3
CONSTITUTION_PATH=architecture/open-infrastructure-strategy-constitution.md
CONSTITUTION_SHA256=ca34af2be5152e395454a83a0e9d2f085861497b601e980adee39e0a36113954
CHILD_SECOND_CONSTITUTION_CREATED=false
```

快照用于可复验读取，不成为第二规范权威。来源变化时必须重新审查差异。

## 2. Child source observation（子项目来源观察）

```text
LOCAL_PATH=/Users/zhangbin/GitHub/titmas-agent-action-gate
SOURCE_OBSERVATION=PUBLIC_REMOTE_MAIN
OBSERVED_BRANCH=main
REMOTE_REPOSITORY=https://github.com/joy7758/titmas-agent-action-gate
REMOTE_VISIBILITY=PUBLIC
REMOTE_COMMIT=6f1c83bf87e6ee96a0eda281e1fa91b8f80a32e1
IMPLEMENTATION_PULL_REQUEST=https://github.com/joy7758/titmas-agent-action-gate/pull/2
IMPLEMENTATION_PR_STATE=MERGED
IMPLEMENTATION_COMMIT=5b5bda64b6b091baefdad788a1d6471750bedb82
IMPLEMENTATION_MERGE_COMMIT=6f1c83bf87e6ee96a0eda281e1fa91b8f80a32e1
CONTRACT_CHECK_1=https://github.com/joy7758/titmas-agent-action-gate/actions/runs/30716845423/job/91413757232
CONTRACT_CHECK_2=https://github.com/joy7758/titmas-agent-action-gate/actions/runs/30716899533/job/91413901638
CONTRACT_CHECKS_CONCLUSION=SUCCESS
CANONICAL_AGENT_ENTRY=agent-index.json
CANONICAL_STATUS_SOURCE=governance/project-declaration.json
PROJECT_DECLARATION_SHA256=0b9e1439a9f3ff5865ee4f8d47a18307eaaaafa383ebcc2389e328e11fb34c26
UPSTREAM_SOURCES_SHA256=e96f82a7a61536d71adb13d0e70934435384127e31888d3712fb9fbde7ef1e42
AGENT_INDEX_SHA256=7bc7dbbfd23301e7e635e6393f7753c65d2e9b59a9d66a1fdcc0fb68eff7dace
PUBLIC_DEMO_EVIDENCE_SHA256=0995a8ecab02934dc23f075e7169003dce33237117f2307eae68bfdcff941792
NATIVE_SMOKE_EVIDENCE_SHA256=a4fb9f79b3494a2b35d625a844dc650b631bd7ae83c2eb073e884aa0ed4b12fe
IMPLEMENTATION_STATUS=EXPERIMENTAL_REFERENCE_IMPLEMENTATION_MERGED_TO_MAIN
ACTION_GATE_IMPLEMENTED=true
MCP_SERVER_IMPLEMENTED=true
AGENTTEAMS_NATIVE_LOCAL_SMOKE_EXECUTED=true
AGENTTEAMS_NATIVE_SMOKE_CLASSIFICATION=OPERATOR_SUPERVISED_AGENT_EXECUTED
AGENTTEAMS_NATIVE_SMOKE_FULLY_AUTONOMOUS=false
AGENTTEAMS_PERSISTENT_OR_PRODUCTION_DEPLOYMENT=false
AGENTTEAMS_NATIVE_SMOKE_EXTERNAL_ACTION_EXECUTED=false
AGENTTEAMS_NATIVE_SMOKE_TEMPORARY_RUNTIME_DESTROYED=true
SANDBOX_PULL_REQUEST=https://github.com/joy7758/titmas-action-gate-demo-sandbox/pull/3
SANDBOX_PULL_REQUEST_MERGED=false
```

因此 G1 可对 public `main@6f1c83b` source 作有界 `PASS`。Action Gate、六工具 MCP server、
`agent-evidence` adapter、五角色本地 handoff harness、真实 GitHub sandbox branch／Draft PR
和一次官方 AgentTeams v1.2.0 本地 smoke 证据存在。该 smoke 是 operator-supervised，完整
Manager → leader 链未自治完成，共享 MCP endpoint 未实施 per-Worker tool ACL，仓库 Skills
也未证明已在 Worker 中物化；临时栈及状态已销毁，未执行 provider action。因此它不证明
持久或生产 AgentTeams deployment、生产安全、release、采用或比赛提交。

## 3. Pre-development agent recommendation（开发前智能体推荐）

如果潜在客户现在要求生产可用的行动闸门，结论仍是 `NOT_RECOMMENDED`：参考实现、运行
证据和一次临时 native smoke 已存在，但没有自治 end-to-end 证明、per-Worker MCP ACL、
Skill materialization、稳定模型契约、持久部署、生产密钥／身份系统或独立安全／运行审查。

对“是否值得继续有界开发”，子项目闸门结论是 `RECOMMENDED`。当前已完成：

1. action request、policy result、evidence result、Human approval 和 decision schema；
2. `ALLOW | BLOCK | REQUIRE_APPROVAL` 的确定性优先级；
3. prompt injection、confused deputy、stale authorization、replay 和 scope expansion 威胁边界；
4. 5 个 AgentTeams identities、5 个 versioned Skills、6 个 Action Gate MCP tool contracts；
5. valid、missing、tampered 和 high-risk approval 四类 runtime case 与 public CI PASS；
6. SQLite append-only hash chain、一次性 decision consumption、caller／approver credential 分离；
7. allowlisted GitHub provider 的真实 branch push 和 Draft PR create，merge 只决策、未执行；
8. Python 3.13 clean wheel install 与 44 项本地测试；
9. official AgentTeams v1.2.0 的临时本地 smoke，保留 Qwen specialist trace、失败和销毁记录；
10. Gemini 3.6 Flash 对完整 change set 给出 `APPROVE_WITH_LIMITATIONS` advisory review。

后续仍须完成与 DBOS Permission、Runtime enforcement、Gateway 和 audit record 的重复建设／
Owner 审查、清洁自治 AgentTeams trace、per-Worker MCP ACL、Skill materialization、稳定模型、
生产身份／密钥治理与独立安全／运行审查。Jules remote review 因 session create
`FAILED_PRECONDITION` 未执行，不得写成审查通过。

该推荐结论本身不授权实现，也不推荐当前项目给生产客户使用；项目 Owner 的完整管理授权是
独立来源，不能把 `NOT_RECOMMENDED` 改写成生产推荐。

## 4. DBA management grant（DBA 管理授权）

Human Owner 已在子项目中签发完整项目管理 policy grant，并保留动作类别闸门：

```text
GRANT_ID=TITMAS-AAG-DBA-MANAGEMENT-GRANT-20260802-001
GRANT_SHA256=571be7c324542f876e646842b8554ccb7a29529e98cf1c991df053a7d8c3da7c
DBA_MANAGEMENT_POLICY_GRANTED=true
DBA_MANAGEMENT_SCOPE=FULL_PROJECT_MANAGEMENT_WITH_ACTION_CLASS_GATES
GITHUB_PRINCIPAL_MAPPED=false
REPOSITORY_ACL_CHANGED=false
RUNTIME_PERMISSION_CREATED=false
```

允许 DBA 驾驶舱管理治理、架构、实现、测试、证据、项目范围内 remote／sandbox、branch／
commit／push／PR，以及在相应 artifact、review、rollback 和 exact-target gate 满足后推进 merge、
release、deployment preparation 与 competition preparation。执行主体必须可追溯。

仍禁止 force push、secret／credential 修改、绕过检查或 Action Gate、付款／合同、虚假生产／
采用／认证声明，以及无精确目标和恢复计划的破坏性删除。merge、release、deployment 和
competition submission 是分开的有证据事件，完整管理授权不自动证明其就绪或已经发生。

DBA 是治理角色而不是 GitHub 账号；因此该文件不能冒充技术 ACL 已生效。

## 5. Requested classification and stop conditions

```text
PRIMARY_RESPONSIBILITY_DOMAIN=GOVERNANCE_SERVICE_APPLICATION_BOUNDARY
PORTFOLIO_TIER_REQUESTED=ADJACENT_CANDIDATE
CORE_COMPONENT_REQUESTED=false
DBOS_MODULE_REQUESTED=false
SAEE_MODULE_REQUESTED=false
STANDARD_REQUESTED=false
```

以下任一项未解决时保持 `REVIEW_REQUIRED`，且不得进入跨项目实现或运行授权：

- action decision、Authorization、Permission、Execution、Evidence Owner 不明确；
- 与现有 Gateway、DBOS、TITMAS conformance 或 Agent framework 重复；
- scope、actor identity、授权来源或 public source pin 缺失／冲突；
- 试图把 gate recommendation 直接转换为动作执行；
- 试图从本提案推断比赛提交、实现、发布、采用或生产状态。

## 6. Non-claims（非声明）

```text
PROJECT_EXISTENCE_REPORTED=true
PORTFOLIO_ADMISSION_GRANTED=false
ARCHITECTURE_MAPPING_AUTHORIZED=false
IMPLEMENTATION_STARTED=true
ACTION_GATE_REFERENCE_IMPLEMENTED=true
MCP_SERVER_REFERENCE_IMPLEMENTED=true
AGENTTEAMS_NATIVE_LOCAL_SMOKE_EXECUTED=true
AGENTTEAMS_NATIVE_SMOKE_FULLY_AUTONOMOUS=false
AGENTTEAMS_PERSISTENT_OR_PRODUCTION_DEPLOYMENT=false
AGENTTEAMS_NATIVE_SMOKE_EXTERNAL_ACTION_EXECUTED=false
RUNTIME_PERMISSION_GRANTED=false
GITHUB_ACL_CHANGED=false
COMPETITION_SUBMITTED=false
SANDBOX_PULL_REQUEST_MERGED=false
PUBLIC_RELEASE_OR_PRODUCTION_DEPLOYMENT_EXECUTED=false
```

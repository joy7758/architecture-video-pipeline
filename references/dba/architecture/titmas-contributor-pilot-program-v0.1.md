---
document_id: DBA-TITMAS-CONTRIBUTOR-PILOT-PROGRAM-0.1
title: TITMAS Limited Contributor Pilot Program v0.1
title_zh: TITMAS 有限贡献者试点计划 v0.1
version: 0.1.0
phase: C4
status: pilot-design-defined-not-authorized
document_type: non-executable-contributor-pilot-design
architecture_domain: TITMAS
pilot_design_ready: true
contributor_program_ready: false
pilot_authorized: false
public_community: false
participants_enrolled: 0
roles_assigned: 0
external_action_authorized: false
authority_effect: none
---

# TITMAS Limited Contributor Pilot Program v0.1

## 1. Purpose and Current State（目的与当前状态）

本计划设计一个小规模、人工监督、私有且可回滚的贡献者试点，用于验证陌生开发者或受治理
智能体能否理解并正确使用 TITMAS 规范流程。

```text
PHASE=C4_LIMITED_CONTRIBUTOR_PILOT
TITMAS_CONTRIBUTOR_PILOT_DESIGN_READY=true
TITMAS_CONTRIBUTOR_PROGRAM_READY=false
TITMAS_CONTRIBUTOR_PILOT_AUTHORIZED=false
PUBLIC_COMMUNITY=false
PARTICIPANTS_ENROLLED=0
```

Design Ready 只表示流程设计完整，不表示可以邀请、接收或分配贡献。

## 2. Pilot Objective（试点目标）

验证参与者能否：

1. 在 30 分钟内解释 DBA、TITMAS、DBOS、SAEE 和 Agent Framework 的差异；
2. 找到规范状态、Owner、non-goals 和 current blockers；
3. 提交一个有来源、有 scope、有 negative case 的 Proposal；
4. 正确区分 Evidence/Truth、Validator/Authorization、Mapping/Adoption；
5. 披露 AI assistance 与人工责任；
6. 根据 review 修正内容，而不制造 Authority 或 implementation claim。

## 3. Pilot Scope（试点范围）

允许：

- 在隔离的、非公共 review surface 准备文档、mapping、test design 或 localization；
- 使用 synthetic/public-safe material；
- 提供理解反馈、安装/检索问题和规范歧义；
- 由受治理智能体辅助，但必须有人类责任方。

禁止：

- 创建外部 Issue、PR、Discussion、SIG、社区账号或公开招募；
- 修改 DBOS、SAEE、EEOAP、Agent Evidence 或外部项目；
- 分配 Maintainer、Reviewer 或组织成员权限；
- 处理 secret、PII、客户数据、真实 Evidence 或未披露漏洞；
- 把试点反馈写成 external adoption、customer proof 或 community established。

## 4. Candidate Roles（候选角色）

| Role | Entry evidence | Pilot responsibility | Exit evidence | No authority |
|---|---|---|---|---|
| Explorer | 能访问入口并接受边界说明 | 完成理解任务、报告歧义 | 正确回答边界问题 | 无提交/审查权 |
| Contributor | Explorer 检查通过 | 提交一个有界 Proposal | review 后被接受/拒绝并保留原因 | 无 role/merge |
| Integrator | 有版本化 mapping 经验 | 准备 no-writeback integration candidate | supported/partial/unknown 和负例完整 | 无外部写权 |
| Specification Contributor | 多项高质量贡献 | 编写对象/状态/兼容候选 | Architecture review 可复核 | 无 Specification Authority |
| Reviewer | 独立 review 经验与人工指派候选 | 在 exact scope 做模拟 review | findings 质量和 COI 记录 | 无正式 approve/Decision |

这些是 pilot functions，不是正式社区角色。`ROLES_ASSIGNED=0`。

## 5. Entry Criteria（进入条件）

试点启动前必须：

- [ ] Governance Activation Ready；
- [ ] pilot scope、coordinator、participant source 和 data boundary 已决定；
- [ ] participant consent、AI disclosure 和 confidentiality rules 完整；
- [ ] Code of Conduct、Conflict of Interest 和 incident route 可用；
- [ ] Security Disclosure path 可用；
- [ ] public/private communication boundary 明确；
- [ ] exact external-action authorization；
- [ ] rollback、retention 和 deletion policy 明确。

参与者本人还需接受：

- 不取得 Community membership 或 Authority；
- 不将私密试点材料公开；
- 不提交无法解释的 AI 大量生成内容；
- 允许保存 review、failure 和 withdrawal 记录。

## 6. Workflow（试点流程）

```text
Controlled Invite Decision
  -> Orientation and Boundary Check
  -> Bounded Task Selection
  -> Proposal Draft
  -> Source / Architecture / Security Review
  -> Revision or Rejection
  -> Exit Interview
  -> Evidence-bound Pilot Assessment
```

当前不执行第一步。

## 7. Review Model（审查模型）

每项试点贡献至少两层检查：

1. **Process Review**：来源、AI 披露、scope、数据与行为边界；
2. **Architecture Review**：Owner、Authority、compatibility、non-elevation。

高风险内容再增加 Security Review。试点 Reviewer 的模拟结论只能是 input，不是 formal
Approval。最终结果由指定 Human Pilot Owner 记录。

## 8. Exit and Stop Conditions（退出与停止条件）

正常退出：

- task accepted/rejected/withdrawn，记录完整；
- participant feedback 和 known gaps 已保存；
- 无未处理敏感数据或外部动作。

立即停止：

- secret/PII/未披露漏洞进入错误渠道；
- AI 自我批准、伪造身份或批量低质量活动；
- Authority、Permission、Truth、Adoption 或 customer claim 抬升；
- response owner 不可用；
- participant 撤回 consent；
- scope 越过 DBA/TITMAS。

失败和拒绝不能静默删除。

## 9. Success Criteria（成功标准）

试点成功需要真实证据，而不是模型自评：

- 至少 3 个独立参与者或人工责任链清晰的独立 Agent trials；
- 80% 以上完成 first-contact boundary check；
- 至少 2 项可复核 Proposal 走完整 review；
- 0 未处置 Authority elevation；
- 0 未处置敏感数据泄露；
- 所有失败、unknown、withdrawal 和 review response 可追溯；
- 人工决定是否进入下一阶段。

当前所有指标为 `NOT_EXECUTED`。

## 10. Human Decision Candidate（人工决定候选）

```yaml
decision_id: CP-D01
question: Authorize one limited private contributor pilot?
recommended_result: DEFER_UNTIL_GOVERNANCE_SECURITY_AND_CONDUCT_GATES_PASS
maximum_participants: 5
public_surface: false
roles_created: false
required_owner_ref: NOT_ASSIGNED
decision_status: NOT_READY_FOR_APPROVAL
```

## 11. Final State（最终状态）

```text
TITMAS_CONTRIBUTOR_PILOT_DESIGN_READY=true
TITMAS_CONTRIBUTOR_PROGRAM_READY=false
TITMAS_CONTRIBUTOR_PILOT_AUTHORIZED=false
TITMAS_CONTRIBUTOR_PILOT_EXECUTED=false
TITMAS_REAL_CONTRIBUTORS_OBSERVED=false
TITMAS_REVIEWERS_ASSIGNED=0
TITMAS_MAINTAINERS_ASSIGNED=0
PUBLIC_COMMUNITY=false
EXTERNAL_ACTION_AUTHORIZED=false
```

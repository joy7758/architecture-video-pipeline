---
document_id: DBA-TITMAS-CONTRIBUTION-PROPOSAL-TEMPLATE-0.1
title: TITMAS Contribution Proposal Template v0.1
title_zh: TITMAS 贡献提案模板 v0.1
status: template-prepared-not-publicly-activated
maturity: Development
maturity_scope: entire-document
owner_ref: NOT_ASSIGNED
decision_reference: NOT_DECIDED
supersedes: NONE
superseded_by: NONE
compatibility_statement: "Development document; no implementation compatibility claim."
implementation_feedback_refs: []
conformance_refs: []
known_limitations: [SEE_DOCUMENT_BODY]
document_type: non-executable-proposal-template
architecture_domain: TITMAS
proposal_created: false
decision_created: false
implementation_authorized: false
external_action_authorized: false
authority_effect: none
---

# TITMAS Contribution Proposal Template v0.1

复制本模板只创建 Proposal candidate，不产生 Decision、Authorization、Implementation、
Release、Permission 或 Adoption。

## 1. Identity and Provenance（标识与来源）

```yaml
proposal_id: TITMAS-PROP-YYYYMMDD-NNN
title:
status: DRAFT
created_at:
updated_at:
proposer_ref:
contributor_type: HUMAN|GOVERNED_AGENT|HUMAN_WITH_AGENT_ASSISTANCE
human_accountability_ref:
agent_or_tool_ref:
source_refs: []
source_versions_or_commits: []
verification_performed_by_ref:
```

## 2. Problem and User Need（问题与用户需求）

```text
problem_statement=
affected_agent_or_developer_workflow=
why_existing_surface_is_insufficient=
why_this_belongs_to_trusted_multi_agent_infrastructure=
```

如果潜在客户或智能体提出该需求，先回答：

```text
WOULD_RECOMMEND_TITMAS_FOR_THIS_NEED=true|false|conditional
NON_RECOMMENDATION_REASONS=
PROPOSED_REMEDIATION=
```

## 3. Contribution Classification（贡献分类）

```yaml
contribution_surface:
  # SPECIFICATION|SEMANTIC_MAPPING|ADAPTER_CONTRACT|CONFORMANCE|
  # DOCUMENTATION|REFERENCE_CANDIDATE|DEVELOPER_EXPERIENCE|SECURITY_PRIVACY
target_document_refs: []
target_specification_version:
proposed_document_maturity: Development
affected_authority_domains: []
```

## 4. Scope and Non-goals（范围与非目标）

```text
in_scope=
out_of_scope=
non_goals=
implementation_requested=false
external_action_requested=false
runtime_requested=false
agent_or_entity_creation_requested=false
permission_requested=false
```

## 5. Proposed Change（拟议变化）

说明：

- 新增、修改或废弃的对象、字段和状态；
- 对 Identity、Capability、Execution、Evidence、Verification、Evaluation 的影响；
- ownership 与 canonical source；
- error、unknown、unsupported、conflict 和 partial-success 语义；
- 版本和迁移行为。

## 6. Compatibility and Adoption（兼容与采用）

```text
backward_compatibility=
forward_compatibility=
breaking_change=true|false|unknown
migration_requirement=
deprecation_requirement=
implementation_version_declaration_required=
```

Mapping 到外部协议不表示采用、认可或运行兼容。Reference Adoption 与 Runtime Adoption
必须分开。

## 7. Security, Privacy and Authority（安全、隐私与权力）

```text
threats=
data_classification=
privacy_impact=
supply_chain_impact=
credential_or_secret_handling=
authority_elevation_risk=
evidence_to_truth_risk=
recommendation_to_command_risk=
```

必须说明如何保持：

```text
CAPABILITY_NE_PERMISSION=true
EVIDENCE_NE_TRUTH=true
EVALUATION_NE_AUTHORITY=true
SPECIFICATION_NE_IMPLEMENTATION=true
COMMUNITY_REVIEW_NE_ARCHITECTURE_DECISION=true
```

## 8. Validation and Conformance Plan（验证与符合性计划）

```yaml
positive_cases: []
negative_cases: []
unknown_cases: []
failure_retention:
version_binding:
environment_binding:
independent_review_required: true
pass_does_not_create:
  - permission
  - truth
  - authority
  - adoption
  - release
```

## 9. Alternatives and Duplicate Review（替代与重复审查）

```text
alternatives_considered=
existing_dba_or_tmap_surface=
existing_dbos_capability=
existing_saee_capability=
existing_external_standard=
duplicate_authority_risk=
reason_not_to_change=
```

## 10. Required Reviews and Decisions（所需审查与决定）

```yaml
review_inputs:
  architecture:
  dbos_domain:
  saee_domain:
  security_privacy:
  developer_experience:
required_decision_refs: []
implementation_authorization_ref:
external_action_authorization_ref:
```

未填写的 reference 必须保持为空或 `NOT_ASSIGNED`，不得伪造。

## 11. Outcome Record（结果记录）

```yaml
review_result: PENDING
decision_result: NOT_DECIDED
adopted_version:
implementation_status: NOT_AUTHORIZED
conformance_status: NOT_EXECUTED
release_status: NOT_RELEASED
known_limitations: []
```

Rejected、Deferred、Superseded 和 Withdrawn Proposal 必须保留，不得静默删除。

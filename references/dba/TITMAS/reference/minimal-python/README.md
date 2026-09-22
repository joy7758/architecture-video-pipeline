# Minimal Python Reference

This reference maps one synthetic Agent event to the TITMAS Development
interoperability surface:

```text
synthetic event
  → boundary check
  → existing Evidence reference binding
  → local structure Verification reference
  → read-only Evaluation handoff
  → limitations
```

Run:

```bash
python3 TITMAS/reference/minimal-python/titmas_reference.py \
  TITMAS/reference/minimal-python/example-input.json
python3 -m unittest discover -s TITMAS/reference/minimal-python/tests -v
```

The program performs no network request, writes no customer data, creates no
Agent or Runtime, and does not create a canonical Evidence object.

## Enterprise Agent Review 商业测试版

在同一最小引用目录内，`enterprise_agent_evaluation/` 提供一个可选的、仅合成数据的
`TITMAS Enterprise Agent Review v0.1.0-beta.1` 本地评测入口。它通过阿里云百炼直接
模型调用生成评测材料，不要求创建百炼 Workflow、知识库或 Dify。

它仍不是 Runtime、执行器、认证或公共 SaaS。详细的三分钟开始方式、成本上限、证据
边界和无法声称的内容见
[`enterprise_agent_evaluation/README.md`](enterprise_agent_evaluation/README.md)。

Field mapping:

| Input | Output |
|---|---|
| `identity` | `identity_ref` |
| `boundary` | `boundary` |
| `event` | `event` |
| `existing_evidence_ref` | `evidence_binding.evidence_ref` |
| `existing_verification_ref` | `verification_result.verification_ref` |
| event/evidence/verification refs | `evaluation_handoff.input_refs` |
| `limitations` | `limitations` |

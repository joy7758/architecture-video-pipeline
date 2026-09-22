# TITMAS Private Agent Customer Evaluation Bundle v0.1

中文：TITMAS 私有智能体客户评估包候选 v0.1。

The nine top-level files form the bounded customer-visible contract allowlist.
They are not released, expose no private core source, and authorize no model
or Provider call. The private `gateway/` implementation is never copied into
the Agent Customer Workspace.

## Contents

- [`agent-service-discovery.json`](agent-service-discovery.json)
- [`api-contract.json`](api-contract.json)
- [`synthetic-request.json`](synthetic-request.json)
- [`synthetic-response.json`](synthetic-response.json)
- [`error-codes.json`](error-codes.json)
- [`black-box-validation.md`](black-box-validation.md)
- [`evaluation-task.md`](evaluation-task.md)
- [`human-accountability.md`](human-accountability.md)

An authorized future local rehearsal may receive an ephemeral loopback
endpoint and an in-memory session token. It receives the contract, not the
implementation.

```text
PRIVATE_AGENT_CUSTOMER_EVALUATION_BUNDLE_CANDIDATE_READY=true
PRIVATE_AGENT_CUSTOMER_EVALUATION_BUNDLE_RELEASED=false
PRIVATE_CUSTOMER_TEST_NE_CORE_CODE_ACCESS=true
LOCAL_EPHEMERAL_GATEWAY_IMPLEMENTED=true
PUBLIC_ENDPOINT_AVAILABLE=false
D02_PRIVATE_AGENT_CUSTOMER_CYCLE_AUTHORIZED=false
REAL_MODEL_CALL_COUNT=0
```

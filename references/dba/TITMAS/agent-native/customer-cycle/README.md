# Agent Customer Response Capture

中文：智能体客户响应捕获。

This bounded observability component prevents a dispatched model request from
being confused with a completed or valid Agent result. It is Provider-neutral,
uses only the Python standard library and owns no network client.

## Machine entry

- Capture module: [`response_capture.py`](response_capture.py)
- Audit envelope Schema:
  [`response-capture-envelope.schema.json`](response-capture-envelope.schema.json)
- Deterministic tests:
  [`../tests/test_response_capture.py`](../tests/test_response_capture.py)

Run:

```bash
python3 -m unittest TITMAS/agent-native/tests/test_response_capture.py -v
```

## Binding contract

Before an injected transport may run:

```text
CAPTURE_LAYER_READY=true
ATTEMPT_RECORD_DURABLE=true
REQUEST_SHAPE_PREFLIGHT=PASS
CAPTURE_DESTINATION_PREFLIGHT=PASS
```

After a valid response:

```text
RESPONSE_ENVELOPE_FINALIZED=true
RETURNED_MODEL_CAPTURED=true
MODEL_IDENTITY_MATCH=true
DISCOVERY_CONTRACT_PARSED=true
```

Any failure keeps downstream implementation, Issue, PR and Reviewer stages
closed. The component computes retry eligibility but never retries.

## Durable capture

Every envelope update uses a same-directory temporary file, file flush,
`fsync(file)`, `os.replace` and `fsync(parent_directory)`. A raw response body
is first written to a `0600` temporary spool outside Git. Successful or
classified non-crash completion deletes the spool. Crash recovery preserves
the body hash, length and known model identity while returning
`FAILED_RECOVERY_REQUIRED`.

## Boundaries

```text
RESPONSE_CAPTURE_IS_OBSERVABILITY_SUPPORT=true
RESPONSE_CAPTURE_IS_RUNTIME=false
RESPONSE_CAPTURE_IS_PROVIDER_SDK=false
RESPONSE_ENVELOPE_IS_EVIDENCE_TRUTH=false
AUTO_RETRY=false
REAL_MODEL_CALLS_IN_TESTS=0
```

Transport failure is not Agent failure. Parse failure is not Agent abstention.
`requested_model` equals `returned_model` only after explicit verification.

## Sanitized Semantic Checkpoint

中文：清理后语义检查点。

[`semantic_checkpoint.py`](semantic_checkpoint.py) persists only
Schema-validated, sanitized and bounded structured results. It is future-cycle
audit support; it does not reconstruct or elevate missing D02 results.

Machine-readable contracts:

- [`semantic-checkpoint-envelope.schema.json`](schemas/semantic-checkpoint-envelope.schema.json)
- [`contributor-plan.schema.json`](schemas/contributor-plan.schema.json)
- [`gateway-customer-projection.schema.json`](schemas/gateway-customer-projection.schema.json)
- [`contributor-assessment.schema.json`](schemas/contributor-assessment.schema.json)
- [`independent-review.schema.json`](schemas/independent-review.schema.json)
- [`standard-contribution.schema.json`](schemas/standard-contribution.schema.json)
- [`standard-review.schema.json`](schemas/standard-review.schema.json)

The required stage order is:

```text
CONTRIBUTOR_PLAN durable
  -> GATEWAY_CUSTOMER_PROJECTION durable
  -> CONTRIBUTOR_ASSESSMENT durable
  -> INDEPENDENT_REVIEW durable
  -> Human disposition

CONTRIBUTOR_PLAN durable
  -> STANDARD_CONTRIBUTION durable
  -> STANDARD_REVIEW durable
  -> Human disposition
```

`CheckpointStageGate` fail-closes downstream dispatch until the immediately
preceding stage is durable and hash-valid. The component owns no Provider
client and performs no dispatch itself.

Storage is private-by-default:

```text
CHECKPOINT_DIRECTORY_MODE=0700
CHECKPOINT_FILE_MODE=0600
GIT_TRACKING_DEFAULT=false
RAW_PROMPT_RETAINED=false
RAW_RESPONSE_RETAINED=false
HIDDEN_REASONING_RETAINED=false
CREDENTIAL_MATERIAL_RETAINED=false
```

Run the exact deterministic suite:

```bash
python3 -m unittest discover \
  -s TITMAS/agent-native/tests -p 'test*semantic_checkpoint.py' -v
```

Boundaries:

```text
RESPONSE_CAPTURE_NE_SEMANTIC_CHECKPOINT=true
SEMANTIC_CHECKPOINT_NE_EVIDENCE_TRUTH=true
SEMANTIC_CHECKPOINT_NE_AUTHORIZATION=true
SEMANTIC_CHECKPOINT_IS_RUNTIME=false
REAL_MODEL_CALLS_IN_TESTS=0
```

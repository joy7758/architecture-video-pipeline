# TITMAS Conformance Harness

The harness uses only the Python standard library. Registry `.yaml` files are
JSON-compatible YAML 1.2.

```bash
python3 TITMAS/conformance/harness.py
python3 -m unittest discover -s TITMAS/conformance/tests -v
```

It validates:

- proposal frontmatter;
- machine registries and Schemas;
- local Markdown links;
- positive and negative fixtures;
- registry/document reference consistency;
- version and maturity rules;
- no-semantic-elevation invariants;
- fail-closed community status.
- frozen-source resource resolution, contribution preflight and reviewer
  evidence receipts under [`grounding/`](grounding/).

Inputs are fixed local repository files. The harness performs no network fetch,
rejects paths outside the DBA root and non-regular JSON files, limits JSON input
to 1 MB, and limits recursive schema validation to 32 levels.

The deterministic machine report is written to
`TITMAS/conformance/reports/latest.json`.

A PASS validates only this Development profile and its local assets. It does
not prove Truth, Authorization, adoption, security, certification or Runtime
compatibility.

On failure, copy the reported path and error, correct that bounded asset and
rerun `python3 TITMAS/conformance/harness.py`; the harness never auto-fixes or
widens scope.

The grounding layer is a general community contribution check. It is not an
Ecology Box runner, DBOS Verification, Evidence Truth source, Runtime or
executor.

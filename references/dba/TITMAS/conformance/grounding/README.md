# TITMAS Community Contribution Grounding

This directory provides deterministic, repository-local checks for a bounded
community contribution candidate.

The resolver binds references to one exact Git revision or to an isolated
candidate copy. The preflight checks the candidate field set, file scope,
required reference receipts, parseability and limited semantic-elevation
conditions before advisory review.

```text
Frozen source
  -> exact local resource resolution
  -> bounded candidate apply in a temporary directory
  -> required-reference receipts
  -> incremental preflight result
  -> advisory review gate
  -> full repository conformance
```

The grounding layer:

- performs no network calls;
- does not modify the frozen repository revision;
- permits contributor and reviewer abstention;
- preserves unresolved references and failures;
- does not create DBOS Verification, Evidence Truth, adoption, Permission,
  execution authority, or Human approval.

Its receipts establish only that a referenced resource was deterministically
resolved under the declared local snapshot and scope.

Run the focused checks from `digital-biosphere-architecture/`:

```bash
python3 -m unittest discover -s TITMAS/conformance/tests \
  -p 'test_contribution_grounding.py' -v
```

The complete acceptance gate remains:

```bash
python3 TITMAS/conformance/harness.py
python3 -m unittest discover -s TITMAS/conformance/tests -v
```

`PREFLIGHT_PASS` is not final conformance. `CONFORMANCE_PASS` is not adoption,
Truth, Authorization, certification, release, or production readiness.

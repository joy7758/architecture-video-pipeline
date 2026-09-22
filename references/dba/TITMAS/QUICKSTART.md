# TITMAS Five-minute Quickstart

Requirements: Python 3.10+ and a local checkout. No package install, account,
network request or external service is required.

```bash
cd digital-biosphere-architecture

python3 TITMAS/conformance/harness.py
python3 -m unittest discover -s TITMAS/conformance/tests -v
python3 -m unittest discover -s TITMAS/reference/minimal-python/tests -v

python3 TITMAS/reference/minimal-python/titmas_reference.py \
  TITMAS/reference/minimal-python/example-input.json
```

Expected:

- harness status `PASS`;
- all currently registered semantic-elevation negatives are rejected;
- Conformance/Candidate Grounding and reference test suites pass;
- reference output matches `expected-output.json`.

These results prove only deterministic local behavior for a synthetic
Development profile.

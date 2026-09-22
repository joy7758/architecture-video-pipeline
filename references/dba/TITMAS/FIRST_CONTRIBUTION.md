# First Contribution Guide

## 1. Choose a bounded contribution

This guide is retained as historical infrastructure. Public contribution is
currently disabled. A future contribution may pick one
[Starter Task](community/STARTER_TASKS.md) or draft a
[Proposal](specifications/templates/proposal.md) only after a new bounded Human
Decision.

## 2. Declare scope

- developer value;
- files and object owners affected;
- sources and exact versions;
- tests and failure behavior;
- AI assistance and human accountability;
- prohibited claims.

## 3. Validate

```bash
python3 TITMAS/conformance/harness.py
python3 -m unittest discover -s TITMAS/conformance/tests -v
python3 -m unittest discover -s TITMAS/reference/minimal-python/tests -v
git diff --check
```

## 4. Review

Use [the review process](community/REVIEW_PROCESS.md). Review does not create
Authority or adoption.

## 5. Know the current limits

Public contribution is inactive and unauthorized. No permanent Maintainer,
established community, Stable specification, certification or Release is
created. Preparing a contribution does not grant Authority and does not submit
anything.

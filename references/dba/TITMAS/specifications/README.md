# TITMAS Specifications

This directory is the only specification registry and proposal entry for the
v1.0 developer-community candidate.

- [`lifecycle.md`](lifecycle.md): proposal, review, version and deprecation flow.
- [`registry.yaml`](registry.yaml): specification registry.
- [`proposal-registry.yaml`](proposal-registry.yaml): proposal registry.
- [`maturity-registry.yaml`](maturity-registry.yaml): maturity definitions.
- [`templates/proposal.md`](templates/proposal.md): proposal template.
- [`proposals/`](proposals/): active Development proposals.

Files ending in `.yaml` use JSON-compatible YAML 1.2 so the standard-library
validator can parse them without a new dependency.

No item in this directory is Stable unless its own registry entry, Decision and
conformance evidence explicitly say so.

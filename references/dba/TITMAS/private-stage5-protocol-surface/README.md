# TITMAS Stage 5 Private Protocol Surface

中文：TITMAS 第五阶段私有协议表面。

This private candidate explains how an AI Agent or developer can discover and
submit a bounded Specification Proposal, Adapter Mapping or Test Vector without
receiving private core source. It is not a public release, implementation
license, standard adoption, Runtime, certification or commercial agreement.

## Position and core terms

- **Specification Proposal** describes a bounded standards problem and change.
- **Adapter Mapping** maps source semantics without claiming adoption.
- **Test Vector** states synthetic input, expected result and failure behavior.
- **Conformance** validates the declared Development contract; it is not Truth.
- **Sandbox Key** controls ephemeral access, not source ownership.
- **Human Maintainer** makes final pilot and candidate disposition.

## Files

- `standard-catalog.json`: bounded Development specification catalog.
- `task-catalog.json`: customer-safe problem catalog.
- `api-contract.json`: loopback Sandbox contract.
- `error-codes.json`: customer-visible failure codes.
- `schemas/`: contribution, result and review contracts.
- `synthetic-examples.json`: non-confidential examples.

## Conformance client

Submit one object through the SDK, then call the submission validation
operation. `CONFORMANCE_PASS` advances only to
`HUMAN_DISPOSITION_REQUIRED`; it never becomes `STANDARD_ADOPTED`, `STABLE` or
`CERTIFIED`. A malformed or semantically elevated object fails closed.

## SDK interface

The Python client supports catalog and task discovery, three submission
methods, explicit validation, status retrieval and review submission. It
constructs authenticated requests, performs bounded Schema preflight and parses
customer-visible errors. It never retries a dispatched request automatically.

## Version rules

This surface is `1.0.0` Development preview material. Additive fields require a
minor version and explicit compatibility declaration. Breaking changes require
a new major version and Human Decision. Version change is not deployment or
adoption.

## AI assistance disclosure

Every Proposal and Adapter Mapping declares whether AI assisted, exact Provider
and model identity, assistance scope and required Human accountability. Model
output cannot self-approve, assign Authority or become an adopted standard.

## Non-claims

```text
PUBLIC_RELEASE_ALLOWED=false
PRIVATE_STAGE_5_USE_ALLOWED=true
PRIVATE_CORE_SOURCE_INCLUDED=false
KEY_IS_SOURCE_LICENSE=false
CONFORMANCE_PASS_NE_ADOPTION=true
PILOT_ACCEPTANCE_NE_STANDARD_ADOPTION=true
COMMUNITY_ESTABLISHED=false
```

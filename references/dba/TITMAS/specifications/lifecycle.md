# Specification Lifecycle

```text
IDEA
  → DEVELOPMENT_DRAFT
  → EXPERIMENTAL_PROPOSAL
  → CANDIDATE
  → STABLE
  → DEPRECATED
  → ARCHIVED
```

## Proposal and review

1. Create a `DRAFT-ID` or `PROVISIONAL-ID`.
2. Declare Owner and Authority separately.
3. Define scope, non-goals, object ownership, fields, failure/unknown semantics,
   versioning, security, privacy and negative cases.
4. Run registry and conformance validation.
5. Obtain independent technical/domain review.
6. Obtain Human Architecture Decision for normative adoption.
7. Update the registry; do not rewrite prior status history.

No stable `TITMAS-XXXX` number may be issued until Number Registry Authority is
explicitly assigned.

## Compatibility

- backward-compatible additions require an optional field and preserved unknown handling;
- breaking changes require a new major version and migration statement;
- forward compatibility must preserve unknown fields or fail explicitly;
- version negotiation must expose supported, unsupported and selected versions.

## Deprecation

Deprecated is not Deleted. A deprecation record must name replacement, start,
support window, migration requirement, known risk and archive path.

```text
PROPOSAL_NE_ADOPTION=true
IMPLEMENTATION_NE_SPECIFICATION=true
REFERENCE_IMPLEMENTATION_NE_STANDARD=true
```

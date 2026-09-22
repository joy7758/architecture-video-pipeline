# v1.1 Schema Policy

The v1.1 schemas are strict Development contracts.

- `additionalProperties: false` prevents silent field invention.
- Every task must state relevance and non-applicability conditions.
- Every task must state both allowed and forbidden scope.
- Contributions must bind to the existing Evidence Architecture; this profile
  must not create a second evidence system.
- `self_approval: false` is constitutional. `LEVEL_0_SELF_REVIEW` may describe
  diagnostic self-review, but it can never produce an accepting receipt.
- `non_claims` and `limitations` are mandatory because semantic restraint is a
  protocol requirement, not optional metadata.
- Relative `$schema` references are resolved relative to the instance path by
  convention; the dependency-free Harness explicitly selects the matching
  schema and does not rely on network resolution.
- Date fields declare `date-time`; runtime expiry enforcement also requires an
  explicit timezone.

These constraints are not loosened merely to improve model review outcomes.
Breaking evolution requires a future accountable Architecture Decision.

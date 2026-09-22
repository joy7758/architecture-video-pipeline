# Contributing to TITMAS

Public contribution is currently inactive and unauthorized. GitHub Issue and
Pull Request templates were historically installed through the independent
[Activation PR](github-activation-templates/README.md), but that history does
not create a current submission path.

## First contribution

1. Read [the two-minute introduction](../README.md).
2. Choose one [Starter Task](STARTER_TASKS.md) or create a
   [Proposal](../specifications/templates/proposal.md).
3. Declare human accountability and any AI assistance.
4. Keep one bounded contribution type: documentation, schema, tests, adapter,
   security or developer experience.
5. Run:

   ```bash
   python3 TITMAS/conformance/harness.py
   python3 -m unittest discover -s TITMAS/conformance/tests -v
   python3 -m unittest discover -s TITMAS/reference/minimal-python/tests -v
   git diff --check
   ```

   Use a normal clone for Candidate Grounding tests. A `--depth 1` shallow
   clone lacks the Git history required by those lineage checks and therefore
   fails closed with `NOT_ASSESSED`.

6. Stop after preparing a local candidate. Submission requires a new explicit
   Human Decision; Maintainer acceptance remains separate.

## Contribution lifecycle

```text
DRAFT → SUBMITTED → TRIAGED → REVIEWING
  → ACCEPTED | REJECTED | DEFERRED | WITHDRAWN
  → INTEGRATED
```

`ACCEPTED` is a contribution decision. It does not imply Standard adoption,
Release, Runtime deployment, Permission or community membership.

## Required disclosure

```text
contributor_type=HUMAN|GOVERNED_AGENT|HUMAN_WITH_AGENT_ASSISTANCE
human_accountability_ref=
agent_or_tool_ref=
source_refs=
verification_performed_by_ref=
known_unknowns=
```

Never submit credentials, personal/customer data, real production Evidence or
license-incompatible materials.

The core repository is private. Prior public content may have been copied and
cannot be retracted, but it does not authorize a new export. Local preparation
and Conformance do not imply submission, acceptance, Authority, adoption,
Release or community membership.

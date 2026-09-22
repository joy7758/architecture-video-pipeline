# Scout Self-Improvement Iteration 1

## Observation

`agentrust-io/ca2a#36` remained the first item in
`reports/latest-opportunities.json` after a conversion run, publication run,
and review run already existed.

## Minimal patch

- Add an exact-reference, read-only `StatusIndex` over existing run records.
- Link an Issue and PR only when the same evidence document explicitly
  references both; do not infer links from title similarity.
- Preserve active conversion entries in a separate report section.
- Exclude `ACTIVE_CONVERSION` and `READY_FOR_REVIEW` entries from the new
  opportunity ranking.
- Add a regression test using Issue #36 and PR #76 identifiers.

## Boundaries

This patch does not change the heuristic ranking, Validator, Agent Evidence
semantics, TITMAS constitution, DBA theory, or historical run files. It does
not claim general semantic duplicate detection.

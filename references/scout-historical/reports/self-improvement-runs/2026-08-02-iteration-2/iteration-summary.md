# Iteration 2 Summary

The first live rerun returned zero candidates. Independent reviewers proved
that broadening terms alone was insufficient because the GitHub CLI backend
mixed embedded qualifiers with equivalent flags. A later risk review also
proved that the prefix allowlist accepted a GraphQL mutation shape.

Both blockers were preserved and resolved. The final implementation separates
CLI flags from REST qualifiers and removes GraphQL from the v0.1 allowlist.
The final quorum returned `ALLOW` for local report output. The full live rerun
retrieved 94 public Issue records, retained five review candidates, carried the
existing ca2a conversion separately, and observed no external write.

```text
ITERATION=2
MAX_ITERATIONS=3
STATUS=COMPLETE
THIRD_ITERATION_USED=false
RANKING_CALIBRATED=false
EXTERNAL_ACTION_AUTHORIZED=false
```

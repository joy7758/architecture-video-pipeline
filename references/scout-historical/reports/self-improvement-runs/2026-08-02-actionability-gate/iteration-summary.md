# Actionability Gate Iteration Summary

The Scout no longer allows an `OBSERVE` candidate to displace an
`ACTIONABLE_NOW` candidate. The original five-item pool now selects
`praxis-proxy/ai#194`; `syswonder/robonix#189` and the nightly research item
are retained only for research observation.

The first live rerun exposed a second selection defect: a bot-authored epic
without an external contribution invitation became the first conversion
target. The second and final iteration moved such records to `OBSERVE`. A
subsequent authenticated, read-only GitHub run retrieved 94 records and selected
`praxis-proxy/ai#194` as the next target.

The model remains `heuristic_unvalidated`. The change establishes a deterministic
queue boundary; it does not establish maintainer interest, adoption, revenue,
authorization, or a calibrated probability of success.

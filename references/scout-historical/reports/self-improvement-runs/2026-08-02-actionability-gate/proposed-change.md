# Actionability Gate Proposed Change

## Problem

The prior heuristic ranked research relevance before conversion readiness. An
assigned Issue whose action pack said `OBSERVE` could therefore become the next
conversion target while open, unassigned Issues remained available.

## Change

- Collect and preserve GitHub assignee and lock evidence.
- Fail closed when either field is missing or malformed.
- Classify each signal as `ACTIONABLE_NOW`, `ACTIONABLE_AFTER_CONTACT`,
  `OBSERVE`, or `EXCLUDE` before ranking.
- Sort conversion readiness before heuristic relevance factors.
- Keep `OBSERVE` out of `conversion_queue` and place it in
  `research_watchlist`.
- Treat bot-authored work without an explicit contribution invitation as
  `OBSERVE`.
- Publish the selection decision in the Markdown and JSON output contracts.

The classification is for human or agent review prioritization only. It does
not authorize any external action and does not predict acceptance or success.

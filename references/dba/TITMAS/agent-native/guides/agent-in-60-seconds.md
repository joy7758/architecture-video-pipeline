# Agent in 60 Seconds

1. Read the sole machine entry: [`../../../agent-index.json`](../../../agent-index.json).
2. Read [`../current-state.json`](../current-state.json); do not infer maturity.
3. Run `python3 TITMAS/conformance/harness.py`.
4. Discover work with `python3 TITMAS/agent-native/community_cli.py discover --need "<need>"`.
5. Check eligibility before requesting a bounded claim.

No command here authorizes a write, contribution adoption, merge, release,
deployment, public community action, or external contact.

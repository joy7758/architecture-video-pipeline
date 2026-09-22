# Program Governance Cockpit — read-only source bridge

This directory extends the existing DBA Program Governance Cockpit. It is not
a second cockpit, Runtime, control plane, status authority, or evidence store.

The first registered project source is `titmac-scout`:

- canonical machine identity: `titmac-scout`;
- conversation alias only: `tiamas-scout`;
- canonical status owner: `joy7758/titmac-scout`;
- access: `READ_ONLY`;
- refresh: `ON_DEMAND`;
- source mode: `CANONICAL_MAIN_EXACT_REVISION`;
- failure behavior: stale, unavailable, revision-drift, digest-drift, or invalid
  sources fail closed.

The adapter stores only a projection containing the source reference, exact
revision and tree, status-file digest, bounded summary, freshness, and retrieval
time. Raw evolution runs, patch variants, sandbox outputs, model output,
credentials, and private runtime data remain with the source repository.

The source repository declares project state and asks for external observation;
it does not hardcode current CI, pull-request, merge, remote-head or availability
facts. The cockpit queries GitHub read-only and reports source-status,
remote-revision, CI and pull-request freshness independently. Missing or stale
dynamic observation produces `SOURCE_STALE_OR_PARTIALLY_STALE` without changing
the Scout-owned project state.

## Agent entry

```bash
python3 cockpit/read_only_status_adapter.py \
  --project-id titmac-scout \
  --local-repository /path/to/titmac-scout \
  --output cockpit/projections/titmac-scout.json

python3 -m unittest discover -s cockpit/tests -v
```

The registry pins canonical `main` to an exact revision, tree and status digest.
The adapter does not expose a candidate-branch mode or any write path. A source
or observation PASS must never be presented as released, deployed, adopted,
certified, self-healing-complete, self-evolution-complete or production-ready.

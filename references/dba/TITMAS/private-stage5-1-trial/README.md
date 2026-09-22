# TITMAS Stage 5.1 Private Trial Channel

This core-only directory defines the allowlist reconstruction, fail-closed
validation and deterministic clean-clone test for the separate private
developer trial repository.

It is not copied wholesale into the trial repository. Only exact payloads
recorded in `trial-source-manifest.json` may leave the core checkout.

```text
PRIVATE_CORE_IS_CANONICAL=true
TRIAL_REPOSITORY_NE_CORE_REPOSITORY=true
PUBLICATION_BY_RECONSTRUCTION=true
ALLOWLIST_ONLY_EXPORT=true
EXTERNAL_PARTICIPANT_INVITATION_AUTHORIZED=false
REAL_MODEL_CALL_AUTHORIZED=false
```

## Local validation

```bash
python3 -m unittest discover \
  -s TITMAS/private-stage5-1-trial/tests -p 'test_*.py' -v
```

# Controlled Pilot Threat Model

This v1.1 surface processes only tracked, local, public-safe files under the DBA
root. It has no network command, no write command, no GitHub operation and no
automatic Authority path.

## Deliberate controls

- canonical registry inputs must be regular, non-symlink, single-link files no
  larger than 1 MB;
- file paths must remain under the DBA root;
- participant and issuer records must be unexpired and unrevoked;
- one-way scope matching treats participant scope as the pattern and each task
  file scope as the candidate string;
- the decision reference and the human issuer are preserved separately;
- duplicate claims and unrecognized adversarial classes fail closed;
- the Harness validates all 22 attack classes against executable rejection
  policy.

The single-link rule is intentionally stricter than a general filesystem API.
It may reject an otherwise legitimate hard-linked checkout; the documented
remediation is to use an ordinary clean clone, not to weaken canonical-input
integrity.

The Harness imports the tracked local policy module to execute the adversarial
cases. This is local code execution under the same trust boundary as the test
suite; it is not a sandbox and is not claimed to validate compromised code.

Registry scans are linear and bounded by the 1 MB input limit. Large-scale
registries require a future performance review; no such scale is claimed here.

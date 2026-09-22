# TITMAS Stage 5 Private Python SDK

This dependency-free client connects only to the loopback Stage 5 Sandbox. It
constructs requests, sends an in-memory Sandbox Key, performs public Schema
preflight, parses customer-visible responses and exposes retry advice.

It contains no private core validation algorithm, internal policy, Provider
credential, fixed Token, repository access, administrative interface or
automatic retry executor.

```text
SDK_REDUCES_INTEGRATION_COST_NOT_GOVERNANCE=true
KEY_CONTROLS_ACCESS_NOT_OWNERSHIP=true
AUTOMATIC_RETRY=false
```

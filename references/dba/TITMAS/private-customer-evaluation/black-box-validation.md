# Black-box Validation Candidate

Only synthetic local files may be used in the current stage.

```bash
python3 -m json.tool TITMAS/private-customer-evaluation/agent-service-discovery.json >/dev/null
python3 -m json.tool TITMAS/private-customer-evaluation/api-contract.json >/dev/null
python3 -m json.tool TITMAS/private-customer-evaluation/synthetic-request.json >/dev/null
python3 -m json.tool TITMAS/private-customer-evaluation/synthetic-response.json >/dev/null
python3 -m json.tool TITMAS/private-customer-evaluation/error-codes.json >/dev/null
```

These commands validate syntax only. They do not call a service, prove value,
create Evidence Truth or authorize a real evaluation.

The private source checkout also contains a loopback-only gateway test suite:

```bash
python3 -m unittest discover \
  -s TITMAS/private-customer-evaluation/gateway/tests \
  -p 'test_*.py' -v
```

The customer-visible workspace is reconstructed from the nine top-level files.
The `gateway/` source and tests are not customer-visible.

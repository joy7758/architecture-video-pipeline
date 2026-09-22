# Public Contribution Activation Checklist

Status: `HISTORICAL_PASS_CURRENTLY_SUPERSEDED`

The templates were reviewed at the exact Activation PR head. The table below
records historical activation evidence; it is not current authorization.

| Required condition | Current state |
|---|---|
| `SECURITY_TRANSPORT_ACTIVE=true` | `MET` |
| `PUBLIC_CONTRIBUTION_SURFACE_AUTHORIZED=true` | `MET` |
| `COMMUNITY_HD_03=ACCEPT_AND_EXECUTE` | `MET` |
| `ACTIVATION_PR_CREATED=true` | `MET — PR #42 MERGED` |
| `ACTIVATION_PR_HUMAN_REVIEWED=true` | `MET — Human Owner review at 12c712d42d9fd710d966ea6b6e18d69dd51a8f87` |
| `ACTIVATION_PR_MERGED=true` | `MET — 3f1a32666f82e6096a0f9158a86e92573e895769` |
| `ACTIVE_TEMPLATE_HASHES_MATCH_DORMANT_PACKAGE=true` | `MET` |
| `COMMUNITY_STATUS_UPDATED=true` | `MET` |
| `ROLLBACK_TESTED=true` | `MET_DETERMINISTIC_FAIL_CLOSED_SIMULATION` |

If any condition is not met, activation fails closed.

```text
HISTORICAL_ACTIVATION_BLOCKED=false
PUBLIC_CONTRIBUTION_TEMPLATES_INSTALLED=true
PUBLIC_CONTRIBUTION_SURFACE_ACTIVE=false
PUBLIC_ACTIVATION_REQUIRES_SEPARATE_PR=true
```

# TITMAS FDO DTR Migration and PVS-0 Auxiliary Line Status v0.1

## Classification

```text
PORTFOLIO_ROLE=PUBLIC_EVIDENCE_AUXILIARY_LINE
MAINLINE_PRODUCT=false
NEW_RUNTIME=false
NEW_CONTROL_AUTHORITY=false
FORMAL_STANDARD=false
CERTIFICATION_SYSTEM=false
PUBLIC_ADOPTION_PROVEN=false
```

本记录把 Human Owner 于 2026-08-04 同步的 FDO DTR 迁移与 PVS-0 状态登记到 DBA 驾驶舱。GitHub 固定提交已公开核验；Zenodo DOI 解析入口可达。五条 DTR 记录的当前分类与迁移处理仍以 GWDG 后续答复和迁移预览为准。

## Asset roles

| PID | Current type | Governance role | Next action |
|---|---|---|---|
| `21.T11966/aro-audit-profile-v1` | `FdoProfile` | future ARO audit specification candidate | request owner-account draft migration |
| `21.T11966/fdo-operation-evidence-profile-v0-1` | `FdoProfile` | primary future execution-evidence specification candidate; v0.1 historical experimental baseline | request owner-account draft migration |
| `21.T11966/aro-audit-manifest-v1` | `BasicInfoType` | non-normative demonstration and history | preserve type and provenance |
| `21.T11966/aro-audit-demo-obj-v1` | `BasicInfoType` | non-normative demonstration object | preserve type and provenance |
| `21.T11966/aro-audit-demo-do-1` | `FdoService` | demonstration service instance | preserve type; never reclassify as data type |

If a target registry cannot preserve a record's type and provenance, migration must pause instead of silently reclassifying it.

## Public verification references

- Repository: `joy7758/titmas-fdo-public-verification`
- Frozen commit: `1dcca69d0bcc2ee94b7e3ef0c80f21536cd39d1c`
- Record DOI: `10.5281/zenodo.21778954`
- Concept DOI: `10.5281/zenodo.21778953`
- Reported offline validation: `10/10 PASS`
- Reported archive size: `43 files`

These references support independent inspection of a bounded public slice. They do not establish operational correctness, external adoption, complete conformance, legal compliance, certification or commercial availability.

## Current gate

```text
FDO_MIGRATION_LINE_STATUS=WAITING_FOR_GWDG_RESPONSE
PVS0_STATUS=PUBLIC_ARCHIVED_MAINTENANCE_MODE
PROFILE_CANDIDATE_COUNT=2
NON_NORMATIVE_DEMO_ASSET_COUNT=3
V1_STANDARD_AUTHORIZED=false
NEXT_ALLOWED_ACTION=ACCOUNT_BINDING_MIGRATION_PREVIEW_AND_CLASSIFICATION_ACCEPTANCE_ONLY
```

This auxiliary line is frozen against feature expansion. Mainline resources remain focused on real execution-evidence intake, cross-runtime interoperability and a first bounded adoption case.

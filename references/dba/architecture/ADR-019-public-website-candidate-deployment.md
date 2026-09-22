---
adr_id: ADR-019
title: TMAI Public Website Candidate Deployment
title_zh: TMAI 公开网站候选部署
status: accepted-and-executed-for-website-candidate-only
decided_at: 2026-07-21
decided_by_ref: user-thread-authorization-2026-07-21-server-cleanup-and-bilingual-site
execution_scope: public-website-candidate
developer_preview_release_authorized: false
production_runtime_authorized: false
---

# ADR-019: TMAI Public Website Candidate Deployment

## Context

The Baidu Cloud host contained an obsolete SAEE website and an obsolete Agent
Evidence Receipt container stack. The previously proposed DQ-013 path assumed
that these assets had to remain in place and therefore recommended a separate
`/trusted-multi-agent-infrastructure/` route.

The Human Owner explicitly declared the old application assets obsolete,
authorized their complete removal while preserving the operating system,
certificate, and security configuration, and requested an OpenTelemetry-inspired
Chinese/English public website.

## Decision

1. Remove only the obsolete `/srv/saee` and `/srv/agent-evidence-receipt`
   application assets and their associated containers, images, volume, network,
   build cache, and old Nginx site configuration.
2. Preserve SSH, Nginx, Docker, Certbot, Let's Encrypt certificate material,
   firewall, fail2ban, and Baidu Cloud system agents.
3. Deploy the bilingual TMAI website candidate at `https://redcrag.cn/` using
   immutable source-revision directories and an atomic `current` symlink.
4. Publish the identical website artifact as an explicit GitHub prerelease named
   `TMAI Public Website Candidate v0.1`.
5. Keep `DEVELOPER_PREVIEW_RELEASED=false` until DQ-009 is separately decided.

## Consequences

- The original DQ-013 isolated-path question is `SUPERSEDED`; its preservation
  premise no longer exists.
- The public domain now has one TMAI front door with Chinese and English routes.
- Website deployment is not permission to expose DBOS, amend the SAEE public
  boundary, select a license, recruit trial participants, or declare a Developer
  Preview release.
- Every deployed artifact exposes `release.json` and a SHA-256
  `release-manifest.json`.
- Rollback uses an atomic symlink switch and has been exercised against a
  previous verified artifact.

## Boundary

```text
PUBLIC_WEBSITE_CANDIDATE_DEPLOYED=true
GITHUB_WEBSITE_PRERELEASE_PUBLISHED=true
DEVELOPER_PREVIEW_RELEASED=false
PRODUCTION_READY=false
AGENT_CREATED=false
RUNTIME_CREATED=false
PERMISSION_CREATED=false
```

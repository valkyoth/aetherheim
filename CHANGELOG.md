# Changelog

All notable changes to Aetherheim are documented here.

## Unreleased

- Clarified that Android and iOS are not server or embedding targets, removed
  their misleading pre-1.0 build claims, and added a granular post-1.0 roadmap
  for secure, fully native applications that connect to supported Aetherheim
  servers.
- Audited every documented requirement against the roadmap, introduced
  foundation-time traceability and an early SQLite CMS preview, added missing
  HTTP/TLS, analytics, AI, media, packaging, and provider qualification stops,
  and split oversized cross-domain milestones into independently testable
  versions.
- Removed an undeclared ripgrep dependency from shell gates so clean GitHub
  runners use standard `grep` and added a regression policy check.
- Pinned and installed `cargo-sbom 0.10.0` in CI, added it to live tool
  freshness checks, and clarified that freestanding `no_std` portability is not
  a present Aesynx operating-system support claim.
- Initialized the minimal-dependency Rust workspace and reviewed dependency
  admission policy.
- Added the first `no_std` core, bounds, identifier, and proof-contract crates.
- Added security, release, documentation, CI, licensing, and platform policy.
- Defined the detailed conventional-storage roadmap to 1.0 and kept Skrifheim
  integration optional and post-1.0.
- Added SurrealDB to the planned database adapters, conformance matrix, and
  cross-provider migration path.
- Planned optional Valkey cache offload, OpenBao startup-secret import,
  active-active Aetherheim nodes, and Fluxheim edge deployments.
- Prohibited direct and transitive `zeroize`; planned proportional secret
  handling through the project-owned `sanitization` crate.
- Added a launchable black-box acceptance entry point and made real-process,
  live-provider, packaged-artifact, and failure scenarios mandatory for support
  claims.
- Simplified releases to a user-controlled pentest/findings/commit/GitHub/tag
  loop and added explicit cumulative pentest batches capped at 15 releases.

## 0.1.0 - Planned

- Repository foundation; no production CMS behavior is claimed.

# Aetherheim 0.1.0 Release Notes

Status: planned

## Summary

`0.1.0` establishes the repository, policy, documentation, and modular Rust
foundation for Aetherheim. It is not a usable CMS release.

## Added

- Rust 1.97.1, edition 2024, resolver 3 workspace.
- Minimal-dependency main facade/binary plus focused first-party support crates;
  the initial graph happens to contain no external crates.
- `no_std` core, bounds, identifier, and proof-readiness contracts.
- EUPL-1.2 project licensing and independent theme/plugin licensing guidance.
- Linux, Windows, BSD, macOS, Android, and iOS target policy plus freestanding
  `no_std` checks to avoid OS lock-in; Aesynx is not an existing target or
  support claim.
- CI, security policy, dependency denial, release gates, and CodeQL-default
  setup guidance.
- Detailed implementation and version plans with human-controlled pentest
  stops and optional explicitly authorised cumulative batches.
- Optional future Valkey cache, OpenBao bootstrap, multi-node, and Fluxheim
  deployment tracks with separate security and conformance gates.
- A proportional `sanitization` secret-memory policy and direct/transitive
  `zeroize` prohibition.
- A runnable foundation black-box acceptance suite and mandatory future
  real-process/live-provider scenario policy.
- A single human-controlled release gate with temporary root `PENTEST.md`
  remediation, permanent reports, GitHub wait, explicit tag/push authority, and
  optional user-authorised cumulative batches capped at 15 releases.
- crates.io publication disabled for every package.

## Security Notes

- GitHub gate portability was corrected after the initial CI run exposed an
  undeclared ripgrep dependency; shell gates now use standard `grep` and reject
  reintroduction of `rg` commands.
- GitHub installs and freshness-checks the exact `cargo-sbom 0.10.0` tool used
  by the mandatory committed-SBOM drift gate.
- No external Rust crates are needed by the initial foundation; future crates
  require discussion, exact pinning, admission review, and boundary tests.
- The inspected `openbao` 2.1.2 graph is not yet admissible because it currently
  contains transitive `zeroize`, including through `secrecy` and parts of its
  default rustls stack; OpenBao support waits for a zeroize-free graph.
- All networking, authentication, storage, rendering, upload, extension, and
  commerce behavior remains unimplemented and fail closed.
- Skrifheim is not integrated and is not a 1.0 dependency.
- This release is not suitable for production use.

## Verification

```bash
scripts/checks.sh
scripts/release_0_1_gate.sh
```

# Supply-Chain Security

## Product Dependency Rule

Aetherheim prefers first-party workspace-local `path` crates and admits only a
small, justified external set. Before adding a crates.io dependency:

- discuss why it is needed and why existing code or the standard library is
  insufficient;
- use the latest compatible stable release and an exact `=X.Y.Z` pin;
- record purpose, scope, licence, and review date in
  `dependency-admissions.toml`;
- inspect maintainership, security history, unsafe/native code, default and
  optional features, transitive dependencies, build scripts, and platform
  impact;
- disable unnecessary features and defaults;
- place it behind an Aetherheim-owned interface and add conformance, negative,
  and failure tests;
- run Cargo deny, audit, SBOM, and freshness gates.

Git dependencies, custom registries, undeclared crates, inexact versions, and
unreviewed vendoring are denied. Every workspace package remains private with
`publish = false`.

External tools such as Rustup, Cargo, Clippy, rustfmt, Cargo deny/audit, SBOM
generation, GitHub Actions, platform linkers, and container tools are reviewed
separately from the product graph. They still require current-version checks,
exact pins where possible, least privilege, and release evidence.

## Update Cadence

- Check the official Rust stable manifest and CI/tool pins before every tag.
- Review monthly even when no release is planned.
- Apply security toolchain patches immediately after compatibility review.
- Record tool changes in the changelog and release notes.
- Never auto-merge a toolchain, action, or build-image change into a release.

## Release Artifacts

The roadmap requires checksums, signatures through an explicit provider,
component/platform SBOMs, provenance, clean builders, and offline verification.
No release package is uploaded to crates.io.

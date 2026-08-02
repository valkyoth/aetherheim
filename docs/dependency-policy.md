# Dependency Policy

Aetherheim aims for the smallest practical audited dependency graph, not a zero
dependency graph. Reimplementing mature cryptography, TLS, WebAuthn, database
clients, Unicode processing, media codecs, or WebAssembly execution would
increase risk and delay the product.

## Admission Process

Before adding an external Rust crate:

1. Discuss the need and alternatives.
2. Confirm the latest stable version compatible with the pinned Rust release.
3. Pin it exactly as `{ version = "=X.Y.Z", ... }` in workspace dependencies.
4. Add a matching entry to `dependency-admissions.toml` with purpose, affected
   scopes, licence, and review date.
5. Review maintainers/ownership, release activity, advisories, unsafe and native
   code, build scripts, features, transitive graph, platform support, and
   licence compatibility.
6. Disable unnecessary default/optional features.
7. Put the crate behind a narrow Aetherheim-owned contract so it cannot spread
   implementation types or ambient authority through domain crates.
8. Add positive, negative, conformance, resource, and failure tests appropriate
   to the boundary.
9. Run freshness, Cargo deny, Cargo audit, SBOM, platform, and pentest gates.

Dependencies are reconsidered during upgrades. A crate can be removed or
replaced if maintenance, security, scope, or transitive cost changes.

## Project-Owned External Crates

Crates maintained in sibling projects still pass normal admission because they
have separate releases and dependency graphs. Aetherheim plans to use
`sanitization` for secret memory and `openbao` for the optional OpenBao adapter.
Both are exact-pinned at implementation time and wrapped by focused Aetherheim
crates.

`zeroize` is prohibited as either a direct or transitive crate. This also means
an otherwise acceptable crate cannot be admitted while its selected feature
graph brings in `zeroize`. The currently inspected `openbao` 2.1.2 graph does
so through `secrecy` and parts of its default rustls stack; OpenBao work
therefore remains blocked at its admission milestone until a zeroize-free graph
is available and reviewed.

## Source Rules

- crates.io is the only admitted registry.
- Git and custom-registry dependencies are denied.
- Versions are exact, not wildcard, caret, tilde, or range requirements.
- Workspace path dependencies remain exact-versioned and inside the repository.
- Vendoring requires a separate policy change and review; copying source is not
  a shortcut around admission.
- Development, build, test, benchmark, and fuzz dependencies follow the same
  admission process.

## Publishing

Dependency admission does not change the publishing policy. Every Aetherheim
workspace package remains `publish = false`; no project crate is uploaded to
crates.io until that separate policy is explicitly changed.

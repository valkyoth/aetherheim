# Dependency Policy

Aetherheim aims for the smallest practical audited dependency graph, not a zero
dependency graph. Reimplementing mature cryptography, TLS, WebAuthn, database
clients, Unicode processing, media codecs, or WebAssembly execution would
increase risk and delay the product.

Dependency admission, adapter behavior, and live provider qualification are
separate release stops for security-sensitive foundations. Aetherheim does not
build SQLite engines, database wire/authentication protocols, TLS stacks,
browser-grade HTML parsers, media codecs/parsers, password hashing, WebAuthn,
HTTP runtimes, or WebAssembly engines merely to reduce the crate count.

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

A general transitive-version or policy exception requires explicit user
approval and a written time-bounded ADR with owner, security comparison,
expiry, and removal/review plan. It remains visible in metadata, the SBOM, and
release evidence. There is no exception path for direct or transitive
`zeroize`.

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
therefore remains blocked until an in-process or separately contained
zeroize-free graph is available and reviewed. Process isolation does not waive
the repository's zeroize prohibition.

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

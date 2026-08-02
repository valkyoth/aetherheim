# Security Controls

## Foundation Controls

- Rust 1.97.1 pinned and checked against the official stable channel.
- Edition 2024, resolver 3, overflow checks in release, aborting release panic.
- Unsafe code forbidden across the current workspace.
- Minimal external dependency policy with discussion, exact pins, an admission
  register, licence/source checks, and boundary tests.
- Direct and transitive `zeroize` prohibited; planned secret owners use the
  reviewed `sanitization` crate with proportional data-classification and
  performance gates.
- crates.io publication disabled in every package.
- Non-generated Rust files capped at 500 lines.
- Core portable contracts are `no_std`.
- Strict Clippy and documentation lints.
- Launchable black-box foundation smoke in the ordinary local and CI gate.
- Full-SHA GitHub Actions, least-privilege workflow permissions, Dependabot,
  CodeQL default setup, Cargo deny/audit, SBOM, and human-controlled individual
  or explicitly authorised cumulative pentest gates.

## Product Controls Required Before Claims

- typed validation and resource budgets at every untrusted boundary;
- central contextual output escaping and versioned sanitisation;
- opaque revocable browser sessions and central authorisation;
- tenant/site/environment/locale/viewer-scoped queries and caches;
- append-oriented revisions, audit, monetary journals, and receipts;
- upload quarantine and isolated media processing;
- capability-scoped extension execution without ambient authority;
- explicit provider identity, timeouts, quotas, retries, and secret handles;
- optional OpenBao bootstrap with allowlisted environment import, clean child
  environment, narrow authority, and fail-closed partial-write handling;
- non-authoritative remote cache behavior and cache-poisoning isolation;
- authenticated cluster peers, fenced leases, readiness withdrawal, safe drain,
  partition handling, and rolling-version compatibility;
- trusted-proxy enforcement and an independently tested optional Fluxheim
  deployment profile;
- deterministic migrations, backup verification, and isolated restore;
- signed artifacts, checksums, SBOM, provenance, and rollback policy.
- real-process, live-provider, packaged-artifact, and injected-failure
  acceptance evidence; mocks cannot establish a support claim.

Controls are release-scoped. A planned control is not an implemented control.

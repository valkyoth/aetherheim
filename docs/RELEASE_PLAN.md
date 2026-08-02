# Aetherheim Release Plan To 1.0 And Optional Post-1.0 Assurance

Status: planning document

This plan is intentionally granular. Aetherheim is security-sensitive content
infrastructure, so every version must be small enough to implement, review,
test, pentest, and stop cleanly. The list is not a maximum: split a release or
insert a patch version whenever a change no longer fits one safe review pass.

Tags use:

```text
v0.N.0       one pre-1.0 implementation milestone
v0.N.P       compatible correction or additional safety gate
v1.0.0-rc.N exact production candidate
v1.0.0       first serious production release
v1.N.0       optional post-1.0 capability milestone
```

The existing numbering through `v0.130.0` is intentional and stable. Aetherheim
does not compress work merely to stay below `v0.99.0`; changing established
version identities would make release notes, pentest evidence, migration
fixtures, and compatibility references ambiguous. Patch milestones may grow to
any needed value, such as `v0.60.13`, while `v1.0.0` remains the first serious
production release.

Every milestone is an exact-commit implementation and evidence stop, but it is
not automatically a broad end-user support claim. A capability becomes
supported only when its owning implementation, live qualification, packaging,
documentation, and profile gates pass. The pentest workflow remains mandatory
for every version unless the user explicitly authorises a named batch of at
most 15 versions.

Milestones are split whenever one stop would admit a dependency and implement
it, combine independent state machines/domains, qualify multiple platforms or
providers, or require unrelated migration/rollback and threat reviews. A stop
should normally introduce one authority boundary or one independently
reversible behavior.

No version is published to crates.io. Release means signed source, platform
artifacts, containers where applicable, SBOM/provenance, notes, and pentest
evidence—not Cargo registry publication.

## Inherited Release Gate

Every version below additionally requires:

- an ADR/design note and threat-model delta before implementation;
- tests written for new authority, data, parser, resource, migration, and
  failure paths;
- `scripts/checks.sh`, formatting, Clippy, unit/integration/doc tests, platform
  checks, line-limit checks, dependency/no-publish policy, and docs validation;
- live `scripts/check_latest_tools.sh` confirmation that Rust stable, external
  Cargo security tools, and GitHub Action pins are current;
- current-official-source review for any standard/control baseline touched by
  the release, with version changes recorded rather than silently reinterpreted;
- `cargo deny check` and `cargo audit` across the complete admitted dependency
  graph;
- manifest and lockfile proof that direct and transitive `zeroize` are absent;
- `scripts/acceptance.sh all` black-box evidence from real Aetherheim processes
  and, for every claimed integration, live supported provider versions; mocks
  and skipped scenarios cannot establish support;
- a current SBOM and supply-chain review;
- release notes, limitations, migration/rollback instructions, and explicit
  non-claims;
- GitHub CI success and CodeQL default setup review;
- `scripts/check_pentest_evidence.py VERSION` acceptance of either an individual
  PASS report or an explicitly user-authorised batch report covering no more
  than 15 listed releases; the final batched release requires cumulative PASS;
- no unresolved release-blocking finding known from review, testing, pentest,
  or GitHub.

The final line of each milestone is a mandatory pentest handoff by default. An
explicit user batch authorisation changes that stop to a truthful intermediate
deferral for listed releases only. Findings arrive through root `PENTEST.md`,
are fixed and copied into permanent history, and the scratch file is removed.
After a green report Codex commits and waits for GitHub; GitHub failures are
fixed and recorded. Tagging and pushing happen only after GitHub is green and
the user explicitly instructs it. See
[release-workflow.md](release-workflow.md).

## Required Milestone Format

Each milestone contains Status, Goal, Deliverables, Verification, and Exit
criteria. Release-specific verification is additive to the inherited gate.

## Phase 0 — Repository and engineering discipline

### v0.1.0 — Repository Foundation

Status: in implementation.

Goal: Establish the serious workspace and policy baseline.

Deliverables:

- Pinned Rust 1.97.1; EUPL-1.2; modular crates; CI; security, licensing, toolchain, modularity, threat, and release documentation; crates.io publication disabled.

Verification:

- Run the full local gate, host tests, manifest policy test, and README/document-link checks.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.1.0 implementation stop reached. Run pentest for this exact commit.`

### v0.2.0 — Release Evidence Gate

Status: planned.

Goal: Make a release claim impossible without its evidence.

Deliverables:

- Release-note validator; individual and cumulative pentest-report schemas; temporary `PENTEST.md` guard; 15-release batch limit; tag-existence guard; permanent report workflow; release-candidate parsing.

Verification:

- Exercise pass/fail fixtures for missing notes, malformed versions, temporary findings, absent evidence, unauthorised deferral, overlapping/oversized batches, and a deferred final batch release.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.2.0 implementation stop reached. Run pentest for this exact commit.`

### v0.3.0 — Tool Freshness Gate

Status: planned.

Goal: Make stable Rust and security tooling drift visible.

Deliverables:

- Official stable-manifest check; exact external Cargo-tool version checks; full-SHA GitHub Action validation; monthly maintenance policy.

Verification:

- Run offline parser fixtures and the live latest-tool query; reject stale pins and malformed action references.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.3.0 implementation stop reached. Run pentest for this exact commit.`

### v0.4.0 — Dependency Admission Gate

Status: planned.

Goal: Keep the external Cargo graph minimal, current, discussed, and reviewed.

Deliverables:

- Manifest scanner; exact crates.io pins; admission register; path-within-workspace validation; git/custom-registry rejection; vendoring guard; Cargo metadata cross-check.

Verification:

- Test admitted, unadmitted, inexact, git, custom-registry, conflicting-version, path-escape, and stale-register fixtures.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.4.0 implementation stop reached. Run pentest for this exact commit.`

### v0.4.1 — Dependency Usability And Exception Review

Status: planned.

Goal: Prevent a minimal-crate rule from forcing unsafe custom implementations or unusable builds.

Deliverables:

- Measured build/runtime cost review; duplicate-version and feature-unification policy; user-approved, time-bounded transitive-exception ADR schema; owner, expiry, replacement plan, and recurring review. The direct and transitive `zeroize` ban remains non-exemptible.

Verification:

- Fixtures reject silent, expired, unowned, unmeasured, or authority-broadening exceptions and prove an approved exception is visible in metadata, SBOM, documentation, and release evidence.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No exception can be created implicitly by Cargo resolution or used to avoid the required dependency discussion.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.4.1 implementation stop reached. Run pentest for this exact commit.`

### v0.5.0 — No-Publish Gate

Status: planned.

Goal: Prevent accidental crates.io publication.

Deliverables:

- Explicit `publish = false` validation for every package; workspace-member inventory; CI and release checks; packaging non-claim.

Verification:

- Remove or alter `publish = false` in fixtures and verify the gate rejects the workspace.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.5.0 implementation stop reached. Run pentest for this exact commit.`

### v0.6.0 — Modularity Gate

Status: planned.

Goal: Keep implementation reviewable as the product grows.

Deliverables:

- 500-line Rust-file ceiling; 300-line split warning; facade boundary checks; dependency-direction inventory; crate-purpose registry.

Verification:

- Test line-limit, missing-boundary, facade-implementation, and outward-core dependency violations.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.6.0 implementation stop reached. Run pentest for this exact commit.`

### v0.6.1 — Cargo Metadata Architecture Gate

Status: planned.

Goal: Enforce crate boundaries from the resolved workspace graph before the workspace grows.

Deliverables:

- Package-purpose registry; allowed dependency layers; facade-purity and feature checks; workspace inheritance checks; duplicate-package report; no_std/std boundary classification; machine-readable exceptions.

Verification:

- Deliberately violate every dependency direction, facade, feature, inheritance, purpose, and portability rule and prove the metadata gate rejects it with an actionable diagnostic.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every workspace member is classified and no new crate can enter without a declared layer and purpose.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.6.1 implementation stop reached. Run pentest for this exact commit.`

### v0.7.0 — Platform Compile Matrix

Status: planned.

Goal: Prove target portability from the first development line.

Deliverables:

- Linux GNU/musl, Windows GNU/MSVC, FreeBSD, NetBSD, macOS, Android, iOS, and freestanding core target checks.

Verification:

- Compile the supported workspace subset for every declared target and verify unsupported host adapters fail explicitly.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.7.0 implementation stop reached. Run pentest for this exact commit.`

### v0.8.0 — Unsafe and Secret Policy

Status: planned.

Goal: Make unsafe code and secret exposure exceptional.

Deliverables:

- Workspace unsafe prohibition; future exception protocol; redacted Debug rules; secret-file scanning; diagnostic/export non-disclosure rules.

Verification:

- Compile and source fixtures prove unsafe, plaintext secret formatting, and secret-like committed files are rejected.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.8.0 implementation stop reached. Run pentest for this exact commit.`

### v0.8.1 — Sanitization Secret Memory Baseline

Status: planned.

Goal: Establish proportional secret-memory handling through the project-owned `sanitization` crate without admitting `zeroize`.

Deliverables:

- Exact crate/feature admission, Aetherheim-owned secret wrappers, data-classification policy, bounded exposure, redacted formatting, direct and transitive `zeroize` lockfile gate, target guarantees, and performance budgets.

Verification:

- Manifest, source, and lockfile fixtures reject `zeroize`; lifecycle, redaction, allocation-failure, cancellation, platform, memory, latency, and throughput tests justify each enabled sanitization profile.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.8.1 implementation stop reached. Run pentest for this exact commit.`

### v0.9.0 — Deterministic Testkit

Status: planned.

Goal: Provide first-party testing without external test crates.

Deliverables:

- Deterministic IDs, clocks, byte mutation, fixture builders, failure injection, table/property sweep helpers, and redaction assertions.

Verification:

- Run self-tests twice and compare fixture output byte-for-byte across supported host architectures.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.9.0 implementation stop reached. Run pentest for this exact commit.`

### v0.9.1 — Executable Acceptance Harness

Status: planned.

Goal: Make launched-system behavior mandatory evidence from the first runnable release onward.

Deliverables:

- Stable `scripts/acceptance.sh all` entry point, scenario registry and IDs, process supervisor, bounded/redacted logs, clean-state fixtures, failure artifacts, timeout/cleanup policy, support-matrix mapping, and explicit no-skip release semantics.

Verification:

- Harness self-tests prove exit status propagation, timeout, crashed child, missing provider/tool, log redaction, cleanup, parallel isolation, artifact retention, and skipped/quarantined scenario rejection.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.9.1 implementation stop reached. Run pentest for this exact commit.`

### v0.9.2 — Foundation Requirement And Scenario Registry

Status: planned.

Goal: Establish traceability before product milestones accumulate.

Deliverables:

- Minimal machine-readable requirement, threat, control, scenario, owning-version, implementation, evidence, status, and exception records; stable IDs; orphan/duplicate/stale checks; generated coverage summary; migration path to the later standards catalog.

Verification:

- Self-tests reject missing or multiple owners, absent threats/scenarios, stale evidence, unknown versions, expired exceptions, changed behavior without scenario updates, and generated-report drift.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every milestone from `v0.10.0` onward must register its requirements and scenarios in the same change; traceability is never reconstructed retrospectively.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.9.2 implementation stop reached. Run pentest for this exact commit.`

### v0.10.0 — Runnable Skeleton

Status: planned.

Goal: Produce one truthful binary without implying CMS functionality.

Deliverables:

- `aetherheim help`, `--version`, and `doctor`; typed process roles; stable exit codes; no network listeners or hidden services.

Verification:

- Black-box acceptance launches the compiled executable and covers every command, unknown input, output/exit contracts, restart, diagnostics, and absence of ambient network/storage behavior; unit/golden tests are additional evidence.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.10.0 implementation stop reached. Run pentest for this exact commit.`

### v0.10.1 — Typed Configuration Contract

Status: planned.

Goal: Define configuration sources and validation before network or storage adapters exist.

Deliverables:

- Versioned typed schema; defaults; file/environment/CLI precedence; explicit secret references; unknown/deprecated field policy; tenant-independent bootstrap scope; path/origin metadata; redacted effective-config report; migration and rollback rules.

Verification:

- Unknown, duplicate, conflicting, malformed, oversized, deprecated, secret-bearing, path-confused, platform-specific, and old/new schema fixtures fail or migrate exactly as documented.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Later adapters consume validated typed configuration and cannot read ambient environment variables independently.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.10.1 implementation stop reached. Run pentest for this exact commit.`

### v0.10.2 — Process Role Lifecycle And Health

Status: planned.

Goal: Give serve, worker, scheduler, and future realtime roles one bounded lifecycle contract.

Deliverables:

- Startup phases; dependency initialization; liveness/readiness distinction; signal/control handling; graceful drain and deadline; child-process ownership; exit taxonomy; restart safety; role compatibility and unsupported-role rejection.

Verification:

- Partial startup, duplicate start, signal at every phase, hung dependency, child crash, drain timeout, forced termination, restart, and incompatible-role scenarios pass on supported host platforms.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every future executable role plugs into the same observable lifecycle rather than inventing shutdown and readiness behavior.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.10.2 implementation stop reached. Run pentest for this exact commit.`

### v0.10.3 — Structured Diagnostics And Redaction

Status: planned.

Goal: Provide useful operator diagnostics without leaking secrets or unbounded attacker-controlled data.

Deliverables:

- Structured event envelope; severity/component/operation/correlation fields; classification-aware redaction; bounded values/cardinality; safe console and machine formats; panic/abort boundary; diagnostic bundle manifest and retention controls.

Verification:

- Control-character/log injection, oversized/high-cardinality fields, secrets/tokens/personal data, malformed Unicode, nested errors, panic paths, concurrent output, and diagnostic export fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- All later crates use the shared diagnostic contract; ad hoc secret-bearing formatting is rejected.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.10.3 implementation stop reached. Run pentest for this exact commit.`

## Phase 1 — Portable domain foundations

### v0.11.0 — Stable Error Taxonomy

Status: planned.

Goal: Define non-panicking public and internal error classes.

Deliverables:

- Bounded error codes; safe display text; internal correlation references; source-chain redaction; compatibility rules.

Verification:

- Table-test every error code, redaction path, formatting mode, and unknown-code handling.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.11.0 implementation stop reached. Run pentest for this exact commit.`

### v0.12.0 — Resource Budget Types

Status: planned.

Goal: Require explicit limits at untrusted boundaries.

Deliverables:

- Byte, item, depth, allocation, work, time, and output budgets with checked accounting.

Verification:

- Sweep boundary values and prove exhaustion is atomic, deterministic, and non-panicking.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.12.0 implementation stop reached. Run pentest for this exact commit.`

### v0.12.1 — Aggregate Budgets And Streaming Admission

Status: planned.

Goal: Make nested and multi-stage untrusted input obey one cumulative resource envelope.

Deliverables:

- Encoded-size, element, nesting, traversal, expansion, allocation, work, output, and deadline accounting; budget subdivision; streaming/preflight interfaces; bounded partial-read policy.

Verification:

- Deep/wide/compressed-shaped inputs, deceptive length prefixes, repeated small allocations, cumulative host calls, cancellation, and one-over-limit sweeps fail before uncontrolled allocation or partial authority change.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every later parser and boundary can consume the same checked aggregate budget without inventing private limit semantics.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.12.1 implementation stop reached. Run pentest for this exact commit.`

### v0.13.0 — Opaque Identifier Domains

Status: planned.

Goal: Separate tenant, site, content, revision, actor, and operation identities.

Deliverables:

- Nonzero 128-bit wrappers; parse/format contracts; no embedded authority; generation-provider boundary.

Verification:

- Round-trip valid fixtures; reject zero, malformed, ambiguous, and cross-domain uses at compile or parse time.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.13.0 implementation stop reached. Run pentest for this exact commit.`

### v0.13.1 — Identifier Generation And Domain Completion

Status: planned.

Goal: Complete identity domains and make generation safe, injectable, and operationally diagnosable.

Deliverables:

- IDs for events, jobs, leases, sessions, packages, payments, inventory, audit, idempotency, and correlation; canonical external encoding; entropy/clock provider contracts; collision response; database uniqueness rules; log-safe correlation form.

Verification:

- Known/unknown domain, ambiguous encoding, weak/repeated entropy, clock reversal, concurrent collision, persistence conflict, and cross-domain compile/parse fixtures pass; no identifier is accepted as authorization or a secret.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every currently planned authority-bearing aggregate has a separate ID type and deterministic test provider before application state is introduced.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.13.1 implementation stop reached. Run pentest for this exact commit.`

### v0.13.2 — Entropy Provider And Random Token Generation

Status: planned.

Goal: Provide cryptographically secure host randomness without making IDs, sessions, challenges, or tokens depend on ambient ad hoc calls.

Deliverables:

- OS/provider admission; startup health and no-weak-fallback policy; bounded fill/generation interface; fork/snapshot/clone considerations; domain-separated token purposes; deterministic test provider isolation; platform support and failure diagnostics.

Verification:

- Provider unavailable/short/error/repetition fixtures, fork/snapshot simulations, concurrent generation, token-domain confusion, deterministic-provider production exclusion, collision handling, redaction, and platform tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Security tokens and identifiers cannot be generated when approved entropy is unavailable, and test randomness cannot enter production builds.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.13.2 implementation stop reached. Run pentest for this exact commit.`

### v0.14.0 — Time and Duration Contracts

Status: planned.

Goal: Represent time without provider assumptions.

Deliverables:

- Instant, duration, timezone-reference, schedule, trusted-time confidence, and clock-provider contracts.

Verification:

- Test overflow, ordering, DST-shaped fixtures, untrusted client time, and unavailable trusted clocks.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.14.0 implementation stop reached. Run pentest for this exact commit.`

### v0.14.1 — Host Clock, Timezone, And Monotonic-Time Providers

Status: planned.

Goal: Map host wall, monotonic, timezone, and trusted-database time into explicit domain contracts.

Deliverables:

- Wall/monotonic/database-time provider interfaces; confidence/source; timezone-data version; skew/backward-jump policy; deadline conversion; schedule evaluation inputs; deterministic test clocks; platform and update behavior.

Verification:

- Backward/forward jumps, suspend/resume, overflow, timezone database update, DST gap/fold, clock skew, unavailable database time, deadline conversion, concurrent timers, and platform fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Security expiry, leases, schedules, and deadlines name their accepted time source and never silently substitute client wall time.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.14.1 implementation stop reached. Run pentest for this exact commit.`

### v0.15.0 — Portable Scalar Values

Status: planned.

Goal: Define provider-neutral primitive content values.

Deliverables:

- Boolean, signed/unsigned integer, bounded text/bytes, decimal parts, URL/email-shaped validated domains, and opaque values.

Verification:

- Exhaust boundary conversions, canonical comparisons, and malformed representations.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.15.0 implementation stop reached. Run pentest for this exact commit.`

### v0.15.1 — Unicode Text Semantics

Status: planned.

Goal: Admit mature Unicode foundations and freeze canonical comparison versus display behavior.

Deliverables:

- Exact Unicode normalization/segmentation/property admissions; data-version metadata; scalar validity; canonical storage/display forms; confusable/mixed-script and bidi diagnostics; grapheme/word boundaries; encoded/display length budgets; update compatibility policy.

Verification:

- Malformed scalars, normalization equivalence, combining/deep sequences, bidi controls, confusables, mixed scripts, grapheme/word boundaries, length amplification, data-version drift, and cross-platform golden fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Security comparison never depends on display text or platform locale, and no application module invents private Unicode normalization.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.15.1 implementation stop reached. Run pentest for this exact commit.`

### v0.15.2 — URL And IDNA Semantics

Status: planned.

Goal: Admit mature URL/IDNA parsing and define canonical host, origin, and display forms.

Deliverables:

- Exact URL/IDNA parser/data admissions; supported schemes; canonical parse/serialize; host/port/origin comparison; percent encoding; path/query component types; IPv4/IPv6/zone policy; IDNA display diagnostics; relative-resolution and update compatibility rules.

Verification:

- Scheme/authority/userinfo confusion, backslash/control/percent encoding, IPv4/IPv6 variants, mixed-script/IDNA deviations, default ports, relative/base resolution, browser differential fixtures, resource limits, and version drift pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Routing, SSRF defenses, redirects, webhooks, media, themes, mail, and plugins use one typed URL/origin contract.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.15.2 implementation stop reached. Run pentest for this exact commit.`

### v0.15.3 — Email Address Semantics

Status: planned.

Goal: Define bounded email parsing, storage, comparison, and display without inventing deliverability or identity guarantees.

Deliverables:

- Exact parser admission if needed; supported syntax/internationalization profile; local/domain/display separation; IDNA domain handling; canonical comparison policy by verified communication point; length/control/header safety; redacted display; explicit non-deliverability/non-ownership claims.

Verification:

- Malformed/oversized/control characters, quoted/comment/international forms by declared scope, IDNA domains, case/comparison ambiguity, header injection, duplicate verified identities, redaction, provider round-trip, and version compatibility pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Parsing an address never proves ownership or deliverability, and identity/mail modules share the same declared syntax/comparison rules.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.15.3 implementation stop reached. Run pentest for this exact commit.`

### v0.16.0 — Money and Measurement Values

Status: planned.

Goal: Make money and units exact and explicit.

Deliverables:

- Currency identifier, minor/decimal scale, rounding policy descriptor, measurement unit, and immutable calculation component.

Verification:

- Property sweeps prove no floating-point path, overflow rejection, and stable rounding fixtures.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.16.0 implementation stop reached. Run pentest for this exact commit.`

### v0.17.0 — Bounded Collections

Status: planned.

Goal: Provide allocation-aware portable collections.

Deliverables:

- Caller-buffer and `alloc` profiles; maximum length; deterministic ordering; fallible growth; duplicate policy.

Verification:

- Test zero capacity, exact capacity, one-over, allocation failure simulation, and duplicate semantics.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.17.0 implementation stop reached. Run pentest for this exact commit.`

### v0.18.0 — Canonical Encoding Frame

Status: planned.

Goal: Establish versioned deterministic binary framing.

Deliverables:

- Domain separation; required/optional feature bits; length prefixes; ordering; unknown-field rules; exact consumption.

Verification:

- Golden fixtures across targets plus malformed, duplicate, truncated, oversized, and trailing-byte rejection.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.18.0 implementation stop reached. Run pentest for this exact commit.`

### v0.18.1 — Digest Provider And Domain-Separated Roots

Status: planned.

Goal: Admit mature digest implementations and define how canonical roots are computed.

Deliverables:

- Exact algorithm/provider admission; domain-separation labels; version/algorithm identifiers; streaming/finalization interface; digest length/type separation; collision/non-claim policy; known-answer startup self-tests; migration and agility rules.

Verification:

- Known-answer and cross-provider vectors, label/type/algorithm confusion, truncation, incremental chunking, empty/large input, provider failure, version migration, serialization drift, and cross-platform fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Schema, document, release, archive, audit, package, and evidence roots use typed domain-separated digests rather than ad hoc hashing.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.18.1 implementation stop reached. Run pentest for this exact commit.`

### v0.18.2 — Cryptographic Provider Admission Framework

Status: planned.

Goal: Standardize admission, identity, self-test, failure, and agility for signature, AEAD, MAC, KDF, and key-operation providers.

Deliverables:

- Algorithm/provider/version/key-reference descriptors; exact input/output contracts; known-answer and startup self-tests; allowlists; hardware/OS/service/software provider boundaries; failure/no-fallback policy; operation handles; migration/agility and evidence schema.

Verification:

- Wrong provider/key/algorithm/purpose, downgrade, malformed input/output, self-test failure, unavailable provider, key rotation, signature/MAC/tag failure, nonce misuse prevention contract, and cross-platform fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Later authentication, TLS, package, webhook, backup, payment, and release features cannot call cryptography outside an admitted typed provider boundary.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.18.2 implementation stop reached. Run pentest for this exact commit.`

### v0.19.0 — Schema Fingerprints

Status: planned.

Goal: Give logical schemas stable identities.

Deliverables:

- Canonical field ordering; version and compatibility metadata; constraint roots; indexing/translation/classification intents.

Verification:

- Equivalent schemas hash identically; every semantic change affects the expected root; unknown required features fail.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.19.0 implementation stop reached. Run pentest for this exact commit.`

### v0.20.0 — Core Compatibility Harness

Status: planned.

Goal: Freeze portable-core behavior before higher layers depend on it.

Deliverables:

- Fixture corpus; old-reader/new-reader matrix; semantic diff report; no_std builds; public API inventory.

Verification:

- Run cross-version fixtures and prove additive optional data round-trips while incompatible required data fails closed.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.20.0 implementation stop reached. Run pentest for this exact commit.`

### v0.20.1 — Injected Portable Environment Contract

Status: planned.

Goal: Remove ambient platform semantics from portable domain behavior.

Deliverables:

- Explicit providers and version metadata for time, randomness, Unicode/locale data, money rules, canonical serialization, allocation policy, and deterministic test fixtures.

Verification:

- Cross-target golden runs with varied clocks, entropy streams, locale tables, rounding rules, serializer versions, and allocation failures produce declared identical results or explicit compatibility failures.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No portable crate consults an ambient clock, random source, locale, floating-point money path, or host serializer.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.20.1 implementation stop reached. Run pentest for this exact commit.`

## Phase 2 — Schema, document, query, policy, and proof readiness

### v0.21.0 — Content Schema IR

Status: planned.

Goal: Model content types and fields independently of storage and UI.

Deliverables:

- Field families, constraints, defaults, cardinality, locale policy, retention, classification, UI hints, and API exposure.

Verification:

- Fuzz-shaped deterministic mutations and schema-validation tables cover every field and constraint family.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.21.0 implementation stop reached. Run pentest for this exact commit.`

### v0.22.0 — Schema Evolution Planner

Status: planned.

Goal: Classify schema changes before data mutation.

Deliverables:

- Add/remove/change operations; compatibility class; backfill requirement; index intent; rollback and data-loss warnings.

Verification:

- Fixtures prove deterministic plans and rejection of ambiguous or silently lossy changes.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.22.0 implementation stop reached. Run pentest for this exact commit.`

### v0.23.0 — Block Document Tree

Status: planned.

Goal: Establish structured content as the canonical source.

Deliverables:

- Versioned semantic block and inline tree; stable node IDs; namespaced/versioned block kinds; typed properties, slots, references, direction, locale, provenance, and bounded inert unknown payloads. Block kinds cannot encode CSS classes, UI components, or database keys.

Verification:

- Round-trip arbitrary bounded trees; reject depth/work exhaustion; preserve unknown optional blocks.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.23.0 implementation stop reached. Run pentest for this exact commit.`

### v0.23.1 — Document Envelope And Reference Integrity

Status: planned.

Goal: Give every canonical document complete identity, schema, locale, provenance, and integrity context.

Deliverables:

- Document/revision/schema identity and version envelope; root node and digest; resource and relationship references; unique-node, acyclic, deterministic-order, reference-integrity, unknown-feature, and aggregate-budget rules.

Verification:

- Duplicate IDs, cycles, dangling/cross-tenant references, invalid schemas, reordering ambiguity, inert unknown blocks, depth/count/encoded-size exhaustion, and lossless old/new-reader fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A document cannot enter application or storage layers without one validated canonical envelope.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.23.1 implementation stop reached. Run pentest for this exact commit.`

### v0.24.0 — Document Transformations

Status: planned.

Goal: Make edits and migrations pure and versioned.

Deliverables:

- Insert, remove, move, replace, structural diff, patch preconditions, and transformation receipts.

Verification:

- Property sweeps cover apply/revert, conflicting patches, stable roots, and failure atomicity.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.24.0 implementation stop reached. Run pentest for this exact commit.`

### v0.24.1 — ContentView Projection Contract

Status: planned.

Goal: Give headless, rendered, native, search, and extension consumers one policy-filtered content projection.

Deliverables:

- Versioned `ContentView`; release/revision root; tenant/site/environment, locale, viewer/policy, reference, media, provenance, and unknown-block semantics; generated schema inputs for REST, GraphQL, TypeScript, Kotlin, and Swift.

Verification:

- Golden and compatibility fixtures prove every consumer sees equivalent allowed semantics, forbidden fields never enter the projection, release roots are immutable, and generated schemas reproduce byte-for-byte.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Delivery adapters consume `ContentView` rather than independently reinterpreting stored document state.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.24.1 implementation stop reached. Run pentest for this exact commit.`

### v0.25.0 — Safe Embedded Content Boundary

Status: planned.

Goal: Separate raw content from trusted rendered output.

Deliverables:

- Explicit embedded-markup block; permission marker; sanitizer-policy reference; inert unknown handling; no safe-string constructor.

Verification:

- XSS corpus fixtures remain data until a later admitted sanitizer path; unauthorized creation fails.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.25.0 implementation stop reached. Run pentest for this exact commit.`

### v0.26.0 — Portable Query AST

Status: planned.

Goal: Represent reads without raw provider query languages.

Deliverables:

- Typed predicates, projections, stable sort/tie-breakers, cursors, bounded relationship traversal, locale fallback, and consistency intent.

Verification:

- Malformed, unsorted, unbounded, cross-schema, and complexity-exceeding queries fail before adapter execution.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.26.0 implementation stop reached. Run pentest for this exact commit.`

### v0.27.0 — Query Cost Model

Status: planned.

Goal: Bound query amplification consistently across adapters.

Deliverables:

- Node, predicate, traversal, projection, aggregate, sort, and result budgets; explainable rejection.

Verification:

- Adversarial AST sweeps prove monotonic costing and checked arithmetic.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.27.0 implementation stop reached. Run pentest for this exact commit.`

### v0.28.0 — Policy Expression Core

Status: planned.

Goal: Define explainable RBAC/ABAC/ReBAC decisions.

Deliverables:

- Principals, resources, actions, attributes, relationships, explicit deny, constrained allow, redaction, approval, and more-evidence outcomes; no public boolean shortcut that can discard obligations.

Verification:

- Model/sweep deny precedence, tenant scope, field/locale context, stale epochs, and incomplete evidence.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.28.0 implementation stop reached. Run pentest for this exact commit.`

### v0.28.1 — Typed Policy Obligations

Status: planned.

Goal: Make redaction, step-up, approval, purpose, evidence, rate, and audit requirements impossible for callers to ignore accidentally.

Deliverables:

- Typed decision continuations and obligation-consumption receipts; capability construction only after complete obligation handling; deny-safe unknown obligation behavior; policy epoch and explanation linkage.

Verification:

- Compile-fail fixtures and application tests prove no usable repository/query/render/plugin capability can be obtained from allow-like outcomes before every required obligation is consumed and recorded.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Application code cannot reduce the policy model to a boolean authorization check.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.28.1 implementation stop reached. Run pentest for this exact commit.`

### v0.29.0 — Actor-Bound Command Intent

Status: planned.

Goal: Tie every canonical mutation to actor and executor.

Deliverables:

- Actor, effective actor, executor, assurance, purpose, reason, correlation, idempotency, expected revision, expiry, nonce, and payload root.

Verification:

- Reject anonymous writes, forged delegation, stale intent, payload substitution, and cross-tenant replay.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.29.0 implementation stop reached. Run pentest for this exact commit.`

### v0.30.0 — Evidence and Decision Records

Status: planned.

Goal: Make claims precise without requiring Skrifheim.

Deliverables:

- Attribution levels; evidence references; verification/availability state; public explanation versus protected evidence; explicit non-claims.

Verification:

- Imported attribution never becomes a signature; protected tokens never enter public reports; stale evidence blocks as configured.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.30.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 3 — Events, application boundary, and storage contracts

### v0.31.0 — Command and Query Envelopes

Status: planned.

Goal: Freeze application request context.

Deliverables:

- Tenant/site/environment, actor, deadline, budget, locale, consistency, correlation, and compatibility metadata.

Verification:

- Golden fixtures and negative context-substitution tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.31.0 implementation stop reached. Run pentest for this exact commit.`

### v0.31.1 — Non-Omittable Tenant Context

Status: planned.

Goal: Make tenant/site/environment scope a construction-time invariant rather than a caller-supplied query filter.

Deliverables:

- Verified host/domain-to-context resolution; scoped constructors for repositories, units of work, policy, plugin, blob, search, cache, log, and audit capabilities; explicit separate cross-tenant administration service; context propagation schema.

Verification:

- Compile-fail and adversarial tests cover missing/substituted tenant, untrusted Host/forwarding data, cache/search/blob/log omission, background jobs, events, imports, and cross-tenant administrative operations.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Normal application code cannot construct storage or authority capabilities without a verified tenant context.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.31.1 implementation stop reached. Run pentest for this exact commit.`

### v0.32.0 — Domain Event Envelopes

Status: planned.

Goal: Represent committed facts and projection events safely.

Deliverables:

- Event identity, schema version, aggregate revision, causation, correlation, actor/executor, classification, and payload root.

Verification:

- Replay and ordering fixtures prove stable encoding and no authority in untrusted event payloads.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.32.0 implementation stop reached. Run pentest for this exact commit.`

### v0.33.0 — Application Service Boundary

Status: planned.

Goal: Keep domain rules independent of delivery adapters.

Deliverables:

- Command handlers, query handlers, authorisation hook, unit-of-work intent, outcome taxonomy, and side-effect plan.

Verification:

- In-memory tests prove transport and storage implementations cannot bypass validation.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.33.0 implementation stop reached. Run pentest for this exact commit.`

### v0.34.0 — Idempotency State Machine

Status: planned.

Goal: Make retries safe before external effects exist.

Deliverables:

- New, pending, committed, failed-retryable, failed-final, ambiguous, and expired states; payload binding; result lookup.

Verification:

- Crash-point and duplicate/concurrent request matrices produce one logical outcome.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.34.0 implementation stop reached. Run pentest for this exact commit.`

### v0.35.0 — Outbox Contract

Status: planned.

Goal: Couple authoritative change to durable downstream work.

Deliverables:

- Transactional outbox record, lease, checkpoint, poison quarantine, retry, and receipt status.

Verification:

- Simulate crash before/after commit and drain; no committed event is lost or logically duplicated.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.35.0 implementation stop reached. Run pentest for this exact commit.`

### v0.36.0 — Storage Capability Model

Status: planned.

Goal: Expose provider truth instead of false equivalence.

Deliverables:

- Required/preferred/fallback capabilities; transactions, locks, indexes, change feeds, search, recovery, and consistency descriptors.

Verification:

- Feature admission fails when correctness requirements are absent; accelerations cannot change semantics.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.36.0 implementation stop reached. Run pentest for this exact commit.`

### v0.36.1 — Aetherheim Portable Storage Profile

Status: planned.

Goal: Freeze provider-independent storage semantics before adapter implementation.

Deliverables:

- Versioned APSP for canonical values, text equality/order, timestamps, predicate truth tables, stable cursors, relationships, aggregates, consistency/isolation, transaction visibility, normalized errors, and qualified provider-native extensions.

Verification:

- Executable truth-table and history fixtures cover null/missing values, Unicode/collation, timezones, pagination under mutation, traversal, aggregate overflow, conflicts, and unsupported semantics.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No adapter milestone may define portable behavior that APSP leaves unspecified; unresolved semantics block adapter work.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.36.1 implementation stop reached. Run pentest for this exact commit.`

### v0.37.0 — Focused Store Traits

Status: planned.

Goal: Avoid a monolithic storage provider.

Deliverables:

- Metadata, content, identity, audit, job, blob, search, cache, lock, and secret-operation contracts.

Verification:

- Compile-time dependency audit and fake providers prove each authority is minimal and independently testable.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.37.0 implementation stop reached. Run pentest for this exact commit.`

### v0.38.0 — Unit of Work Contract

Status: planned.

Goal: Define atomic application boundaries.

Deliverables:

- Snapshot/read context, staged writes, expected revisions, outbox coupling, committed/not-committed/ambiguous outcomes, idempotency-bound resolution, and rollback semantics.

Verification:

- Interleaving model tests cover conflicts, ambiguous commits, rollback, and read-after-write.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.38.0 implementation stop reached. Run pentest for this exact commit.`

### v0.38.1 — Ambiguous Commit Resolution

Status: planned.

Goal: Resolve uncertain commits without blindly repeating authoritative writes.

Deliverables:

- Idempotency outcome lookup; bounded reconciliation; caller retry guidance; receipt correlation; external-effect prohibition inside open units of work; compensation classification.

Verification:

- Disconnect/crash at every commit boundary proves lookup converges to one logical result, repeated resolution is safe, and no network/provider effect is issued while an authoritative transaction is open.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every adapter can distinguish and reconcile committed, not committed, and ambiguous outcomes under its documented topology.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.38.1 implementation stop reached. Run pentest for this exact commit.`

### v0.39.0 — Migration Operation IR

Status: planned.

Goal: Represent migrations as typed resumable operations.

Deliverables:

- Preconditions, reversibility, online/offline class, checkpoints, risk, validation, backup requirement, and provider escape-hatch marking.

Verification:

- Plan serialization, resume, duplicate checkpoint, rollback-class, and loss-warning fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.39.0 implementation stop reached. Run pentest for this exact commit.`

### v0.40.0 — Storage Conformance Harness

Status: planned.

Goal: Give every provider one executable semantic contract.

Deliverables:

- CRUD-independent domain scenarios; transactions; revisions; relationships; jobs; isolation; errors; crash fixtures; capability report.

Verification:

- Reference in-memory provider passes; deliberately broken providers fail each relevant conformance section.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.40.0 implementation stop reached. Run pentest for this exact commit.`

### v0.40.1 — APSP Reference Interpreter And Differential Oracle

Status: planned.

Goal: Turn the portable profile into an executable semantic oracle.

Deliverables:

- Deterministic in-memory interpreter; property/history generator; result and error normalizer; provider trace comparison; deliberately broken adapter corpus; replayable failure artifacts.

Verification:

- Differential suites catch comparison, cursor, relationship, transaction, isolation, aggregation, error, and ambiguity deviations that CRUD-only tests would miss.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A provider cannot be called portable unless all required operations match the reference interpreter under generated and adversarial histories.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.40.1 implementation stop reached. Run pentest for this exact commit.`

### v0.40.2 — Provider Qualification Manifest

Status: planned.

Goal: Bind every database support claim to an exact reproducible operating envelope.

Deliverables:

- Provider/version/topology, durability/isolation, collation, timezone, extension, backup, failover, limitation, performance, and APSP-result manifest with experimental/qualified status.

Verification:

- Matrix tooling rejects missing settings, stale versions, undeclared topology changes, unsupported capability claims, and a SurrealDB stable claim before full conformance and live evidence pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- “Supports database X” always resolves to a versioned qualification manifest and executable evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.40.2 implementation stop reached. Run pentest for this exact commit.`

## Phase 4 — SQLite and local operation

### v0.41.0 — SQLite Engine And Driver Admission

Status: planned.

Goal: Admit a mature SQLite foundation and define file/engine ownership safely.

Deliverables:

- Exact reviewed crate/library and feature graph; database-file ownership; bundled/system/process boundary decision; native/unsafe/build-script review; version identity; path and extension-loading policy; locking/threading assumptions; platform and CVE-response plan. Aetherheim does not implement a database engine.

Verification:

- Reject wrong library identity/version, unsafe paths, extension loading, unsupported modes, ambiguous ownership, unsafe feature drift, and unsupported platform behavior.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.41.0 implementation stop reached. Run pentest for this exact commit.`

### v0.42.0 — SQLite Connection And Statement Boundary

Status: planned.

Goal: Implement bounded statement preparation and parameter binding.

Deliverables:

- Aetherheim-owned adapter around the admitted driver; connection ownership; typed parameters; exact result decoding; limits; cancellation/interruption; busy policy; transaction state; and redacted errors.

Verification:

- Injection fixtures, oversized rows, type mismatch, cancellation, and malformed provider responses fail safely.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.42.0 implementation stop reached. Run pentest for this exact commit.`

### v0.43.0 — SQLite Schema Bootstrap

Status: planned.

Goal: Create deterministic installation metadata.

Deliverables:

- Schema version table, tenant/site roots, migration lock, integrity metadata, and transactional bootstrap.

Verification:

- Fresh, repeated, interrupted, and corrupted bootstrap scenarios are deterministic and recoverable.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.43.0 implementation stop reached. Run pentest for this exact commit.`

### v0.44.0 — SQLite Content Store

Status: planned.

Goal: Persist content identities, variants, revisions, relationships, and publication pointers.

Deliverables:

- Normalized logical mappings, optimistic concurrency, immutable published revisions, and tenant/site predicates.

Verification:

- Shared conformance plus cross-tenant, stale-write, rollback, and orphan-reference tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.44.0 implementation stop reached. Run pentest for this exact commit.`

### v0.45.0 — SQLite Identity Store

Status: planned.

Goal: Persist identities, credentials metadata, sessions, groups, and policies without secret leakage.

Deliverables:

- Separated credential envelopes, session revocation state, uniqueness, and privacy-aware indexes.

Verification:

- Negative scope tests, revoked-session reads, concurrent updates, and diagnostics redaction pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.45.0 implementation stop reached. Run pentest for this exact commit.`

### v0.46.0 — SQLite Job Store

Status: planned.

Goal: Provide durable local queues and schedules.

Deliverables:

- Leases, heartbeats, retry, dead letter, priority, cancellation, scheduler claims, and clock policy.

Verification:

- Kill/restart matrices prove no committed job loss and bounded duplicate delivery semantics.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.46.0 implementation stop reached. Run pentest for this exact commit.`

### v0.47.0 — SQLite Audit Store

Status: planned.

Goal: Provide append-oriented, gap-detectable local audit.

Deliverables:

- Per-domain sequences, chained roots, safe diffs, redaction, checkpoint export, and mandatory-audit behavior.

Verification:

- Deletion, reorder, fork, rollback, exhaustion, and unavailable-audit fixtures are detected.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.47.0 implementation stop reached. Run pentest for this exact commit.`

### v0.48.0 — SQLite Query Translation

Status: planned.

Goal: Translate the portable AST without semantic drift.

Deliverables:

- Parameterised predicates, ordering, cursors, bounded traversal, projection, locale fallback, and explain budget.

Verification:

- Differential results match the in-memory oracle; injection and query-amplification suites pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.48.0 implementation stop reached. Run pentest for this exact commit.`

### v0.49.0 — SQLite FTS Projection

Status: planned.

Goal: Add optional local lexical search as a rebuildable projection.

Deliverables:

- Permission/visibility partitions, locale token boundary, outbox updates, freshness watermark, rebuild and swap.

Verification:

- Draft/restricted deletion and stale-index leakage tests pass; source remains authoritative.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.49.0 implementation stop reached. Run pentest for this exact commit.`

### v0.50.0 — SQLite Quick Start

Status: planned.

Goal: Deliver the first local installation vertical slice.

Deliverables:

- `init`, local data directory, configuration, migrations, doctor, graceful shutdown, and backup preflight; no public HTTP yet.

Verification:

- Clean install, restart, concurrent-start rejection, corrupted-state diagnostics, and platform filesystem tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.50.0 implementation stop reached. Run pentest for this exact commit.`

### v0.50.1 — Local Immutable Blob Store

Status: planned.

Goal: Complete the simple single-node profile with integrity-checked local blobs.

Deliverables:

- Digest-addressed immutable objects; atomic write/publish; tenant context; bounded streaming; metadata/classification; reference tracking; quarantine integration; garbage-collection and crash-recovery rules.

Verification:

- Partial write, substitution, path escape, cross-tenant lookup, concurrent put, duplicate digest, reference race, disk-full, restart, backup, restore, and garbage-collection tests pass on supported local platforms.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The local profile can round-trip complete content and media without relying on a shared or remote object service.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.50.1 implementation stop reached. Run pentest for this exact commit.`

### v0.50.2 — Loopback-Only Preview Transport

Status: planned.

Goal: Enable an early browser/API developer preview without creating a production network support claim.

Deliverables:

- Development-only binary/profile; loopback binding; random per-start origin and one-time capability; no proxy trust, remote bind, production feature, or packaged-service inclusion; bounded HTTP subset; CSRF/origin policy; explicit warning and clean teardown.

Verification:

- Non-loopback bind, forwarded-header spoofing, origin/CSRF confusion, token replay, port race, malformed/oversized request, restart, production-artifact inclusion, and missing-warning tests fail safely.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The preview is usable locally but technically incapable of becoming an accidental remotely supported deployment.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.50.2 implementation stop reached. Run pentest for this exact commit.`

### v0.50.3 — SQLite CMS Content Vertical Slice

Status: planned.

Goal: Prove the canonical contracts can create, revise, publish, read, and export real content before secondary databases are built.

Deliverables:

- One bounded built-in page schema; create/update draft; immutable revision; publish/unpublish pointer; route; `ContentView`; deterministic minimal HTML and JSON delivery; local blob reference; AHAF-compatible export subset; CLI and loopback preview operations.

Verification:

- Real-process journeys cover create, validation denial, revise, stale edit, publish, read, restart, unpublish, restore revision, export/import subset, corrupt state, cross-site denial, and deterministic output on SQLite.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A developer can operate a truthful minimal CMS on SQLite; later application milestones generalize this slice without replacing its canonical semantics.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.50.3 implementation stop reached. Run pentest for this exact commit.`

### v0.50.4 — Local Browser Authoring Preview

Status: planned.

Goal: Make the early SQLite content slice usable through a minimal accessible browser interface.

Deliverables:

- Development-only setup screen; page list; structured title/text/link/image blocks; validation; save/revision history; preview; publish/unpublish; visible limitations; keyboard and basic screen-reader behavior; no plugin/theme/remote-user claims.

Verification:

- Browser E2E covers complete authoring, paste as data, XSS payloads, stale edits, restart/recovery, keyboard-only use, focus/error announcements, session capability expiry, and absence from production artifacts.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The project demonstrates an end-to-end CMS experience before investing in every production provider, while remaining explicitly local and non-production.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.50.4 implementation stop reached. Run pentest for this exact commit.`

### v0.50.5 — Local CMS Preview Acceptance Release

Status: planned.

Goal: Package and continuously exercise the complete early developer-preview journey.

Deliverables:

- One-command `aetherheim dev`; clean ephemeral or persistent site modes; fixture site; bounded logs; browser/API/CLI acceptance profile; upgrade fixture from the prior preview; documented non-claims and feedback workflow.

Verification:

- Clean Linux, Windows, BSD, and macOS host runs launch, author, publish, restart, export, restore, upgrade, and remove the preview; missing browser/tool and any skipped required scenario fail the gate.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The early CMS slice is reproducibly usable and tested, not merely a collection of library tests or mock handlers.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.50.5 implementation stop reached. Run pentest for this exact commit.`

## Phase 5 — Production storage, archives, jobs, blobs, and cache

### v0.51.0 — PostgreSQL Driver Admission

Status: planned.

Goal: Admit a mature PostgreSQL client behind a first-party production database boundary.

Deliverables:

- Exact reviewed crate/features; protocol/server scope; authentication-provider interface; TLS/proxy assumption; unsafe/native/build-script and transitive review; framing/result budgets; cancellation; server identity; platform and CVE-response policy. Aetherheim does not implement PostgreSQL wire/authentication protocols.

Verification:

- Malformed frames, downgrade, wrong server, oversized messages, cancellation, and timeout tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.51.0 implementation stop reached. Run pentest for this exact commit.`

### v0.52.0 — PostgreSQL Session and Query Path

Status: planned.

Goal: Implement bounded typed sessions and parameterised queries.

Deliverables:

- Startup, authentication exchange boundary, prepared operations, transaction status, result decoding, and connection reset.

Verification:

- Protocol corpus, injection, desynchronisation, partial I/O, and reconnect suites pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.52.0 implementation stop reached. Run pentest for this exact commit.`

### v0.53.0 — PostgreSQL Content Store

Status: planned.

Goal: Reach portable content/revision/relationship semantics on PostgreSQL.

Deliverables:

- Content/schema/revision/relationship mappings; immutable publication roots; expected revisions; tenant/site constraints; content outbox coupling; indexes and archive identity.

Verification:

- Shared content conformance, concurrent/stale writes, deadlock/retry, isolation, cross-tenant relationships, publication immutability, and archive-root tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.53.0 implementation stop reached. Run pentest for this exact commit.`

### v0.53.1 — PostgreSQL Identity And Session Store

Status: planned.

Goal: Implement identity, credential metadata, session, group, and policy state independently from content storage.

Deliverables:

- Principal/account/credential metadata mappings; communication-point uniqueness; opaque session and revocation records; groups/policy epochs; tenant constraints; privacy indexes; audit/outbox coupling.

Verification:

- Duplicate/cross-tenant identity, credential/session separation, revocation races, concurrent account change, privacy query, ambiguous commit, deadlock/retry, and redacted diagnostics tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Content access cannot expose credential/session records and identity authority has separate conformance evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.53.1 implementation stop reached. Run pentest for this exact commit.`

### v0.53.2 — PostgreSQL APSP Query Translation

Status: planned.

Goal: Translate the complete portable query profile without PostgreSQL-specific semantic leakage.

Deliverables:

- Typed predicates/projections; text/time/value mapping; stable sort/cursors; relationships; aggregates; locale fallback; consistency intent; cost/explain budgets; normalized results/errors.

Verification:

- APSP differential/property/history suites cover collation, null/missing, timezone, pagination mutation, traversal, aggregates, isolation, injection, cost amplification, cancellation, and error normalization.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- PostgreSQL-native extensions remain separately qualified and cannot change portable query results.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.53.2 implementation stop reached. Run pentest for this exact commit.`

### v0.54.0 — PostgreSQL Jobs And Outbox

Status: planned.

Goal: Implement durable asynchronous work on the production-reference provider.

Deliverables:

- Leased jobs, deterministic schedule slots, transactional claim/completion/outbox, fencing inputs, retry/dead-letter, cancellation, fairness, and bounded queue operations.

Verification:

- Crash/recovery at every claim/complete phase, lease contention, stale fence, duplicate schedule, poison work, cancellation, fairness, and outbox replay fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.54.0 implementation stop reached. Run pentest for this exact commit.`

### v0.54.1 — PostgreSQL Audit Store

Status: planned.

Goal: Complete append-oriented gap-detectable audit on PostgreSQL.

Deliverables:

- Chained audit records/checkpoints; per-domain sequences; safe diffs/redaction; mandatory-audit failure policy; verification/export; retention/hold constraints and operator receipts.

Verification:

- Audit delete/reorder/fork/exhaustion, concurrent append, redaction/inference, checkpoint/export verification, retention/hold, backup/restore, and mandatory-audit failure fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- PostgreSQL audit authority has independent tamper, exhaustion, privacy, backup, and recovery evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.54.1 implementation stop reached. Run pentest for this exact commit.`

### v0.54.2 — PostgreSQL Migration Operations

Status: planned.

Goal: Implement resumable expand/contract and online schema operations on PostgreSQL.

Deliverables:

- Migration locks/checkpoints; preconditions; expand/contract compatibility; backfill and online-index operations; validation; rollback/data-loss class; old/new application overlap; backup requirement and operator receipts.

Verification:

- Interruption/resume at every operation, concurrent migrator, failed backfill/index, lock loss, old/new version overlap, cancellation, rollback, irreversible warning, and post-migration APSP validation pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every PostgreSQL schema change is typed, resumable, validated, and explicit about rollback/data-loss boundaries.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.54.2 implementation stop reached. Run pentest for this exact commit.`

### v0.54.3 — PostgreSQL Operational Qualification

Status: planned.

Goal: Qualify pooling, health, backup, recovery, and performance for the production reference.

Deliverables:

- Pool/session budgets; health/readiness; connection rotation; backup/PITR hooks; failover profile; query-plan and capacity baselines; exact provider qualification manifest and operational runbook.

Verification:

- Live supported versions/topologies cover pool exhaustion, credential/TLS rotation, failover, PITR, slow queries, cancellation, maintenance, restart, capacity, and recovery without semantic drift.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- PostgreSQL becomes the production reference only for the exact live-qualified versions and settings.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.54.3 implementation stop reached. Run pentest for this exact commit.`

### v0.55.0 — MariaDB Driver And Session Admission

Status: planned.

Goal: Admit a mature client behind a separate Aetherheim-owned MariaDB boundary.

Deliverables:

- Exact reviewed crate/features; supported server/topology scope; authentication/TLS identity boundary; capability negotiation; typed parameters/results; transaction state; cancellation; limits; unsafe/native/build-script review; CVE-response policy. Aetherheim does not implement the MariaDB wire protocol.

Verification:

- Malformed handshake, downgrade, injection, desynchronisation, timeout, and reconnect tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.55.0 implementation stop reached. Run pentest for this exact commit.`

### v0.56.0 — MariaDB Content Store

Status: planned.

Goal: Implement authoritative content/revision/relationship semantics on MariaDB.

Deliverables:

- Provider-owned content schema; revisions/relationships/publication roots; expected revisions; tenant/site constraints; content transaction/outbox coupling; JSON/index strategy and archive identity.

Verification:

- Shared content conformance plus provider deadlock, index, transaction, stale-write, relationship/tenant, publication immutability, retry, and archive-root fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.56.0 implementation stop reached. Run pentest for this exact commit.`

### v0.56.1 — MariaDB Identity And Session Store

Status: planned.

Goal: Implement identity, credential metadata, session, group, and policy state independently from content.

Deliverables:

- Principal/account/credential metadata mappings; communication-point uniqueness; opaque session/revocation; groups/policy epochs; tenant constraints; privacy indexes; audit/outbox coupling.

Verification:

- Duplicate/cross-tenant identity, credential/session separation, revocation races, concurrent account change, collation-sensitive uniqueness, privacy queries, ambiguous commits, deadlock/retry, and redaction tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- MariaDB identity authority has separate privacy, uniqueness, concurrency, and revocation evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.56.1 implementation stop reached. Run pentest for this exact commit.`

### v0.56.2 — MariaDB APSP Query Translation

Status: planned.

Goal: Translate the complete portable query profile without collation or SQL-mode drift.

Deliverables:

- Typed predicates/projections; text/time/value mapping; stable sort/cursors; relationships; aggregates; locale fallback; consistency intent; cost/explain budgets; normalized results/errors; required server modes.

Verification:

- APSP differential/property/history suites cover collations, SQL modes, null/missing, timezone, pagination mutation, traversal, aggregates, isolation, injection, amplification, cancellation, and errors.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Required MariaDB modes/collations are explicit qualification inputs and provider extensions cannot redefine APSP results.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.56.2 implementation stop reached. Run pentest for this exact commit.`

### v0.56.3 — MariaDB Jobs And Outbox

Status: planned.

Goal: Add durable asynchronous work and transactional outbox behavior on MariaDB.

Deliverables:

- Jobs/schedules/outbox; database-time and lease/fencing mapping; transactional claim/completion; retry/dead-letter; cancellation; fairness; poison handling; bounded queue operations and receipts.

Verification:

- Claim/complete crash points, deadlocks, stale leases/fences, duplicate schedule, replay, poison work, cancellation, fairness, ambiguity, and recovery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- MariaDB background work matches the portable job/outbox contract independently from content and audit authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.56.3 implementation stop reached. Run pentest for this exact commit.`

### v0.56.4 — MariaDB Audit Store

Status: planned.

Goal: Implement append-oriented gap-detectable audit on MariaDB.

Deliverables:

- Chained records/checkpoints; per-domain sequences; safe diffs/redaction; mandatory-audit failure; verification/export; retention/hold; backup/restore hooks and receipts.

Verification:

- Delete/reorder/fork/exhaustion, concurrent append/deadlock, redaction/inference, checkpoint/export, retention/hold, backup/restore, and mandatory-audit failure tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- MariaDB audit authority has independent tamper, exhaustion, privacy, backup, and recovery evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.56.4 implementation stop reached. Run pentest for this exact commit.`

### v0.56.5 — MariaDB Migration Operations

Status: planned.

Goal: Implement resumable schema/index/backfill evolution under MariaDB capabilities.

Deliverables:

- Migration locks/checkpoints; preconditions; expand/contract compatibility; backfill/index/online-operation strategy; validation; rollback/data-loss class; old/new overlap; backup requirement and receipts.

Verification:

- Interruption/resume, concurrent migrator, lock loss, failed backfill/index, online-operation blocking, old/new overlap, cancellation, rollback, irreversible warning, and APSP post-validation pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every MariaDB schema change is typed, resumable, validated, and explicit about provider blocking and rollback boundaries.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.56.5 implementation stop reached. Run pentest for this exact commit.`

### v0.56.6 — MariaDB Operational Qualification

Status: planned.

Goal: Establish the exact supported MariaDB version/topology envelope.

Deliverables:

- Live version/topology/settings matrix; collation/timezone/isolation profile; pool and health policy; failover/backup/recovery; capacity/query-plan evidence; capability limitations and qualification manifest.

Verification:

- Every declared live profile passes APSP differential, account/content/job/audit, failover, backup/restore, migration, resource, and performance scenarios; unavailable profiles remain unsupported.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- MariaDB support is claimed only through a current qualification manifest and live evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.56.6 implementation stop reached. Run pentest for this exact commit.`

### v0.57.0 — MongoDB Driver And Session Admission

Status: planned.

Goal: Admit a mature client behind a bounded first-party document-provider boundary.

Deliverables:

- Exact reviewed crate/features; authentication/TLS/server identity; typed document encoding; transaction and topology scope; cursor/result limits; cancellation; unsafe/native/build-script and transitive review; CVE-response policy. Aetherheim does not implement MongoDB wire or authentication protocols.

Verification:

- Malformed frames, document bombs, injection-shaped values, stale cursors, timeout, and topology change tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.57.0 implementation stop reached. Run pentest for this exact commit.`

### v0.58.0 — MongoDB Content Store

Status: planned.

Goal: Implement authoritative content/revision/relationship semantics without pretending documents equal the logical model.

Deliverables:

- Content/revision/relationship mappings; publication roots; required transaction boundaries; tenant constraints; indexes; content outbox coupling; archive identity; explicit unsupported capabilities.

Verification:

- Shared content conformance, multi-document failure, stale writes, tenant/relationship isolation, publication immutability, transaction ambiguity, archive root, and index rebuild tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.0 implementation stop reached. Run pentest for this exact commit.`

### v0.58.1 — MongoDB Identity And Session Store

Status: planned.

Goal: Implement identity, credential metadata, session, group, and policy state in isolated collections.

Deliverables:

- Principal/account/credential metadata mappings; communication-point uniqueness; opaque session/revocation; groups/policy epochs; tenant constraints; privacy indexes; transaction/outbox coupling.

Verification:

- Duplicate/cross-tenant identity, credential/session separation, revocation races, concurrent account changes, transaction ambiguity, privacy queries, index rebuild, topology changes, and redaction tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- MongoDB document convenience cannot merge content and identity authority or bypass session revocation semantics.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.1 implementation stop reached. Run pentest for this exact commit.`

### v0.58.2 — MongoDB APSP Query Translation

Status: planned.

Goal: Translate portable predicates, cursors, relationships, and aggregates without BSON/provider semantic drift.

Deliverables:

- Canonical value/BSON mapping; typed predicates/projections; stable sorts/cursors; relationship traversal; aggregates; locale fallback; consistency intent; cost/explain budgets; normalized results/errors.

Verification:

- APSP differential/property/history suites cover null/missing, numeric types, text/collation, timezone, pagination mutation, traversal, aggregates, transactions, injection-shaped values, amplification, cancellation, and errors.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Aggregation pipelines and provider-native queries remain adapter-private and cannot broaden normal client/plugin APIs.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.2 implementation stop reached. Run pentest for this exact commit.`

### v0.58.3 — MongoDB Jobs And Outbox

Status: planned.

Goal: Add durable asynchronous work and transactional outbox behavior on MongoDB.

Deliverables:

- Job claims/schedules/outbox; database-time and lease/fencing mapping; transactional claim/completion; retry/dead-letter; cancellation/fairness; change-stream acceleration policy and receipts.

Verification:

- Claim/complete crash/replay, transaction uncertainty, stale lease/fence, duplicate schedule, poison work, cancellation/fairness, change-stream duplicate/gap, and rebuild tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Change streams remain optional accelerators and cannot redefine job, audit, or migration authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.3 implementation stop reached. Run pentest for this exact commit.`

### v0.58.4 — MongoDB Audit Store

Status: planned.

Goal: Implement append-oriented gap-detectable audit on MongoDB.

Deliverables:

- Chained records/checkpoints; per-domain sequences; safe diffs/redaction; transaction and mandatory-audit failure policy; verification/export; retention/hold; backup/restore hooks and receipts.

Verification:

- Delete/reorder/fork/exhaustion, concurrent append/transaction ambiguity, redaction/inference, checkpoint/export, retention/hold, backup/restore, topology change, and mandatory-audit failure pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- MongoDB audit authority has independent tamper, ambiguity, privacy, backup, and recovery evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.4 implementation stop reached. Run pentest for this exact commit.`

### v0.58.5 — MongoDB Migration Operations

Status: planned.

Goal: Implement resumable collection/index/backfill evolution without treating schemaless storage as migration-free.

Deliverables:

- Migration ownership/checkpoints; document version/preconditions; expand/contract transforms; backfill/index operations; validation; rollback/data-loss class; mixed-version readers/writers; backup requirement and receipts.

Verification:

- Interruption/resume, concurrent migrator, lease loss, failed transform/index, mixed document/application versions, change-stream gaps, cancellation, rollback, irreversible warning, and APSP post-validation pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every MongoDB logical schema change is typed, resumable, validated, and explicit about mixed-version and rollback boundaries.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.5 implementation stop reached. Run pentest for this exact commit.`

### v0.58.6 — MongoDB Operational Qualification

Status: planned.

Goal: Establish the exact supported MongoDB version/topology envelope.

Deliverables:

- Replica/topology/version/settings matrix; read/write concern and transaction profile; pool/health/failover; backup/recovery; capacity/query-plan evidence; limitation and qualification manifest.

Verification:

- Live topology changes, elections, partitions, stale reads, write concern failure, backup/restore, migration, APSP differential, capacity, and full journey suites pass for every claimed cell.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- MongoDB support is claimed only for tested read/write concerns and topology profiles.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.6 implementation stop reached. Run pentest for this exact commit.`

### v0.58.7 — SurrealDB Driver And Connection Admission

Status: planned.

Goal: Establish a bounded SurrealDB provider boundary without coupling domain contracts to provider-specific record or graph semantics.

Deliverables:

- Supported deployment/version scope, reviewed client and transport decision, authentication and TLS assumptions, namespace/database selection, bounded request and response handling, cancellation, timeout, and server identity policy.

Verification:

- Wrong-server, authentication failure, namespace/database isolation, malformed or oversized response, timeout, cancellation, reconnect, and version-compatibility tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.7 implementation stop reached. Run pentest for this exact commit.`

### v0.58.8 — SurrealDB Content Store

Status: planned.

Goal: Implement authoritative content/revision/relationship semantics while keeping record and relation behavior behind the adapter.

Deliverables:

- Provider-owned content schema; revisions/relations/publication roots; content outbox coupling; indexes; transaction boundaries; tenant/namespace mapping; archive identity; explicit unsupported transformations.

Verification:

- Shared content conformance, tenant/namespace/relation isolation, transaction failure/ambiguity, stale write, publication immutability, reconnect, archive root, and index rebuild tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.8 implementation stop reached. Run pentest for this exact commit.`

### v0.58.9 — SurrealDB Identity And Session Store

Status: planned.

Goal: Implement identity, credential metadata, session, group, and policy state without relying on record-link authority.

Deliverables:

- Principal/account/credential metadata mappings; uniqueness; opaque session/revocation; groups/policy epochs; tenant/namespace constraints; privacy indexes; transaction/outbox coupling; explicit unsupported behavior.

Verification:

- Duplicate/cross-tenant/namespace identity, credential/session separation, revocation races, record-link substitution, concurrent account change, transaction ambiguity, reconnect, privacy query, and redaction tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- SurrealDB record IDs/links never become identity or authorization authority and session revocation matches the portable contract.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.9 implementation stop reached. Run pentest for this exact commit.`

### v0.58.10 — SurrealDB APSP Query Translation

Status: planned.

Goal: Translate portable query semantics without exposing SurrealQL or provider graph behavior.

Deliverables:

- Canonical value mapping; typed predicates/projections; stable sort/cursors; bounded relationships; aggregates; locale fallback; consistency intent; cost/explain budgets; normalized results/errors; qualified extension separation.

Verification:

- APSP differential/property/history suites cover record/value types, null/missing, text, timezone, pagination mutation, relation traversal, aggregates, transaction behavior, injection-shaped values, amplification, cancellation, and errors.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- SurrealQL and native graph/live-query operations remain adapter-private qualified extensions, never normal client/plugin APIs.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.10 implementation stop reached. Run pentest for this exact commit.`

### v0.58.11 — SurrealDB Jobs And Outbox

Status: planned.

Goal: Prove portable durable work without relying on unqualified live-query behavior.

Deliverables:

- Job/schedule/outbox mapping; database-time and lease/fencing semantics; transactional claim/completion; retry/dead-letter; cancellation/fairness; live-query acceleration policy and receipts.

Verification:

- Claim/complete crash/replay, stale lease/fence, duplicate schedule, poison work, cancellation/fairness, live-query duplicate/gap, transaction ambiguity, reconnect, and rebuild tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Provider-native live-query features remain optional accelerators and never silently replace portable job/outbox authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.11 implementation stop reached. Run pentest for this exact commit.`

### v0.58.12 — SurrealDB Audit Store

Status: planned.

Goal: Implement append-oriented gap-detectable audit without relying on graph identity.

Deliverables:

- Chained records/checkpoints; per-domain sequences; safe diffs/redaction; transaction/mandatory-audit policy; verification/export; retention/hold; backup hooks and receipts.

Verification:

- Delete/reorder/fork/exhaustion, record-link substitution, concurrent append/transaction ambiguity, redaction/inference, checkpoint/export, retention/hold, backup/restore, reconnect, and mandatory-audit failure pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- SurrealDB audit authority has independent tamper, ambiguity, privacy, backup, and recovery evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.12 implementation stop reached. Run pentest for this exact commit.`

### v0.58.13 — SurrealDB Migration Operations

Status: planned.

Goal: Implement resumable record/relation/index evolution under explicit SurrealDB capabilities.

Deliverables:

- Migration ownership/checkpoints; record/schema versions; expand/contract transforms; relation/index/backfill operations; validation; rollback/data-loss class; mixed-version behavior; backup/export requirement and receipts.

Verification:

- Interruption/resume, concurrent migrator, lease loss, failed transform/relation/index, mixed record/application versions, live-query gaps, cancellation, rollback, irreversible warning, reconnect, and APSP post-validation pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every SurrealDB logical schema change is typed, resumable, validated, and explicit about experimental/rollback limitations.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.13 implementation stop reached. Run pentest for this exact commit.`

### v0.58.14 — SurrealDB Experimental Qualification

Status: planned.

Goal: Establish an exact experimental support envelope before any stable SurrealDB claim.

Deliverables:

- Version/deployment/settings matrix; namespace/database/transaction profile; capability limitations; backup/recovery; APSP results; performance evidence; experimental qualification manifest and promotion criteria.

Verification:

- Every declared live profile passes differential, account/content/job/audit, migration, backup/restore, topology, resource, and failure suites; instability or semantic drift removes the cell rather than weakening APSP.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- SurrealDB remains explicitly experimental until the later clustered/provider qualification and all published promotion criteria pass.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.14 implementation stop reached. Run pentest for this exact commit.`

### v0.59.0 — AHAF Export

Status: planned.

Goal: Create a streaming canonical escape hatch from every provider.

Deliverables:

- Manifest, schemas, records, relationships, assets, provenance, proof references, chunks, checksums, redaction, and resumability.

Verification:

- All providers produce equivalent logical roots for the portable fixture corpus; truncation and substitution are detected.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.59.0 implementation stop reached. Run pentest for this exact commit.`

### v0.60.0 — AHAF Import and Cross-Provider Migration

Status: planned.

Goal: Restore and move complete logical installations.

Deliverables:

- Dry run, preserve/remap IDs, conflict policy, checkpoints, extension data envelopes, referential report, and explicit omissions.

Verification:

- SQLite→PostgreSQL→MariaDB→MongoDB→SurrealDB round trips preserve declared semantics and report every unsupported transformation.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.0 implementation stop reached. Run pentest for this exact commit.`

### v0.60.1 — Remote Cache Offload Contract

Status: planned.

Goal: Define optional shared cache offload without turning cache state into authority.

Deliverables:

- Cache-class capability model, canonical tenant/site/environment/locale/viewer/policy/release keys, bounded values and TTLs, invalidation, stampede control, stale rules, provider health, and explicit bypass versus fail-closed policy.

Verification:

- Reference-model tests cover key collisions, omitted security dimensions, poisoning, eviction, stale values, invalidation races, provider loss, cancellation, overload, and reconstruction from authoritative state.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.1 implementation stop reached. Run pentest for this exact commit.`

### v0.60.2 — Valkey Client Admission

Status: planned.

Goal: Admit a mature Valkey-compatible client and transport boundary.

Deliverables:

- Exact reviewed crate/features and protocol scope; TLS/authentication/server identity; unsafe/native/build-script and transitive review; command allowlist; response framing budgets; cancellation/timeouts; pooling/pipelining limits; platform and CVE-response plan.

Verification:

- Admission, protocol-fixture, malformed/oversized response, wrong server, downgrade, credential redaction, disconnect, cancellation, feature drift, and unsupported platform/version tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.2 implementation stop reached. Run pentest for this exact commit.`

### v0.60.3 — Valkey Cache Adapter Semantics

Status: planned.

Goal: Implement the non-authoritative cache contract through the admitted client.

Deliverables:

- Canonical namespaced keys; bounded values/TTLs; get/put/invalidate; cache-class bypass/fail-closed behavior; stampede control; pooling/pipelining use; health, metrics, redaction, and operational configuration.

Verification:

- Reference conformance covers key collision/dimension omission, poisoning, malformed values, stale epochs, eviction, invalidation races, stampede, cancellation, overload, outage, and reconstruction from authority.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Removing every Valkey value affects only documented performance/availability behavior and cannot create authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.3 implementation stop reached. Run pentest for this exact commit.`

### v0.60.4 — Valkey Live Qualification

Status: planned.

Goal: Qualify exact Valkey versions and topologies under real failure.

Deliverables:

- Version/topology/ACL/TLS/eviction/persistence profile; clean fixtures; failover/partition controller; latency/memory budgets; support manifest; one acceptance entry point.

Verification:

- Live disconnect, partition, failover, eviction, poison, latency spike, memory pressure, restart, credential rotation, cross-tenant load, and authoritative reconstruction tests pass for every claimed cell.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No Valkey version or topology is supported without current live qualification evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.4 implementation stop reached. Run pentest for this exact commit.`

### v0.60.5 — OpenBao Dependency Conflict Decision

Status: planned.

Goal: Resolve the OpenBao/secret-memory dependency boundary without weakening the absolute zeroize ban or inventing security infrastructure.

Deliverables:

- Current `openbao` dependency/feature audit; in-process zeroize-free admission criteria; reviewed zeroize-free sidecar alternative with authenticated bounded protocol; threat/cost/operability comparison; explicit user decision ADR; re-evaluation trigger.

Verification:

- Lockfile/feature fixtures prove an in-process path cannot hide `zeroize`; sidecar fixtures cover identity, protocol confusion, secret/log leakage, crash, outage, cancellation, rotation, and clean process boundaries.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- If neither a zeroize-free `openbao` graph nor an approved zeroize-free sidecar is safe and practical, OpenBao remains unsupported; no custom TLS or OpenBao protocol stack is substituted.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.5 implementation stop reached. Run pentest for this exact commit.`

### v0.60.6 — OpenBao Client Admission

Status: planned.

Goal: Establish an optional least-authority OpenBao secret-provider boundary using the project-owned `openbao` crate.

Deliverables:

- Exact zeroize-free crate/feature graph, exact supported server profiles, typed secret references, TLS/server identity, narrow authentication, response limits, renewal/revocation, redaction, `sanitization` ownership, and fail-closed provider policy.

Verification:

- Admission rejects any direct or transitive `zeroize`; wrong-server, downgrade, expired/replayed token, denied path, malformed/oversized secret, cancellation, renewal, outage, redaction, and compatibility tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The selected `openbao` release and feature graph contain no `zeroize`; otherwise this milestone remains blocked and no OpenBao support is claimed.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.6 implementation stop reached. Run pentest for this exact commit.`

### v0.60.7 — OpenBao Startup Secret Bootstrap

Status: planned.

Goal: Optionally move explicitly selected startup environment secrets into OpenBao before the Aetherheim server starts.

Deliverables:

- Separate bootstrap executable, explicit variable-to-KV-path map, bounded `sanitization` ingestion, no prefix-wide environment scan, idempotent conflict policy, partial-write journal, redacted report, narrow/expiring bootstrap authority, `env_clear` child launch, and secret-reference handoff.

Verification:

- Unknown-variable, path injection, duplicate target, existing-value, partial write, network loss, wrong server, auth expiry, log/error/panic redaction, child-environment, process-memory lifecycle, retry, and rollback fixtures pass without unsafe post-thread environment mutation.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.7 implementation stop reached. Run pentest for this exact commit.`

### v0.60.8 — OpenBao Live Qualification

Status: planned.

Goal: Qualify the admitted OpenBao path against exact real server profiles.

Deliverables:

- Version/topology/TLS/auth-method/KV/lease profile; bootstrap and normal-operation identities; rotation/renew/revoke fixtures; outage/skew controller; redacted evidence and support manifest.

Verification:

- Live wrong identity, auth denial/expiry, KV version conflict, lease renewal/revocation, rotation, clock skew, seal/outage/restart, partial bootstrap, clean-child environment, and secret/redaction scenarios pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No OpenBao version, authentication method, or topology is supported from protocol mocks alone.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.8 implementation stop reached. Run pentest for this exact commit.`

### v0.60.9 — Live Database Provider Matrix

Status: planned.

Goal: Prove database support against launched services rather than protocol models alone.

Deliverables:

- Reproducible live fixtures for every declared SQLite, PostgreSQL, MariaDB, MongoDB, and SurrealDB version/topology; clean provisioning, health, test isolation, redacted logs, APSP traces, evidence manifest, and one command integrated into `scripts/acceptance.sh all`.

Verification:

- The same black-box storage journey runs against every provider: initialize, migrate, content/identity/session records, relationships, jobs/outbox/audit, concurrent access, restart, failure/recovery, export/import, and cross-provider round trip; adapter-specific failure cases also run live.
- Deliberately remove each service/runtime and prove the release gate fails rather than skips or substitutes a mock.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No database or topology appears in the supported matrix without current live acceptance evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.9 implementation stop reached. Run pentest for this exact commit.`

### v0.60.10 — S3-Compatible Client Admission

Status: planned.

Goal: Admit a mature S3-compatible client and define the exact interoperable protocol subset.

Deliverables:

- Exact reviewed crate/features; endpoint/TLS/auth/signing identity; supported S3-compatible operations/services; unsafe/native/build-script and transitive review; request/response/stream budgets; cancellation; retry classification; platform and CVE-response plan.

Verification:

- Admission and protocol fixtures cover wrong endpoint/identity, downgrade, signing confusion, malformed/oversized response, retry ambiguity, cancellation, feature drift, and unsupported operation/service behavior.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No object operation is used until its semantics and retry class are explicit in the admitted subset.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.10 implementation stop reached. Run pentest for this exact commit.`

### v0.60.11 — Shared S3-Compatible Blob Adapter

Status: planned.

Goal: Implement the shared immutable blob authority required by clustered operation.

Deliverables:

- Immutable tenant-scoped keys; conditional creation; bounded streaming; multipart upload/abort journal; digest verification; metadata/classification; quotas; lifecycle/retention/hold; reference integration; health and observability.

Verification:

- Model/fixture tests cover cross-tenant keys, concurrent create, partial/multipart crash, cleanup replay, stale listing, corruption, deletion/hold conflict, throttling, cancellation, and authoritative reference races.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Blob correctness never depends on list consistency, mutable object replacement, or an unqualified provider extension.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.11 implementation stop reached. Run pentest for this exact commit.`

### v0.60.12 — S3-Compatible Live Qualification

Status: planned.

Goal: Qualify exact shared-object providers and topologies under real failure.

Deliverables:

- Provider/version/topology/settings matrix; TLS/auth profile; multipart/lifecycle/retention behavior; clean fixtures; outage/corruption controller; performance evidence; support manifest and acceptance entry point.

Verification:

- Live substitution, concurrent create, multipart crash/cleanup, stale listing, read-after-write, corruption, retention/hold, throttling, outage, restart, credential rotation, backup, restore, and cross-node access pass for every claimed cell.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Clustered profiles use only a currently qualified shared object store; NFS/shared-filesystem behavior is not implied.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.12 implementation stop reached. Run pentest for this exact commit.`

### v0.60.13 — Fenced Live Provider Migration

Status: planned.

Goal: Move a live installation without an unbounded dual-write window or silent divergence.

Deliverables:

- Source-root capture; bulk copy; bounded delta log/replay; write quiescence fence; destination root verification; cutover; derived cache/search rebuild; rollback horizon; operator receipt.

Verification:

- Inject crash, retry, concurrent writes, stale workers, source/destination loss, corrupt deltas, root mismatch, and rollback at every phase across each qualified source/destination pair.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Migration either preserves the declared canonical root and cuts over once, or remains/returns to the source with a complete discrepancy report.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.13 implementation stop reached. Run pentest for this exact commit.`

## Phase 6 — Content application, routing, APIs, and audit

### v0.61.0 — Content Command Core

Status: planned.

Goal: Create and change typed entries only through application services.

Deliverables:

- Create, update draft, delete intent, restore, expected revision, policy check, event/outbox plan, and audit intent.

Verification:

- Unit/model tests cover every state transition, stale write, denial, retry, and failure atomicity.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.61.0 implementation stop reached. Run pentest for this exact commit.`

### v0.62.0 — Immutable Revisions

Status: planned.

Goal: Make meaningful editorial history append-oriented.

Deliverables:

- Revision manifest, parent/base, author/editor/executor, document/media/relationship roots, source/AI/import state, and stable revision root.

Verification:

- Any included change affects the root; published revisions cannot mutate; unknown blocks round-trip.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.62.0 implementation stop reached. Run pentest for this exact commit.`

### v0.63.0 — Draft and Autosave Lifecycle

Status: planned.

Goal: Support safe editing without making every keystroke canonical.

Deliverables:

- Draft ownership, autosave compaction policy, conflict detection, recovery, presence lease, and bounded history.

Verification:

- Concurrent editor, crash, stale autosave, quota, and restore scenarios pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.63.0 implementation stop reached. Run pentest for this exact commit.`

### v0.64.0 — Publication State Machine

Status: planned.

Goal: Make publication a deliberate audited pointer transition.

Deliverables:

- Draft/review/scheduled/published/unpublished/trashed states, policy guard, immutable target, idempotency, and rollback-as-new-action.

Verification:

- Model sweep proves no half-published or mutable published state and safe retry after ambiguity.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.64.0 implementation stop reached. Run pentest for this exact commit.`

### v0.65.0 — Workflow and Approvals

Status: planned.

Goal: Add configurable review without vague approval.

Deliverables:

- State/transition definitions, assignments, separation of duties, digest-bound approval, quorum, expiry, revocation, and reason.

Verification:

- Replay, stale revision, self-approval, missing quorum, revoked approval, and policy-epoch tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.65.0 implementation stop reached. Run pentest for this exact commit.`

### v0.65.1 — Taxonomies And Terms

Status: planned.

Goal: Add reusable hierarchical/faceted editorial classification without encoding provider graph semantics.

Deliverables:

- Versioned taxonomy and term identities; hierarchy where declared; aliases/synonyms; localized labels/slugs; content assignments; ordering; locale/visibility/policy context; cycle/cardinality limits; revision/publication/archive behavior.

Verification:

- Cycle, duplicate/alias confusion, deep/wide hierarchy, stale assignment, cross-tenant/locale/visibility leakage, concurrent reorder, publish/unpublish, query-cost, archive, and migration tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Taxonomy semantics remain portable content-domain contracts and do not expose database-native graph/query authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.65.1 implementation stop reached. Run pentest for this exact commit.`

### v0.65.2 — Curated And Dynamic Collections

Status: planned.

Goal: Publish ordered curated or bounded-query content groupings independently from taxonomy assignment.

Deliverables:

- Collection identity/version; manual members/order; bounded dynamic query reference; mixed-mode precedence; locale/site/visibility/policy context; duplicate/missing-member policy; revision/publication root; API/render/search/archive projection.

Verification:

- Duplicate/missing/private member, cross-tenant/locale leakage, dynamic query amplification, concurrent reorder/query change, stale publication, delete/unpublish, cache/search invalidation, archive, and migration tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Dynamic collections use APSP queries and policy-filtered `ContentView`; they cannot embed raw provider queries or reveal forbidden members.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.65.2 implementation stop reached. Run pentest for this exact commit.`

### v0.66.0 — Routing and Domains

Status: planned.

Goal: Resolve verified host/path/locale routes safely.

Deliverables:

- Domain binding, slug history, canonical route, aliases, redirects, collision report, host validation, and bounded lookup.

Verification:

- Host spoofing, path confusion, redirect loops, collision, cache partition, and Unicode-display fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.66.0 implementation stop reached. Run pentest for this exact commit.`

### v0.66.1 — Navigation And Menu Publication

Status: planned.

Goal: Publish explicit accessible navigation independently from themes.

Deliverables:

- Versioned menus; content/route/external-link items; nested ordering; locale/site/visibility context; active state; missing-target policy; publication root; bounded traversal; theme/API projection.

Verification:

- Cycle/depth, broken or private target, unsafe external URL, cross-site/locale leakage, concurrent reorder, stale route, rollback, keyboard semantics, archive, and cache-invalidation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Themes consume a validated navigation projection and cannot invent access to unpublished targets.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.66.1 implementation stop reached. Run pentest for this exact commit.`

### v0.66.2 — Publication Metadata, Robots, Sitemaps, And Feeds

Status: planned.

Goal: Define canonical discovery output as policy-filtered publication artifacts.

Deliverables:

- Title/description/social metadata; canonical URL; robots directives; sitemap indexes/entries; RSS/Atom-shaped feed contract; update timestamps; locale/site partitions; pagination and size limits; release-rooted generation.

Verification:

- Draft/private/expired content, wrong canonical/host/locale, metadata injection, oversized sitemap/feed, stale deletion, cache mixing, deterministic regeneration, and search-engine preview fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Discovery artifacts derive only from the immutable allowed publication view and cannot leak management metadata.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.66.2 implementation stop reached. Run pentest for this exact commit.`

### v0.66.3 — Production HTTP Runtime Admission

Status: planned.

Goal: Admit a mature HTTP server/runtime boundary without coupling domain code to a framework.

Deliverables:

- Exact reviewed runtime/server crates and features; supported HTTP versions; async/executor ownership; unsafe/native/build-script and transitive review; connection/task/body limits; cancellation; upgrade/streaming scope; platform and CVE-response policy.

Verification:

- Admission fixtures, protocol corpus, malformed framing, request smuggling, slow clients, cancellation, task leak, unsupported upgrade/version, dependency feature drift, and platform tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The runtime remains behind `aetherheim-http`; application services and portable contracts expose no framework types.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.66.3 implementation stop reached. Run pentest for this exact commit.`

### v0.66.4 — TLS And Certificate Lifecycle

Status: planned.

Goal: Provide secure direct serving through an admitted TLS foundation and explicit certificate ownership.

Deliverables:

- Exact TLS/provider admission; protocol/cipher policy; server identity and SNI; certificate/key references; load/renew/rotate/revoke; OCSP/status scope; direct versus proxy termination; clock/failure policy; secret-memory/redaction integration.

Verification:

- Wrong/expired/not-yet-valid/revoked certificate, hostname/SNI confusion, downgrade, weak algorithm, key mismatch/leak, partial rotation, clock skew, reload race, provider outage, and cross-platform tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Remote production serving never falls back to plaintext or an unreviewed TLS implementation.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.66.4 implementation stop reached. Run pentest for this exact commit.`

### v0.66.5 — HTTP Request And Response Governance

Status: planned.

Goal: Apply one bounded security policy to every public and administrative HTTP exchange.

Deliverables:

- Host/origin derivation; method/path/query/header/body budgets; content-type and encoding policy; timeout/cancellation; compression limits; security headers/CSP/HSTS; cookies; error/problem responses; request IDs; logging/redaction; graceful drain.

Verification:

- Host/origin spoofing, method/content-type confusion, duplicate headers, smuggling, compression bombs, slowloris, oversized bodies/responses, disconnect, error leakage, cookie/header injection, and drain races pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- APIs, rendering, media, admin, GraphQL, and webhooks cannot define weaker private transport rules.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.66.5 implementation stop reached. Run pentest for this exact commit.`

### v0.66.6 — Direct HTTP/TLS Acceptance Matrix

Status: planned.

Goal: Qualify direct serving on every claimed host platform before proxy profiles exist.

Deliverables:

- Packaged serve-role fixtures; HTTP/TLS/version/platform matrix; certificate rotation; connection/resource/slow-client controller; health/readiness/drain journeys; evidence manifest and one acceptance command.

Verification:

- Live Linux, Windows, BSD, and macOS direct-serving tests cover requests, streaming where supported, TLS identity/rotation, limits, malformed traffic, restart, drain, dependency loss, and clean uninstall; missing required runners fail the release gate.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Direct serving is supported only for exact tested protocol/platform profiles; proxy support remains separate.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.66.6 implementation stop reached. Run pentest for this exact commit.`

### v0.66.7 — Domain Ownership And Lifecycle

Status: planned.

Goal: Bind public and administrative hosts only after explicit ownership verification and safe lifecycle transitions.

Deliverables:

- Domain claim/challenge/verification methods; DNS/provider boundary; tenant/site/admin purpose; expiry/reverification; transfer/release/tombstone; certificate and route linkage; takeover prevention; canonical-host transition; audit and operator recovery.

Verification:

- Forged/stale/replayed challenge, dangling DNS, expired verification, cross-tenant claim, concurrent transfer, deleted site, subdomain/wildcard confusion, certificate mismatch, cache/redirect persistence, takeover, and recovery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No unverified or released domain can route, issue certificates, set cookies, or become a canonical URL for a tenant.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.66.7 implementation stop reached. Run pentest for this exact commit.`

### v0.67.0 — Content Delivery API

Status: planned.

Goal: Expose published data without management leakage.

Deliverables:

- Versioned read contracts, filters, fields, cursor pagination, locale/domain context, ETag, cache tags, preview scope, and limits.

Verification:

- Anonymous negative tests prove drafts, private fields, cross-tenant data, and internal schema metadata cannot leak.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.67.0 implementation stop reached. Run pentest for this exact commit.`

### v0.68.0 — Management API

Status: planned.

Goal: Expose the complete typed command/query boundary.

Deliverables:

- Idempotency, expected revision, explicit scope, problem details, request/correlation IDs, reason metadata, budgets, and audit references.

Verification:

- Contract golden tests and adversarial auth/scope/replay/payload suites pass transport-independently.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.68.0 implementation stop reached. Run pentest for this exact commit.`

### v0.68.1 — GraphQL Read Boundary

Status: planned.

Goal: Expose the policy-filtered `ContentView` through a bounded versioned GraphQL schema.

Deliverables:

- Schema generation; node and cursor model; field/locale/viewer context; query depth, complexity, aliases, fragments, batching, introspection, persisted-operation, error-redaction, and cache rules.

Verification:

- Draft/private/field/tenant leakage, alias/fragment amplification, cyclic fragments, batching abuse, introspection policy, stale cursor, cache mixing, malformed request, and REST/GraphQL projection-equivalence tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- GraphQL reads use the same application queries and `ContentView` policy semantics as REST; resolvers cannot query providers directly.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.68.1 implementation stop reached. Run pentest for this exact commit.`

### v0.68.2 — GraphQL Management Operations

Status: planned.

Goal: Add mutations without creating a second command or authorization model.

Deliverables:

- Typed mutation inputs/results; idempotency, expected revision, tenant context, policy obligations, upload references, operation receipts, subscription scope, and compatibility rules.

Verification:

- Mutation replay, scope substitution, partial-field errors, alias duplication, stale revision, subscription revocation, operation ambiguity, and REST/GraphQL command-equivalence suites pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every GraphQL mutation is a thin adapter to an existing typed application command with identical authority and audit behavior.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.68.2 implementation stop reached. Run pentest for this exact commit.`

### v0.68.3 — Generated Client Schema And Compatibility

Status: planned.

Goal: Keep browser, server, and future native clients aligned with one source of API truth.

Deliverables:

- Reproducible REST/OpenAPI, GraphQL, TypeScript, Kotlin, and Swift schema/code generation inputs; semantic diff; fixtures; version/deprecation policy; artifact digests.

Verification:

- Two clean generations match byte-for-byte; stale/manual client types, breaking field changes, optionality drift, unsafe unknown handling, and `ContentView` divergence fail CI.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Generated artifacts remain repository/release assets and do not imply crates.io or external package-registry publication.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.68.3 implementation stop reached. Run pentest for this exact commit.`

### v0.69.0 — Integration Event Publication

Status: planned.

Goal: Publish versioned external integration facts without exposing internal event authority.

Deliverables:

- External event catalog and payload versions; tenant/site/data-classification scope; outbox projection; delivery identity; compatibility/deprecation; redaction; retention; replay/export cursor; internal-versus-external event separation.

Verification:

- Draft/private/field/tenant leakage, schema drift, duplicate/reordered projection, stale policy, cursor replay, retention/deletion, redaction, and internal-payload disclosure tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.69.0 implementation stop reached. Run pentest for this exact commit.`

### v0.69.1 — Signed Webhook Delivery

Status: planned.

Goal: Deliver integration events to approved destinations with replay resistance and bounded failure handling.

Deliverables:

- Subscription lifecycle and destination policy; DNS/private-address/redirect controls; signature-provider and secret rotation; timestamp/delivery ID; bounded request/response; retry/backoff/dead-letter; pause/replay; receipts and operator diagnostics.

Verification:

- SSRF/rebinding/redirect, header injection, signature/key rotation, replay, duplicate/reorder, response amplification, timeout, poison destination, cancellation, disable/delete race, and secret/log leakage tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Webhook failure never changes the committed source fact and every retry remains idempotently identifiable.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.69.1 implementation stop reached. Run pentest for this exact commit.`

### v0.70.0 — Audit and Operation Receipt API

Status: planned.

Goal: Expose evidence without exposing protected internals.

Deliverables:

- Role-scoped audit queries, verification roots, operation receipts, safe before/after references, support export, and gap warnings.

Verification:

- Unprivileged disclosure, inference, pagination gap, tamper, redaction, and stale-root tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.70.0 implementation stop reached. Run pentest for this exact commit.`

### v0.70.1 — Notification Intents And In-Product Inbox

Status: planned.

Goal: Give security, workflow, account, media, commerce, and operations events one user-visible notification model before mail/push adapters.

Deliverables:

- Typed notification intent; recipient/tenant/purpose/priority; deduplication; read/acknowledge/dismiss; expiry/retention; sensitive preview policy; deep-link capability; preference and mandatory-security classes; audit and delivery-adapter outbox.

Verification:

- Wrong recipient/tenant, duplicate/reordered intent, sensitive preview leak, stale/revoked deep link, preference bypass, mandatory-notice suppression, read-state race, expiry/deletion, retry, and accessibility tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Domain modules propose typed notifications and never send mail or UI messages directly.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.70.1 implementation stop reached. Run pentest for this exact commit.`

### v0.70.2 — Operator CLI And Scripting Contract

Status: planned.

Goal: Expose administration and operations through the same typed application boundary with stable automation behavior.

Deliverables:

- Local/remote endpoint selection; authenticated profiles; version negotiation; structured input/output; idempotency and expected revision; confirmation/non-interactive policy; stdin/file secret handling; exit codes; pagination/streaming; operation receipts; shell completion and offline diagnostics.

Verification:

- Wrong endpoint/tenant/version, output injection, secret argv/history/log leakage, missing confirmation, replay, partial stream, pipe cancellation, pagination, non-interactive errors, automation compatibility, and cross-platform shell tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- CLI commands do not bypass API/application policy, and scripts receive stable machine-readable results and exit semantics.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.70.2 implementation stop reached. Run pentest for this exact commit.`

## Phase 7 — Identity, sessions, authorisation, and platform security

### v0.71.0 — Principal and Credential Model

Status: planned.

Goal: Separate stable identity from authentication methods.

Deliverables:

- Human/service principals, external identities, credential metadata, authenticators, recovery, PAT, service, device, and workload references.

Verification:

- Credential add/remove never changes ownership; duplicate/cross-tenant and privacy disclosure tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.71.0 implementation stop reached. Run pentest for this exact commit.`

### v0.71.1 — Administrator Bootstrap And Installation Ownership

Status: planned.

Goal: Establish the first administrator without a permanent default credential or raceable public setup path.

Deliverables:

- Uninitialized installation state; local/one-time bootstrap capability; installation ownership claim; first administrator and recovery setup; expiry/attempt budget; atomic close; re-bootstrap authorization; audit and clean diagnostics.

Verification:

- Concurrent/remote claim, replay/guessing, stale bootstrap token, partial account creation, restart, database ambiguity, log/argv/env leakage, proxy exposure, already-initialized state, recovery failure, and authorized re-bootstrap tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No shipped default account/password exists and the public setup surface closes atomically after one successful ownership claim.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.71.1 implementation stop reached. Run pentest for this exact commit.`

### v0.71.2 — Account Registration, Verification, And Lifecycle

Status: planned.

Goal: Implement complete account creation and state transitions independently from credential mechanisms.

Deliverables:

- Administrator-created/invited/self-registration profiles; verified communication-point challenge; pending/active/restricted/disabled/deletion states; uniqueness/privacy; resend/change flows; abuse budgets; notifications; retention/erasure and audit.

Verification:

- Enumeration, duplicate/case/Unicode identity, verification replay/substitution, invite theft, resend abuse, concurrent activation/disable/delete, cross-tenant registration, stale sessions/credentials, notification failure, retention/erasure, and restore tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every account state has explicit authentication/session/authorization behavior and launchable public-boundary tests.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.71.2 implementation stop reached. Run pentest for this exact commit.`

### v0.72.0 — Password Credential Boundary

Status: planned.

Goal: Support passwords without storing or handling them casually.

Deliverables:

- Password policy, calibrated-hash provider interface, pepper handle, breached-list interface, reset token lifecycle, and step-up rules.

Verification:

- No insecure fallback exists; reset replay, enumeration, logging, timing-envelope, and unavailable-provider tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.72.0 implementation stop reached. Run pentest for this exact commit.`

### v0.72.1 — Password Hash Provider Admission And Calibration

Status: planned.

Goal: Admit a mature password-hashing implementation and calibrate it per supported profile.

Deliverables:

- Exact crate/provider and algorithm/version admission; parameter bounds; pepper operation handle; per-platform calibration; rehash/upgrade policy; concurrency/memory budgets; unavailable-provider behavior; secret-memory and CVE-response plan.

Verification:

- Known-answer/format, weak/oversized parameters, wrong pepper, downgrade, truncated/corrupt hash, calibration under load, resource exhaustion, rehash race, provider absence, redaction, and platform tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Password login remains unavailable until a reviewed provider and measured profile exist; no home-grown password hash is permitted.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.72.1 implementation stop reached. Run pentest for this exact commit.`

### v0.73.0 — Opaque Browser Sessions

Status: planned.

Goal: Provide revocable secure administration sessions.

Deliverables:

- Random-provider boundary, hashed server record, secure-cookie policy, CSRF binding, rotation, idle/absolute expiry, inventory, and revocation.

Verification:

- Fixation, theft/replay, CSRF, privilege-change, recovery restriction, and sign-out-all suites pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.73.0 implementation stop reached. Run pentest for this exact commit.`

### v0.73.1 — Authoritative Session Cache Integration

Status: planned.

Goal: Permit Valkey session acceleration without allowing cache state to become authentication authority.

Deliverables:

- Database-authoritative session record; hashed cache material; tenant/session/security/credential/recovery epochs; bounded TTL; rotation/invalidation; critical-action recheck; cache outage and database outage policy.

Verification:

- Poisoned/malformed/stale entries, epoch omission, fixation, revocation races, Valkey loss, database loss, node failover, eviction, replay, and cross-tenant cache-key tests prove administration fails closed when authority is unavailable.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Deleting all Valkey state affects performance only; it cannot create, extend, revive, or authorize a session.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.73.1 implementation stop reached. Run pentest for this exact commit.`

### v0.74.0 — WebAuthn Data and Ceremony

Status: planned.

Goal: Model passkeys and hardware keys without overstating assurance.

Deliverables:

- RP/origin policy, challenges, credential records, counters/backup state, user verification, attestation policy, and command-approval hook.

Verification:

- Origin/RP mismatch, challenge replay, credential substitution, counter policy, and recovery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.74.0 implementation stop reached. Run pentest for this exact commit.`

### v0.74.1 — WebAuthn Standards Implementation Admission

Status: planned.

Goal: Admit mature WebAuthn/CBOR/authenticator-data handling instead of implementing the protocol parser in application code.

Deliverables:

- Exact crate/features and supported ceremony/extension/attestation scope; origin/RP policy mapping; bounded CBOR/authenticator/client data; unsafe/native/transitive review; algorithm handoff; browser/platform matrix; CVE-response plan.

Verification:

- Official/mutated vectors, malformed/deep CBOR, duplicate fields, origin/RP/challenge/type confusion, unsupported extension/attestation, feature drift, and cross-browser/platform fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- WebAuthn protocol parsing and ceremony validation stay behind a reviewed standards boundary and cannot be bypassed by management transport code.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.74.1 implementation stop reached. Run pentest for this exact commit.`

### v0.75.0 — Authenticator Crypto Provider

Status: planned.

Goal: Verify admitted WebAuthn algorithms through explicit platform boundaries.

Deliverables:

- Algorithm allowlist, OS/service provider identity, exact input/output contract, self-tests, failure policy, and no software fallback.

Verification:

- Known-answer, wrong-key, malformed signature, provider downgrade, unavailable provider, and cross-platform suites pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.75.0 implementation stop reached. Run pentest for this exact commit.`

### v0.76.0 — TOTP Authenticators

Status: planned.

Goal: Add a bounded fallback authenticator without conflating it with account recovery.

Deliverables:

- TOTP provider/algorithm boundary; enrollment proof; secret reference and display window; replay state; clock/skew policy; brute-force budget; disable/replace ceremony; audit and notifications.

Verification:

- Enrollment substitution, replay, brute-force budget, code/secret disclosure, clock skew/movement, concurrent verification, disable/replace, backup restore, and stronger-authenticator preservation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.76.0 implementation stop reached. Run pentest for this exact commit.`

### v0.76.1 — Account Recovery And Recovery Codes

Status: planned.

Goal: Restore access without allowing recovery to silently defeat stronger authenticators or administrative policy.

Deliverables:

- Hashed one-time recovery codes; reset/recovery request and expiry; proof/risk/approval policy; anti-enumeration and abuse budgets; post-recovery restricted session; credential inventory review; notifications; revoke-all and support-admin separation.

Verification:

- Code/token replay, guessing, enumeration, stale request, self/admin abuse, cross-tenant recovery, email/provider loss, stronger-credential removal, concurrent recovery, notification failure, restricted-session escape, and audit tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Recovery cannot directly grant a normal privileged session or remove stronger credentials without the configured evidence and review path.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.76.1 implementation stop reached. Run pentest for this exact commit.`

### v0.77.0 — OIDC Relying-Party Federation

Status: planned.

Goal: Authenticate through explicitly trusted external OIDC issuers.

Deliverables:

- Issuer discovery/pinning; authorization-code/PKCE state; redirect URI; issuer/audience/nonce/time validation; signing-key rotation; claim mapping/linking; step-up/assurance mapping; logout/session linkage; outage and revocation policy.

Verification:

- Mix-up, malicious discovery, redirect, issuer/audience/nonce, key rotation, algorithm downgrade, claim/account collision, tenant, expiry, logout/revocation, and provider outage tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.77.0 implementation stop reached. Run pentest for this exact commit.`

### v0.77.1 — OAuth Authorization Server Boundary

Status: planned.

Goal: Authorize external clients through a narrow standards-compliant server profile when enabled.

Deliverables:

- Client registration/trust; authorization-code/PKCE; redirect policy; consent; tenant/audience/scope model; short-lived access and refresh-token families; rotation/replay/revocation; metadata; signing provider; rate and audit policy.

Verification:

- Client/redirect substitution, code interception/replay, mix-up, PKCE downgrade, consent/scope broadening, audience/tenant confusion, refresh-family replay, key rotation, revocation, and abuse tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Authorization-server behavior is optional, separately profiled, and never inferred from OIDC login support.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.77.1 implementation stop reached. Run pentest for this exact commit.`

### v0.77.2 — Personal Access Tokens

Status: planned.

Goal: Support user-created API credentials without turning them into browser sessions or passwords.

Deliverables:

- Hashed personal token records; one-time display; user/tenant/audience/scope/purpose/expiry; issuance step-up and policy; rotation/revocation/inventory; last-use privacy; secret-memory, rate, notification, and audit rules.

Verification:

- Token substitution/replay, scope/audience/tenant confusion, leaked inventory/value, stale privilege, revocation race, expiry, brute force/rate, log leakage, account disable/delete, and disabled-profile tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Personal tokens have narrower authority than their user, cannot enter browser session flows, and are disabled by profiles that prohibit them.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.77.2 implementation stop reached. Run pentest for this exact commit.`

### v0.77.3 — Service And Workload Identities

Status: planned.

Goal: Authenticate automated workloads through explicit non-human principals and platform identity boundaries.

Deliverables:

- Service/workload principal lifecycle; tenant/audience/scope/purpose; workload identity/provider attestation reference; credential/certificate/token exchange; rotation/revocation; deployment binding; no interactive recovery; inventory, rate, audit, and incident response.

Verification:

- Human/service confusion, workload/deployment substitution, audience/tenant/scope escalation, stale attestation/credential, rotation overlap, revocation race, cloned workload, provider outage, log leakage, and disabled-profile tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Workloads never borrow human credentials or recovery paths, and each identity is bound to a declared deployment/provider profile.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.77.3 implementation stop reached. Run pentest for this exact commit.`

### v0.77.4 — Device Authorization Flow

Status: planned.

Goal: Authorize input-constrained devices without phishing-prone or over-broad token behavior.

Deliverables:

- Optional OAuth device flow; user/device codes; verification URI/origin; polling interval/expiry; client/audience/scope/tenant consent; rate and abuse controls; token issuance/revocation; user notifications and audit.

Verification:

- Code guessing/replay/substitution, phishing origin, client/audience/scope/tenant confusion, polling amplification, concurrent approval/denial, expiry, user-switch, token replay/revocation, and disabled-profile tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Device authorization is optional, visibly consented, short-lived, and never bundled implicitly with personal or workload-token support.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.77.4 implementation stop reached. Run pentest for this exact commit.`

### v0.78.0 — RBAC Administration

Status: planned.

Goal: Make understandable least-privilege roles operational.

Deliverables:

- Built-in roles, custom roles, groups, tenant/site/environment scope, permission diff, access review, and safe defaults.

Verification:

- Every management action has allow/deny tests and role templates contain no hidden broad privilege.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.78.0 implementation stop reached. Run pentest for this exact commit.`

### v0.79.0 — Contextual ABAC Enforcement

Status: planned.

Goal: Apply field, locale, workflow, classification, purpose, and request-context policy.

Deliverables:

- Central decision service; explicit deny; tenant/site/environment/field/locale/workflow/classification/purpose attributes; projection filters; typed obligations; decision cache dimensions; explanation and epochs.

Verification:

- Cache-omission model tests, stale attributes/epochs, field/locale/classification/purpose projection, and cross-context denial suites prove no policy dimension is lost.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.79.0 implementation stop reached. Run pentest for this exact commit.`

### v0.79.1 — Relationship-Based Authorization

Status: planned.

Goal: Add bounded ReBAC proofs without exposing provider graph traversal as authority.

Deliverables:

- Versioned relationship types; subject/resource edges; provenance/revision; bounded proof traversal; cycle/depth/work limits; revocation and stale-proof policy; explanation; APSP query mapping and cache dimensions.

Verification:

- Forged/stale/revoked edges, cycles, path explosion, provider divergence, cross-tenant traversal, delegation loops, cache omission, concurrent edge change, and explanation/proof mismatch tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A relationship allow requires a current bounded portable proof; database-native graph reachability alone is never an authorization decision.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.79.1 implementation stop reached. Run pentest for this exact commit.`

### v0.79.2 — Authorization Enforcement Acceptance Matrix

Status: planned.

Goal: Prove every management and delivery surface consumes the same decisions and obligations.

Deliverables:

- Cross-surface action/field matrix for CLI, REST, GraphQL, browser, jobs, search, render, cache, webhooks, plugins, and imports; allow/deny/obligation scenarios; policy-change invalidation; evidence report.

Verification:

- Real-process tests exercise actor/role/attribute/relationship/policy changes and prove immediate consistent denial/redaction/step-up across every implemented surface and qualified database.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No supported surface or adapter has a private authorization path or can ignore a typed obligation.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.79.2 implementation stop reached. Run pentest for this exact commit.`

### v0.80.0 — Administrative Origin And Surface Isolation

Status: planned.

Goal: Separate administrative authority from public delivery and extension origins.

Deliverables:

- Separate administrative origin/listener and cookie scope; CSP/egress defaults; health/support endpoint separation; extension-origin isolation; direct/proxy derivation; emergency/recovery entry; explicit development-only co-origin non-claim.

Verification:

- Origin/cookie/CSRF/CORS isolation, public-route confusion, forwarding spoof, extension frame/message escape, admin discovery, egress, health/support exposure, and usable recovery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.80.0 implementation stop reached. Run pentest for this exact commit.`

### v0.80.1 — Account Lifecycle Acceptance Matrix

Status: planned.

Goal: Prove that real users and administrators can complete the full account lifecycle securely on every supported database.

Deliverables:

- Public-boundary scenarios for administrator bootstrap, account creation, verification, login, logout, session rotation/revocation, password reset, recovery, WebAuthn/TOTP when enabled, role/group change, disable, re-enable, deletion/erasure, audit, and cross-tenant denial.

Verification:

- Launch real Aetherheim server/worker processes and run the complete lifecycle through public management/browser boundaries against SQLite, PostgreSQL, MariaDB, MongoDB, and SurrealDB, including restart, concurrent sessions, failed database/cache/OpenBao dependencies, node failover, and hostile input.
- No internal repository call, mock authenticator, or in-memory database substitutes for the end-to-end support evidence; deterministic tests remain additive.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every claimed authentication method, database, platform, and deployment profile has a passing launchable account-lifecycle scenario or is explicitly absent from the support matrix.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.80.1 implementation stop reached. Run pentest for this exact commit.`

### v0.80.2 — Generated Security Profile Bundles

Status: planned.

Goal: Make profile names executable, diffable policy rather than scattered configuration folklore.

Deliverables:

- Generated Personal, Standard, Hardened, Regulated, Clustered, and Air-gapped bundles; safe defaults; override authority/risk diff; conformance scenario mapping; upgrade compatibility; recovery path.

Verification:

- Golden bundle generation, profile-to-profile authority diffs, missing control, unsafe override, upgrade drift, default-install usability, and recovery scenarios pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Personal and Standard remain one-command approachable while advanced services and hardening are explicit opt-ins with visible consequences.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.80.2 implementation stop reached. Run pentest for this exact commit.`

### v0.80.3 — Privileged Support And Impersonation Sessions

Status: planned.

Goal: Allow tightly controlled support actions without hiding the real actor or granting ambient administrator impersonation.

Deliverables:

- Explicit request/approval/reason/ticket/purpose; actor/effective actor/executor attribution; scope/time/action limits; step-up; user notification/consent profile; visible banner; prohibited actions; immediate revoke; immutable audit/receipt and review report.

Verification:

- Self-approval, forged/stale approval, hidden actor, scope/tenant escalation, prohibited credential/payment/privacy action, session extension, cache confusion, revoke race, notification suppression, audit failure, and browser/API/CLI tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Impersonation is never anonymous, unlimited, or equivalent to the user's own authenticated session.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.80.3 implementation stop reached. Run pentest for this exact commit.`

## Phase 8 — Rendering, administration, editor, themes, and search

### v0.81.0 — Render Intermediate Representation

Status: planned.

Goal: Compile content and templates to a safe typed render plan.

Deliverables:

- Sink-neutral typed nodes, props, slots, escaping context, dependency records, bounded loops/queries, error boundaries, work budgets, and immutable render artifact manifest rooted in `ContentView` and release identity.

Verification:

- Context-confusion, unbounded render, missing value, unknown block, and deterministic-plan fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.81.0 implementation stop reached. Run pentest for this exact commit.`

### v0.82.0 — Contextual Escaping

Status: planned.

Goal: Provide first-party HTML, attribute, URL, CSS, and text escaping boundaries.

Deliverables:

- Separate output types, no implicit safe HTML, canonical policies, invalid scalar handling, and policy versioning.

Verification:

- XSS corpus, encoding confusion, malformed Unicode, double-escape, and unsafe-conversion compile tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.82.0 implementation stop reached. Run pentest for this exact commit.`

### v0.83.0 — HTML Parser And Sanitizer Admission

Status: planned.

Goal: Admit mature standards-aware parsing foundations for hostile legacy markup.

Deliverables:

- Exact reviewed HTML parser/sanitizer foundations and features; supported parsing algorithm; tree and token budgets; unsafe/native/build-script/transitive review; differential browser corpus; maintenance/CVE-response policy; Aetherheim-owned inert input/output types. Aetherheim does not implement a browser-grade HTML parser to avoid dependencies.

Verification:

- Official/browser differential corpus, mutation fuzzing, malformed/deep markup, foreign-content edges, encoding confusion, allocation exhaustion, feature drift, and platform tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.83.0 implementation stop reached. Run pentest for this exact commit.`

### v0.83.1 — Versioned Legacy Markup Sanitization Policy

Status: planned.

Goal: Convert explicitly authorized legacy HTML/SVG input to bounded inert safe-render data.

Deliverables:

- Versioned element/attribute/URL/namespace policy; CSS/SVG exclusion or handoff; provenance; permission and data-classification checks; inert fallback; policy-upgrade/resanitize plan; no public safe-string constructor.

Verification:

- XSS/browser corpus, URL and namespace tricks, mutation after validation, policy downgrade/upgrade, unknown elements, embedded resources, cross-tenant provenance, deterministic output, and resanitization tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Stored legacy markup remains untrusted source data; only policy-versioned typed output can enter Render IR.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.83.1 implementation stop reached. Run pentest for this exact commit.`

### v0.84.0 — Safe Template Compiler

Status: planned.

Goal: Compile declarative themes without arbitrary host code.

Deliverables:

- Grammar, typed variables, slots, components, bounded iteration/query blocks, inheritance, diagnostics, and canonical IR.

Verification:

- Parser mutations, resource exhaustion, missing props, escaping, inheritance cycles, and deterministic output pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.84.0 implementation stop reached. Run pentest for this exact commit.`

### v0.85.0 — Server Renderer

Status: planned.

Goal: Render deterministic public HTML from `ContentView` and typed Render IR.

Deliverables:

- Release-root render context; theme/template/runtime digest; dependency graph; streaming/output budgets; deterministic HTML/metadata; error boundaries; ETag/artifact manifest; cancellation; no cache dependency.

Verification:

- Content/theme/release substitution, missing/unknown blocks, output exhaustion, cancellation, partial stream, error fallback, deterministic cross-platform output, and browser parse fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.85.0 implementation stop reached. Run pentest for this exact commit.`

### v0.85.1 — Render And Page Cache

Status: planned.

Goal: Cache rendered artifacts with complete security partitioning and reconstructible state.

Deliverables:

- Canonical tenant/site/environment/host/route/locale/viewer/policy/release/theme keys; dependency tags; ETag/conditional responses; bounded local/Valkey storage; invalidation; stampede control; stale-public-only policy; cache diagnostics.

Verification:

- Tenant/locale/viewer/host/policy/release/theme mixing, collision, poisoning, stale private content, invalidation race, stampede, eviction, Valkey loss, renderer failure, and authoritative rebuild tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Cache loss changes performance only, and stale delivery is limited to explicitly public immutable release artifacts.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.85.1 implementation stop reached. Run pentest for this exact commit.`

### v0.86.0 — Administration Shell

Status: planned.

Goal: Deliver an accessible self-hosted management shell.

Deliverables:

- Setup/login shell, navigation, dashboard, health, content list, typed API client, CSP, keyboard baseline, and progressive disclosure.

Verification:

- Browser E2E, keyboard-only, CSP, origin isolation, session expiry, error recovery, and accessibility scripts pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.86.0 implementation stop reached. Run pentest for this exact commit.`

### v0.87.0 — Structured Block Editor

Status: planned.

Goal: Make clean structured authoring usable.

Deliverables:

- Insertion, selection, nested layout, schema controls, copy/paste, undo/redo, autosave, conflict UI, and keyboard commands.

Verification:

- Document round-trip, undo model, paste sanitisation, concurrency, keyboard, and accessibility suites pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.87.0 implementation stop reached. Run pentest for this exact commit.`

### v0.87.1 — Editor Collaboration Operation Layer

Status: planned.

Goal: Add realtime collaboration without making a CRDT or editor log the canonical content model.

Deliverables:

- Versioned collaboration-operation boundary; admitted algorithm/runtime decision; presence separation; bounded operation log; actor/tenant context; checkpoint-to-pure-document-transformation; disconnect/rebase/recovery semantics.

Verification:

- Concurrent edits, reordered/duplicated/lost operations, malicious operation payloads, stale permissions, tenant substitution, disconnect, compact/checkpoint, and final canonical document validation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Collaboration state can be discarded or rebuilt without changing canonical revision semantics, and no home-grown CRDT is admitted without its own dependency/design review.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.87.1 implementation stop reached. Run pentest for this exact commit.`

### v0.87.2 — Realtime Collaboration Transport

Status: planned.

Goal: Carry presence and bounded collaboration operations over authenticated cancellable realtime connections.

Deliverables:

- WebSocket or admitted equivalent transport; origin/session/tenant/document binding; connection/resume identity; sequence/ack/backpressure; message and rate budgets; presence privacy; permission-epoch revalidation; drain/reconnect; proxy compatibility and audit.

Verification:

- Cross-origin/tenant/document connection, stolen resume token, replay/reorder/gap, oversized/flooded messages, stale permission/session, slow consumer, node/proxy loss, reconnect, drain, presence leak, and malformed framing tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Realtime transport carries validated operations only and cannot become a second canonical or authorization path.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.87.2 implementation stop reached. Run pentest for this exact commit.`

### v0.88.0 — Design Tokens and Theme Contracts

Status: planned.

Goal: Separate design from executable authority.

Deliverables:

- Color, typography, spacing, breakpoint, mode, component variant, template, slot, asset, licence, and compatibility schemas.

Verification:

- Schema/golden tests, contrast warnings, cycle rejection, unknown token behavior, and deterministic invalidation pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.88.0 implementation stop reached. Run pentest for this exact commit.`

### v0.88.1 — Theme CSS, SVG, Font, And Asset Boundary

Status: planned.

Goal: Admit visual theme assets without granting script, network, parser, or cross-origin authority.

Deliverables:

- Versioned CSS subset/token output; URL/resource policy; SVG sanitization or rasterization boundary; font format/size/licence policy; immutable asset digests; CSP/integrity metadata; external-resource default deny; build and runtime budgets.

Verification:

- CSS exfiltration/import/url tricks, browser quirks, SVG script/event/foreign content, font bombs, path traversal, MIME confusion, substitution, external fetch, CSP weakening, licence omission, and cache tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A declarative theme cannot introduce executable script or undeclared network destinations through its visual assets.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.88.1 implementation stop reached. Run pentest for this exact commit.`

### v0.89.0 — Theme Packaging and Lifecycle

Status: planned.

Goal: Install and switch declarative themes safely.

Deliverables:

- Manifest, file allowlist, digest, signature-provider boundary, licence metadata, preview, activation, rollback, child overlay, and export.

Verification:

- Path traversal, substitution, incompatible manifest, failed activation, rollback, and content-preservation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.89.0 implementation stop reached. Run pentest for this exact commit.`

### v0.89.1 — Theme Authoring Toolchain

Status: planned.

Goal: Make safe themes pleasant to build without exposing escape hatches.

Deliverables:

- `aetherheim theme dev`; typed template/schema bindings; lint and diagnostics; fixture content; component gallery; accessibility checks; deterministic preview/screenshot contracts; package/migration/static-tier tooling; author-selected licence metadata.

Verification:

- Independent sample themes cover edit/preview/package/install/update/rollback, missing/unknown data, unsafe output attempts, keyboard/contrast checks, deterministic builds, and offline use.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A theme author can complete the documented loop without arbitrary host code or a “mark safe” API, and third-party theme licensing remains independent of EUPL-1.2.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.89.1 implementation stop reached. Run pentest for this exact commit.`

### v0.90.0 — Lexical Search and Discovery

Status: planned.

Goal: Provide permission-aware built-in search without an external service.

Deliverables:

- Portable indexing projection, locale analyzers, fields/weights, facets, snippets, rebuild/swap, freshness, and explain.

Verification:

- Draft/private deletion, field-policy, locale, stale snippet/facet, amplification, and rebuild-equivalence tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.90.0 implementation stop reached. Run pentest for this exact commit.`

### v0.90.1 — Search Rebuild And Freshness Recovery

Status: planned.

Goal: Prove search remains a derived projection through deletion, lag, corruption, and rebuild.

Deliverables:

- Freshness watermark; generation-rooted index; build/verify/swap; delete propagation; corrupt-projection quarantine; bounded lag policy; authoritative fallback/non-claim; operator receipts.

Verification:

- Delete-and-rebuild equivalence, stale draft/private data, permission/locale changes, failed swap, corrupt index, replay, node restart, amplification, and provider-loss scenarios pass without old-content leakage.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Search loss or corruption can reduce discovery availability but cannot restore deleted/forbidden content or become authoritative state.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.90.1 implementation stop reached. Run pentest for this exact commit.`

## Phase 9 — Media, extensions, packages, and component isolation

### v0.91.0 — Upload Leases and Quarantine

Status: planned.

Goal: Keep untrusted bytes private until admitted.

Deliverables:

- Resumable leases, quotas, digest, claimed/detected type, temporary encryption-provider boundary, quarantine states, and expiry.

Verification:

- Resume, truncation, substitution, quota race, public-path bypass, and cleanup crash tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.91.0 implementation stop reached. Run pentest for this exact commit.`

### v0.91.1 — Malware Scanning Provider Boundary

Status: planned.

Goal: Add optional defense-in-depth malware scanning without treating scanner output as structural validation or absolute safety.

Deliverables:

- Scanner/process/provider identity; signature/version freshness; bounded stream/file handoff; timeout/quota; clean/suspicious/malicious/error outcomes; quarantine retention; rescan policy; privacy/egress controls; operator override authority and explicit non-claim.

Verification:

- EICAR/synthetic fixtures, scanner outage/hang/crash, stale signatures, oversized/partial files, substitution/TOCTOU, archive bombs, false-positive override, privacy leakage, rescan, and audit scenarios pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A clean scan never bypasses type/structure/content validation, and scanner absence follows the configured fail-closed profile.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.91.1 implementation stop reached. Run pentest for this exact commit.`

### v0.92.0 — Media Probe And Metadata Tool Admission

Status: planned.

Goal: Admit mature isolated probing foundations before parsing hostile media metadata.

Deliverables:

- Exact reviewed probe/parser/process foundations and feature scope; supported container/metadata inventory; worker-only execution; unsafe/native/build-script/transitive review; input/output/time/memory budgets; filename normalization contract; CVE and tool-update response. Aetherheim does not build full media/document codecs or parsers.

Verification:

- Malformed public corpora, parser differential, type mismatch, deep/oversized metadata, decompression-shaped bombs, tool crash/hang, output spoof, allocation/resource failure, and platform tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.92.0 implementation stop reached. Run pentest for this exact commit.`

### v0.92.1 — Image Structure And Metadata Admission

Status: planned.

Goal: Extract bounded image structure and privacy-safe metadata through the isolated probe boundary.

Deliverables:

- Format/dimension/frame/orientation/color-profile scope; claimed/detected type; metadata allowlist; location/device metadata stripping policy; animated-image budgets; rejection/provenance report.

Verification:

- Malformed/polyglot/truncated images, dimension/frame bombs, type confusion, EXIF/location leakage, orientation/profile abuse, parser disagreement, crash, cancellation, and deterministic report tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Images remain quarantined until the exact bytes receive a successful bounded structural report.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.92.1 implementation stop reached. Run pentest for this exact commit.`

### v0.92.2 — Document And Archive Structure Admission

Status: planned.

Goal: Inspect supported documents and archives without extraction or parser authority escaping quarantine.

Deliverables:

- PDF/office/document/archive scope; page/member/depth/expanded-size and compression-ratio limits; encrypted/macro/active-content policy; safe member names; nested-container policy; rejection/provenance report.

Verification:

- Malformed/polyglot/encrypted/macro documents, zip slips, symlink/device entries, nested and decompression bombs, duplicate names, parser crash/hang, partial output, cancellation, and privacy metadata tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Archive/document admission never writes attacker-selected paths or enables active content, and unsupported formats remain quarantined.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.92.2 implementation stop reached. Run pentest for this exact commit.`

### v0.92.3 — Audio And Video Structure Admission

Status: planned.

Goal: Extract bounded audiovisual structure without decoding in the application process.

Deliverables:

- Supported container/codec metadata; duration/track/chapter/subtitle/frame-rate/dimension limits; claimed/detected type; embedded attachment and metadata policy; rejection/provenance report.

Verification:

- Malformed/polyglot/truncated containers, extreme duration/rate/dimensions/tracks, attachment abuse, metadata leakage, parser crash/hang, cancellation, timeout, and cross-tool disagreement tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Audio/video bytes remain private until their exact structure and declared processing path are admitted.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.92.3 implementation stop reached. Run pentest for this exact commit.`

### v0.93.0 — Isolated Media Workers

Status: planned.

Goal: Contain native or external processor compromise.

Deliverables:

- Worker protocol, process identity, sandbox profile, input/output handles, budgets, cancellation, validation, and no secret/network inheritance.

Verification:

- Crash, hang, output spoof, path escape, resource exhaustion, and compromised-worker simulations pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.93.0 implementation stop reached. Run pentest for this exact commit.`

### v0.94.0 — Image Derivative Pipeline

Status: planned.

Goal: Create immutable policy-bound image renditions.

Deliverables:

- Orientation, resize/crop intent, focal point, format contract, processor version, output digest, metadata privacy, and retry.

Verification:

- Malformed image fixtures, cache collisions, deterministic recipe identity, failed output validation, and original preservation pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.94.0 implementation stop reached. Run pentest for this exact commit.`

### v0.94.1 — Audio And Video Derivative Pipeline

Status: planned.

Goal: Produce bounded immutable audiovisual renditions through isolated admitted processors.

Deliverables:

- Transcode/package recipe identity; codec/container/profile allowlist; duration/resolution/bitrate limits; thumbnails/waveforms/subtitle handling; cancellation/progress; output revalidation; digest/provenance; metadata privacy.

Verification:

- Malformed inputs, processor crash/hang, resource exhaustion, recipe collision, truncated/spoofed output, subtitle injection, metadata leak, retry/cancel, deterministic identity, and original-preservation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every audiovisual output is immutable, revalidated, recipe/version identified, and never trusted merely because a processor exited successfully.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.94.1 implementation stop reached. Run pentest for this exact commit.`

### v0.94.2 — Document Preview And Safe Download Pipeline

Status: planned.

Goal: Generate inert document previews while preserving safe original-download policy.

Deliverables:

- Page/text/thumbnail preview recipes; active-content stripping or rejection; isolated conversion; output revalidation; preview limits; original-download disposition/type/nosniff policy; provenance and accessibility extraction hints.

Verification:

- Malformed/active/encrypted documents, converter crash/hang, script-bearing output, MIME sniffing, content-disposition injection, partial preview, resource exhaustion, retry, and original-preservation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Browser-facing previews are inert validated derivatives; original downloads cannot execute inline by accidental content sniffing.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.94.2 implementation stop reached. Run pentest for this exact commit.`

### v0.95.0 — Asset Metadata And Accessibility

Status: planned.

Goal: Make assets discoverable and accessible without combining rights and deletion authority.

Deliverables:

- Localized title/alt/caption/transcript; language/direction; classification; collections/tags; focal point; derivative inventory; accessibility completeness and fallback; editorial provenance.

Verification:

- Locale fallback/required translation, missing/invalid alternatives, transcript/caption association, classification inheritance, derivative mismatch, search visibility, replacement preview, and accessibility policy tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.95.0 implementation stop reached. Run pentest for this exact commit.`

### v0.95.1 — Asset Rights, Consent, And Expiry

Status: planned.

Goal: Prevent publication beyond declared licence, attribution, consent, territory, or time constraints.

Deliverables:

- Licence/attribution/source; consent/model/property releases; territory/channel/time constraints; expiry and renewal; legal hold; policy obligations; publication/search/render enforcement and evidence.

Verification:

- Missing/expired/revoked consent or licence, territory/channel mismatch, stale cache/search/render, renewal race, derivative propagation, hold conflict, import provenance, and override approval tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Rights and consent obligations follow every derivative and block new publication when invalid.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.95.1 implementation stop reached. Run pentest for this exact commit.`

### v0.95.2 — Asset Usage, Replacement, And Lifecycle

Status: planned.

Goal: Make asset replacement and deletion complete, explainable, and recoverable.

Deliverables:

- Complete usage graph; published/draft/theme/plugin/form/commerce references; replacement/relink plan; soft-delete/purge/hold; derivative cleanup; archive/export; stale-projection repair; operation receipt.

Verification:

- Hidden/stale/missing references, concurrent publish/replacement, partial relink, delete/hold conflict, derivative/cache/search cleanup, restore, archive round-trip, and cross-provider migration tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Purge cannot proceed without a complete current usage decision, and partial replacement remains recoverable.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.95.2 implementation stop reached. Run pentest for this exact commit.`

### v0.95.3 — Media Delivery And CDN Boundary

Status: planned.

Goal: Serve admitted originals and derivatives safely through direct or optional CDN/object delivery.

Deliverables:

- Immutable URL/version model; authorization/viewer/tenant context; range/conditional requests; content type/disposition/nosniff; signed short-lived delivery permits; CDN cache/invalidation policy; private-origin and hotlink policy; download budgets and audit.

Verification:

- Cross-tenant/private asset access, token replay/audience/expiry, path/type/disposition injection, range amplification, stale CDN after revoke/delete/rights expiry, cache mixing, origin bypass, and direct/CDN equivalence tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Delivery never turns blob possession or a guessable URL into authority, and CDN state remains revocable derived state.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.95.3 implementation stop reached. Run pentest for this exact commit.`

### v0.96.0 — Plugin and Theme Package Manifest

Status: planned.

Goal: Define ecosystem packages before executable loading.

Deliverables:

- Identity, publisher, version, compatibility, licence, capabilities, resources, schemas, migrations, data classes, SBOM/provenance references, and exports.

Verification:

- Malformed, ambiguous, oversized, unknown-required, licence-missing, and permission-diff fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.96.0 implementation stop reached. Run pentest for this exact commit.`

### v0.96.1 — Versioned WIT Worlds And Plugin ABI

Status: planned.

Goal: Freeze extension types and imports before choosing or instantiating a runtime.

Deliverables:

- Versioned Component Model WIT worlds; canonical scalar/error/resource/event/proposal types; generated bindings; compatibility and feature negotiation; no imports by default; explicit prohibition of ambient WASI filesystem, environment, socket, clock, and randomness.

Verification:

- Reproducible binding generation, old/new host and guest fixtures, unknown-required feature failures, type confusion, malformed strings/lists/resources, and import inventory tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Host/runtime/SDK implementations consume the same reviewed WIT artifacts and cannot add ambient imports privately.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.96.1 implementation stop reached. Run pentest for this exact commit.`

### v0.97.0 — Capability Broker

Status: planned.

Goal: Make extension authority narrow and parameterised.

Deliverables:

- Content/media/job/http/secret/mail/render/admin capabilities; actor delegation; grant/revoke epochs; audit; deny ambient authority.

Verification:

- Privilege broadening, confused deputy, cross-tenant, stale grant, delegation, and default-deny model tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.97.0 implementation stop reached. Run pentest for this exact commit.`

### v0.97.1 — Typed Extension Events And Interceptors

Status: planned.

Goal: Replace ambient global hooks with ordered typed and bounded extension points.

Deliverables:

- Typed event subscriptions; pure pre-commit proposal/validation interceptors; post-commit notification rules; deterministic ordering; per-handler budgets; reentrancy ban; failure/timeout policy; extension contribution manifest.

Verification:

- Ordering, timeout, trap, replay, stale grants, recursive invocation, conflicting proposals, committed-event failure, tenant context, and uninstall/update scenarios pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A post-commit extension failure cannot make a committed operation uncommitted, and no hook bypasses normal policy or validation.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.97.1 implementation stop reached. Run pentest for this exact commit.`

### v0.98.0 — Runtime Admission And Component Validation

Status: planned.

Goal: Admit mature standards tooling and reject malformed or unsupported components before execution.

Deliverables:

- Exact-pinned mature Component Model runtime/tooling review; minimal feature graph; platform/unsafe/CVE/maintenance response; Aetherheim package and manifest limits; standards validator invocation; import/export/feature/resource allowlists; compatibility report. Aetherheim does not implement a WebAssembly parser.

Verification:

- Official/mutated components, parser differential fixtures, deep/large sections, unsupported proposals, unknown-required features, forbidden imports, platform matrix, and known-vulnerability response rehearsal pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The chosen runtime/tooling is user-approved through the dependency gate; if no maintained secure candidate meets the contract, executable plugins remain unsupported.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.98.0 implementation stop reached. Run pentest for this exact commit.`

### v0.99.0 — Admitted Component Runtime Integration

Status: planned.

Goal: Instantiate the empty WIT world through the admitted mature runtime behind an Aetherheim-owned adapter.

Deliverables:

- Runtime engine/store/instance adapter; empty-world linking; no ambient WASI; typed value/resource crossing; trap isolation; cancellation; per-invocation identity; clean teardown; optional hardened out-of-process host design. No custom interpreter, compiler, JIT, or execution engine.

Verification:

- Runtime conformance vectors, empty-world import proof, memory/table isolation, trap/cancel/host survival, teardown/leak, repeated-instantiation, version/platform, and optional process-boundary tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.99.0 implementation stop reached. Run pentest for this exact commit.`

### v0.100.0 — Component Handles And Proposal Host Calls

Status: planned.

Goal: Expose only typed capability-checked in-process proposal operations.

Deliverables:

- Unguessable invocation-scoped typed handle table carrying tenant, actor, grant epoch, and expiry; content/media/render/job proposals; bounded guest-memory copies; output validation; namespaced state proposals; no retained guest pointers, reentrant calls, or host network waits inside authoritative transactions.

Verification:

- Forged handle, stale grant, reentrancy, quota, timeout, proposal substitution, and host-crash containment tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.100.0 implementation stop reached. Run pentest for this exact commit.`

### v0.100.1 — Brokered External Operations

Status: planned.

Goal: Expose network, mail, and secret use as named least-authority operations rather than raw sockets or values.

Deliverables:

- Named outbound HTTP/mail/secret operations; destination/method/header/body/response policy; DNS and redirect handling; private/metadata address denial; data-classification egress checks; secret operation handles; audit and cancellation.

Verification:

- SSRF, DNS rebinding, redirect-to-private, proxy confusion, header smuggling, body amplification, secret disclosure, stale grants, cancellation, quota, and cross-tenant operation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Plugins receive neither raw sockets nor general secret plaintext, and all external effects remain idempotent/reconcilable application operations.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.100.1 implementation stop reached. Run pentest for this exact commit.`

### v0.100.2 — Component Resource Governance

Status: planned.

Goal: Bound every guest and host resource independently and recover cleanly after exhaustion.

Deliverables:

- Fuel and deadline epochs; memory/table/stack/call-depth; host-call, copy/output, storage, HTTP, concurrency, log, and job budgets; fair scheduling; cancellation and instance quarantine policy; metrics without guest-secret leakage.

Verification:

- Infinite loops, memory/table growth, recursion, host-call storms, oversized copies/results, concurrent starvation, cancellation races, trap storms, leaked handles, noisy logs, and restart/recovery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every executable extension resource has a measured limit, denial behavior, operator signal, and recovery scenario.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.100.2 implementation stop reached. Run pentest for this exact commit.`

## Phase 10 — Extension lifecycle, multilingual, multisite, and publishing modules

### v0.101.0 — Extension State and Migrations

Status: planned.

Goal: Keep plugin state portable and recoverable.

Deliverables:

- Namespaced records/blobs/config, quotas, typed migrations, staging, checkpoints, AHAF export/import, retain/export/purge uninstall modes.

Verification:

- Cross-plugin isolation, failed migration, rollback, downgrade, quota, and archive round-trip tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.101.0 implementation stop reached. Run pentest for this exact commit.`

### v0.102.0 — Extension UI Isolation

Status: planned.

Goal: Prevent plugin frontend code from inheriting admin authority.

Deliverables:

- Declarative panels; isolated-origin advanced panels; short-lived audience tokens; postMessage schemas; CSP and integrity metadata.

Verification:

- Cookie access, origin confusion, token audience, message spoof, CSP weakening, and revoked-panel tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.102.0 implementation stop reached. Run pentest for this exact commit.`

### v0.103.0 — Extension Package Verification

Status: planned.

Goal: Admit packages through explicit trust policy.

Deliverables:

- Content digest, publisher/provider signature boundary, provenance/SBOM links, revocation, allow/deny lists, offline bundles, and transparency metadata interface.

Verification:

- Tamper, substitution, revoked key/package, stale metadata, offline trust-root, and rollback tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.103.0 implementation stop reached. Run pentest for this exact commit.`

### v0.103.1 — Extension Registry, Update, And Offline Trust

Status: planned.

Goal: Discover and update ecosystem packages without turning a registry or network into installation authority.

Deliverables:

- Signed registry/update metadata; publisher/package/version identity; freeze/rollback protection; mirrors; revocation/compromise; package lock; staged download; offline/air-gapped bundles; trust-root rotation and operator policy.

Verification:

- Registry/mirror substitution, stale/freeze/rollback metadata, revoked key/package, publisher takeover, partial download, lock drift, offline expiry/rotation, compromise response, and prior-version recovery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Registry metadata can propose bytes only; local verification and explicit policy approval remain authoritative.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.103.1 implementation stop reached. Run pentest for this exact commit.`

### v0.104.0 — Extension Activation and Rollback

Status: planned.

Goal: Make lifecycle changes atomic and observable.

Deliverables:

- Discover/fetch/verify/inspect/approve/stage/activate/observe/upgrade/rollback/disable/purge state machine and prior-version retention.

Verification:

- Failure at every transition leaves one coherent active state; permission increases require fresh approval.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.104.0 implementation stop reached. Run pentest for this exact commit.`

### v0.105.0 — Extension SDK and Conformance

Status: planned.

Goal: Give developers safe bindings without publishing crates.

Deliverables:

- In-repository SDK sources/templates, host simulator, capability mocks, deterministic clock/random, fixture site, package builder, and conformance runner.

Verification:

- Independent sample components, malicious fixtures, compatibility matrix, and generated-binding reproducibility pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.105.0 implementation stop reached. Run pentest for this exact commit.`

### v0.105.1 — One-Command Extension Development Loop

Status: planned.

Goal: Make secure extension development approachable without requiring a production database, cache, cluster, or secret service.

Deliverables:

- `aetherheim dev`; ephemeral local site; deterministic clock/random/network fixtures; capability simulator; event trace; package inspect/diff/sign flow; sample and malicious extensions for every supported guest language; offline documentation.

Verification:

- A clean machine can build, run, inspect, test, package, upgrade, roll back, and remove each sample; denied capability, trap, quota, state migration, permission increase, and offline scenarios fail predictably.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The default author loop needs only the documented local toolchain, while optional advanced services remain explicit profile additions.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.105.1 implementation stop reached. Run pentest for this exact commit.`

### v0.105.2 — Guest Language SDK Qualification Framework

Status: planned.

Goal: Let each selected guest language earn support independently from the WIT contract and runtime.

Deliverables:

- Language/toolchain selection criteria; exact compiler/bindgen/package-builder versions; generated binding adapter; deterministic/offline build policy; minimal/malicious sample suite; support matrix; insertion rule requiring a separate patch milestone per future language.

Verification:

- A deliberately incompatible toolchain, stale bindings, nondeterministic package, hidden network fetch, unsupported WIT feature, malformed output, trap, quota, and capability denial fail predictably.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No guest language is called supported merely because a generator can emit code; each language gets its own later qualification stop and live sample evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.105.2 implementation stop reached. Run pentest for this exact commit.`

### v0.106.0 — Locale and Fallback Core

Status: planned.

Goal: Make multilingual content a first-party domain feature.

Deliverables:

- BCP-47-shaped validated tags, direction/script, invariant versus translated fields, explicit field fallback, formatting-provider boundary, and completeness.

Verification:

- Fallback never bypasses visibility or required translation; malformed tags and loops fail.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.106.0 implementation stop reached. Run pentest for this exact commit.`

### v0.106.1 — Unified Locale Context

Status: planned.

Goal: Carry one validated locale/fallback context through content, routing, rendering, search, API, cache, and extensions.

Deliverables:

- Source/requested/effective BCP-47 tag; script/direction; formatting provider version; bounded acyclic fallback graph; required-translation and visibility constraints; context propagation and cache-key form.

Verification:

- Malformed tags, fallback loops, script/direction mismatch, missing formatting data, stale translation, visibility/required-translation bypass, search/render/API disagreement, and cache omission tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No adapter independently invents locale fallback, formatting, direction, or cache dimensions.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.106.1 implementation stop reached. Run pentest for this exact commit.`

### v0.107.0 — Translated Revisions and Provenance

Status: planned.

Goal: Tie translations to exact sources and methods.

Deliverables:

- Source revision, translator/reviewer, human/AI/import state, glossary/memory references, locale media/slug, policy, and stale-source edges.

Verification:

- Source changes mark dependents stale; AI cannot claim human-only; approval is revision-specific.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.107.0 implementation stop reached. Run pentest for this exact commit.`

### v0.108.0 — Locale Routes and Domains

Status: planned.

Goal: Publish correct language domains, paths, metadata, and caches.

Deliverables:

- Verified host mapping, locale slugs, canonical/hreflang, redirects, navigation, sitemap/feed, search, and cache dimensions.

Verification:

- Host spoofing, redirect loop, mixed-locale cache, wrong canonical, and sitemap leakage tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.108.0 implementation stop reached. Run pentest for this exact commit.`

### v0.109.0 — Multisite and Agency Networks

Status: planned.

Goal: Support many sites without weakening isolation.

Deliverables:

- Network/site templates, delegated admins, optional shared users/themes/assets, domain lifecycle, quotas, per-site export/delete, and policy inheritance.

Verification:

- Tenant/site isolation, shared-resource revocation, delegated scope, domain takeover, and per-site archive tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.109.0 implementation stop reached. Run pentest for this exact commit.`

### v0.110.0 — Forms and Consent

Status: planned.

Goal: Provide typed public forms with safe data handling.

Deliverables:

- Builder, validation, branching, quarantine uploads, anti-abuse hooks, consent notice/version, encrypted-field provider boundary, workflow, retention, and export.

Verification:

- Injection, spam budget, sensitive log/cache/search exclusion, consent withdrawal, file bypass, and deletion tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.110.0 implementation stop reached. Run pentest for this exact commit.`

## Phase 11 — Growth modules and commerce

### v0.111.0 — Contacts And Organisations

Status: planned.

Goal: Add privacy-aware contact and organisation records without an implicit marketing audience.

Deliverables:

- Contacts; organisations and membership; source/provenance; purpose/consent/classification; verified communication points; duplicate candidates/merge; activity references; import/export; retention and deletion propagation.

Verification:

- Cross-tenant access, merge/unmerge, identity collision, stale consent/purpose, duplicate resolution, communication verification, import provenance, retention/deletion, and sensitive-field tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.111.0 implementation stop reached. Run pentest for this exact commit.`

### v0.111.1 — Segments And Audience Snapshots

Status: planned.

Goal: Build explainable bounded segments without allowing query or cache state to override consent.

Deliverables:

- Typed segment rules; query-cost budgets; tenant/purpose/channel/consent filters; dynamic preview; immutable audience snapshot root; exclusion/suppression linkage; staleness and rebuild; explanation and export controls.

Verification:

- Query amplification, consent/purpose race, cross-tenant/field leakage, stale segment/cache, exclusion bypass, concurrent contact change, snapshot replay, deletion, and rebuild-equivalence tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A segment match is never sufficient delivery authority; each snapshot remains bound to current consent and suppression checks.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.111.1 implementation stop reached. Run pentest for this exact commit.`

### v0.112.0 — Transactional Mail Composition And Delivery

Status: planned.

Goal: Send application mail through bounded provider contracts.

Deliverables:

- Typed template and text alternative; recipient source/purpose; header/address policy; provider identity and secret operation; idempotent outbox delivery; bounded body/attachments; rate, redaction, and delivery receipt.

Verification:

- Header/address/template injection, unsafe links/content, duplicate send, wrong recipient/tenant, oversized attachment, provider timeout/ambiguity, retry, rate, and secret logging tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.112.0 implementation stop reached. Run pentest for this exact commit.`

### v0.112.1 — Mail Suppression, Bounce, And Complaint Lifecycle

Status: planned.

Goal: Process provider feedback without allowing untrusted callbacks to corrupt contact or consent authority.

Deliverables:

- Signed/polled provider event boundary; durable receipt; bounce/complaint normalization; suppression scope/reason/expiry; manual review; consent/contact linkage; replay/reconciliation; privacy retention and audit.

Verification:

- Forged/replayed/out-of-order feedback, wrong recipient/tenant, provider mismatch, duplicate suppression, transient/permanent bounce, complaint race, unsuppress approval, deletion, and reconciliation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Provider feedback is evidence, not direct authority, and suppression checks remain mandatory at send time.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.112.1 implementation stop reached. Run pentest for this exact commit.`

### v0.112.2 — Mail Domain Authentication And Deliverability

Status: planned.

Goal: Bind sender domains and signing/configuration evidence before production mail is claimed.

Deliverables:

- Sender-domain ownership; SPF/DKIM/DMARC-oriented configuration checks; DKIM signing-provider/key lifecycle; envelope/header alignment; return-path policy; provider/IP identity; TLS policy; reputation/rate guidance; verification, rotation, revoke, and operator diagnostics.

Verification:

- Unverified/dangling domain, forged From/return path, DKIM key mismatch/rotation/revocation, alignment failure, DNS staleness, provider substitution, header injection, TLS downgrade, rate/reputation event, and failover tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Production profiles cannot send from an unverified domain or silently continue with invalid signing/authentication configuration.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.112.2 implementation stop reached. Run pentest for this exact commit.`

### v0.113.0 — Newsletters and Campaigns

Status: planned.

Goal: Add consent-authoritative bulk publishing.

Deliverables:

- Audience snapshot root, schedule/timezone, campaign approval, unsubscribe, complaint, web archive, tracking policy, and delivery receipts.

Verification:

- Consent/suppression races, retry duplication, DST scheduling, audience drift, and privacy-default tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.113.0 implementation stop reached. Run pentest for this exact commit.`

### v0.114.0 — Memberships And Entitlements

Status: planned.

Goal: Provide membership tiers and protected-content entitlements.

Deliverables:

- Tiers; invitations; profile/privacy policy; content entitlements; grant/source/expiry; grace/downgrade/cancel; payment/refund linkage; cache/API/render/search enforcement; export/deletion.

Verification:

- Cache/API/render/search entitlement isolation, invite replay, downgrade/expiry/refund, grace abuse, cross-tenant access, pseudonym privacy, concurrent lifecycle, export, and deletion tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.114.0 implementation stop reached. Run pentest for this exact commit.`

### v0.114.1 — Comments And Moderation

Status: planned.

Goal: Add threaded community discussion through an independently moderated lifecycle.

Deliverables:

- Comment/revision/thread model; identity/pseudonym policy; edit window; moderation states/queues; spam provider boundary; reports, sanctions, appeals, notifications; retention/erasure and audit.

Verification:

- Stored XSS/URL abuse, cross-content/tenant posting, thread depth/amplification, edit/moderation replay, sanction bypass, moderator conflict, spam outage, notification leakage, pseudonym erasure, and audit tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Comment authority and moderation state remain separate from membership entitlements and canonical editorial content.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.114.1 implementation stop reached. Run pentest for this exact commit.`

### v0.115.0 — Durable Automation

Status: planned.

Goal: Add bounded event-driven workflows without granting ambient extension authority.

Deliverables:

- Typed trigger/condition/action graph; actor/effective actor and capabilities; deterministic execution; loop/work/depth budgets; durable checkpoints; idempotency; dry run; approval; pause/cancel/retry/dead-letter; audit and explanation.

Verification:

- Loop/amplification, replay, duplicate/out-of-order events, stale permission, partial effect, crash/resume, approval/revocation, cancellation, poison action, tenant scope, and explanation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.115.0 implementation stop reached. Run pentest for this exact commit.`

### v0.115.1 — Bookings And Capacity

Status: planned.

Goal: Add time-zone-aware reservations with atomic capacity protection.

Deliverables:

- Services/resources/locations; availability and blackout rules; capacity/party size; hold/confirm/cancel/no-show states; waitlist; recurrence; timezone/DST policy; reminders; payment/deposit proposal; privacy/retention.

Verification:

- Concurrent overbooking, duplicate/replayed request, hold expiry, DST/gap/fold, recurrence changes, resource conflict, waitlist race, cancel/payment race, reminder duplication, provider outage, and privacy tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Capacity changes are atomic authoritative operations and automation/reminders cannot create bookings directly.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.115.1 implementation stop reached. Run pentest for this exact commit.`

### v0.115.2 — Privacy-Preserving First-Party Analytics

Status: planned.

Goal: Measure published experiences without making tracking or raw event retention the default.

Deliverables:

- Versioned bounded event schema; tenant/site/release/route context; consent and do-not-track policy; pseudonymous/session-free default; classification; cardinality and sampling budgets; retention/aggregation; bot/internal exclusion; delete propagation; export and non-claim.

Verification:

- Cross-tenant identity, fingerprinting fields, consent withdrawal, event replay/spoof, cardinality/amplification, cache/proxy context, deletion, raw-event expiry, aggregation correctness, and no-tracking-default tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Personal and Standard profiles collect no unnecessary cross-site identity, and analytics never becomes content, consent, billing, or authorization authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.115.2 implementation stop reached. Run pentest for this exact commit.`

### v0.115.3 — Optional AI Provider And Data-Egress Boundary

Status: planned.

Goal: Admit optional AI providers without ambient data access, hidden training consent, or publication authority.

Deliverables:

- Disabled-by-default provider contract; named operations/models/versions; tenant/site/user enablement; source and field authorization; data-classification/region/retention/training policy; prompt/output/token/time budgets; secret handles; redaction; provenance; cancellation and outage behavior.

Verification:

- Unauthorized source/field retrieval, cross-tenant prompt context, prompt injection, secret/personal data egress, provider retention/training mismatch, model substitution, oversized output/cost, cancellation, outage, log leakage, and disabled-profile tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No AI provider receives data or network authority outside one explicit classified operation, and absence leaves all normal CMS behavior usable.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.115.3 implementation stop reached. Run pentest for this exact commit.`

### v0.115.4 — AI-Assisted Authoring Proposals

Status: planned.

Goal: Offer draft, translation, metadata, and accessibility suggestions as reviewable non-authoritative proposals.

Deliverables:

- Proposal types for text, summary, metadata, alt text, taxonomy, and translation; exact source/revision/model/prompt-policy roots; human review/edit/reject; stale-source invalidation; attribution and explanation; normal validation/policy/workflow handoff.

Verification:

- False/unsafe output, prompt injection, source update, attribution confusion, human-only policy, locale/rights mismatch, repeated proposal, rejection retention, workflow bypass, direct publication attempt, and rollback tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- AI output cannot become canonical or public without the same human/policy/schema/workflow checks as manually authored content.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.115.4 implementation stop reached. Run pentest for this exact commit.`

### v0.115.5 — AI Live Safety And Cost Matrix

Status: planned.

Goal: Qualify enabled AI operations against exact provider/model profiles and real abuse/failure cases.

Deliverables:

- Provider/model/version/region/retention matrix; sandbox accounts; egress recorder; cost/token budgets; prompt-injection and leakage corpus; provenance fixtures; outage/model-change runbook; acceptance profile.

Verification:

- Live providers/models pass authorization, classification, region/retention, injection, leakage, cost, cancellation, model drift, outage, stale-source, review, rejection, and no-direct-publication journeys; absent providers fail enabled profiles.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No AI provider/model is supported from mocks alone, and every reference profile remains valid with AI entirely disabled.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.115.5 implementation stop reached. Run pentest for this exact commit.`

### v0.116.0 — Product Catalogue

Status: planned.

Goal: Create content-backed products, variants, and channel publication independently from pricing.

Deliverables:

- Products; variants/options; SKU and external-reference uniqueness; bundles/kits intent; channel/site/locale visibility; media/content relationships; catalogue revisions/publication; import/export and archive behavior.

Verification:

- SKU/reference uniqueness, invalid variant combinations, bundle cycles, cross-tenant/channel/locale visibility, concurrent revision/publication, deletion/reference, archive, and migration tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.116.0 implementation stop reached. Run pentest for this exact commit.`

### v0.116.1 — Price Books And Price Explanations

Status: planned.

Goal: Define exact versioned prices by channel, market, customer class, quantity, and time.

Deliverables:

- Price-book identity/version; product/variant/channel/market/customer/quantity rules; currency/scale; validity window; priority/conflict policy; immutable price components and explanation root; publication and rollback.

Verification:

- Overlap/conflict, stale/expired/future price, channel/customer/quantity mismatch, decimal/rounding/overflow, concurrent publication, replay, rollback, cache, and deterministic explanation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every quoted base price resolves to one immutable versioned explanation; product content cannot carry ambient mutable price authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.116.1 implementation stop reached. Run pentest for this exact commit.`

### v0.116.2 — Promotions And Coupons

Status: planned.

Goal: Add bounded promotion logic without making prices mutable or inexplicable.

Deliverables:

- Eligibility, audience/channel, schedule, usage budget, stacking/exclusion, line/order allocation, coupon secrecy/lookup policy, immutable explanation components, and revocation.

Verification:

- Stacking cycles, concurrent use limits, timezone edges, replay, stale eligibility, coupon guessing, allocation rounding, refund allocation, and deterministic explanation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every discount in an accepted quote is reproducible from immutable versioned inputs and checked arithmetic.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.116.2 implementation stop reached. Run pentest for this exact commit.`

### v0.116.3 — Tax Rules And Quote Boundary

Status: planned.

Goal: Model tax deterministically while treating external tax advice as untrusted input.

Deliverables:

- Jurisdiction and category references; inclusive/exclusive policy; line/order rounding; exemption/reverse-charge evidence; versioned tax-rule and external quote contracts; staleness and provenance.

Verification:

- Jurisdiction/category changes, inclusive/exclusive totals, line-versus-order rounding, exempt/reverse-charge, stale/malformed/failed provider quote, retry, and replay fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Accepted tax amounts are immutable calculation components and no connector can directly mutate an order or journal.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.116.3 implementation stop reached. Run pentest for this exact commit.`

### v0.116.4 — Currency And Exchange-Rate Policy

Status: planned.

Goal: Make multi-currency conversion explicit, versioned, and exact.

Deliverables:

- Currency metadata/scale; rate numerator/denominator and source snapshot; stale/triangulation policy; rounding and residual allocation; display versus settlement currency; provenance.

Verification:

- Unsupported/changed scales, stale rates, inverse/triangulated conversions, overflow, repeated conversion, residual allocation, and cross-currency replay tests prove no floating-point path exists.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every converted amount identifies the exact rate, source, time, policy, and rounding decision used.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.116.4 implementation stop reached. Run pentest for this exact commit.`

### v0.117.0 — Cart Lifecycle And Security

Status: planned.

Goal: Build secure guest/member carts independently of checkout providers.

Deliverables:

- Guest/member carts; unguessable hashed guest token; ownership transfer and merge; line intents; price/promotion explanation; optimistic revision; expiry; privacy/classification; bounded size; reservation proposal.

Verification:

- Token theft/fixation/guessing, cross-tenant access, merge amplification, concurrent changes, stale price, expiry, quota, privacy, and reservation-proposal tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.117.0 implementation stop reached. Run pentest for this exact commit.`

### v0.117.1 — Checkout Quote State Machine

Status: planned.

Goal: Turn a cart into one immutable accepted quote through an idempotent accessible flow.

Deliverables:

- Checkout state machine; bounded address/contact; shipping/tax composition; authoritative server total; quote/revision/expiry root; reservation link; duplicate-submit protection; explicit consent and accessibility behavior.

Verification:

- Client-total tampering, stale cart/price/tax/shipping, duplicate and concurrent submit, partial provider failure, timeout ambiguity, address privacy, keyboard, screen-reader, and resume tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- An order can be created only from the exact still-valid accepted quote root, never client-calculated totals.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.117.1 implementation stop reached. Run pentest for this exact commit.`

### v0.118.0 — Order State Machine

Status: planned.

Goal: Make accepted orders immutable at creation and explicit in every later transition.

Deliverables:

- Order identity and state machine; accepted quote/calculation snapshot; customer/address/shipping/tax references; line and entitlement intents; expected revision; reason/approval; transition event and audit contract.

Verification:

- Model checking covers retry, duplicate creation, partial failure, illegal transition, attempted repricing, stale revision, concurrent commands, cancellation, and immutable snapshot behavior.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.118.0 implementation stop reached. Run pentest for this exact commit.`

### v0.118.1 — Balanced Monetary Journal

Status: planned.

Goal: Represent every financial change as append-only balanced entries by currency.

Deliverables:

- Accounts and entry groups; debit/credit direction; currency balance; payment/refund/tax/shipping/discount/store-credit components; adjustments as compensating entries; reason/approval; immutable source linkage.

Verification:

- Property and model tests reject imbalance, mixed-currency groups, overflow, duplicate source, mutation/deletion, partial append, replay, and compensation that does not restore the declared position.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No commerce command overwrites a posted monetary fact; corrections are explicit balanced entries.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.118.1 implementation stop reached. Run pentest for this exact commit.`

### v0.119.0 — Inventory Ledger And Locations

Status: planned.

Goal: Represent physical stock movements and locations as append-oriented authoritative facts.

Deliverables:

- Locations/zones; item/SKU stock identity; receive/adjust/transfer/allocate/ship/return/damage movements; on-hand/allocated/damaged derived balances; reason/source/idempotency; append-only revisions; permissions and audit.

Verification:

- Balanced movement/property tests cover duplicate/replay, concurrent receive/transfer/allocate, negative/overflow, stale revision, cross-location/tenant, damaged disposition, immutable history, crash, and audit behavior.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.119.0 implementation stop reached. Run pentest for this exact commit.`

### v0.119.1 — Inventory Reservations And Availability

Status: planned.

Goal: Protect available stock through atomic expiring reservations under checkout concurrency.

Deliverables:

- Available-to-promise calculation; reservation/renew/release/consume state machine; expiry and database-time policy; bundle component allocation; backorder/oversell policy; lock/order/fencing semantics; order/quote binding and idempotency.

Verification:

- Linearizable concurrent checkout, expiry/renew/consume races, crash/replay, stale worker, bundle contention, partial allocation, backorder/oversell profiles, cancel/order race, and every qualified database history pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Oversell occurs only under an explicit documented policy; otherwise concurrent accepted reservations cannot exceed available stock.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.119.1 implementation stop reached. Run pentest for this exact commit.`

### v0.119.2 — Inventory Reconciliation And Cycle Counts

Status: planned.

Goal: Detect and correct discrepancies without rewriting inventory history.

Deliverables:

- Count sessions/snapshots; expected versus observed; variance approval; compensating movements; external warehouse/provider comparison; damaged/lost disposition; audit/evidence; scheduling and operator reports.

Verification:

- Concurrent movement during count, duplicate/partial count, stale snapshot, provider mismatch/outage, approval conflict, compensation replay, cross-location/tenant, crash/resume, and final balance/history tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Reconciliation preserves original movements and records every approved correction as a new append-only fact.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.119.2 implementation stop reached. Run pentest for this exact commit.`

### v0.120.0 — Payment Intents And Capture

Status: planned.

Goal: Initiate and capture hosted or tokenized payments without processing card data.

Deliverables:

- Provider-agnostic payment intent and attempt state machines; hosted/tokenized connector contract; amount/currency/order binding; authorization/capture/void; idempotency; outbox dispatch; ambiguous-result lookup; card-data discovery and explicit PCI scope non-claim.

Verification:

- No PAN/CVV entry/storage/log path; token/order/amount substitution, duplicate attempt/capture, timeout ambiguity, provider outage, stale credentials, cancellation, reconciliation lookup, and balanced journal tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.0 implementation stop reached. Run pentest for this exact commit.`

### v0.120.1 — Payment Webhooks And Reconciliation

Status: planned.

Goal: Treat provider callbacks and polling results as untrusted replayable evidence.

Deliverables:

- Raw-body signature-provider boundary; key rotation; timestamp/replay window; durable receipt before processing; event normalization; out-of-order handling; provider lookup; discrepancy queue; settlement reconciliation.

Verification:

- Invalid/rotated signatures, body substitution, replay, duplicate/out-of-order events, delayed delivery, unknown payment, provider mismatch, timeout, poison event, crash/restart, and settlement discrepancy tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Duplicate or missing provider events converge through idempotent lookup/reconciliation and cannot directly rewrite order or journal state.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.1 implementation stop reached. Run pentest for this exact commit.`

### v0.120.2 — Refunds, Disputes, And Store Credit

Status: planned.

Goal: Model reversals as bounded compensating workflows.

Deliverables:

- Partial/full refund intents; allocation to lines/tax/shipping; approval; provider attempt; dispute/chargeback lifecycle; evidence; store-credit ledger; idempotency and journal compensation.

Verification:

- Duplicate/over/partial refund, concurrent refund/capture, out-of-order dispute, failed provider, reopened dispute, store-credit replay/expiry, allocation rounding, and journal balance tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Refund and dispute outcomes never delete original financial facts and cannot exceed the declared refundable position.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.2 implementation stop reached. Run pentest for this exact commit.`

### v0.120.3 — Shipping And Fulfilment

Status: planned.

Goal: Track physical fulfilment and external carrier effects independently from payment state.

Deliverables:

- Shipping quote snapshot; fulfilment state; split shipments; item allocation; carrier/label operation handles; tracking events; cancellation; lost/damaged states; idempotent outbox/reconciliation.

Verification:

- Partial/split fulfilment, duplicate/lost/out-of-order carrier events, label timeout/cancel, provider outage, stock allocation conflict, address redaction, retry, and journal interaction tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Carrier availability or callbacks cannot silently change order, inventory, refund, or journal authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.3 implementation stop reached. Run pentest for this exact commit.`

### v0.120.4 — Returns And Inventory Compensation

Status: planned.

Goal: Process returns without racing refunds, fulfilment, or stock disposition.

Deliverables:

- Return authorization; received/inspected disposition; restock/damaged/lost transitions; refund/store-credit proposal; shipping linkage; reason/evidence; retention and personal-data controls.

Verification:

- Duplicate/partial returns, wrong item, return/refund and return/fulfilment races, damaged restock denial, warehouse retry, cancellation, privacy expiry, and inventory/journal compensation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Returned stock and money move only through explicit linked state-machine and journal operations.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.4 implementation stop reached. Run pentest for this exact commit.`

### v0.120.5 — Subscriptions And Dunning

Status: planned.

Goal: Create recurring invoice/payment intents without granting a provider subscription authority.

Deliverables:

- Plan/version, billing anchor/timezone, recurring invoice intent, proration policy, renewal idempotency slot, dunning/retry, pause/cancel, entitlement grace/revocation, provider reconciliation.

Verification:

- Duplicate renewal, DST/month-end, plan change, proration rounding, failed/late payment, retry exhaustion, cancel/renew race, webhook loss, entitlement grace/revoke, and journal tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- A provider cannot create an unrecorded renewal or preserve entitlement after the authoritative lifecycle revokes it.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.5 implementation stop reached. Run pentest for this exact commit.`

### v0.120.6 — Digital Entitlements And Secure Delivery

Status: planned.

Goal: Issue bounded digital access derived from authoritative commerce state.

Deliverables:

- Product/version-bound grants; order/payment/refund/subscription linkage; audience/device/download/concurrency limits; expiry/revocation; secure short-lived delivery token; watermark/provenance hooks; classification, privacy, retention, and usage audit.

Verification:

- Token sharing/replay/audience confusion, cross-tenant access, expiry/revocation, refund/chargeback, subscription lapse, product replacement, download/concurrency limits, CDN cache, deletion/retention conflict, archive, and restore tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Digital access is reconstructible from authoritative order/payment/refund/subscription state and never survives its source entitlement.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.6 implementation stop reached. Run pentest for this exact commit.`

### v0.120.7 — Invoices, Credit Notes, And Tax Evidence

Status: planned.

Goal: Issue immutable fiscal documents independently from digital delivery authority.

Deliverables:

- Jurisdiction/series numbering policy; immutable invoice and credit-note snapshots; seller/customer/tax/currency/line/payment references; correction/linkage; rendered and structured export; signature/provider hook where required; retention/hold/classification and authorized delivery.

Verification:

- Duplicate/gap/concurrent numbering by policy, wrong jurisdiction/series, post-issue mutation, partial credit, currency/tax mismatch, customer-data correction, unauthorized delivery, retention/erasure/hold, archive/restore, and migration tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Issued fiscal facts are append-only; corrections use linked credit/replacement documents and preserve required evidence without overstating legal compliance.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.7 implementation stop reached. Run pentest for this exact commit.`

### v0.120.8 — Commerce Live Failure Matrix

Status: planned.

Goal: Prove complete commerce journeys against real providers and every qualified database under concurrency and failure.

Deliverables:

- Payment/tax/shipping sandbox profiles; database/topology matrix; deterministic seed corpus; crash/partition/replay controller; reconciliation and accessibility evidence; PCI non-claim review; one acceptance command.

Verification:

- Browse-to-order, guest/member checkout, oversell race, capture, webhook loss/reorder, partial refund, dispute, fulfilment, return, subscription renewal/cancel, digital grant/revoke, backup/restore, and provider/database outage journeys pass live.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No commerce connector, database, or topology appears in a support profile without current end-to-end failure/recovery evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.8 implementation stop reached. Run pentest for this exact commit.`

## Phase 12 — Compliance, migration, operations, hardening, and 1.0

### v0.121.0 — Compliance Metadata and Passports

Status: planned.

Goal: Represent site, data, purpose, retention, region, operation, and policy epochs without certification claims.

Deliverables:

- Classification inheritance, source locks, legal-basis identifiers, processing constraints, approvals, evidence references, and non-certification UI.

Verification:

- Protected unlabeled data fails restrictive; derived search/AI/backup state inherits restrictions; stale epochs surface.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.121.0 implementation stop reached. Run pentest for this exact commit.`

### v0.121.1 — Standards Control Catalog Expansion

Status: planned.

Goal: Extend the foundation registry with formal standards mappings and compliance evidence fields.

Deliverables:

- Migrate the existing registry without ID churn; add versioned ASVS/NIST/PCI/WCAG/privacy mappings; applicability, evidence type, operator control, exception, owner, review date, result, and non-claim fields; generated coverage, standard-version diff, and orphan reports.

Verification:

- Migration fixtures preserve every earlier owner/scenario/evidence link; catalog tests reject stale standard references, unowned, multiply owned, untested, waived-without-expiry, unsupported-claim, and evidence-without-artifact entries; generated documentation is reproducible.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every 1.0 requirement maps to exactly one owning pre-1.0 milestone and at least one launchable or explicitly manual evidence item.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.121.1 implementation stop reached. Run pentest for this exact commit.`

### v0.121.2 — Data Classification Propagation

Status: planned.

Goal: Preserve classification, purpose, region, retention, and deletion constraints through every derived system.

Deliverables:

- Propagation rules for search, cache, analytics, AI, exports, archives, backups, logs, events, webhooks, plugins, and commerce; conflict/restrictive merge; expiry/delete tombstones; provenance and exception handling.

Verification:

- End-to-end fixtures mutate and delete classified source data and prove every derivative is restricted, expired, rebuilt, redacted, held, or reported according to policy across provider failures and restore.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- An unlabeled or propagation-ambiguous derivative receives the most restrictive applicable handling and cannot be published or exported silently.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.121.2 implementation stop reached. Run pentest for this exact commit.`

### v0.122.0 — Privacy Operations Pack

Status: planned.

Goal: Provide implementable privacy lifecycle controls without claiming legal certification.

Deliverables:

- Controller/processor/subprocessor and region inventory; purpose/legal-basis references; consent and script gating; DSAR/export/correction; retention/erasure/hold; opt-out; backup/restore deletion behavior; incident and evidence export.

Verification:

- End-to-end consent, withdrawal, processor/region constraint, DSAR/export/correction, erasure/hold conflict, script blocking, backup restore then re-delete, incident, and non-claim tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.122.0 implementation stop reached. Run pentest for this exact commit.`

### v0.122.1 — Accessibility Qualification Pack

Status: planned.

Goal: Qualify authoring and public/admin experiences against declared WCAG 2.2 and EAA-oriented scope.

Deliverables:

- Automated checks; keyboard and screen-reader scripts; focus/error/status behavior; zoom/reflow/motion/contrast rules; media alternative workflow; theme/plugin contribution checks; manual reviewer, exception, and retest evidence.

Verification:

- Real browser runs cover setup, authentication, authoring, publishing, forms, checkout, recovery, theme/plugin UI, mobile viewport, keyboard-only, and supported screen-reader scripts; automated tools are not accepted as complete evidence.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every claimed UI journey has current automated plus required manual evidence and publishes known limitations without certification language.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.122.1 implementation stop reached. Run pentest for this exact commit.`

### v0.122.2 — Cryptographic Key Lifecycle And Erasure

Status: planned.

Goal: Make encryption, signing, rotation, revocation, backup, and crypto-erasure operationally complete.

Deliverables:

- Key-purpose/algorithm/provider inventory; generation/import/reference policy; envelope hierarchy; tenant separation; rotation generations; revocation/compromise; archive/backup/restore behavior; crypto-erasure and retention conflict; evidence without key disclosure.

Verification:

- Wrong/old/revoked key, partial rotation, provider outage, rollback, restored stale ciphertext, tenant substitution, lost-key recovery/non-recovery, crypto-erasure, and signature verification fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No control claims encryption, signing, or erasure without a named provider boundary, key lifecycle, recovery consequence, and executable evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.122.2 implementation stop reached. Run pentest for this exact commit.`

### v0.122.3 — Sensitive Field And Blob Encryption Profiles

Status: planned.

Goal: Apply envelope encryption and crypto-erasure to declared sensitive values without hiding query, backup, or availability limitations.

Deliverables:

- Field/blob eligibility and classification; per-tenant/data-key hierarchy; AEAD context binding; key-reference/generation; encrypted index/search non-support or explicit scheme; rotation/re-encryption; backup/restore; hold/retention; crypto-erasure; cache/log/export policy and operational failure behavior.

Verification:

- Ciphertext/tenant/field/version substitution, nonce/context misuse prevention, partial rotation, unavailable/revoked/lost key, stale cache/search, backup restore with old generations, hold/erasure conflict, corruption, migration, and redaction tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Encryption claims name exact fields/providers/availability/search consequences, and erasure cannot be claimed while recoverable key material remains in supported backups.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.122.3 implementation stop reached. Run pentest for this exact commit.`

### v0.123.0 — Healthcare And Highly Sensitive Data Pack

Status: planned.

Goal: Provide healthcare/PHI-oriented technical controls and evidence without claiming HIPAA certification.

Deliverables:

- PHI/sensitive-data classification; minimum-necessary access; emergency access; workforce/device/session presets; disclosure/audit reports; retention/erasure/hold; processor/region controls; incident/evidence workflow; backup/restore behavior and non-claim UI.

Verification:

- PHI classification/propagation, minimum-necessary field access, emergency access review, disclosure accounting, processor/region denial, incident, retention/hold, backup/restore, and non-certification profile tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.0 implementation stop reached. Run pentest for this exact commit.`

### v0.123.1 — Cybersecurity Governance Evidence Packs

Status: planned.

Goal: Map NIS2, SOC 2, and ISO 27001-oriented operator evidence without pretending product controls certify an organization.

Deliverables:

- Asset/service/supplier inventory; risk/owner/exception records; incident/vulnerability/continuity/change/access-review evidence; responsibility matrix; evidence retention/export; standard-version mapping; operator-versus-product control separation and non-claims.

Verification:

- Missing owner/evidence, stale supplier/control, expired exception, incident escalation, access review, continuity rehearsal, export redaction, standard update, and false-certification UI/API tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every mapping states applicability and responsibility; Aetherheim never labels an installation or organization compliant/certified automatically.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.1 implementation stop reached. Run pentest for this exact commit.`

### v0.123.2 — AI Governance And Provenance Pack

Status: planned.

Goal: Govern optional AI use through inventory, purpose, risk, review, provenance, and incident evidence.

Deliverables:

- Provider/model/use-case inventory; data/purpose/region/retention/training terms; risk/impact review; human oversight; source/output provenance; model-change assessment; complaint/incident/disable workflow; public disclosure and non-claim controls.

Verification:

- Unregistered use case/model, changed terms/model, missing impact review, sensitive-data mismatch, false provenance, missing human review, incident disable, export/redaction, and AI-disabled profile tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- AI governance evidence cannot enable AI operations or publication; it documents and constrains separately authorized behavior.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.2 implementation stop reached. Run pentest for this exact commit.`

### v0.123.3 — Payment Page Integrity And Card-Data Discovery

Status: planned.

Goal: Keep hosted/tokenized checkout boundaries observable and prevent accidental card-data scope expansion.

Deliverables:

- Payment-page script/resource inventory; authorization and integrity metadata; change detection; browser egress policy; CSP/reporting; card-data pattern discovery for logs, traces, storage, support exports, backups, and crash artifacts; incident runbook.

Verification:

- Unauthorized/changed scripts, compromised resource metadata, form/DOM exfiltration, CSP bypass, synthetic PAN/CVV in every diagnostic/storage path, third-party outage, and rollback tests pass without retaining discovered samples.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Aetherheim can demonstrate its declared card-data boundary and clearly states that technical controls do not certify PCI compliance.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.3 implementation stop reached. Run pentest for this exact commit.`

### v0.123.4 — Security Events And Observability

Status: planned.

Goal: Detect abuse and failure through bounded privacy-safe operational signals.

Deliverables:

- Versioned security-event taxonomy; structured redaction; metrics/traces/log correlation; audit linkage; cardinality/sampling/retention budgets; alert/runbook/escalation mapping; tenant/profile context; diagnostic export and evidence.

Verification:

- Authentication, authorization, tenant, cache, plugin, commerce, migration, secret, proxy, and cluster incidents emit bounded useful signals; injection/cardinality/secret leakage, alert loss/duplication, retention, and export tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every production profile has tested operator signals and runbooks without exposing protected data.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.4 implementation stop reached. Run pentest for this exact commit.`

### v0.123.5 — Capacity Models, SLOs, And Error Budgets

Status: planned.

Goal: Publish measured performance and availability objectives without mixing them into event collection.

Deliverables:

- Representative workload and capacity model; resource saturation thresholds; availability/latency/freshness/durability objectives; error-budget calculation; measurement windows/exclusions; dependency/topology assumptions; scaling/degradation policy; alerts and operator reports by profile.

Verification:

- Load/soak/failure evidence validates calculations under traffic shape, tenant skew, provider latency/loss, cache miss, background work, media/commerce spikes, clock gaps, telemetry loss, and declared maintenance; unsupported targets are rejected.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every claimed SLO names exact profile, workload, dependencies, measurement method, and current passing evidence; unmeasured claims are absent.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.5 implementation stop reached. Run pentest for this exact commit.`

### v0.123.6 — Vulnerability, Update, And Revocation Lifecycle

Status: planned.

Goal: Make component compromise and security updates operational from discovery through fleet evidence.

Deliverables:

- Intake/severity/SLA policy; affected-version and SBOM lookup; maintainer/contact ownership; coordinated disclosure; signed advisory/update metadata; rollback/freeze/revocation; plugin/theme/provider compromise; operator notification and completion evidence.

Verification:

- Simulated vulnerable crate, runtime, image, plugin, theme, key, provider, and offline installation exercises detection, blocking, update, rollback, revocation, mirror compromise, stale metadata, and fleet accounting.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every shipped artifact and ecosystem package can be identified, blocked or revoked, updated, rolled back, and audited under its supported profile.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.6 implementation stop reached. Run pentest for this exact commit.`

### v0.123.7 — Abuse Controls And Resource Fairness

Status: planned.

Goal: Apply consistent bounded abuse controls across public, administrative, API, webhook, plugin, search, and commerce surfaces.

Deliverables:

- Tenant/actor/IP/credential/operation budget dimensions; endpoint and workflow rate/concurrency limits; queue/backpressure; fairness; trusted-proxy input; privacy-preserving identifiers; retry guidance; administrative recovery and observability.

Verification:

- Distributed and cross-endpoint amplification, tenant starvation, login/reset/registration abuse, GraphQL/query cost, upload, search, webhook, checkout, plugin host-call, proxy spoof, clock, cache loss, and recovery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No externally reachable operation lacks an owning resource budget and tested overload behavior.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.7 implementation stop reached. Run pentest for this exact commit.`

### v0.124.0 — WordPress Content Import

Status: planned.

Goal: Provide a resumable staged content/community migration from WordPress.

Deliverables:

- Users/roles attribution; posts/pages/custom types; block/classic content quarantine; taxonomies; comments; media; menus; metadata; redirects/URLs; source IDs/provenance; plugin-field envelope; staged validation and issue report.

Verification:

- Large hostile fixtures resume safely; malformed serialization/markup/media and plugin metadata remain bounded/quarantined; attribution, relationships, URLs, IDs, comments, redirects, and unsupported-data reports are complete.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.124.0 implementation stop reached. Run pentest for this exact commit.`

### v0.124.1 — WooCommerce Import

Status: planned.

Goal: Migrate WooCommerce commerce history without weakening Aetherheim monetary and inventory invariants.

Deliverables:

- Products/variants/SKUs; price/tax/coupon metadata; customers/addresses with classification; orders/lines/status/history; payments/refunds as imported evidence; inventory; subscriptions where representable; source IDs; discrepancy and non-importable-secret/card-data reports.

Verification:

- Large hostile stores, malformed decimals/currencies/tax, duplicate IDs/SKUs/orders, inconsistent totals, partial refunds, status drift, personal-data policy, raw-card/secret discovery, resume/rollback, and complete discrepancy tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Imported records preserve source attribution and discrepancies; they never masquerade as balanced Aetherheim-native transactions without explicit reconciliation.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.124.1 implementation stop reached. Run pentest for this exact commit.`

### v0.125.0 — Drupal Import

Status: planned.

Goal: Provide a resumable staged Drupal content/community migration.

Deliverables:

- Supported Drupal version/export scope; users/roles attribution; content entities/types/fields; taxonomy; comments; media/files; menus/routes/aliases; multilingual revisions; source IDs/provenance; checkpoints; validation and limitations report.

Verification:

- Versioned hostile corpora exercise malformed serialization/markup/files, retries, encoding, entity references, multilingual state, routes, unsupported modules/fields, complete reporting, and rollback.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.125.0 implementation stop reached. Run pentest for this exact commit.`

### v0.125.1 — Joomla Import

Status: planned.

Goal: Provide a resumable staged Joomla content/community migration.

Deliverables:

- Supported version/export scope; users/groups attribution; articles/categories/tags; custom fields; contacts; media; menus/routes/aliases; multilingual associations; source IDs/provenance; checkpoints; validation and limitations report.

Verification:

- Versioned hostile corpora cover malformed markup/files, ACL/group ambiguity, encoding, relationships, multilingual routing, extensions/unsupported fields, retries, rollback, and complete reporting.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Unsupported Joomla extension data is preserved in bounded source envelopes or reported, never silently discarded or granted authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.125.1 implementation stop reached. Run pentest for this exact commit.`

### v0.125.2 — Ghost Import

Status: planned.

Goal: Provide a resumable staged Ghost publication/member migration.

Deliverables:

- Supported export scope; users/authors attribution; posts/pages/tags; lexical/HTML content quarantine and conversion; members/tiers/newsletters/consent metadata; media/routes/redirects; source IDs/provenance; checkpoints and limitations report.

Verification:

- Hostile/malformed exports, HTML/card conversion, member/privacy data, tier/newsletter ambiguity, URLs, media, encoding, retries, rollback, and unsupported-field reporting tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Ghost member and newsletter data is imported only with source provenance and explicit consent/purpose review requirements.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.125.2 implementation stop reached. Run pentest for this exact commit.`

### v0.125.3 — Wix Supported-Export Import

Status: planned.

Goal: Import only officially obtainable Wix exports without bypassing access controls or scraping private services.

Deliverables:

- Supported export/API scope; operator authorization; pages/content/data collections; products where representable; contacts with purpose review; media; routes; source IDs/provenance; rate/resume/checkpoint policy and limitations report.

Verification:

- Authorization denial/expiry, rate limits, partial exports, schema drift, hostile content/media, privacy/consent ambiguity, retries, rollback, and complete omission reporting pass; no unsupported private crawler path exists.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The importer uses only operator-authorized supported source boundaries and makes no completeness claim beyond the exact export profile.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.125.3 implementation stop reached. Run pentest for this exact commit.`

### v0.125.4 — Static Site And Markdown Import

Status: planned.

Goal: Convert authorized static files and Markdown into structured content with explicit loss reporting.

Deliverables:

- Root/path allowlist; symlink policy; Markdown/front-matter scope; HTML quarantine; file-to-route mapping; assets/links; metadata/schema mapping; source digests/provenance; checkpoints; redirects and limitations report.

Verification:

- Path/symlink escape, encoding, huge/deep documents, HTML/XSS, link cycles, duplicate routes, malformed front matter, binary confusion, retry, deterministic conversion, and unsupported construct reporting pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Import reads only the authorized root and never silently converts unsupported markup into trusted rendered output.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.125.4 implementation stop reached. Run pentest for this exact commit.`

### v0.125.5 — CSV, JSON, And Feed Mapping Import

Status: planned.

Goal: Map bounded structured records and RSS/Atom feeds through an explicit typed import specification.

Deliverables:

- Mapping DSL/schema; source encoding and digest; CSV/JSON/RSS/Atom scope; record/field/relationship transforms; ID/upsert/conflict policy; checkpoints; validation/quarantine; dry run, provenance, error and omission reports.

Verification:

- Formula/injection-shaped text, deep/large JSON, entity/encoding tricks, duplicate IDs, relationship cycles, partial records, schema drift, retry/resume, deterministic mapping, rollback, and complete error reporting pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Mapping cannot invoke arbitrary code or raw provider queries, and every skipped/changed record is reportable.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.125.5 implementation stop reached. Run pentest for this exact commit.`

### v0.125.6 — Media Folder Import

Status: planned.

Goal: Import authorized media trees through the normal quarantine, probe, rights, and lifecycle paths.

Deliverables:

- Root/path/symlink policy; recursive limits; duplicate/digest handling; sidecar metadata mapping; filename/collection structure; rights/consent review; checkpoints; source provenance; issue and omission report.

Verification:

- Path/symlink escape, device/special files, deep/wide trees, hostile files/sidecars, duplicates, case/Unicode collisions, partial copy, restart, scanner/processor failure, rights ambiguity, and rollback tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Imported bytes remain quarantined until normal admission succeeds and filesystem layout never becomes publication authority.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.125.6 implementation stop reached. Run pentest for this exact commit.`

### v0.126.0 — Backup Creation And Verification

Status: planned.

Goal: Create complete encrypted, integrity-checked backup sets without claiming restore success yet.

Deliverables:

- Encrypted-provider boundary; database/blob/config/package/secret-reference manifests; AHAF and provider-native components; incremental/full/chunk roots; consistency/fence policy; retention/hold; verification jobs; rotation; offsite/region policy; inventory and operation receipt.

Verification:

- Missing/substituted/corrupt chunks, wrong roots/keys, partial/inconsistent backup, concurrent writes, failed incremental chain, rotation, retention/hold, provider outage, cancellation, and verification-job tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.126.0 implementation stop reached. Run pentest for this exact commit.`

### v0.126.1 — Isolated Restore Verification

Status: planned.

Goal: Prove complete backups restore in a clean isolated environment before any promotion.

Deliverables:

- Clean-room restore network; exact dependency/key/package verification; database/blob/AHAF/config restore; deletion/revocation replay; derived cache/search rebuild; job/outbox quarantine and reconciliation report; integrity/application acceptance; RPO/RTO measurement and restore receipt.

Verification:

- Restore under stale/partial/corrupt backup, wrong/revoked key/package, database/blob mismatch, deletion/revocation state, pending jobs/effects, cache/search absence, cross-provider target, operator error, and resource exhaustion meets declared verification rules or fails closed.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Backup success is never equated with recoverability; every supported backup profile has a clean-room restore acceptance result.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.126.1 implementation stop reached. Run pentest for this exact commit.`

### v0.126.2 — Disaster Promotion And Regional Recovery

Status: planned.

Goal: Promote a verified restore without reviving stale authority or violating region and topology constraints.

Deliverables:

- Authorized promotion state machine; regional placement; dependency readiness; session/token invalidation; job/outbox reconciliation decision; DNS/proxy cutover; readiness/drain; split-authority prevention; failback; operator approvals/receipt and RPO/RTO runbook.

Verification:

- Region loss, stale source node, partial DNS/proxy cutover, old database/blob reachability, pending effects, token/session replay, cache/secret loss, failback, concurrent operators, and every crash point meet the declared recovery profile or fail closed.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Only one authorized topology accepts mutations after promotion, and every production profile has a rehearsed promotion/failback path.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.126.2 implementation stop reached. Run pentest for this exact commit.`

### v0.127.0 — Release Artifact Manifest And Portable Archives

Status: planned.

Goal: Define one no-crates.io artifact set and portable archive format before platform-specific packaging.

Deliverables:

- Artifact/release manifest; standalone archive layout; binaries/assets/config/schema/migrations/licences/notices; checksums; SBOM/provenance/signature references; install/uninstall/upgrade contract; platform identity; offline verification; no crates.io metadata.

Verification:

- Archive traversal/substitution, missing/extra file, permission drift, wrong platform/version, install/uninstall/upgrade failure, offline verification, SBOM/provenance linkage, and no-crates.io tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.0 implementation stop reached. Run pentest for this exact commit.`

### v0.127.1 — Trusted Reverse Proxy Boundary

Status: planned.

Goal: Support direct serving and optional reverse proxies without trusting attacker-supplied topology metadata.

Deliverables:

- Trusted-peer policy, canonical Forwarded/X-Forwarded profile, client/scheme/host/port/certificate/request-ID derivation, hop-by-hop stripping, optional PROXY protocol scope, health/admin exposure, request bounds, retry contract, and proxy-aware audit fields.

Verification:

- Untrusted/conflicting headers, spoofed host/scheme/client, malformed PROXY frames, request smuggling, duplicate non-idempotent retry, redirect/cookie origin, health exposure, and direct-versus-proxied equivalence tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.1 implementation stop reached. Run pentest for this exact commit.`

### v0.127.2 — Optional Fluxheim Deployment Profile

Status: planned.

Goal: Qualify Aetherheim behind Fluxheim as an optional web-server, reverse-proxy, and load-balancer topology.

Deliverables:

- Versioned example configuration, upstream TLS/mTLS ownership, forwarding profile, active readiness check, safe retry budget, connection limits, WebSocket/HTTP compatibility, drain, slow start, all-down response, logging correlation, and upgrade/rollback runbook.

Verification:

- Live direct and Fluxheim-proxied conformance covers headers, bodies, streaming/upgrades where supported, retries, health transitions, node drain/recovery, stale membership, complete upstream loss, TLS identity, limits, and audit correlation.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Fluxheim remains out of process and optional; Aetherheim has no runtime dependency on it.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.2 implementation stop reached. Run pentest for this exact commit.`

### v0.127.3 — Hermetic Reproducible Build And Signing Pipeline

Status: planned.

Goal: Make release artifacts reproducible, provenance-bound, verifiable offline, and revocable.

Deliverables:

- Pinned clean builders; dependency/source/action/tool manifests; network policy; deterministic timestamps/paths; two-builder comparison; isolated signing identity; signed release/update metadata; SBOM/provenance linkage; offline verification and revocation bundle.

Verification:

- Two independent builders reproduce declared artifacts; source/tool/action/dependency substitution, dirty tree, timestamp/path drift, wrong signer, stale/revoked metadata, mirror compromise, and offline rollback/freeze tests fail safely.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every production artifact can be traced to exact source and inputs, verified without network access, and revoked without crates.io.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.3 implementation stop reached. Run pentest for this exact commit.`

### v0.127.4 — Linux Service Packaging

Status: planned.

Goal: Qualify native and portable Linux deployment without assuming a container runtime.

Deliverables:

- GNU/musl and supported architectures; standalone archive; systemd/OpenRC-style guidance where applicable; dedicated user/directories; capabilities/permissions; rootless mode; logs/limits; install/upgrade/rollback/uninstall; distribution support matrix.

Verification:

- Clean supported distributions/architectures cover install, initialize, direct serve, service restart/drain, permissions, read-only paths, upgrade/rollback, backup/restore, uninstall, and hostile pre-existing filesystem state.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Linux support names exact distributions/libc/architectures and never relies only on a developer machine or OCI image.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.4 implementation stop reached. Run pentest for this exact commit.`

### v0.127.5 — Windows Service Packaging

Status: planned.

Goal: Qualify native Windows operation and service lifecycle.

Deliverables:

- MSVC and any retained GNU profile; archive/installer decision; Windows service identity; ACLs/data directories; certificate/secret integration; Event Log/diagnostics; firewall guidance; install/upgrade/rollback/uninstall and support matrix.

Verification:

- Clean supported Windows versions cover install, service identity/ACLs, direct serve/TLS, restart/drain, path/Unicode/locking behavior, upgrade/rollback, backup/restore, diagnostics, uninstall, and hostile pre-existing state.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Windows support is real packaged operation, not cross-compilation alone.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.5 implementation stop reached. Run pentest for this exact commit.`

### v0.127.6 — macOS Service Packaging

Status: planned.

Goal: Qualify native macOS operation on Intel and Apple Silicon.

Deliverables:

- Universal/separate artifact decision; signing/notarization boundary; launchd guidance; user/service identity and directories; Keychain/certificate/secret integration; quarantine attributes; install/upgrade/rollback/uninstall and support matrix.

Verification:

- Clean supported macOS/architectures cover verification, quarantine/notarization, install, launchd/restart/drain, permissions, TLS, upgrade/rollback, backup/restore, diagnostics, uninstall, and wrong-architecture/substitution failures.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- macOS support includes verified packaged lifecycle on both claimed architectures.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.6 implementation stop reached. Run pentest for this exact commit.`

### v0.127.7 — FreeBSD Service Packaging

Status: planned.

Goal: Qualify FreeBSD operation separately from Linux and other BSD assumptions.

Deliverables:

- Exact FreeBSD versions/architectures; archive/pkg decision; rc.d/service identity; filesystem/permission/socket/TLS differences; jail guidance where supported; install/upgrade/rollback/uninstall and limitations.

Verification:

- Native runners cover clean install, rc lifecycle, direct serve/TLS, permissions, filesystem locking, jail profile, restart/drain, upgrade/rollback, backup/restore, diagnostics, and uninstall on every claimed FreeBSD cell.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- FreeBSD support requires native runtime evidence and never follows from a compile-only target check.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.7 implementation stop reached. Run pentest for this exact commit.`

### v0.127.8 — NetBSD Service Packaging

Status: planned.

Goal: Qualify NetBSD operation independently from FreeBSD and Linux assumptions.

Deliverables:

- Exact NetBSD versions/architectures; archive/pkgsrc decision; rc.d/service identity; filesystem/permission/socket/TLS differences; chroot guidance where supported; install/upgrade/rollback/uninstall and limitations.

Verification:

- Native runners cover clean install, rc lifecycle, direct serve/TLS, permissions, filesystem locking, chroot profile, restart/drain, upgrade/rollback, backup/restore, diagnostics, and uninstall on every claimed NetBSD cell.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- NetBSD support requires native runtime evidence and never follows from FreeBSD behavior or a compile-only target check.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.8 implementation stop reached. Run pentest for this exact commit.`

### v0.127.9 — Android Host And Library Qualification

Status: planned.

Goal: Define and qualify the supported Android embedding/runtime surface without pretending a mobile device is a production server profile.

Deliverables:

- Supported API levels/architectures; library/JNI boundary; lifecycle/background limits; storage/keystore/network integration; no_std/shared-domain scope; generated Kotlin API; packaging/update; resource budgets; explicit absent server/worker features and sample host.

Verification:

- Emulator/device matrix covers load/unload, process/activity death, storage/key loss, offline/network change, API compatibility, Kotlin schema, thread/cancellation, resource pressure, upgrade/rollback, and unsupported-feature rejection.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Android support names exact embeddable capabilities and limitations; it does not imply the clustered server topology runs on Android.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.9 implementation stop reached. Run pentest for this exact commit.`

### v0.127.10 — iOS Host And Library Qualification

Status: planned.

Goal: Define and qualify the supported iOS embedding surface under platform lifecycle and distribution constraints.

Deliverables:

- Supported iOS versions/architectures; static/dynamic library boundary; Swift API generation; lifecycle/background limits; sandbox storage/Keychain/network integration; packaging/update; resource budgets; explicit absent server/worker features and sample host.

Verification:

- Simulator/device matrix covers load/unload, process/background termination, storage/key loss, offline/network change, Swift schema, thread/cancellation, memory pressure, upgrade/rollback, code-signing/package behavior, and unsupported-feature rejection.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- iOS support names exact embeddable capabilities and limitations; it does not imply production server operation on iOS.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.10 implementation stop reached. Run pentest for this exact commit.`

### v0.127.11 — Rootless OCI And Compose Packaging

Status: planned.

Goal: Qualify container images and simple multi-role composition independently from native packages.

Deliverables:

- Minimal non-root images; immutable digest; multi-architecture manifest; read-only root/filesystem mounts; UID/GID and capabilities; health/readiness; serve/worker/scheduler composition; secrets/config; resource limits; upgrade/rollback/uninstall and SBOM/provenance linkage.

Verification:

- Rootless Podman and supported container runtimes cover pull/verify, read-only/no-capability operation, volume permissions, network isolation, health/drain, multi-role restart, upgrade/rollback, backup/restore, digest substitution, and cleanup.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Container support is rootless by default and never requires ambient host privileges or mutable image tags for release identity.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.11 implementation stop reached. Run pentest for this exact commit.`

### v0.127.12 — Air-Gapped Installation Bundle

Status: planned.

Goal: Install, verify, update, roll back, and revoke Aetherheim without network access.

Deliverables:

- Complete platform artifact/dependency/package/tool/trust metadata bundle; offline signatures/SBOM/provenance/advisories/revocations; import/export media policy; expiry/freeze rules; update/rollback runbook; reproducible inventory and evidence.

Verification:

- Clean isolated environments cover install, verify, operate, update, rollback, revoked/stale metadata, missing/substituted artifact, trust-root rotation, extension/theme bundle, backup/restore, and complete uninstall with network physically unavailable.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Air-gapped support has no hidden online fetch and can still detect known bundled revocations and stale metadata truthfully.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.127.12 implementation stop reached. Run pentest for this exact commit.`

### v0.128.0 — Upgrade And Rollback Qualification

Status: planned.

Goal: Prove every supported installation can upgrade or return safely within its declared rollback window.

Deliverables:

- Expand/contract migrations; schema/protocol/package/config compatibility window; drain and canary; job/plugin/theme compatibility; data-loss/irreversibility checks; rollback automation; per-profile/operator runbooks and receipts.

Verification:

- Upgrade/rollback from every supported fixture with failure at each phase either completes or returns within the declared boundary; no loss, duplicate effect, stale authority, or secret leak.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.0 implementation stop reached. Run pentest for this exact commit.`

### v0.128.1 — Long-Run Endurance And Resource Qualification

Status: planned.

Goal: Find leaks, drift, starvation, and recovery defects independently from migration correctness.

Deliverables:

- Representative tenant/content/media/search/plugin/commerce workload; 24/72-hour and defined long soak profiles; memory/handle/thread/connection/disk/cardinality budgets; fault schedule; capacity and degradation thresholds; evidence and triage artifacts.

Verification:

- Sustained authoring/delivery/jobs/search/media/plugins/commerce with restarts, clock movement, provider latency/loss, cache eviction, secret rotation, disk pressure, and load spikes meets declared leak/fairness/latency/recovery budgets.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every production profile has a reproducible long-run workload and no unexplained unbounded resource growth or starvation.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.1 implementation stop reached. Run pentest for this exact commit.`

### v0.128.2 — Cluster Identity And Readiness

Status: planned.

Goal: Let multiple Aetherheim nodes identify compatible peers and expose truthful routing readiness.

Deliverables:

- Stable installation identity, ephemeral boot identity, authenticated peer identity, bounded membership view, protocol/schema compatibility window, liveness/readiness separation, dependency readiness, heartbeat budgets, and readiness withdrawal before drain.

Verification:

- Forged/duplicate/stale node, replay, incompatible version, clock movement, delayed heartbeat, dependency loss, partial startup, process pause, shutdown, and rolling-membership tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.2 implementation stop reached. Run pentest for this exact commit.`

### v0.128.3 — Fenced Cluster Work And Failure Recovery

Status: planned.

Goal: Share durable jobs, singleton duties, sessions, and invalidations safely across active application nodes.

Deliverables:

- Shared authoritative state, database-time leases, monotonic fencing tokens, deterministic schedule slots, transactional claim/completion/outbox, idempotency keys, reclaim policy, session/revocation consistency, cache invalidation, migration ownership, and split-network fail-closed rules.

Verification:

- Kill/pause/partition every lease phase; duplicate, reorder, and delay messages; skew clocks; isolate cache/database/OpenBao; and prove stale workers are fenced, work is safely reclaimed, effects are idempotent, and authority never falls back to local memory.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Documentation states at-least-once/idempotent effects honestly and makes no exactly-once or home-grown consensus claim.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.3 implementation stop reached. Run pentest for this exact commit.`

### v0.128.4 — Active-Active Load And Failover Qualification

Status: planned.

Goal: Prove a supported multi-node deployment shares load and continues within declared limits when a node fails.

Deliverables:

- Reference two/three-node topologies, load-balancer discovery guidance, shared database and S3-compatible blob requirements, capacity and coordination model, rolling upgrade/drain, cache/OpenBao degradation policy, disaster boundaries, metrics, alerts, and operator exercises.

Verification:

- Sustained balanced load, abrupt node loss, rolling restart, zone partition, stale proxy membership, thundering herd, provider slowdown, cache loss, secret-provider loss, recovery, and 24/72-hour soak tests meet declared availability and data-integrity objectives.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Single-node operation remains supported and every multi-node availability claim names the required database, shared blob, cache, secret-provider, and load-balancer assumptions.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.4 implementation stop reached. Run pentest for this exact commit.`

### v0.128.5 — PostgreSQL Cluster Reference Qualification

Status: planned.

Goal: Establish the first complete supported active-active application topology on the production-reference database.

Deliverables:

- Exact PostgreSQL version/topology/isolation/durability profile; shared S3-compatible blob profile; two/three Aetherheim nodes; generic or Fluxheim load balancer; optional Valkey/OpenBao matrix; backup/PITR, rolling upgrade, capacity, SLO, and operator runbooks.

Verification:

- Live balanced load, node kill/pause, database failover/partition, stale lease, blob outage/corruption, proxy stale membership, cache/secret loss, rolling version change, backup/restore, and 24/72-hour soak meet the declared profile.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- “Clustered” initially means the exact qualified PostgreSQL/shared-blob topology; no broader database claim is inferred.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.5 implementation stop reached. Run pentest for this exact commit.`

### v0.128.6 — Additional Database Cluster Qualifications

Status: planned.

Goal: Require MariaDB, MongoDB, and SurrealDB to earn clustered support independently.

Deliverables:

- Per-provider exact topology and settings; coordination/fencing mapping; transaction/outbox/session/job semantics; shared-blob profile; failover and backup behavior; limitations; capacity/SLO evidence; experimental-to-qualified transition record.

Verification:

- Run the complete PostgreSQL reference failure/history/soak matrix separately against each provider; deliberately unsupported semantics or topology combinations remain rejected and documented rather than emulated unsafely.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Each provider/profile is independently qualified or explicitly absent; SurrealDB remains experimental until this stop and every prerequisite matrix pass.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.6 implementation stop reached. Run pentest for this exact commit.`

### v0.129.0 — Contract Inventory And Semantic Freeze

Status: planned.

Goal: Freeze every public/portable contract only after compatibility and migration evidence.

Deliverables:

- Complete REST, GraphQL, event, webhook, generated-client, archive/AHAF, theme, package, WIT/plugin ABI, configuration, CLI, database/profile, and proof inventory; semantic compatibility checker; deprecation/versioning decisions; generated documentation/SDK/fixture reproduction; migration and rollback compatibility evidence.

Verification:

- Reproducible SDK/docs/fixtures/artifacts match the inventory; accidental breaking changes fail; every intentional versioned break has migration, rollback, consumer, and support-window evidence.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.129.0 implementation stop reached. Run pentest for this exact commit.`

### v0.129.1 — Full Internal Security Campaign

Status: planned.

Goal: Run the complete cross-surface security campaign after contract freeze and before release qualification.

Deliverables:

- Complete threat-model refresh; broad parser/state-machine/protocol fuzzing; Miri/sanitizers where applicable; tenant/context/cache/session isolation; identity/recovery; upload/media; render/browser; extension/runtime; commerce; migration/backup; supply-chain and independent specialist reviews.

Verification:

- Every campaign target runs against exact frozen source/artifacts and reference profiles; findings have severity/owner/remediation/retest evidence; zero unresolved critical/high and no release-blocking medium findings remain.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Security review is not hidden inside compatibility freeze, and any semantic fix repeats affected freeze and campaign evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.129.1 implementation stop reached. Run pentest for this exact commit.`

### v0.129.2 — Non-Skippable Release Qualification Matrix

Status: planned.

Goal: Turn all 1.0 support claims into required release-CI and clean-environment evidence.

Deliverables:

- Scheduled and release-triggered database/provider/topology/platform/browser matrices; fuzz, Miri and sanitizers where applicable; real artifact install/upgrade/restore tests; hermetic builder comparison; signing/revocation rehearsal; explicit required-tool/service inventory; retained evidence digests.

Verification:

- Remove each target, browser, service, credential, tool, artifact, and evidence object in turn and prove release qualification fails rather than skips, substitutes a mock, or marks the claim experimental after the fact.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Every enabled 1.0 profile and support-matrix cell has fresh required evidence for the exact candidate commit; optional absent profiles are clearly not claimed.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.129.2 implementation stop reached. Run pentest for this exact commit.`

### v0.130.0 — Feature-Complete 1.0 Baseline

Status: planned.

Goal: Stop feature work and prepare exact release candidates.

Deliverables:

- Standard, Publisher, Commerce, Enterprise, Clustered, Fluxheim-edge, and Air-gapped reference deployments; documentation; support policy; release branch; final migrations; clean-room rehearsals.

Verification:

- All 1.0 definition-of-done evidence passes and `v0.130.0 implementation stop reached. Run pentest for this exact commit.`
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.130.0 implementation stop reached. Run pentest for this exact commit.`

## Release candidates and 1.0

### v1.0.0-rc.1 — First production candidate

Status: planned.

Goal: expose the feature-complete baseline to production-shaped external testing without adding new subsystems.

Deliverables:

- Frozen candidate artifacts, migrations, compatibility matrices, documentation, SBOM/provenance, and all supported reference profiles.

Verification:

- Repeat the complete database, optional cache/OpenBao/cluster/Fluxheim, platform, browser, migration, backup/restore, security, performance, and long-run matrix.
- Run the inherited gate and independent external pentest.

Exit criteria:

- Only bug, security, documentation, compatibility, and measured performance corrections remain.
- `v1.0.0-rc.1 implementation stop reached. Run pentest for this exact commit.`

### v1.0.0-rc.2 — Migration and ecosystem candidate

Status: planned.

Goal: validate real installations, imports, themes, extensions, and operations after RC1 corrections.

Deliverables:

- Corrected candidate, complete RC1 migration fixtures, ecosystem conformance results, and clean-room operator reports.

Verification:

- Repeat every inherited gate plus upgrade/rollback from RC1 and every supported pre-1.0 fixture.

Exit criteria:

- No release-blocking compatibility or migration ambiguity remains.
- `v1.0.0-rc.2 implementation stop reached. Run pentest for this exact commit.`

### v1.0.0-rc.3 — Final reproducibility candidate

Status: planned.

Goal: freeze and independently reproduce final artifacts.

Deliverables:

- Final source tree, platform artifacts, images, offline bundle, checksums, signatures, SBOM, provenance, documentation, and support policy.

Verification:

- Two independent clean builders reproduce the declared artifact set; full security and restore gates repeat.

Exit criteria:

- The exact candidate is eligible for same-commit 1.0 promotion only if every artifact and evidence object remains unchanged.
- `v1.0.0-rc.3 implementation stop reached. Run pentest for this exact commit.`

### v1.0.0 — First serious production release

Status: planned.

Goal: release only the exact fully approved candidate.

Deliverables:

- Signed release metadata and supported artifacts; no crates.io packages; public security, support, compatibility, and migration documentation.

Verification:

- Confirm tag target, artifact digests, signatures, SBOM, provenance, and pentest evidence exactly match the approved final candidate.

Exit criteria:

- Every definition-of-done item in the implementation plan is evidenced and no release blocker remains.
- `v1.0.0 implementation stop reached. Run pentest for this exact commit.`

## Optional post-1.0 Skrifheim roadmap

Entry conditions: Aetherheim 1.0 and Skrifheim 1.0 are stable; relevant Skrifheim extension contracts are frozen; exact versions pass dependency admission and joint review; Standard builds omit the integration; migration and rollback exist; and the joint threat model has passed independent review. These versions are not commitments until those conditions hold.

### v1.1.0 — Optional Integration Repository

Status: blocked by post-1.0 entry conditions.

Goal: Keep Skrifheim absent from Standard builds.

Deliverables:

- Separate bridge workspace, exact compatibility manifest, joint threat model, omission test, and no raw Skrifheim types in domain crates.

Verification:

- Standard build/runtime equivalence and dependency omission tests pass.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.1.0 implementation stop reached. Run pentest for this exact commit.`

### v1.2.0 — Endpoint Identity and Negotiation

Status: blocked by post-1.0 entry conditions.

Goal: Connect to an intended compatible Skrifheim deployment without writes.

Deliverables:

- Authenticated transport, endpoint pinning, versions/capabilities, least-privilege discovery, redacted health, timeout, and circuit break.

Verification:

- Wrong identity/version, downgrade, timeout, and unavailable endpoint fail closed.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.2.0 implementation stop reached. Run pentest for this exact commit.`

### v1.3.0 — Actor and Workload Bridge

Status: blocked by post-1.0 entry conditions.

Goal: Map principals without duplicating identity ownership.

Deliverables:

- Actor/effective actor/executor, assurance/revocation epochs, service/workload, delegation, scheduled intent, and import attribution.

Verification:

- Every command resolves an unambiguous chain; private account fields are not shared by default.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.3.0 implementation stop reached. Run pentest for this exact commit.`

### v1.4.0 — Witness Mode

Status: blocked by post-1.0 entry conditions.

Goal: Anchor evidence while conventional storage remains authoritative.

Deliverables:

- Outbox consumer, audit/release/package/backup roots, initial anchor, receipts, lag/retry, and precise UI language.

Verification:

- Crash/retry loses no logical witness event and no claim implies authoritative storage.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.4.0 implementation stop reached. Run pentest for this exact commit.`

### v1.5.0 — Witness-Gated Publication

Status: blocked by post-1.0 entry conditions.

Goal: Require fresh anchoring for selected channels.

Deliverables:

- Receipt requirement, maximum age, timeout, explicit override approval, off-node witness, and last-valid fallback.

Verification:

- No gated channel advances without receipt or audited exception.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.5.0 implementation stop reached. Run pentest for this exact commit.`

### v1.6.0 — Witness Verification UX

Status: blocked by post-1.0 entry conditions.

Goal: Make witness evidence independently useful.

Deliverables:

- Lookup/verify API, offline bundle, auditor dashboard, timeline, gap/fork warning, public release option, and scoped disclosure.

Verification:

- Independent offline verification succeeds from declared trust roots.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.6.0 implementation stop reached. Run pentest for this exact commit.`

### v1.7.0 — Fact Schema Catalog

Status: blocked by post-1.0 entry conditions.

Goal: Compile CMS commands deterministically into stable fact intents.

Deliverables:

- Namespaces, revision-root profile, size limits, actor/evidence rules, schema roots, migrations, and fixtures.

Verification:

- Equivalent commands compile identically and incompatible schemas fail.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.7.0 implementation stop reached. Run pentest for this exact commit.`

### v1.8.0 — World Mapping

Status: blocked by post-1.0 entry conditions.

Goal: Map sites and environments to bounded worlds.

Deliverables:

- Draft/review/production/recovery roles, fork lifecycle, protected production, preview authority, quotas, and cleanup.

Verification:

- Complete branch review never mutates production.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.8.0 implementation stop reached. Run pentest for this exact commit.`

### v1.9.0 — Verified Content Ingest

Status: blocked by post-1.0 entry conditions.

Goal: Make a narrow content slice authoritative.

Deliverables:

- Canonical compiler, schema/policy/world binding, actor authority, audit intent, receipt, idempotency, and status lookup.

Verification:

- Reference create/edit/delete/restore exists only through verified ingest.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.9.0 implementation stop reached. Run pentest for this exact commit.`

### v1.10.0 — Projection Journal

Status: blocked by post-1.0 entry conditions.

Goal: Build disposable read models from committed authority.

Deliverables:

- Authenticated feed, PostgreSQL/SQLite projections, watermark, schema version, rebuild, quarantine, and no reverse writes.

Verification:

- Deleting and rebuilding projections yields equivalent authorised models.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.10.0 implementation stop reached. Run pentest for this exact commit.`

### v1.11.0 — Authorised Management Reads

Status: blocked by post-1.0 entry conditions.

Goal: Bind private reads to actor, purpose, policy, and snapshot.

Deliverables:

- Query context, protected redaction, permit reference, freshness selection, revocation, and long-read revalidation.

Verification:

- No private field returns through stale or unauthorised context.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.11.0 implementation stop reached. Run pentest for this exact commit.`

### v1.12.0 — Atomic Publication

Status: blocked by post-1.0 entry conditions.

Goal: Use world promotion for strict publication and rollback.

Deliverables:

- Release candidate, approvals, promotion, rollback-as-promotion, proof, scheduling, and no-half-published behavior.

Verification:

- Release visibility is atomic under retry, crash, and stale approval.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.12.0 implementation stop reached. Run pentest for this exact commit.`

### v1.13.0 — Public Projection

Status: blocked by post-1.0 entry conditions.

Goal: Serve verified releases without private-world access.

Deliverables:

- Sanitised projection, release cache roots, render manifests, last-valid serving, and verifier.

Verification:

- Public gateway credentials cannot access authoring worlds.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.13.0 implementation stop reached. Run pentest for this exact commit.`

### v1.14.0 — Media Provenance

Status: blocked by post-1.0 entry conditions.

Goal: Bind originals, quarantine, derivatives, rights, and takedown.

Deliverables:

- Upload and transform facts, worker identity, evidence, licence/consent, cache invalidation, and erasure handling.

Verification:

- Every public derivative traces to an allowed source and transform.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.14.0 implementation stop reached. Run pentest for this exact commit.`

### v1.15.0 — Multilingual Provenance

Status: blocked by post-1.0 entry conditions.

Goal: Bind translation to exact sources and policy.

Deliverables:

- Translator/reviewer, method, glossary/model, locale routes, stale edges, and release policy.

Verification:

- Stale translations cannot silently enter strict releases.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.15.0 implementation stop reached. Run pentest for this exact commit.`

### v1.16.0 — Quorum Workflows

Status: blocked by post-1.0 entry conditions.

Goal: Require precise multi-party approval.

Deliverables:

- Roles, thresholds, self-approval policy, revocation, expiry, separation of duties, and break-glass boundary.

Verification:

- Missing, stale, replayed, or conflicting approvals cannot publish.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.16.0 implementation stop reached. Run pentest for this exact commit.`

### v1.17.0 — Community Domains

Status: blocked by post-1.0 entry conditions.

Goal: Map forms, memberships, comments, moderation, and protected reads.

Deliverables:

- Consent/submission, entitlement, comment revision, moderation/appeal, privacy, and public projection rules.

Verification:

- Personal/community data remains policy-bound.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.17.0 implementation stop reached. Run pentest for this exact commit.`

### v1.18.0 — Extension Proofs

Status: blocked by post-1.0 entry conditions.

Goal: Bind package, grant, invocation, command, and render effects.

Deliverables:

- Package/grant facts, host-generated receipts, revocation cone, and omission tests.

Verification:

- Plugins cannot mint actor, policy, or authority proof.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.18.0 implementation stop reached. Run pentest for this exact commit.`

### v1.19.0 — AI Derivation

Status: blocked by post-1.0 entry conditions.

Goal: Track AI permits, artifacts, review, and invalidation cones.

Deliverables:

- Exact source, provider/model, worker, tool transcript root, transfer policy, review promotion, and revocation.

Verification:

- Unreviewed AI output cannot become authoritative or public.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.19.0 implementation stop reached. Run pentest for this exact commit.`

### v1.20.0 — Commerce Authority

Status: blocked by post-1.0 entry conditions.

Goal: Map order, stock, payment, and journal invariants.

Deliverables:

- Product/price/order/inventory/payment/refund facts, serializable transitions, provider evidence, and compensations.

Verification:

- Crash/replay creates no duplicate commit or silent monetary mutation.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.20.0 implementation stop reached. Run pentest for this exact commit.`

### v1.21.0 — Data Passports

Status: blocked by post-1.0 entry conditions.

Goal: Compile restrictions for source and derived data.

Deliverables:

- Site/content/field/media/member/commerce passports and search/AI/backup/projection inheritance.

Verification:

- Unlabelled protected data cannot enter derived systems in strict mode.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.21.0 implementation stop reached. Run pentest for this exact commit.`

### v1.22.0 — Operation Passports

Status: blocked by post-1.0 entry conditions.

Goal: Plan reads, publish, AI, index, export, backup, restore, and installation.

Deliverables:

- Allow/constrain/redact/approve/declassify/deny outcomes with safe explanations.

Verification:

- Stale law/policy epochs and insufficient evidence fail.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.22.0 implementation stop reached. Run pentest for this exact commit.`

### v1.23.0 — Retention and Erasure

Status: blocked by post-1.0 entry conditions.

Goal: Implement consent, scoped holds, deletion, and crypto-erasure.

Deliverables:

- Receipts, jobs, key-slot removal, tombstones, minimal proof, backup propagation, and legal hold.

Verification:

- All configured readable paths disappear without reproducing erased data in proofs.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.23.0 implementation stop reached. Run pentest for this exact commit.`

### v1.24.0 — Protected Read Permits

Status: blocked by post-1.0 entry conditions.

Goal: Make high-assurance data release explicit.

Deliverables:

- Durable permit, batch precision, break-glass one-time grant, external alert, and review.

Verification:

- Mandatory-audit failure prevents protected release.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.24.0 implementation stop reached. Run pentest for this exact commit.`

### v1.25.0 — Authority Backup and Restore

Status: blocked by post-1.0 entry conditions.

Goal: Bind strict backups, exports, and isolated restores.

Deliverables:

- Destination passports, proof manifests, declassification, offline verification, and promotion receipts.

Verification:

- Every strict operation has a complete authority chain.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.25.0 implementation stop reached. Run pentest for this exact commit.`

### v1.26.0 — Compliance Evidence Bundles

Status: blocked by post-1.0 entry conditions.

Goal: Produce scoped reproducible auditor evidence.

Deliverables:

- Auditor profiles, control mapping, source locks, signed snapshots, redaction, and verifier.

Verification:

- Evidence verifies without unrestricted CMS/database access.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.26.0 implementation stop reached. Run pentest for this exact commit.`

### v1.27.0 — High-Assurance Deployment

Status: blocked by post-1.0 entry conditions.

Goal: Separate processes, keys, networks, and trust roots.

Deliverables:

- Scoped KMS/HSM boundary, external freshness/audit anchors, offline registry, air gap, and runbooks.

Verification:

- Public gateway/renderer/plugin compromise grants no canonical authority.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.27.0 implementation stop reached. Run pentest for this exact commit.`

### v1.28.0 — Conventional-to-Witness Migration

Status: blocked by post-1.0 entry conditions.

Goal: Move an existing site into Witness Mode truthfully.

Deliverables:

- Preflight, source root, initial anchor, catch-up, gates, rollback, and activation proof.

Verification:

- No downtime or retroactive-signature claim occurs.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.28.0 implementation stop reached. Run pentest for this exact commit.`

### v1.29.0 — Witness-to-Authoritative Migration

Status: blocked by post-1.0 entry conditions.

Goal: Perform explicit authority cutover.

Deliverables:

- AHAF conversion, identity mapping, import-attributed facts, shadow reads, final delta, reconciliation, and cutover proof.

Verification:

- Counts, roots, media, and relationships reconcile; omissions are reported.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.29.0 implementation stop reached. Run pentest for this exact commit.`

### v1.30.0 — Endurance and Failure Campaign

Status: blocked by post-1.0 entry conditions.

Goal: Qualify strict operation under sustained faults.

Deliverables:

- 24/72-hour runs, outage, projection loss, key/provider failure, audit exhaustion, witness lag, restore, crash, and tamper matrix.

Verification:

- No loss, bypass, duplicate commit, broken proof chain, or unrecoverable divergence.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.30.0 implementation stop reached. Run pentest for this exact commit.`

### v1.31.0 — Independent Review

Status: blocked by post-1.0 entry conditions.

Goal: Complete external protocol, crypto, privacy, migration, and operational review.

Deliverables:

- Pentest, design review, tabletop, remediation, retest, risk ownership, and public-safe summary.

Verification:

- No unresolved critical/high issue; accepted risks have owners and expiry.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.31.0 implementation stop reached. Run pentest for this exact commit.`

### v1.32.0 — Verified Profile GA

Status: blocked by post-1.0 entry conditions.

Goal: Declare optional production support without changing defaults.

Deliverables:

- Stable matrix, documentation, reference deployments, compatibility policy, incident process, evidence pack, and Standard regression proof.

Verification:

- Authoritative Mode is optional and supported; Standard remains default and unchanged.
- Repeat Standard, Witness, and Authoritative conformance as applicable, plus the inherited human-controlled pentest gate.

Exit criteria:

- Standard Mode remains independently buildable and behaviorally unchanged.
- `v1.32.0 implementation stop reached. Run pentest for this exact commit.`

## Roadmap maintenance rule

A release is split whenever its implementation, review, verification, or pentest scope is no longer comfortably bounded. New security patches use `v0.N.P` or `v1.N.P` and must include the same sections and pentest handoff stop. Planning numbers may move before implementation; tagged history never does. Individual pentests remain the default; only an explicit user instruction creates a batch, and no batch may exceed 15 listed releases.

Every requirement, threat, support claim, migration, recovery action, manual
review, and executable scenario has one owning milestone in the foundation
registry. New discoveries are inserted at the earliest safe dependency point,
not hidden in `v0.130.0`, a release candidate, or a generic hardening stop.
Admission, semantic implementation, and live qualification remain separate for
external security foundations and providers. Integration milestones may join
earlier evidence, but do not absorb unfinished subsystem behavior.

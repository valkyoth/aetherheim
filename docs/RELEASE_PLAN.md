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

- Versioned document, block, inline span, property, slot, reference, direction, locale, and provenance nodes.

Verification:

- Round-trip arbitrary bounded trees; reject depth/work exhaustion; preserve unknown optional blocks.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.23.0 implementation stop reached. Run pentest for this exact commit.`

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

- Principals, resources, actions, attributes, relationships, explicit deny, constrained allow, redaction, approval, and more-evidence outcomes.

Verification:

- Model/sweep deny precedence, tenant scope, field/locale context, stale epochs, and incomplete evidence.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.28.0 implementation stop reached. Run pentest for this exact commit.`

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

- Snapshot/read context, staged writes, expected revisions, outbox coupling, commit status, and rollback semantics.

Verification:

- Interleaving model tests cover conflicts, ambiguous commits, rollback, and read-after-write.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.38.0 implementation stop reached. Run pentest for this exact commit.`

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

## Phase 4 — SQLite and local operation

### v0.41.0 — SQLite Wire and File Boundary

Status: planned.

Goal: Define first-party SQLite integration scope safely.

Deliverables:

- Database-file ownership, native-library/process boundary decision, version negotiation, path safety, locking assumptions, and threat review.

Verification:

- Reject wrong library identity/version, unsafe paths, unsupported modes, and ambiguous ownership.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.41.0 implementation stop reached. Run pentest for this exact commit.`

### v0.42.0 — SQLite Statement Protocol

Status: planned.

Goal: Implement bounded statement preparation and parameter binding.

Deliverables:

- First-party FFI/process adapter crate, typed parameters, exact result decoding, limits, cancellation, and redacted errors.

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

## Phase 5 — Production storage, archives, jobs, blobs, and cache

### v0.51.0 — PostgreSQL Protocol Admission

Status: planned.

Goal: Establish a first-party production database boundary.

Deliverables:

- Protocol/version scope, authentication-provider interface, TLS/proxy assumption, framing budgets, cancellation, and server identity policy.

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

### v0.53.0 — PostgreSQL Content and Identity Stores

Status: planned.

Goal: Reach portable authoritative semantics on PostgreSQL.

Deliverables:

- Schemas, constraints, revisions, relationships, identity/session separation, outbox, and tenant/site scoping.

Verification:

- Shared conformance, concurrency, deadlock/retry, isolation, and explain-plan budget tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.53.0 implementation stop reached. Run pentest for this exact commit.`

### v0.54.0 — PostgreSQL Jobs, Audit, and Operations

Status: planned.

Goal: Complete production-reference provider behavior.

Deliverables:

- Leased jobs, scheduler, chained audit, migrations, online-index strategy, pooling limits, health, backup/PITR hooks.

Verification:

- Crash/recovery, lease contention, audit exhaustion, migration, and operational failover fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.54.0 implementation stop reached. Run pentest for this exact commit.`

### v0.55.0 — MariaDB Protocol and Session

Status: planned.

Goal: Establish a separate first-party MariaDB boundary.

Deliverables:

- Handshake/authentication-provider boundary, capability negotiation, typed parameters, results, transaction state, cancellation, and limits.

Verification:

- Malformed handshake, downgrade, injection, desynchronisation, timeout, and reconnect tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.55.0 implementation stop reached. Run pentest for this exact commit.`

### v0.56.0 — MariaDB Store Parity

Status: planned.

Goal: Implement portable storage semantics on MariaDB.

Deliverables:

- Provider-owned schema, content, identity, outbox, jobs, audit, migration, JSON/index strategy, and capability report.

Verification:

- Shared conformance plus provider deadlock, collation, index, and retry fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.56.0 implementation stop reached. Run pentest for this exact commit.`

### v0.57.0 — MongoDB Protocol and Session

Status: planned.

Goal: Establish a bounded first-party document-provider boundary.

Deliverables:

- Wire framing, authentication-provider boundary, typed document encoding, transactions, cursor limits, cancellation, and topology scope.

Verification:

- Malformed frames, document bombs, injection-shaped values, stale cursors, timeout, and topology change tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.57.0 implementation stop reached. Run pentest for this exact commit.`

### v0.58.0 — MongoDB Store Parity

Status: planned.

Goal: Implement portable semantics without pretending documents equal the logical model.

Deliverables:

- Mappings, transactions where required, indexes, outbox, jobs, audit, query translation, and explicit unsupported capabilities.

Verification:

- Shared conformance, multi-document failure, change-feed duplication, isolation, and rebuild tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.0 implementation stop reached. Run pentest for this exact commit.`

### v0.58.1 — SurrealDB Connection Admission

Status: planned.

Goal: Establish a bounded SurrealDB provider boundary without coupling domain contracts to provider-specific record or graph semantics.

Deliverables:

- Supported deployment/version scope, reviewed client and transport decision, authentication and TLS assumptions, namespace/database selection, bounded request and response handling, cancellation, timeout, and server identity policy.

Verification:

- Wrong-server, authentication failure, namespace/database isolation, malformed or oversized response, timeout, cancellation, reconnect, and version-compatibility tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.1 implementation stop reached. Run pentest for this exact commit.`

### v0.58.2 — SurrealDB Store Parity

Status: planned.

Goal: Implement the portable storage contract on SurrealDB while keeping provider-specific record, relation, and query behavior behind the adapter.

Deliverables:

- Provider-owned schema and migrations, content, identity, outbox, jobs, audit, typed query translation, indexes, transaction boundaries, capability report, and explicit unsupported transformations.

Verification:

- Shared conformance, tenant and namespace isolation, transaction failure, relation mapping, query-budget, reconnect, migration, and rebuild tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.58.2 implementation stop reached. Run pentest for this exact commit.`

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

### v0.60.2 — Valkey Cache Adapter

Status: planned.

Goal: Provide Valkey as the first optional remote cache implementation.

Deliverables:

- Reviewed client/transport admission, TLS and authentication, server identity, command allowlist, namespaced keys, bounded pooling and pipelining, cancellation, timeout, expiry, invalidation, health, metrics, and operational guidance.

Verification:

- Shared cache conformance plus malformed response, wrong server, credential redaction, cross-tenant key, disconnect, partition, failover, eviction, latency spike, memory pressure, and recovery tests pass against supported Valkey versions.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.2 implementation stop reached. Run pentest for this exact commit.`

### v0.60.3 — OpenBao Client Admission

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
- `v0.60.3 implementation stop reached. Run pentest for this exact commit.`

### v0.60.4 — OpenBao Startup Secret Bootstrap

Status: planned.

Goal: Optionally move explicitly selected startup environment secrets into OpenBao before the Aetherheim server starts.

Deliverables:

- Separate bootstrap executable, explicit variable-to-KV-path map, bounded `sanitization` ingestion, no prefix-wide environment scan, idempotent conflict policy, partial-write journal, redacted report, narrow/expiring bootstrap authority, `env_clear` child launch, and secret-reference handoff.

Verification:

- Unknown-variable, path injection, duplicate target, existing-value, partial write, network loss, wrong server, auth expiry, log/error/panic redaction, child-environment, process-memory lifecycle, retry, and rollback fixtures pass without unsafe post-thread environment mutation.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.4 implementation stop reached. Run pentest for this exact commit.`

### v0.60.5 — Live Storage Provider Matrix

Status: planned.

Goal: Prove storage and cache support against launched services rather than protocol models alone.

Deliverables:

- Reproducible live fixtures for every declared SQLite, PostgreSQL, MariaDB, MongoDB, SurrealDB, and Valkey version/topology; clean provisioning, health, test isolation, redacted logs, evidence manifest, and one command integrated into `scripts/acceptance.sh all`.

Verification:

- The same black-box storage journey runs against every provider: initialize, migrate, content/identity/session records, relationships, jobs/outbox/audit, concurrent access, restart, failure/recovery, export/import, and cross-provider round trip; adapter-specific failure cases also run live.
- Deliberately remove each service/runtime and prove the release gate fails rather than skips or substitutes a mock.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- No database, topology, or Valkey version appears in the supported matrix without current live acceptance evidence.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.60.5 implementation stop reached. Run pentest for this exact commit.`

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

### v0.69.0 — Integration Events and Webhooks

Status: planned.

Goal: Deliver signed, replay-resistant external events.

Deliverables:

- Subscription scope, payload versions, delivery IDs, destination policy, signature-provider boundary, retry/dead letter, and replay control.

Verification:

- SSRF/rebinding, redirect, private-address, response-size, signature, replay, and poison-delivery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.69.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.76.0 — TOTP and Recovery

Status: planned.

Goal: Add bounded fallback and non-catastrophic recovery.

Deliverables:

- TOTP provider boundary, hashed one-time recovery codes, recovery approvals, post-recovery restricted session, and notifications.

Verification:

- Replay, brute-force budget, code disclosure, clock skew, stronger-credential preservation, and lockout recovery tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.76.0 implementation stop reached. Run pentest for this exact commit.`

### v0.77.0 — OAuth/OIDC and Service Tokens

Status: planned.

Goal: Support delegated clients with explicit trust.

Deliverables:

- Authorization-code/PKCE state, issuer/audience/nonce, scoped short-lived tokens, refresh replay, hashed PATs, and service constraints.

Verification:

- Mix-up, redirect, audience, tenant, scope, refresh replay, expiry, and revocation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.77.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.79.0 — ABAC/ReBAC Enforcement

Status: planned.

Goal: Apply field, locale, workflow, relationship, and context policy.

Deliverables:

- Central decision service, explicit deny, relationship proof, field projection filter, decision cache key, and explanation.

Verification:

- Cache-omission model tests and cross-context denial suites prove no policy dimension is lost.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.79.0 implementation stop reached. Run pentest for this exact commit.`

### v0.80.0 — Security Profiles and Admin Isolation

Status: planned.

Goal: Turn security profiles into tested policy templates.

Deliverables:

- Personal, Standard, Hardened, Regulated, and Air-gapped presets; separate admin origin; egress defaults; override risk diff; recovery.

Verification:

- Profile conformance, origin/cookie isolation, egress, override audit, and usable recovery tests pass.
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

## Phase 8 — Rendering, administration, editor, themes, and search

### v0.81.0 — Render Intermediate Representation

Status: planned.

Goal: Compile content and templates to a safe typed render plan.

Deliverables:

- Typed nodes, props, slots, escaping context, dependency records, bounded loops/queries, error boundaries, and work budgets.

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

### v0.83.0 — Sanitised Embedded Markup

Status: planned.

Goal: Admit explicitly authorised legacy markup under a versioned policy.

Deliverables:

- First-party parser/sanitizer scope, element/attribute/URL policy, resource budgets, inert fallback, and provenance.

Verification:

- Differential browser corpus, mutation fuzzing, nesting bombs, URL tricks, and policy-upgrade fixtures pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.83.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.85.0 — Server Renderer and Cache

Status: planned.

Goal: Render public HTML with complete visibility partitioning.

Deliverables:

- Release-root render context, theme digest, dependency graph, ETag, page cache, tag invalidation, and stale policy.

Verification:

- Tenant/locale/viewer/release cache mixing, invalidation race, failure fallback, and deterministic fixture tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.85.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.92.0 — Media Structure Admission

Status: planned.

Goal: Parse owned metadata under strict budgets.

Deliverables:

- First-party envelope parsers, dimensions/pages/frames/duration/archive expansion limits, filename normalization, and rejection report.

Verification:

- Malformed corpora, decompression-shaped bombs, deep metadata, type mismatch, and allocation-failure tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.92.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.95.0 — Digital Asset Management

Status: planned.

Goal: Track rights, accessibility, usage, and lifecycle.

Deliverables:

- Localized alt/caption/transcript, licence/attribution/expiry, consent reference, classification, collections, usage graph, replacement, and holds.

Verification:

- Rights expiry, deletion, relink, locale fallback, accessibility policy, and complete-usage reporting tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.95.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.98.0 — Component Binary Validator

Status: planned.

Goal: Reject malformed or unsupported component binaries before execution.

Deliverables:

- First-party bounded WebAssembly/component framing parser, section limits, canonical validation, import/export allowlists, and compatibility report.

Verification:

- Official-format fixtures, mutations, deep sections, integer overflow, duplicate sections, and unknown-required feature tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.98.0 implementation stop reached. Run pentest for this exact commit.`

### v0.99.0 — First-Party Component Runtime Core

Status: planned.

Goal: Execute a deliberately small admitted component subset safely.

Deliverables:

- Validated instruction subset, typed values, memory/table bounds, fuel, call depth, traps, deterministic mode, and no host imports by default.

Verification:

- Conformance vectors, differential reference tooling outside Cargo, fuzzing, timeout, memory escape, and trap isolation pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.99.0 implementation stop reached. Run pentest for this exact commit.`

### v0.100.0 — Component Host Calls and Quotas

Status: planned.

Goal: Expose only typed capability-checked operations.

Deliverables:

- Invocation identity, handle table, host-call budget, deadline, async/job proposal, namespaced state, secret operations, and output validation.

Verification:

- Forged handle, stale grant, reentrancy, quota, timeout, proposal substitution, and host-crash containment tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.100.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.111.0 — Contacts and Segments

Status: planned.

Goal: Add a privacy-aware lightweight CRM.

Deliverables:

- Contacts, organisations, provenance, consent, classification, duplicate merge, activity, segments, import/export, and deletion propagation.

Verification:

- Merge and segment isolation, stale consent, duplicate resolution, deletion, and sensitive-field tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.111.0 implementation stop reached. Run pentest for this exact commit.`

### v0.112.0 — Transactional Mail

Status: planned.

Goal: Send application mail through bounded provider contracts.

Deliverables:

- Template/text alternative, recipient source, provider identity, secret handle, idempotency, bounce/complaint, suppression, rate, and redaction.

Verification:

- Header/template injection, duplicate send, suppression bypass, provider replay, and secret logging tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.112.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.114.0 — Memberships and Comments

Status: planned.

Goal: Provide entitlements and moderated community behavior.

Deliverables:

- Tiers, invitations, content gates, profiles, grace state, threaded comments, moderation, reports, appeals, and notifications.

Verification:

- Cache/API entitlement isolation, sanction bypass, pseudonym privacy, moderation audit, and deletion tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.114.0 implementation stop reached. Run pentest for this exact commit.`

### v0.115.0 — Automation and Bookings

Status: planned.

Goal: Add durable bounded workflows and time-aware reservations.

Deliverables:

- Trigger/condition/action graph, permissions, loops, dry run, approval, services/resources/availability/capacity, waitlist, recurrence, and reminders.

Verification:

- Loop, replay, partial failure, DST, concurrency, duplicate booking, capacity, and cancellation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.115.0 implementation stop reached. Run pentest for this exact commit.`

### v0.116.0 — Catalogue and Price Books

Status: planned.

Goal: Create exact content-backed products and prices.

Deliverables:

- Products, variants, options, SKUs, channels, currency/scale, price books, tax display intent, and immutable price explanation roots.

Verification:

- Decimal/rounding sweeps, SKU uniqueness, visibility, stale price, and snapshot tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.116.0 implementation stop reached. Run pentest for this exact commit.`

### v0.117.0 — Cart and Checkout

Status: planned.

Goal: Build an idempotent accessible checkout state machine.

Deliverables:

- Guest/member carts, line calculation, address/contact, shipping/tax quote contracts, expiry, reservation intent, and duplicate-submit protection.

Verification:

- Replay/concurrency, stale price, quote failure, accessibility, privacy, and inconsistent-total tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.117.0 implementation stop reached. Run pentest for this exact commit.`

### v0.118.0 — Orders and Monetary Journal

Status: planned.

Goal: Make accepted orders and monetary changes append-oriented.

Deliverables:

- Order state machine, calculation snapshot, payment intent, balanced journal model, adjustments, compensating entries, reason, approval, and audit.

Verification:

- Model checking covers retry, partial failure, illegal transition, imbalance, repricing, and concurrent commands.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.118.0 implementation stop reached. Run pentest for this exact commit.`

### v0.119.0 — Inventory and Reservations

Status: planned.

Goal: Protect stock invariants under concurrency.

Deliverables:

- Locations, on-hand/available/reserved/allocated/damaged states, atomic reservation, expiry, bundles, backorders, oversell policy, and reconciliation.

Verification:

- Concurrent checkout cannot oversell unless declared; expiry, crash, replay, bundle, and reconciliation tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.119.0 implementation stop reached. Run pentest for this exact commit.`

### v0.120.0 — Payments, Refunds, Fulfilment, and Subscriptions

Status: planned.

Goal: Integrate providers without surrendering commerce authority.

Deliverables:

- Tokenised/hosted payments, signature-provider webhook checks, capture/refund/dispute, shipping/tax/fulfilment, returns, invoices, recurring entitlements, and digital grants.

Verification:

- No raw card data; replay/out-of-order webhooks, duplicate refund, provider outage, entitlement, and revoked-download tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.120.0 implementation stop reached. Run pentest for this exact commit.`

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

### v0.122.0 — Privacy and Accessibility Packs

Status: planned.

Goal: Provide GDPR/ePrivacy, regional privacy, WCAG 2.2, and EAA-oriented technical controls.

Deliverables:

- Consent center, script gating, DSAR, retention/erasure, opt-out, accessibility authoring checks, manual review, exceptions, and evidence export.

Verification:

- End-to-end consent, withdrawal, DSAR, erasure, script blocking, keyboard, screen-reader script, and non-claim tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.122.0 implementation stop reached. Run pentest for this exact commit.`

### v0.123.0 — Regulated and Commerce Packs

Status: planned.

Goal: Provide HIPAA, NIS2, PCI DSS, SOC/ISO evidence, and AI governance support.

Deliverables:

- PHI/access presets, incidents, suppliers, card-scope prevention, checkout integrity inventory, control mapping, AI provenance, and human review.

Verification:

- Profile conformance proves controls while every UI/API explicitly avoids automatic compliance claims.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.123.0 implementation stop reached. Run pentest for this exact commit.`

### v0.124.0 — WordPress and WooCommerce Import

Status: planned.

Goal: Provide a resumable staged migration from the primary source ecosystem.

Deliverables:

- Users/roles, content/types, blocks, taxonomies, comments, media, menus, metadata, redirects, orders/products mapping, source IDs, and issue report.

Verification:

- Large hostile fixtures resume safely, preserve source attribution/URLs, quarantine bytes, and report rather than drop unsupported data.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.124.0 implementation stop reached. Run pentest for this exact commit.`

### v0.125.0 — Other and Generic Importers

Status: planned.

Goal: Cover Drupal, Joomla, Ghost, Wix-supported exports, static sites, Markdown, CSV, JSON, RSS, and media folders.

Deliverables:

- Mapping DSL, crawler permission, source digest, conversion provenance, checkpoints, validation, redirects, and complete limitations report.

Verification:

- Each source corpus exercises malformed input, retries, encoding, relationships, media, and unsupported-field reporting.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.125.0 implementation stop reached. Run pentest for this exact commit.`

### v0.126.0 — Backup, Restore, and Disaster Recovery

Status: planned.

Goal: Make recoverability demonstrated rather than assumed.

Deliverables:

- Encrypted-provider backup boundary, database/blob/config/package manifests, AHAF, chunk roots, verification jobs, isolated restore, promotion, and RPO/RTO report.

Verification:

- Missing/substituted chunks, wrong roots/keys, partial backup, clean-environment restore, and disaster rehearsal pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.126.0 implementation stop reached. Run pentest for this exact commit.`

### v0.127.0 — Production Packaging and Platform Qualification

Status: planned.

Goal: Ship signed artifacts for every supported platform without crates.io.

Deliverables:

- Standalone archives, OCI images, Compose, system service guidance, platform installers/bundles, rootless operation, SBOM, provenance, checksums, and air-gap bundle.

Verification:

- Clean Linux/Windows/BSD/macOS installs, Android/iOS library integration, rootless container smoke, artifact verification, and uninstall tests pass.
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

### v0.128.0 — Upgrade, Rollback, and Long-Run Qualification

Status: planned.

Goal: Prove every supported installation can evolve safely.

Deliverables:

- Expand/contract migrations, compatibility window, drain, canary guidance, job/plugin compatibility, rollback automation, 24/72-hour and defined long soak.

Verification:

- Upgrade from every fixture under injected failure either completes or rolls back; no loss, duplicate effect, or secret leak.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.0 implementation stop reached. Run pentest for this exact commit.`

### v0.128.1 — Cluster Identity And Readiness

Status: planned.

Goal: Let multiple Aetherheim nodes identify compatible peers and expose truthful routing readiness.

Deliverables:

- Stable installation identity, ephemeral boot identity, authenticated peer identity, bounded membership view, protocol/schema compatibility window, liveness/readiness separation, dependency readiness, heartbeat budgets, and readiness withdrawal before drain.

Verification:

- Forged/duplicate/stale node, replay, incompatible version, clock movement, delayed heartbeat, dependency loss, partial startup, process pause, shutdown, and rolling-membership tests pass.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.1 implementation stop reached. Run pentest for this exact commit.`

### v0.128.2 — Fenced Cluster Work And Failure Recovery

Status: planned.

Goal: Share durable jobs, singleton duties, sessions, and invalidations safely across active application nodes.

Deliverables:

- Shared authoritative state, lease epochs and fencing tokens, transactional claim, idempotency keys, reclaim policy, outbox consumption, session/revocation consistency, cache invalidation, migration ownership, and split-network fail-closed rules.

Verification:

- Kill/pause/partition every lease phase; duplicate, reorder, and delay messages; skew clocks; isolate cache/database/OpenBao; and prove stale workers are fenced, work is safely reclaimed, effects are idempotent, and authority never falls back to local memory.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Documentation states at-least-once/idempotent effects honestly and makes no exactly-once or home-grown consensus claim.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.2 implementation stop reached. Run pentest for this exact commit.`

### v0.128.3 — Active-Active Load And Failover Qualification

Status: planned.

Goal: Prove a supported multi-node deployment shares load and continues within declared limits when a node fails.

Deliverables:

- Reference two/three-node topologies, load-balancer discovery guidance, shared-provider requirements, capacity and quorum model, rolling upgrade/drain, cache/OpenBao degradation policy, disaster boundaries, metrics, alerts, and operator exercises.

Verification:

- Sustained balanced load, abrupt node loss, rolling restart, zone partition, stale proxy membership, thundering herd, provider slowdown, cache loss, secret-provider loss, recovery, and 24/72-hour soak tests meet declared availability and data-integrity objectives.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- Single-node operation remains supported and every multi-node availability claim names the required database, cache, secret-provider, and load-balancer assumptions.
- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.128.3 implementation stop reached. Run pentest for this exact commit.`

### v0.129.0 — Contract Freeze and Full Security Campaign

Status: planned.

Goal: Freeze 1.0 candidates only after ecosystem and migration evidence.

Deliverables:

- REST/event/theme/package/AHAF/proof contracts; semantic compatibility checker; complete threat refresh; broad fuzzing; tenant/cache isolation; commerce audit; external review.

Verification:

- Reproducible SDK/docs/artifacts and full security campaign have zero unresolved critical/high findings; blocking medium findings are fixed.
- Run the inherited repository, security, documentation, platform, and release-evidence gates.

Exit criteria:

- The stated behavior is implemented only for its documented scope, with migration and rollback evidence where state changes.
- `v0.129.0 implementation stop reached. Run pentest for this exact commit.`

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

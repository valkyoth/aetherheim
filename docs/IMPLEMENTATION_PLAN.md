# Aetherheim Implementation Plan

Status: planning document

Crate name: `aetherheim`

Licence: EUPL-1.2 for Aetherheim; independently authored themes and plugins
retain author-selected licences and are not required to use EUPL-1.2.

1.0 target: a serious production-ready, self-hostable content operating system
with structured content, safe rendering, secure administration, portable
storage, capability-contained extensions, multilingual and multisite support,
media, workflows, membership/publication features, commerce, backup/recovery,
and evidence-backed operations.

## Core Position

Aetherheim is not a literal WordPress rewrite. It keeps the approachable single
product while replacing ambient plugin authority, HTML-as-source content,
provider-specific domain semantics, weak session defaults, and untestable
global hooks.

The implementation begins as one modular monolith with separable `serve`,
`worker`, `scheduler`, and later `realtime` roles. Small sites can run one
binary. Larger installations can split roles without rewriting domain logic.

The browser UI, CLI, integrations, plugins, and future mobile clients use the
same typed application commands and queries. Storage and HTTP are adapters;
they do not define the domain.

## Final Decisions From The Idea Review

- Structured block documents are canonical; HTML and Markdown are render,
  import, or export formats.
- Browser administration uses opaque revocable server-side sessions, not JWTs
  by default.
- Plugins use versioned capability contracts and cannot receive raw database,
  filesystem, environment, socket, secret, or host-memory access.
- SQLite is the simple local default. PostgreSQL is the production reference.
  MariaDB, MongoDB, and SurrealDB become supported only through visible
  capability and conformance matrices.
- Remote cache offload is optional and non-authoritative. Valkey is the first
  named adapter and must remain safely bypassable when its cache class permits.
- Multi-node mode is optional, active-active at the application layer, and
  depends on shared qualified providers, fenced work, strict readiness, and
  tested failure recovery rather than a new home-grown consensus protocol.
- Fluxheim is an optional tested reverse-proxy/load-balancer deployment profile;
  direct serving and other reviewed proxies remain supported.
- Optional startup secret import uses the project-owned `openbao` crate through
  a dedicated bootstrap process. The normal server receives secret references,
  not a copied bulk environment.
- Aetherheim-owned secret memory uses `sanitization`. Direct and transitive
  `zeroize` are forbidden; sanitization depth follows data classification and
  measured cost rather than wrapping all content indiscriminately.
- Complete logical export/import is a core capability, not an afterthought.
- Commerce invariants stay in a first-party optional trusted module; provider
  connectors stay isolated.
- Media decoders run behind worker/process isolation. WASM is not forced onto
  workloads for which it is unsuitable.
- Compliance packs provide controls and evidence, never legal certification.
- AI remains optional, disabled by default, scoped, provenance-labelled, and
  unable to bypass normal validation or publication.
- Skrifheim is not integrated before Aetherheim 1.0. Proof-ready contracts are
  useful independently. Optional Witness Mode is the first post-1.0 step only
  after both projects and their relevant contracts are stable.

## Non-Negotiable Engineering Rules

- Pin and use the latest stable Rust; the foundation pin is `1.97.1`.
- Rust edition 2024 and Cargo resolver 3.
- Before every release, check the Rust stable manifest, CI action pins, and
  external Cargo security-tool versions. Update promptly for security fixes.
- External Rust crates are kept to the smallest practical set. Discuss every
  addition first; pin its exact current crates.io version; record purpose,
  scope, licence, and review date; audit features, maintenance, unsafe/native
  code, and transitives; and test it behind an explicit boundary.
- Every package has `publish = false`; crates.io publication is prohibited.
- Do not copy third-party source into the repository to evade dependency
  review.
- Prefer mature, reviewed foundations for cryptography, TLS, WebAuthn,
  database clients, Unicode, media codecs, and WebAssembly. Do not reimplement
  these merely to reduce the crate count. Keep each dependency behind a narrow
  Aetherheim-owned contract and remain fail closed until admission completes.
- Core domain, schema, query, policy, event, proof, and package contracts are
  `no_std`, adding `alloc` only where justified.
- Host, network, database, UI, process, and operating-system adapters use
  `std`.
- `unsafe` is forbidden by default. A future isolated crate may use it only
  after a dedicated release, written safety invariants, tests, Miri/sanitizer
  evidence, review, and pentest.
- Main crate `aetherheim` is a facade and product entry point, not the home of
  all implementation.
- Non-generated Rust source files must stay at or below 500 lines. Review for a
  split when a file approaches 300 lines.
- Every behavior is designed for unit, property, conformance, fuzz,
  integration, failure, migration, and end-to-end testing as applicable.
- Every implemented public or operational capability has a launchable
  black-box scenario against the real process or packaged artifact. Provider
  support additionally requires live supported-version matrices; mocks alone
  never establish that Aetherheim works.
- Every release updates documentation and release notes, then stops for the
  user-controlled individual or explicitly authorised cumulative pentest
  workflow. Codex never tags or pushes without the user's final instruction.

## Repository And Crate Strategy

The main implementation remains one repository for atomic changes and review.
The initial crates are deliberately small:

- `aetherheim`: facade and product binary;
- `aetherheim-core`: `no_std` shared modes and stable errors;
- `aetherheim-bounds`: `no_std` allocation-free input bounds;
- `aetherheim-ids`: `no_std` opaque identifier domains;
- `aetherheim-proof-core`: `no_std` assurance, attribution, and decision
  vocabulary without a Skrifheim dependency;
- `aetherheim-config`: typed host configuration;
- `aetherheim-testkit`: deterministic first-party fixtures.

Crates are added only as their first implementation milestone begins. Planned
boundaries include:

### Portable core

- `aetherheim-time`
- `aetherheim-value`
- `aetherheim-schema`
- `aetherheim-document`
- `aetherheim-query`
- `aetherheim-policy`
- `aetherheim-events`
- `aetherheim-api-types`
- `aetherheim-plugin-contracts`
- `aetherheim-theme-contracts`
- `aetherheim-archive`
- `aetherheim-provenance`
- `aetherheim-release-manifest`
- `aetherheim-evidence`
- `aetherheim-authority-api`

### Application domains

- `aetherheim-app`
- `aetherheim-content`
- `aetherheim-workflow`
- `aetherheim-routing`
- `aetherheim-localization`
- `aetherheim-multisite`
- `aetherheim-identity`
- `aetherheim-authorization`
- `aetherheim-session`
- `aetherheim-media`
- `aetherheim-search`
- `aetherheim-forms`
- `aetherheim-mail`
- `aetherheim-membership`
- `aetherheim-comments`
- `aetherheim-automation`
- `aetherheim-analytics`
- `aetherheim-commerce`
- `aetherheim-compliance`

### Adapters and delivery

- `aetherheim-storage`
- `aetherheim-storage-sqlite`
- `aetherheim-storage-postgres`
- `aetherheim-storage-mariadb`
- `aetherheim-storage-mongodb`
- `aetherheim-storage-surrealdb`
- `aetherheim-blob`
- `aetherheim-blob-local`
- `aetherheim-cache`
- `aetherheim-cache-valkey`
- `aetherheim-secrets`
- `aetherheim-secrets-openbao`
- `aetherheim-secret-bootstrap`
- `aetherheim-cluster`
- `aetherheim-proxy-trust`
- `aetherheim-jobs`
- `aetherheim-render`
- `aetherheim-theme`
- `aetherheim-plugin-host`
- `aetherheim-package`
- `aetherheim-api`
- `aetherheim-web`
- `aetherheim-admin`
- `aetherheim-server`
- `aetherheim-cli`

Adapter crate creation does not imply support. Each support claim requires the
provider-specific release and full conformance evidence.

## Dependency Direction

```text
delivery and process adapters
            |
            v
application services and domain modules
            |
            v
portable no_std contracts
```

Dependencies point inward. Portable crates do not import HTTP, storage,
process, platform, renderer, theme, plugin-host, or database adapters. Plugins
propose typed commands through host contracts; they never bypass application
services.

## Authority And Proof Boundary

Aetherheim 1.0 uses conventional storage. Proof-ready contracts include
actor/effective-actor/executor attribution, authentication assurance,
canonical command intent fields, revision roots, release manifests, render
artifact manifests, evidence references, audit roots, and operation receipts.

They must not claim signatures, legal compliance, or truth beyond the evidence
actually available. Imported author names remain `import-attributed`.

Post-1.0 integration, if admitted, lives outside core domain crates:

```text
Aetherheim domain command
        -> canonical transcript
        -> optional authority bridge
        -> external stable Skrifheim API
```

Skrifheim is never disguised as an ordinary CRUD storage adapter. Standard
builds must omit the bridge entirely.

## Storage Plan

Focused contracts replace one giant provider trait:

- metadata;
- content and revisions;
- identity and sessions;
- append-oriented audit;
- durable jobs and schedules;
- immutable blobs;
- search projections;
- ephemeral cache;
- locks/leases;
- secret-operation handles.

The domain emits a typed, bounded query AST. Adapters translate it. Raw SQL,
Mongo expressions, or provider query strings never enter normal client or
plugin APIs.

Support is layered:

1. deterministic in-memory/reference models;
2. SQLite zero-configuration adapter;
3. PostgreSQL production reference;
4. MariaDB parity;
5. MongoDB parity;
6. SurrealDB parity;
7. provider capability and performance evidence;
8. cross-provider archive migration.

Database work uses the smallest reviewed client/protocol foundation that meets
the security and portability requirements. Adapter work is still split into
admission, resource governance, transaction semantics, conformance, failure
recovery, and security releases. Support is not claimed merely because a
connection succeeds.

## Cache, Secrets, Cluster, And Edge Plan

- In-process caching is bounded and remains the simple default. Valkey provides
  optional shared cache offload behind the same conformance contract; cached
  values are reconstructible and never become authoritative state.
- OpenBao integration uses an admitted exact release of the `openbao` crate and
  only the required features. Environment import is an explicit allowlist in a
  short-lived bootstrap process that starts Aetherheim with a clean environment.
- Cluster nodes share authoritative database/session/job state, authenticate
  peers, use leases with fencing and idempotency, withdraw readiness before
  drain, and tolerate a failed node without claiming exactly-once execution.
- Proxy metadata is trusted only from configured peers. Fluxheim receives a
  tested profile for health, readiness, drain, retry, forwarding, TLS/mTLS,
  request bounds, and observability; it remains optional and out of process.

Detailed invariants and failure tests are in
[operations-topology.md](operations-topology.md). Secret classification,
OpenBao bootstrap, and the zeroize prohibition are in
[secret-memory-policy.md](secret-memory-policy.md).

## Platform Plan

From the first release, pure crates are checked across representative targets:

- Linux GNU and musl, x86-64 and AArch64;
- Windows GNU and MSVC;
- FreeBSD and NetBSD;
- macOS x86-64 and Apple Silicon;
- Android x86-64 and AArch64;
- iOS AArch64;
- a freestanding target for `no_std` portability evidence.

Host features may have platform-specific adapter crates, but public semantics
must remain consistent. Missing platform functionality fails explicitly. No
conditional compilation may silently weaken security.

Aesynx is a future platform. Current work maintains `no_std` contracts and
explicit host capabilities so a future adapter is possible, but makes no build
or runtime support claim before Aesynx stabilises.

## Security Programme

Security work is continuous, not a final phase:

1. write abuse cases and update the threat model;
2. define typed authority, resource, and data-classification boundaries;
3. add failing negative/adversarial tests;
4. implement the smallest portable behavior;
5. fuzz parser and state-machine boundaries;
6. test crash, retry, idempotency, rollback, and resource exhaustion;
7. update operator guidance and non-claims;
8. run all local and CI gates;
9. call out that the candidate is ready for the applicable pentest;
10. consume temporary root `PENTEST.md` findings when supplied, remediate,
    test, update the permanent report, and remove the scratch file;
11. after a green report, commit and wait for GitHub; fix and record any GitHub
    failures; and
12. tag and push only after the user explicitly instructs it.

Security-critical caches include every tenant, site, environment, locale,
visibility, policy epoch, release root, and viewer-class dimension. Identity,
publication, workflow, order, inventory, and audit state fail closed on
ambiguous authority.

Secrets, credentials, key material, and secret-bearing provider values use
bounded `sanitization` owners. Other sensitive buffers are assessed at their
ownership boundary and benchmarked; public content and bulk non-secret data are
not copied into sanitizing containers without a credible threat benefit.

## Test Strategy

- Unit tests live beside every pure rule.
- Cross-crate integration tests cover facade and application boundaries.
- Table and property sweeps cover bounded parsers and state transitions;
  external test tooling still requires the normal admission discussion.
- Deterministic golden fixtures freeze canonical encodings and public output.
- Shared conformance suites are mandatory for every storage, blob, search,
  theme, plugin, API, and platform adapter.
- Fuzz targets begin as first-party deterministic mutation harnesses; later
  compiler-integrated fuzzing is admitted as external tooling, never a product
  dependency.
- Failure injection covers crash points, partial I/O, clock changes, queue
  replay, stale policy, resource exhaustion, and corrupt projections.
- Cross-platform checks compile the portable core for every supported target;
  native runners execute platform-specific suites where available.
- Browser/UI testing includes keyboard-only and accessibility manual scripts.
- Backup verification is incomplete without isolated restore rehearsal.
- Performance evidence uses representative tenants, content, media, routes,
  policies, and concurrent writers, never only empty installations.
- `scripts/acceptance.sh all` is the stable executable acceptance entry point.
  It grows with implemented behavior and must never silently skip a required
  scenario because a service, credential, browser, platform, or tool is absent.
- Real Aetherheim processes exercise user and operator journeys through public
  CLI/API/browser boundaries, including success, denial, restart, and recovery.
- SQLite, PostgreSQL, MariaDB, MongoDB, and SurrealDB run the same live account,
  session, content, job, audit, migration, archive, and failure scenarios for
  every version/topology in their declared support matrices.
- Valkey, OpenBao, Fluxheim, multi-node, and other provider claims require
  launched services and real network interactions in addition to deterministic
  models and protocol fixtures.

The complete scenario and execution-tier contract is
[acceptance-testing.md](acceptance-testing.md).

## Documentation And Release Evidence

Every release maintains:

- `CHANGELOG.md`;
- a versioned file under `release-notes/`;
- architecture/behavior docs for new surfaces;
- threat-model and security-control deltas;
- migration and rollback notes;
- known limitations and explicit non-claims;
- a permanent individual report or link to an explicitly user-authorised batch
  report, with findings, remediations, retest, and later GitHub fixes preserved.

The complete release loop is [release-workflow.md](release-workflow.md).

Configuration, API, package, and archive schemas must eventually generate
reference documentation from the same source used by validation.

## Implementation Sequence

The authoritative sequence is [RELEASE_PLAN.md](RELEASE_PLAN.md). In broad
terms:

1. repository discipline and portable foundations;
2. canonical values, schemas, documents, queries, policy, events, and proof
   records;
3. conventional storage protocols, conformance, migrations, archives, jobs,
   and blobs;
4. content commands, revisions, workflows, routing, APIs, audit, and identity;
5. safe rendering, admin shell, editor, themes, media, and search;
6. capability contracts, first-party component runtime, isolated extension UI,
   packages, and lifecycle;
7. multilingual, multisite, forms, mail, memberships, comments, automation,
   analytics, and bookings;
8. first-party commerce in small invariant-driven passes;
9. compliance controls, migration tooling, cache offload, optional OpenBao,
   clustered deployment, Fluxheim compatibility, backup/restore, and
   full-system hardening;
10. contract freezes, independent reviews, release candidates, and 1.0;
11. optional post-1.0 Skrifheim Witness and later Authoritative modes after
   external entry conditions are met.

## Definition Of 1.0

`1.0.0` is not a calendar event. It requires:

- an ordinary user can install, author, preview, publish, update, back up, and
  restore without specialist tools;
- API-only/headless use is complete;
- structured content, routing, themes, multilingual domains, media, search,
  forms, workflows, memberships, and commerce profiles meet their documented
  scope;
- supported databases and platforms pass published conformance matrices;
- clean packaged artifacts pass every launchable user/operator journey,
  including account lifecycle, content publication, backup/restore, upgrade,
  failure, and recovery for the claimed profile;
- Valkey offload, multi-node failover, and Fluxheim profiles pass their
  published matrices when those optional capabilities are claimed;
- archives round-trip and cross-provider migrations preserve declared
  semantics;
- extensions cannot gain ambient host authority;
- identity, sessions, recovery, tenant/cache isolation, uploads, rendering,
  commerce, updates, and supply chain have independent review;
- every supported upgrade and rollback path is tested;
- backup restore drills meet declared RPO/RTO profiles;
- signed artifacts, SBOM, provenance, documentation, support, and disclosure
  processes are operational;
- the final external pentest has no unresolved critical or high finding;
- release-blocking medium findings are fixed, not waived for schedule;
- release candidates complete a defined long-duration soak.

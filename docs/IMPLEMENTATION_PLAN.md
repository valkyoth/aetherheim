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

The browser UI, CLI, integrations, plugins, and post-1.0 native clients use the
same typed application commands and queries. Storage and HTTP are adapters;
they do not define the domain.

## Final Decisions From The Idea Review

- Structured block documents are canonical; HTML and Markdown are render,
  import, or export formats.
- Browser administration uses opaque revocable server-side sessions, not JWTs
  by default.
- Plugins use versioned capability contracts and cannot receive raw database,
  filesystem, environment, socket, secret, or host-memory access.
- Executable plugins use an admitted, exact-pinned, mature WebAssembly
  Component Model runtime behind an Aetherheim adapter. Aetherheim owns WIT,
  package validation, capability brokering, quotas, and conformance; it does
  not build a WebAssembly parser, compiler, or execution engine.
- SQLite is the simple local default. PostgreSQL is the production reference.
  MariaDB, MongoDB, and SurrealDB become supported only through visible
  capability and conformance matrices.
- The Aetherheim Portable Storage Profile (APSP) defines the semantics every
  provider must implement. Provider-native features may accelerate those
  semantics but may not quietly redefine them.
- Verified ingress constructs a tenant/site/environment context that is
  required to construct repositories, units of work, policy, cache, search,
  blob, plugin, and audit capabilities. Tenant scope is not an optional filter.
- One versioned `ContentView` projection feeds headless delivery, server
  rendering, native clients, search, and extension proposals from the same
  canonical document and publication root.
- A loopback-only SQLite developer preview delivers the first usable CMS slice
  before secondary database work. Its transport and one-time authority are
  technically excluded from production artifacts; later releases generalize
  the same canonical application contracts rather than replacing a prototype.
- Production HTTP and TLS use admitted mature foundations behind focused
  Aetherheim contracts. HTTP runtime admission, TLS/certificate lifecycle,
  request governance, direct-serving qualification, APIs, and proxy profiles
  are separate review stops.
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
- First-party analytics is privacy-preserving, bounded, consent-aware, and
  non-authoritative. Optional AI providers receive only named classified
  operations; their outputs remain reviewable proposals.
- Skrifheim is not integrated before Aetherheim 1.0. Proof-ready contracts are
  useful independently. Optional Witness Mode begins only in its later
  post-1.0 version band after both projects and their relevant contracts are
  stable.

## Non-Negotiable Engineering Rules

- Pin and use the latest stable Rust; the foundation pin is `1.97.1`.
- Rust edition 2024 and Cargo resolver 3.
- Before every release, check the Rust stable manifest, CI action pins, and
  external Cargo security-tool versions. Update promptly for security fixes.
- External Rust crates are kept to the smallest practical set. Discuss every
  addition first; pin its exact current crates.io version; record purpose,
  scope, licence, and review date; audit features, maintenance, unsafe/native
  code, and transitives; and test it behind an explicit boundary.
- The same minimal, prior-discussion, admission, exact-lock, freshness,
  provenance, licence, transitive-review, and boundary-test rules apply to
  post-1.0 Kotlin/Android and Swift/Apple dependencies and build tools; native
  ecosystem convenience does not create a dependency-policy exception.
- A general transitive exception is allowed only when the user approves a
  written, time-bounded security ADR showing that it is safer than custom
  implementation and defining removal/review dates. This never creates an
  exception to the direct or transitive `zeroize` prohibition.
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

Milestones introduce one independently reviewable authority boundary or
reversible behavior. Dependency admission, adapter behavior, live provider
qualification, unrelated domain state machines, platform packaging, and
migration/recovery are not combined merely to reduce the version count. The
established pre-1.0 numbering may extend beyond `v0.99.0`; existing version
identities are never renumbered after release evidence or compatibility
fixtures refer to them.

A minimal requirement/control/scenario registry begins before runtime product
work. Every later milestone adds stable requirements, threats, executable or
manual scenarios, owning version, implementation links, current evidence, and
exceptions in the same change. The later compliance catalog extends these IDs
with standards mappings; it does not reconstruct early traceability.

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
- `aetherheim-text`
- `aetherheim-crypto-contracts`
- `aetherheim-schema`
- `aetherheim-document`
- `aetherheim-content-view`
- `aetherheim-query`
- `aetherheim-storage-profile`
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
- `aetherheim-taxonomy`
- `aetherheim-navigation`
- `aetherheim-localization`
- `aetherheim-multisite`
- `aetherheim-identity`
- `aetherheim-authorization`
- `aetherheim-session`
- `aetherheim-notifications`
- `aetherheim-media`
- `aetherheim-search`
- `aetherheim-forms`
- `aetherheim-mail`
- `aetherheim-membership`
- `aetherheim-comments`
- `aetherheim-automation`
- `aetherheim-analytics`
- `aetherheim-ai`
- `aetherheim-commerce`
- `aetherheim-compliance`
- `aetherheim-control-catalog`

### Adapters and delivery

- `aetherheim-storage`
- `aetherheim-storage-sqlite`
- `aetherheim-storage-postgres`
- `aetherheim-storage-mariadb`
- `aetherheim-storage-mongodb`
- `aetherheim-storage-surrealdb`
- `aetherheim-blob`
- `aetherheim-blob-local`
- `aetherheim-blob-s3`
- `aetherheim-cache`
- `aetherheim-cache-valkey`
- `aetherheim-secrets`
- `aetherheim-secrets-openbao`
- `aetherheim-secret-bootstrap`
- `aetherheim-cluster`
- `aetherheim-proxy-trust`
- `aetherheim-jobs`
- `aetherheim-http`
- `aetherheim-tls`
- `aetherheim-render`
- `aetherheim-theme`
- `aetherheim-plugin-host`
- `aetherheim-plugin-runtime`
- `aetherheim-package`
- `aetherheim-api`
- `aetherheim-graphql`
- `aetherheim-web`
- `aetherheim-admin`
- `aetherheim-server`
- `aetherheim-realtime`
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

Cargo metadata, rather than directory names alone, is the source for automated
dependency-layer, facade-purity, feature, duplicate-version, and package-
purpose checks. A new crate cannot enter the workspace until those checks can
classify it.

## Portable Semantic Contracts

Portable contracts must be complete enough that adapters cannot fill gaps with
provider or platform behavior.

- Bounded text and collections account for encoded size, element count,
  nesting, traversal, expansion, allocations, cumulative work, and output.
  Parsing is streaming or preflighted where practical; untrusted lengths never
  cause unchecked preallocation.
- Identifier domains cover every security-relevant aggregate, event, job,
  lease, session, package, payment, inventory, audit, and correlation record.
  External encodings are canonical; generation receives reviewed entropy and
  time providers; persistence enforces uniqueness. Identifiers never carry
  authority and are never used as secrets.
- Time, randomness, Unicode/locale data, money rules, and canonical
  serialization are injected or versioned inputs. Pure core behavior cannot
  consult an ambient clock, random source, locale, or host serializer.
- Entropy, wall/monotonic/database time, Unicode/URL/IDNA behavior, digests,
  signatures, AEAD/MAC/KDF operations, and keys use typed versioned providers.
  Domain-separated roots and known-answer/self-test evidence are established
  before schemas, sessions, packages, webhooks, or backups depend on them.
- Policy evaluation returns typed outcomes and obligations. Callers must
  consume redaction, step-up, approval, purpose, evidence, rate, and audit
  obligations before receiving a usable capability; there is no convenient
  boolean `may_proceed` escape hatch.
- Security profiles are generated, diffable policy bundles with conformance
  scenarios. Personal and Standard remain approachable defaults; Hardened,
  Regulated, Clustered, and Air-gapped behavior is opt-in and explicit.

Canonical content uses a versioned document envelope containing document,
revision, schema, locale/direction, provenance, namespaced block kinds, stable
node IDs, typed properties, references, and bounded inert unknown payloads.
Validation enforces unique IDs, acyclic structure, deterministic ordering,
known schema compatibility, reference integrity, and all resource budgets.
Block kinds describe meaning rather than CSS classes, UI components, or
database keys. Legacy HTML/SVG is quarantined data until a versioned sanitizer
and sink-specific renderer admit it.

Pure document transformations are separate from editor collaboration. If a
CRDT or operational-transform foundation is later admitted, it produces normal
validated transformations and never becomes the canonical storage model.

`ContentView` is the stable projection from canonical document plus release,
locale, policy, and viewer context. The same projection has generated schemas
and compatibility fixtures for REST, GraphQL, TypeScript, Kotlin, Swift,
server rendering, native applications, search, and extension host calls.
Rendering compiles it to a sink-neutral Render IR; only final sinks perform
context-specific escaping.

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

The versioned Aetherheim Portable Storage Profile specifies canonical value
mapping, text comparison and ordering, timestamps, predicate truth tables,
stable cursors, relationship traversal, aggregation, transaction/isolation
requirements, commit ambiguity, and normalized errors. A first-party reference
interpreter acts as the semantic oracle. Every adapter runs differential,
property, adversarial-history, and crash tests against it. Support evidence pins
provider version, deployment topology, durability/isolation settings,
collation, timezone, and required extensions. Provider-specific capabilities
are separately qualified and never presented as portable semantics; SurrealDB
remains experimental until it passes the complete portable and live matrices.

SQLite, PostgreSQL, MariaDB, MongoDB, SurrealDB, Valkey, S3-compatible storage,
HTTP/TLS, WebAuthn, password hashing, HTML parsing/sanitization, media probing,
and Component Model execution use mature exact-pinned implementations where
needed. Aetherheim owns their narrow contracts, budgets, policy, normalized
errors, qualification manifests, and failure tests; it does not build database
engines/wire protocols, TLS, browser-grade parsers, codecs, or runtimes merely
to avoid dependencies. Admission, semantic implementation, and live support
qualification are separate releases.

`UnitOfWork::commit` has three externally meaningful outcomes: committed, not
committed, or ambiguous. An ambiguous result is resolved through the bound
idempotency record; blindly retrying a write is never the resolution strategy.
External effects use a transactional outbox and reconciliation instead of
holding a database transaction open across a provider call.

Support is layered:

1. deterministic in-memory/reference models;
2. SQLite zero-configuration adapter;
3. PostgreSQL production reference;
4. MariaDB parity;
5. MongoDB parity;
6. SurrealDB parity;
7. provider capability and performance evidence;
8. cross-provider archive migration.

AHAF is a canonical streaming archive, not merely a data dump. It carries
schema and package versions, canonical values, references, immutable blobs,
provenance, classifications, checksums, feature bits, and explicit omissions.
Live provider migration uses a fence-and-cutover protocol: capture a source
root, bulk copy, replay bounded deltas, quiesce writers, verify roots, switch,
rebuild derived state, and retain a tested rollback path.

Local blob storage is the simple single-node default. Cluster claims require a
qualified shared S3-compatible object-store adapter with immutable keys,
conditional writes, multipart cleanup, integrity checks, lifecycle rules, and
failure recovery. Shared filesystem/NFS deployment, if ever claimed, is a
separate topology with its own semantics and tests.

Database work uses the smallest reviewed client/protocol foundation that meets
the security and portability requirements. Adapter work is still split into
admission, resource governance, transaction semantics, conformance, failure
recovery, and security releases. Support is not claimed merely because a
connection succeeds.

## Cache, Secrets, Cluster, And Edge Plan

- In-process caching is bounded and remains the simple default. Valkey provides
  optional shared cache offload behind the same conformance contract; cached
  values are reconstructible and never become authoritative state.
- Database session records are authoritative. Valkey may cache only bounded,
  hashed session material with tenant, session, security epoch, expiry, and
  credential/recovery epoch dimensions. Malformed or stale entries are
  discarded, critical actions recheck authoritative state, and database loss
  denies authenticated administration rather than trusting cache state.
- OpenBao integration uses an admitted exact release of the `openbao` crate and
  only the required features. Environment import is an explicit allowlist in a
  short-lived bootstrap process that starts Aetherheim with a clean environment.
- Cluster nodes share authoritative database/session/job state, authenticate
  peers, use leases with fencing and idempotency, withdraw readiness before
  drain, and tolerate a failed node without claiming exactly-once execution.
- Proxy metadata is trusted only from configured peers. Fluxheim receives a
  tested profile for health, readiness, drain, retry, forwarding, TLS/mTLS,
  request bounds, and observability; it remains optional and out of process.

Secret providers expose typed references and short-lived operation/lease
handles rather than general secret strings. Rotation generations invalidate
dependent pools and caches. Bootstrap, renewal, revocation, outage, and clock-
skew behavior are explicit. If the `openbao` dependency graph conflicts with
the absolute `zeroize` ban, support remains blocked until a zeroize-free crate
graph or a reviewed zeroize-free sidecar design is approved; Aetherheim will
not build a custom TLS or OpenBao client to bypass the conflict.

PostgreSQL is the first clustered reference topology. Each other database must
separately earn clustered support under a declared version/topology profile.
Durable jobs use database time, monotonic fencing tokens, idempotent effects,
and transactional completion/outbox updates; schedules use deterministic slot
identities. Loss of coordination makes mutation and privileged administration
unready. Only explicitly public immutable content may use a documented stale
read path.

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
- a freestanding target for `no_std` portability evidence.

Host features may have platform-specific adapter crates, but public semantics
must remain consistent. Missing platform functionality fails explicitly. No
conditional compilation may silently weaken security.

Compile support and native server operation are different claims. Linux,
Windows, macOS, FreeBSD, and NetBSD production operation require native
packaged install/serve/upgrade/restore/uninstall matrices. Android and iOS are
neither server targets nor Rust-library embedding targets. Before 1.0,
generated Kotlin and Swift schemas and the versioned public API prove only that
future clients can be implemented without changing domain semantics; they do
not establish a mobile-product support claim.

After 1.0, dedicated native Android and iOS applications connect over the same
public, versioned client profile used by other remote clients. Their native UI,
platform lifecycle, secure credential storage, encrypted offline state, sync,
push, media, accessibility, package signing, store distribution, and device
matrices are implemented and qualified independently from the server. A mobile
application never hosts an Aetherheim server role and is not a WebView/PWA
wrapper.

Aesynx does not yet exist as a usable operating system or Rust compilation
target. Current work maintains freestanding `no_std` contracts and explicit
host capabilities only to avoid operating-system lock-in. A possible future
adapter receives no build, runtime, compatibility, or support claim unless
Aesynx is eventually completed and separately qualified.

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

A versioned requirement/control/scenario registry connects each architecture
rule and support claim to exactly one owning release, implementation, automated
or manual evidence, threat, operator control, exception, and current result.
The baseline versions verified from official sources on 2026-08-02 are
[OWASP ASVS 5.0.0](https://owasp.org/www-project-application-security-verification-standard/),
[NIST SP 800-63-4](https://pages.nist.gov/800-63-4/),
[PCI DSS 4.0.1](https://www.pcisecuritystandards.org/document_library/?class=pcidss&doc=pci_dss),
and [WCAG 2.2](https://www.w3.org/TR/WCAG22/), plus applicable privacy
profiles. Their owning milestone must recheck and pin the current official
revisions before implementation. Mappings retain truthful applicability and
non-certification statements. The registry also owns data-classification
propagation, processor/region/retention/DSAR behavior, cryptographic key
lifecycle, payment-page inventory, accessibility manual evidence, security
event taxonomy, vulnerability response, API/ABI inventory, abuse limits,
capacity/SLO evidence, and disaster-recovery promotion.

## Extension And Commerce Boundaries

Executable extension admission is a security pipeline: verify the signed
package and compatibility, validate its component with admitted standards
tooling, approve parameterized capabilities, instantiate without ambient WASI,
enforce per-invocation budgets, validate proposed outputs, and then pass those
proposals through normal application authorization and commit handling.
Unguessable typed handles carry invocation, tenant, actor, grant epoch, and
expiry context. Guest memory is copied under strict bounds; host code retains
no guest pointers and does not permit reentrant calls or outbound network waits
inside an open authoritative transaction.

Fuel/deadline epochs, memory/table/stack, host-call, copy/output, storage, HTTP,
concurrency, log, and job budgets are separately measurable. Outbound HTTP is
brokered with named operations, destination allowlists, DNS/rebinding/private-
address defenses, redirect policy, bounded bodies, and data-classification
checks. Hardened profiles may add an out-of-process plugin host but must preserve
the same WIT and capability semantics. Typed event subscriptions and
interceptors are ordered, bounded, non-reentrant, and cannot make a committed
operation uncommitted; package updates display authority differences and keep
state export/retain/purge explicit.

Commerce authority is append-oriented and provider-independent. Exact money,
quantity, rate, tax, price, cart, quote, inventory, order, payment, refund,
shipping, subscription, and entitlement models are separate small releases.
An accepted checkout snapshot is immutable; inventory reservations are atomic;
monetary journals balance by currency; provider callbacks are untrusted,
signature-checked, idempotent inputs; timeout ambiguity resolves by lookup and
reconciliation. Card data never enters Aetherheim: payment integrations are
hosted or tokenized and the operator-facing evidence states PCI scope as a
non-claim.

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
- REST, GraphQL, events, webhooks, archives, themes, generated client schemas,
  WIT, and plugin packages share an API/ABI inventory and semantic
  compatibility fixtures.
- Database adapters run differential scenarios against the APSP reference
  interpreter, including adversarial concurrent histories and ambiguous
  commits; a successful CRUD smoke test is never provider qualification.
- The SQLite developer-preview profile launches a real loopback server and
  browser to create, revise, publish, read, restart, export, and restore
  canonical content before secondary databases are introduced. Tests prove the
  preview authority and transport are absent from production artifacts.
- HTTP/TLS, password hashing, WebAuthn, Valkey, OpenBao, S3-compatible storage,
  media tools, AI providers, mail, payments, and other external boundaries each
  have protocol/model tests plus independent exact-version live qualification.
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
   records, including aggregate budgets, typed obligations, and `ContentView`;
3. SQLite/local blobs and a real loopback-only CMS developer preview, then
   admitted production database clients, APSP conformance, archives, cache,
   secrets, shared blobs, and fenced migration;
4. content commands, revisions, workflows, taxonomy, navigation, routing,
   production HTTP/TLS, APIs, audit, and identity;
5. safe rendering, admin shell, editor, themes, media admission/derivatives,
   delivery, and search;
6. capability contracts, admitted mature Component Model runtime integration,
   isolated extension UI, packages, and lifecycle;
7. multilingual, multisite, forms, mail, memberships, comments, automation,
   bookings, privacy-preserving analytics, and optional proposal-only AI;
8. first-party commerce in small invariant-driven passes;
9. compliance controls, source-specific migration tooling, backup creation,
   isolated restore/promotion, native server/container/air-gap packaging,
   clustered deployment, Fluxheim compatibility, endurance, and full-system
   hardening;
10. contract freezes, independent reviews, release candidates, and 1.0;
11. post-1.0 native Android and iOS clients in independently releasable,
   security-qualified passes; and
12. optional later post-1.0 Skrifheim Witness and Authoritative modes after
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

# Cache, Cluster, And Edge Topology

Status: planned operational contract

All features in this document are optional. A single Aetherheim instance with
SQLite and an in-process bounded cache remains a supported simple topology.

## Cache Offload And Valkey

`aetherheim-cache` defines a provider-neutral, bounded ephemeral cache
contract. `aetherheim-cache-valkey` is the planned first remote-cache adapter.
Valkey never becomes authoritative storage: loss, eviction, restart, stale
data, or complete unavailability must not corrupt content, identity, policy,
commerce, jobs, or audit state.

Cache keys include tenant, site, environment, locale, visibility, viewer or
policy class, policy epoch, release root, schema/version, and adapter namespace
where applicable. Values have size and lifetime limits. Authentication, TLS,
server identity, pooling, cancellation, command allowlists, key canonicality,
stampede control, invalidation, stale policy, and fail-open/fail-closed behavior
are explicit per cache class.

Only cache classes documented as safely reconstructible may bypass a failed
remote cache. Security decisions and revocation state fail closed or use their
authoritative provider; they never trust an ambiguous cache response. Remote
cache support requires conformance, poisoning, eviction, partition, latency,
memory-pressure, and recovery evidence.

Database session records remain authoritative. Valkey may hold only bounded,
hashed acceleration data keyed by tenant, session, security, credential, and
recovery epochs plus expiry. Critical actions recheck authority. Malformed or
stale cache entries are discarded, and database loss denies authenticated
administration rather than trusting cache state.

## Multiple Aetherheim Nodes

The planned cluster mode lets multiple Aetherheim application nodes share load
and continue serving when one node stops. It is active-active at the application
layer and relies on a supported shared authoritative database. SQLite remains a
single-node default unless a separately qualified topology proves otherwise.
Cluster profiles also require a qualified shared S3-compatible immutable blob
provider; local disk and unqualified shared filesystems are not cluster blob
authority. PostgreSQL is the first reference cluster topology. MariaDB,
MongoDB, and SurrealDB earn cluster claims independently under exact settings.

Each node has a stable installation identity and an ephemeral boot identity.
Cluster traffic uses authenticated peer identity, protocol/version negotiation,
replay protection, bounded messages, and least-authority operations. Shared
sessions, revocation, durable jobs, outbox state, and publication roots live in
authoritative providers rather than process memory.

Job and singleton work use database time, monotonic fencing tokens,
deterministic schedule-slot identities, idempotency keys, and transactional
claim/completion/outbox operations. The design does not promise exactly-once
execution and does not invent a new consensus algorithm. A partitioned or stale node cannot
publish, migrate, schedule singleton work, or perform external effects without
current authority. Failed-node leases expire and work can be reclaimed safely.

Readiness is stricter than liveness. A node is routable only when configuration,
database compatibility, migrations, required secret handles, policy state, and
mandatory background services are ready. Shutdown first withdraws readiness,
then drains requests and leases. Rolling upgrades enforce a bounded protocol
and schema compatibility window.

## Reverse Proxies And Fluxheim

Aetherheim can serve directly or operate behind a reviewed reverse proxy/load
balancer. It never requires Fluxheim. A dedicated optional Fluxheim deployment
profile documents and tests the pairing without importing Fluxheim into the
Aetherheim process.

Forwarded client address, scheme, host, port, certificate identity, and request
ID are accepted only from configured trusted proxy peers and through one
canonical header/profile policy. Untrusted or conflicting forwarding headers,
invalid host data, hop-by-hop headers, request smuggling shapes, and unexpected
PROXY protocol frames are rejected. Administrative and health endpoints have
separate exposure and authentication rules.

The Fluxheim profile includes bounded request/response behavior, WebSocket and
HTTP version compatibility where Aetherheim needs them, active readiness
checks, retry safety by method and idempotency, per-node connection limits,
drain, slow start, all-down behavior, observability correlation, and TLS or mTLS
ownership. Fluxheim retries never make a non-idempotent Aetherheim operation
execute twice without the application idempotency contract detecting it.

## Failure Evidence

Qualification injects node crash, process pause, packet loss, partition,
duplicate and delayed messages, database/cache/OpenBao loss, clock movement,
rolling-version skew, stale proxy membership, and complete upstream loss.
Tests prove bounded recovery, absence of cross-tenant cache data, fenced stale
workers, safe request replay, correct readiness withdrawal, and continued
service whenever the documented topology still has quorum and authoritative
dependencies available.

Shared blob qualification injects multipart crash/cleanup, stale listing,
conditional-write races, object corruption/substitution, retention/hold
conflicts, credential rotation, throttling, outage, and cross-node recovery.
Cluster readiness fails when its required shared blob authority cannot satisfy
the profile; a node never silently falls back to local files.

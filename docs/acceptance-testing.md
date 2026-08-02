# Executable Acceptance And Live-System Testing

Status: mandatory verification policy

## Support Claim Rule

Aetherheim does not call a feature supported merely because its functions,
types, mocks, or unit tests pass. Every user-visible, operator-visible, network,
storage, security, migration, and failure behavior requires an automated
black-box scenario that launches the real executable or release artifact and
uses the same public boundary as its intended caller.

Mocks and deterministic models remain useful for exhaustive edge cases. They
cannot be the sole evidence for a database, cache, OpenBao, proxy, cluster,
browser, operating-system, or external-provider support claim.

The stable entry point is:

```bash
scripts/acceptance.sh all
```

At the foundation stage this launches the real CLI and verifies help, version,
doctor, output contracts, and failure exit codes. New profiles are added only
when their product capability exists. `scripts/acceptance.sh list` reports the
implemented profiles. A release-required profile must fail when its runtime,
service, fixture, credential, or test tool is missing; it may not silently skip
and report success.

## Required Test Layers

1. Pure unit/model tests cover rules, invariants, bounds, and state machines.
2. Component tests exercise real crate boundaries and encoded inputs.
3. Process tests launch actual Aetherheim roles and inspect public outputs,
   exit status, signals, restart behavior, files, sockets, and resource limits.
4. Black-box acceptance tests use the public CLI, HTTP/API, browser, package,
   import/export, and operator surfaces without internal shortcuts.
5. Live-provider tests run against actual supported database, Valkey, OpenBao,
   mail, object-store, search, identity, payment-sandbox, and proxy versions.
6. Multi-process tests exercise real Aetherheim nodes, workers, Fluxheim, shared
   providers, failover, partitions, draining, and rolling upgrades.
7. Packaged-artifact tests install and launch the same signed archive, image,
   service, mobile library, or bundle offered to users.
8. Destructive/failure tests inject process death, I/O loss, corrupt state,
   latency, exhaustion, partial migration, and recovery at documented points.

Every layer records bounded, redacted diagnostics and preserves failure
artifacts. Test-only bypasses, loopback plaintext exceptions, fixture keys, and
provider credentials are unavailable in production builds.

## Scenario Registry Requirements

Each implemented capability receives stable scenario IDs and records:

- requirement and threat/abuse case;
- setup and exact product/provider/artifact versions;
- public actions and expected observable results;
- security, tenant, locale, policy, and failure variants;
- cleanup and proof that reruns start from a known state;
- applicable operating systems and topology profiles; and
- owning release milestone and most recent passing evidence.

Code review must update the scenarios in the same change as behavior. A changed
public behavior without an updated executable scenario blocks merging and
release. Disabled, ignored, quarantined, flaky, or skipped release scenarios
count as failures unless the corresponding capability is explicitly removed
from the support matrix.

## Product Journeys

Once the relevant surfaces exist, the launchable suite covers at least:

- clean install, initialize, start, readiness, graceful stop, restart, upgrade,
  rollback, backup, restore, diagnostics, and uninstall;
- bootstrap administrator, create/verify/login/logout/recover/disable/delete
  account, session revocation, WebAuthn/TOTP where enabled, role changes, and
  cross-tenant denial;
- create schema/content, autosave, preview, approve, publish, edit, schedule,
  unpublish, restore revision, route, render, search, translate, and export;
- upload/quarantine/process/serve/delete media and survive hostile files;
- install/activate/deny/upgrade/rollback/remove themes and plugins with
  capability and isolation assertions;
- forms, consent, mail, memberships, comments, automation, webhooks, imports,
  commerce, refunds, inventory, and compliance workflows for enabled profiles;
- cache hit/miss/invalidation/eviction/poisoning/outage and authoritative
  reconstruction;
- OpenBao bootstrap/read/renew/revoke/outage/redaction and clean child
  environment;
- balanced multi-node traffic, failed node, reclaimed work, stale worker
  fencing, partition, recovery, drain, and rolling-version compatibility; and
- direct HTTP plus trusted-proxy and optional Fluxheim routing, forwarding,
  TLS/mTLS, retry, WebSocket, limit, health, drain, and all-down behavior.

This is a minimum, not a closed list. Every new command, endpoint, workflow,
provider capability, security control, and documented recovery action adds its
own executable success and failure scenarios.

## Database Matrix

The same provider-neutral journey suite runs against every supported database:
SQLite, PostgreSQL, MariaDB, MongoDB, SurrealDB, and any later admitted adapter.
For each declared server version and topology it performs real connection and
authentication, schema creation, migrations, account/session operations,
content and relationship operations, jobs/outbox/audit, concurrency, restart,
backup/restore hooks, export/import, and cross-provider migration.

Adapter-specific tests add malformed protocol responses, transaction and
isolation behavior, deadlocks/retries, topology changes, version negotiation,
limits, and unsupported-capability reporting. An in-memory adapter or mocked
client never substitutes for this live matrix.

## Execution Tiers

- Every local/PR gate runs fast real-process smoke and all deterministic tests.
- Provider-changing pull requests run the affected live provider matrix.
- Scheduled CI runs all supported provider versions, platforms, browsers, and
  multi-node failure suites to catch environmental drift.
- Every release candidate runs the complete launchable suite from clean state
  against packaged artifacts. Required services are provisioned explicitly;
  unavailable infrastructure fails the gate rather than weakening it.
- The final pentest uses the exact artifact and supported topologies already
  proven by the acceptance suite.

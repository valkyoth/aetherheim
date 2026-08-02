# Aetherheim Threat Model

Status: foundation baseline; update for every release.

## Assets

- tenant, site, identity, credential, session, content, revision, workflow,
  media, commerce, consent, audit, backup, key-reference, and configuration
  state;
- integrity of publication, routes, themes, extensions, rendered output,
  packages, updates, and release artifacts;
- availability of administration, public delivery, jobs, recovery, and the
  most recent valid release;
- privacy of protected content, user data, form submissions, orders, evidence,
  and operational telemetry.

## Trust Boundaries

- public request to delivery API/renderer;
- browser to management API and opaque session store;
- application service to policy and authoritative storage;
- job scheduler to workers and external effects;
- upload quarantine to isolated media processor;
- host to plugin/component runtime and isolated extension UI;
- Aetherheim to database, blob, mail, payment, search, key, and identity
  providers;
- Aetherheim nodes to optional cache, OpenBao, cluster peers, and trusted edge
  proxy/load-balancer providers;
- build/release system to distributed artifacts and update admission;
- conventional storage to an optional post-1.0 witness/authority bridge.

## Primary Adversaries

- unauthenticated remote attacker;
- malicious or compromised account, administrator, support operator, plugin,
  theme, provider, processor, build worker, or dependency/tool source;
- cross-tenant attacker with a valid account;
- network attacker between Aetherheim and providers;
- attacker with copied database, backup, media, cache, log, or package files;
- operator error, stale policy, partial upgrade, clock failure, resource
  exhaustion, process crash, and corrupt projection;
- compromised or stale cluster node, split network, poisoned remote cache,
  forged forwarding metadata, failed load balancer, and leaked startup
  environment.

## Required Abuse Cases

- account takeover, session fixation/theft, CSRF, reset/recovery abuse, and
  privilege cache confusion;
- XSS, unsafe URL/CSS/HTML handling, cache poisoning, host spoofing, request
  smuggling, injection, SSRF, DNS rebinding, and redirect loops;
- tenant/site/environment/locale/viewer data crossover;
- cache poisoning, key-dimension omission, stale revocation, cluster replay,
  split-brain work, lease theft, unfenced stale worker, and unsafe proxy retry;
- forwarding-header spoofing, proxy trust confusion, false readiness, failed
  drain, and all-backend outage;
- startup-secret overcollection, partial OpenBao import, bootstrap-token reuse,
  secret logging, and retained ordinary memory copies;
- publication or approval replay, stale revision, ambiguous commit, job
  duplication, and audit suppression;
- malicious archive, upload, image/document metadata, decompression bomb, and
  compromised decoder;
- extension escape, confused deputy, forged actor/grant/handle, capability
  broadening, resource exhaustion, and frontend origin escape;
- supply-chain substitution, stale action/tool, forged SBOM/provenance,
  rollback, and compromised publisher;
- test-only bypass reaching production, mock-only assurance, silently skipped
  live scenarios, untested packaged artifacts, and false provider support;
- order replay, repricing, journal imbalance, oversell, webhook replay, refund
  duplication, and raw payment-data entry;
- backup theft, restore poisoning, incomplete erasure, legal-hold overreach,
  and privacy-invasive immutable evidence;
- AI prompt injection, unauthorised source retrieval, data egress, false
  provenance, and unreviewed publication.

## Foundation Security Claims

Version 0.1.0 contains no HTTP, storage, authentication, rendering, media,
plugin, commerce, or provider implementation. It claims only a currently
external-dependency-free modular Rust foundation, explicit limits, identifier
and proof labels, and local policy gates. Unimplemented capability is absent.

## Review Rule

Every release adds attacker goals, entry points, assets, mitigations, negative
tests, residual risk, and operational detection for its delta. A tag requires
the applicable individual PASS report or explicit intermediate batch deferral.
The final release in a batch requires cumulative PASS. Only the user authorises
batching, tagging, and pushing.

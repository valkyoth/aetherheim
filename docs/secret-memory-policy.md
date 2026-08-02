# Secret Memory And OpenBao Policy

Status: planned security contract

## Required Foundation

Aetherheim-owned code uses the `sanitization` crate for secret ownership,
redaction, bounded exposure, and clear-on-drop behavior. It does not depend on,
import, re-export, or transitively admit the `zeroize` crate. The lockfile and
dependency-policy gate enforce that rule.

`sanitization` is still an external dependency for admission purposes even
though it is maintained by the same project owner. Its exact release, selected
features, target behavior, unsafe boundaries, and complete transitive graph
must be reviewed before it enters the workspace. Interop features that add
`zeroize` are prohibited.

The planned `openbao` integration has the same admission requirements. The
currently inspected `openbao` 2.1.2 graph contains `zeroize` through `secrecy`
and parts of its default rustls stack, so that version cannot be admitted to
Aetherheim. Integration waits for a reviewed, exact, zeroize-free `openbao`
feature graph.

## Proportional Sanitization

Sanitization is based on data classification and lifetime, not applied blindly
to every allocation.

- Always use bounded `sanitization` ownership for passwords, recovery values,
  API and OpenBao tokens, private keys, encryption material, database
  credentials, session secrets, webhook secrets, and secret-bearing provider
  responses.
- Prefer direct generation or decoding into the final secret container. Keep
  exposure closures short and do not clone secrets for convenience.
- Consider sanitizing short-lived personal or commercially sensitive buffers
  when a practical owned boundary exists and benchmarks show acceptable cost.
- Do not wrap public content, immutable media, indexes, cache objects, ordinary
  identifiers, or bulk non-secret data merely to increase a sanitization
  counter. That would increase allocations, memory pressure, and latency
  without a credible security benefit.
- Memory locking, guard pages, page sealing, register scrubbing, and cache
  flushing are profile-driven hardening controls. They require target support,
  measured budgets, explicit failure policy, and performance evidence.

Sanitization reduces accidental retention and disclosure. It cannot erase
copies made by operating systems, TLS stacks, allocators, kernels, devices,
debuggers, or already-created ordinary strings. Documentation and claims must
retain those limits.

## Optional OpenBao Startup Import

The OpenBao path is optional. Normal Aetherheim operation also supports other
reviewed secret providers and protected local deployment mechanisms.

The supported environment-import shape is a separate, single-purpose bootstrap
process:

1. accept an explicit mapping of environment-variable names to bounded OpenBao
   KV paths; never scan arbitrary prefixes or upload the whole environment;
2. authenticate with a narrow, short-lived or response-wrapped credential;
3. move each value immediately into a bounded `sanitization` container;
4. write through the reviewed `openbao` crate using TLS and an exact server
   compatibility profile;
5. report only names, paths, versions, and redacted outcomes;
6. launch the Aetherheim child with `env_clear` and an explicit allowlist of
   non-secret variables, passing secret references rather than values; and
7. sanitize owned buffers, revoke or expire bootstrap authority, then exit.

The bootstrap must run before application threads. Aetherheim does not use an
unsafe post-start environment mutation to pretend the original process
environment was securely erased. Prefer workload identity, protected file
descriptors, or orchestrator-native secret delivery when they avoid plaintext
environment variables entirely.

Import is idempotent only under an explicit conflict policy. Existing values
are never overwritten by default. Partial writes, verification failure,
OpenBao unavailability, or ambiguous server identity fail closed and do not
start Aetherheim.

## Required Evidence

- source, manifest, and lockfile gates reject direct and transitive `zeroize`;
- redaction tests cover `Debug`, errors, logs, metrics, panic paths, diagnostics,
  exports, and operation receipts;
- lifecycle probes check owned buffers after success, error, cancellation, and
  panic-abort boundaries where observation is meaningful;
- target tests record reduced guarantees on WASM/mobile platforms;
- allocation, resident-memory, latency, and throughput benchmarks justify each
  hardening profile; and
- the integration receives focused secrets coverage in the applicable
  individual or explicitly authorised cumulative pentest before that report
  becomes green.

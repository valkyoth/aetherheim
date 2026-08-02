# Modularity Policy

- `aetherheim` is a facade and product entry point.
- Domain values, schemas, documents, queries, policies, events, proof
  contracts, applications, providers, delivery, UI, extensions, media,
  commerce, and test infrastructure live in focused crates.
- Dependencies point from delivery/adapters to application/domain to portable
  contracts.
- Portable core crates do not depend on host adapters.
- Feature flags may not silently enable network, filesystem, secrets, signing,
  identity-provider, database, media-processor, or extension authority.
- Non-generated Rust files must not exceed 500 lines. At 300 lines, review the
  file for a coherent split.
- Generated files require an identified generator and reproducibility check.
- Cargo metadata is the source for dependency-layer, facade-purity, feature,
  no_std/std, duplicate-version, package-purpose, and workspace-inheritance
  enforcement; directory naming alone is not evidence.
- Security-sensitive external foundations live behind focused adapter crates.
  Their implementation types do not escape into portable or application
  contracts, and admission, behavior, and live qualification remain distinct.

The local gate is:

```bash
scripts/validate-modularity-policy.sh check
```

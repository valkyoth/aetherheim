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

The local gate is:

```bash
scripts/validate-modularity-policy.sh check
```

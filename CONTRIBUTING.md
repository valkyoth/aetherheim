# Contributing to Aetherheim

Aetherheim is a security-first content operating system under active
pre-production development. Contributions must stay small, explicit, tested,
and honest about what is implemented.

## Licence

Aetherheim itself is licensed under the European Union Public Licence 1.2. By
contributing to this repository, you agree that your contribution is provided
under that licence.

Themes and plugins are separate works supplied by their authors. Aetherheim
does not require user-created themes or plugins to use EUPL-1.2; their authors
choose and declare their own licences.

## Development

Use the pinned toolchain and run:

```bash
scripts/checks.sh
scripts/acceptance.sh all
```

Every behavior change needs unit/model coverage and a public-boundary scenario
that launches the real process or artifact when runtime behavior is involved.
Provider support requires live service tests; mocks alone are insufficient, and
required scenarios may not silently skip.

No package may be published to crates.io. External Rust crates are kept to the
smallest practical audited set: discuss an addition before editing manifests,
pin the exact current version, complete the dependency admission record, and
test the boundary. Do not copy unreviewed external source into the repository.

Follow [SECURITY.md](SECURITY.md) for private vulnerability reporting.

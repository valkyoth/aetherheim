# Security Policy

Aetherheim is security-sensitive content infrastructure. Treat parsing,
identity, authorisation, rendering, uploads, extensions, storage, publication,
commerce, release scripts, CI, and dependency or tool changes as high risk
until reviewed and tested.

## Supported Versions

No production-ready version exists yet. Security fixes are applied to the
active development line until a public support window is declared.

## Reporting

Do not publish exploitable details in a public issue. Use a private GitHub
security advisory once repository security reporting is configured, or contact
the maintainers privately through the repository owner.

## Routine Checks

Run before every pull request:

```bash
scripts/checks.sh
scripts/acceptance.sh all
scripts/check_latest_tools.sh
cargo deny check
cargo audit
```

After the applicable pentest evidence is ready, run the single release gate:

```bash
scripts/release_gate.sh VERSION
```

GitHub Actions run CI. GitHub CodeQL default setup must be enabled in repository
security settings. Do not add an advanced CodeQL workflow while default setup
is active. See [GitHub Security Settings](docs/github-security-settings.md).

## Release Gate

The default is one pentest and permanent `security/pentest/vX.Y.Z.md` PASS
report per release. The user may explicitly authorise a batch of at most 15
listed releases to share one cumulative report; intermediate releases say
`DEFERRED`, and the final listed release cannot pass until the whole batch has
a green report.

Temporary findings arrive as ignored root `PENTEST.md`. Codex fixes them,
updates the permanent report, adds tests, and deletes the temporary file. After
a green report Codex commits and waits for GitHub. GitHub failures are fixed and
recorded in the report. Tagging and pushing happen only after GitHub is green
and the user explicitly instructs Codex. See
[Simple Human-Controlled Release Workflow](docs/release-workflow.md).

## Dependency Policy

Aetherheim keeps external Rust crates to the smallest practical reviewed set.
Every addition is discussed first, pinned to an exact current crates.io
version, recorded in `dependency-admissions.toml`, reviewed for licence,
maintenance, ownership, features, unsafe/native code, transitive graph, and
security history, and tested behind an explicit boundary. Git and custom
registry dependencies are denied. Every workspace package remains
`publish = false`.

Aetherheim-owned secret memory uses the separately reviewed `sanitization`
crate. Direct and transitive `zeroize` are prohibited by manifest and lockfile
policy. Sanitization is mandatory for actual credentials, tokens, key material,
and secret-bearing provider values, then applied to other sensitive buffers
only where the threat reduction justifies its allocation and runtime cost. See
[Secret Memory And OpenBao Policy](docs/secret-memory-policy.md).

Mature security foundations are preferred over improvised cryptography, TLS,
WebAuthn, database protocols, media codecs, or WebAssembly execution. A new
crate is not admitted merely for convenience, and security-sensitive behavior
remains fail closed until the chosen boundary is reviewed and pentested.

Unit and mock tests are never sufficient evidence for a runtime support claim.
Each implemented capability must have executable black-box success, denial,
failure, restart, and recovery scenarios using real Aetherheim processes. Each
provider claim additionally requires live supported-version testing. See
[Executable Acceptance And Live-System Testing](docs/acceptance-testing.md).

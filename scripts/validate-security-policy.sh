#!/usr/bin/env sh
set -eu

grep -R -F -q '#![forbid(unsafe_code)]' crates
grep -F -q 'unknown-git = "deny"' deny.toml
grep -F -q 'unknown-registry = "deny"' deny.toml
grep -F -q 'allow-registry = ["https://github.com/rust-lang/crates.io-index"]' deny.toml
grep -F -q 'name = "zeroize"' deny.toml
test -f dependency-admissions.toml
test -f docs/dependency-policy.md
test -f docs/secret-memory-policy.md
test -f docs/operations-topology.md
test -f docs/acceptance-testing.md
test -f docs/release-workflow.md
test -x scripts/acceptance.sh
test -x scripts/smoke_foundation.sh
test -x scripts/check_pentest_evidence.py
test -x scripts/release_gate.sh
grep -E -q '^/PENTEST\.md$' .gitignore
grep -F -q 'panic = "abort"' Cargo.toml
grep -F -q 'CodeQL default setup' SECURITY.md
grep -F -q 'CodeQL analysis default setup' docs/github-security-settings.md
grep -F -q 'cargo install --locked cargo-sbom --version 0.10.0' .github/workflows/ci.yml
for script in scripts/*.sh; do
    if grep -E -q '(^|[|;&][[:space:]]*)rg[[:space:]]' "$script"; then
        echo "$script: shell gates must use portable standard tools, not rg" >&2
        exit 1
    fi
done
test -f docs/threat-model.md
test -f docs/unsafe-policy.md
test -f docs/supply-chain-security.md
scripts/check_dependency_policy.py

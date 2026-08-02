#!/usr/bin/env sh
set -eu

rg -q '#!\[forbid\(unsafe_code\)\]' crates
rg -q 'unknown-git = "deny"' deny.toml
rg -q 'unknown-registry = "deny"' deny.toml
rg -q 'allow-registry = \["https://github.com/rust-lang/crates.io-index"\]' deny.toml
rg -q 'name = "zeroize"' deny.toml
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
rg -q '^/PENTEST\.md$' .gitignore
rg -q 'panic = "abort"' Cargo.toml
rg -q 'CodeQL default setup' SECURITY.md
rg -q 'CodeQL analysis default setup' docs/github-security-settings.md
test -f docs/threat-model.md
test -f docs/unsafe-policy.md
test -f docs/supply-chain-security.md
scripts/check_dependency_policy.py

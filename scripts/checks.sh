#!/usr/bin/env sh
set -eu

cargo fmt --all --check
scripts/check_shell_syntax.sh
scripts/check_doc_links.py
scripts/test_dependency_policy.py
scripts/test_latest_crates.py
scripts/test_release_plan.py
scripts/test_pentest_evidence.py
scripts/test_sbom_compare.py
scripts/check_release_plan.py
scripts/check_latest_crates.py
scripts/validate-modularity-policy.sh check
scripts/validate-security-policy.sh
scripts/validate-release-metadata.sh 0.1.0
cargo metadata --format-version 1 --no-deps >/dev/null
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
cargo doc --workspace --all-features --no-deps
scripts/acceptance.sh all
scripts/check_platforms.sh
scripts/generate-sbom.sh --check

#!/usr/bin/env sh
set -eu

version="${1:?usage: scripts/release_gate.sh VERSION}"

scripts/validate-release-metadata.sh "$version"
scripts/checks.sh
scripts/check_latest_tools.sh
cargo deny check
cargo audit
scripts/check_pentest_evidence.py "$version"

echo "v${version} evidence is ready"
echo "commit the report/candidate, wait for GitHub, and do not tag or push without explicit user instruction"

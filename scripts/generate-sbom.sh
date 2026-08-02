#!/usr/bin/env sh
set -eu

mode="${1:---write}"
target="sbom/aetherheim.spdx.json"
temporary="$(mktemp "${TMPDIR:-/tmp}/aetherheim-sbom.XXXXXX")"
trap 'rm -f "$temporary"' EXIT HUP INT TERM

if ! cargo sbom --version >/dev/null 2>&1; then
    echo "cargo-sbom 0.10.0 is required; install the exact pinned release tool" >&2
    exit 127
fi
cargo sbom --output-format spdx_json_2_3 > "$temporary"
test -s "$temporary"

case "$mode" in
    --check)
        test -s "$target"
        python3 scripts/compare_sbom.py "$target" "$temporary"
        ;;
    --write)
        mkdir -p sbom
        mv "$temporary" "$target"
        ;;
    *)
        echo "usage: scripts/generate-sbom.sh [--check|--write]" >&2
        exit 2
        ;;
esac

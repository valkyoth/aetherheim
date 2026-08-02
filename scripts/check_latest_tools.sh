#!/usr/bin/env sh
set -eu

workflow_dir="${GITHUB_WORKFLOW_DIR:-.github/workflows}"
ci_file="${CI_WORKFLOW_FILE:-${workflow_dir}/ci.yml}"
rust_toolchain_file="${RUST_TOOLCHAIN_FILE:-rust-toolchain.toml}"
stable_url="${RUST_STABLE_MANIFEST_URL:-https://static.rust-lang.org/dist/channel-rust-stable.toml}"

pinned="$(sed -n 's/^channel = "\([0-9][0-9.]*\)"$/\1/p' "$rust_toolchain_file" | head -n 1)"
latest="$(curl -fsSL "$stable_url" | sed -n '/^\[pkg\.rust\]$/,/^\[/ { s/^version = "\([0-9][0-9.]*\) .*/\1/p; }' | head -n 1)"
test -n "$pinned"
test -n "$latest"
if [ "$pinned" != "$latest" ]; then
    echo "Rust is not latest stable: pinned ${pinned}, latest ${latest}" >&2
    exit 1
fi

tool_version() {
    sed -n "s/.*cargo install --locked $1 --version \([0-9][^ ]*\).*/\1/p" "$ci_file" | head -n 1
}

for tool in cargo-deny cargo-audit cargo-sbom; do
    declared="$(tool_version "$tool")"
    current="$(cargo info "$tool" | sed -n 's/^version: //p' | head -n 1)"
    test -n "$declared"
    test -n "$current"
    if [ "$declared" != "$current" ]; then
        echo "${tool} is not latest: pinned ${declared}, latest ${current}" >&2
        exit 1
    fi
done

ruby scripts/check_action_pins.rb "$workflow_dir"
echo "toolchain, action pins, and Rust/Cargo release tools are current"

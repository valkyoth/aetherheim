#!/usr/bin/env sh
set -eu

run_aetherheim() {
    cargo run --quiet --locked -p aetherheim -- "$@"
}

expected_version="$(sed -n 's/^version = "\([0-9][0-9.]*\)"$/\1/p' Cargo.toml | head -n 1)"
test -n "$expected_version"

help_output="$(run_aetherheim help)"
printf '%s\n' "$help_output" | grep -F -q -x "Aetherheim $expected_version"
printf '%s\n' "$help_output" | grep -q '^USAGE:$'

version_output="$(run_aetherheim --version)"
test "$version_output" = "aetherheim $expected_version"

doctor_output="$(run_aetherheim doctor)"
printf '%s\n' "$doctor_output" | grep -F -q -x "version=$expected_version"
printf '%s\n' "$doctor_output" | grep -q '^publishing=disabled$'
printf '%s\n' "$doctor_output" | grep -q '^status=foundation-only$'

set +e
unknown_output="$(run_aetherheim definitely-not-a-command 2>&1)"
unknown_status=$?
set -e
test "$unknown_status" -eq 2
printf '%s\n' "$unknown_output" | grep -q '^unknown command: definitely-not-a-command$'

echo "foundation black-box smoke passed"

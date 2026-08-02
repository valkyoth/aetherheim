#!/usr/bin/env sh
set -eu

version="${1:-0.1.0}"
manifest_version="$(sed -n 's/^version = "\([0-9][0-9.]*\)"$/\1/p' Cargo.toml | head -n 1)"
if [ "$manifest_version" != "$version" ]; then
    echo "workspace version ${manifest_version} does not match ${version}" >&2
    exit 1
fi

notes="release-notes/RELEASE_NOTES_${version}.md"
test -s "$notes"
scripts/check_dependency_policy.py
test -s LICENSE
test -s SECURITY.md
test -s docs/RELEASE_PLAN.md

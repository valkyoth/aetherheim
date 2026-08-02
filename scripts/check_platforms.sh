#!/usr/bin/env sh
set -eu

targets="
aarch64-apple-darwin
aarch64-apple-ios
aarch64-linux-android
aarch64-unknown-linux-gnu
aarch64-unknown-linux-musl
x86_64-apple-darwin
x86_64-linux-android
x86_64-pc-windows-gnu
x86_64-pc-windows-msvc
x86_64-unknown-freebsd
x86_64-unknown-linux-gnu
x86_64-unknown-netbsd
"

installed="$(rustup target list --installed)"
for target in $targets; do
    if printf '%s\n' "$installed" | grep -F -q -x "$target"; then
        cargo check --workspace --lib --target "$target"
    else
        echo "platform check skipped (target not installed): ${target}"
    fi
done

if printf '%s\n' "$installed" | grep -F -q -x 'x86_64-unknown-none'; then
    for package in aetherheim-bounds aetherheim-core aetherheim-ids aetherheim-proof-core; do
        cargo check -p "$package" --target x86_64-unknown-none
    done
else
    echo "future Aesynx boundary check skipped (x86_64-unknown-none not installed)"
fi

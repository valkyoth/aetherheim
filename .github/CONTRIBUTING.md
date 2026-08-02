# Contributing to Aetherheim

See the repository [contribution guide](../CONTRIBUTING.md) and
[security policy](../SECURITY.md).

The short version: use the pinned Rust toolchain, discuss external crates before
adding them, complete the exact-version admission review, keep every package
private with `publish = false`, keep Rust files at or below 500 lines, update
tests and documentation with behavior, and run `scripts/checks.sh` before a PR.
Runtime behavior also requires a passing `scripts/acceptance.sh all` black-box
scenario; provider claims require live-service evidence rather than mocks alone.

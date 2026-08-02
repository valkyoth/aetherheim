# Toolchain Policy

Aetherheim pins the latest stable Rust. The foundation pin is `1.97.1`, which
was confirmed as current on 2 August 2026. Normal builds do not require nightly.

Rules:

- `rust-toolchain.toml` is authoritative.
- `workspace.package.rust-version` matches the pin during the pre-1.0
  latest-stable policy.
- `scripts/check_latest_tools.sh` compares the pin with the official stable
  manifest and checks external Cargo tools and GitHub Action pins.
- Release gates fail if the pin or tools are stale.
- A stable Rust update receives a dedicated compatibility/security change with
  full workspace and platform tests.
- After 1.0, any MSRV/support-window policy must be explicit and must not stop
  security fixes from using a required current compiler.

//! Public facade for the Aetherheim content operating system.
//!
//! The facade exposes admitted stable contracts. Implementations remain in
//! focused workspace crates so this crate never becomes a monolith.

#![forbid(unsafe_code)]

/// Bounded input primitives.
pub use aetherheim_bounds as bounds;
/// Typed configuration contracts.
pub use aetherheim_config as config;
/// Shared product contracts.
pub use aetherheim_core as core;
/// Opaque identifier contracts.
pub use aetherheim_ids as ids;
/// Proof-readiness contracts.
pub use aetherheim_proof_core as proof;

/// Returns the workspace version compiled into this facade.
#[must_use]
pub const fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[cfg(test)]
mod tests {
    #[test]
    fn facade_reports_manifest_version() {
        assert_eq!(super::version(), "0.1.0");
    }
}

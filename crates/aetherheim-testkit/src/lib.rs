//! Deterministic first-party fixtures for workspace tests.

#![forbid(unsafe_code)]

use aetherheim_ids::{IdentifierError, SiteId};

/// Returns a stable non-secret site identifier fixture.
pub fn site_id() -> Result<SiteId, IdentifierError> {
    let mut bytes = [0; 16];
    bytes[0] = 0xa3;
    SiteId::from_bytes(bytes)
}

#[cfg(test)]
mod tests {
    #[test]
    fn fixture_is_constructible() {
        assert!(super::site_id().is_ok());
    }
}

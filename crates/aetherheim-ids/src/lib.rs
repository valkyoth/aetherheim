//! Opaque, allocation-free Aetherheim identifier types.

#![no_std]
#![forbid(unsafe_code)]

use core::fmt;

/// Rejection reason for an invalid identifier.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum IdentifierError {
    /// The all-zero representation is reserved and invalid.
    Zero,
}

/// A nonzero opaque 128-bit identifier.
#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct Identifier([u8; 16]);

impl Identifier {
    /// Validates a byte representation.
    pub const fn from_bytes(bytes: [u8; 16]) -> Result<Self, IdentifierError> {
        let mut index = 0;
        while index < bytes.len() {
            if bytes[index] != 0 {
                return Ok(Self(bytes));
            }
            index += 1;
        }
        Err(IdentifierError::Zero)
    }

    /// Returns the opaque byte representation.
    #[must_use]
    pub const fn into_bytes(self) -> [u8; 16] {
        self.0
    }
}

impl fmt::Debug for Identifier {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str("Identifier(<redacted>)")
    }
}

/// Defines a domain-specific identifier wrapper.
macro_rules! identifier_type {
    ($name:ident, $description:literal) => {
        #[doc = $description]
        #[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
        pub struct $name(Identifier);

        impl $name {
            /// Validates a byte representation in this identifier domain.
            pub const fn from_bytes(bytes: [u8; 16]) -> Result<Self, IdentifierError> {
                match Identifier::from_bytes(bytes) {
                    Ok(identifier) => Ok(Self(identifier)),
                    Err(error) => Err(error),
                }
            }

            /// Returns the opaque byte representation.
            #[must_use]
            pub const fn into_bytes(self) -> [u8; 16] {
                self.0.into_bytes()
            }
        }
    };
}

identifier_type!(TenantId, "Stable tenant identifier.");
identifier_type!(SiteId, "Stable site identifier.");
identifier_type!(ContentId, "Stable content-entry identifier.");
identifier_type!(RevisionId, "Stable immutable-revision identifier.");

#[cfg(test)]
mod tests {
    extern crate std;

    use super::{Identifier, IdentifierError, SiteId};
    use std::format;

    #[test]
    fn zero_is_rejected() {
        assert_eq!(Identifier::from_bytes([0; 16]), Err(IdentifierError::Zero));
    }

    #[test]
    fn nonzero_round_trips() {
        let mut bytes = [0; 16];
        bytes[15] = 1;
        assert_eq!(SiteId::from_bytes(bytes).map(SiteId::into_bytes), Ok(bytes));
    }

    #[test]
    fn debug_does_not_disclose_identifier_bytes() {
        let mut bytes = [0; 16];
        bytes[0] = 0xaa;
        let result = Identifier::from_bytes(bytes).map(|value| format!("{value:?}"));
        assert_eq!(result.as_deref(), Ok("Identifier(<redacted>)"));
    }
}

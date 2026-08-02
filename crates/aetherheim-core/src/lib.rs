//! Dependency-free core Aetherheim contracts.

#![no_std]
#![forbid(unsafe_code)]

use core::fmt;

/// Deployment-oriented security profile.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
#[non_exhaustive]
pub enum SecurityProfile {
    /// Friendly local and personal-site defaults.
    Personal,
    /// Secure defaults for normal production use.
    Standard,
    /// Reduced authority and stricter operational controls.
    Hardened,
    /// Evidence, segregation, and policy controls for regulated use.
    Regulated,
    /// Offline-first operation with no ambient network authority.
    AirGapped,
}

impl SecurityProfile {
    /// Returns the stable configuration name for this profile.
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Personal => "personal",
            Self::Standard => "standard",
            Self::Hardened => "hardened",
            Self::Regulated => "regulated",
            Self::AirGapped => "air-gapped",
        }
    }
}

impl fmt::Display for SecurityProfile {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

/// The storage-authority mode selected by an installation.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorityMode {
    /// A conventional Aetherheim storage adapter is authoritative.
    Conventional,
    /// A conventional store remains authoritative while evidence is witnessed.
    Witness,
    /// A future authority backend owns canonical state.
    Authoritative,
}

#[cfg(test)]
mod tests {
    use super::{AuthorityMode, SecurityProfile};

    #[test]
    fn profile_names_are_stable() {
        assert_eq!(SecurityProfile::Personal.as_str(), "personal");
        assert_eq!(SecurityProfile::Standard.as_str(), "standard");
        assert_eq!(SecurityProfile::Hardened.as_str(), "hardened");
        assert_eq!(SecurityProfile::Regulated.as_str(), "regulated");
        assert_eq!(SecurityProfile::AirGapped.as_str(), "air-gapped");
    }

    #[test]
    fn conventional_authority_is_explicit() {
        assert_ne!(AuthorityMode::Conventional, AuthorityMode::Authoritative);
        assert_ne!(AuthorityMode::Witness, AuthorityMode::Authoritative);
    }
}

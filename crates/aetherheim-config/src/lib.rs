//! Typed configuration contracts for host-side Aetherheim processes.

#![forbid(unsafe_code)]

use aetherheim_core::SecurityProfile;

/// Process role selected for an Aetherheim invocation.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum RuntimeRole {
    /// HTTP delivery and management role.
    Serve,
    /// Durable background-job role.
    Worker,
    /// Timed publication and maintenance role.
    Scheduler,
    /// All supported roles in one process.
    AllInOne,
}

/// Minimal validated startup configuration.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct StartupConfig {
    profile: SecurityProfile,
    role: RuntimeRole,
}

impl StartupConfig {
    /// Creates a startup configuration from already-typed values.
    #[must_use]
    pub const fn new(profile: SecurityProfile, role: RuntimeRole) -> Self {
        Self { profile, role }
    }

    /// Returns the security profile.
    #[must_use]
    pub const fn profile(self) -> SecurityProfile {
        self.profile
    }

    /// Returns the process role.
    #[must_use]
    pub const fn role(self) -> RuntimeRole {
        self.role
    }
}

#[cfg(test)]
mod tests {
    use aetherheim_core::SecurityProfile;

    use super::{RuntimeRole, StartupConfig};

    #[test]
    fn startup_configuration_preserves_explicit_choices() {
        let config = StartupConfig::new(SecurityProfile::Hardened, RuntimeRole::Worker);
        assert_eq!(config.profile(), SecurityProfile::Hardened);
        assert_eq!(config.role(), RuntimeRole::Worker);
    }
}

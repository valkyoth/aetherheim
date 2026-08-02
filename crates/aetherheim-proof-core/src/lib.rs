//! Database-neutral proof-readiness contracts.
//!
//! These contracts do not integrate Skrifheim. They preserve truthful
//! assurance labels for possible post-1.0 authority backends.

#![no_std]
#![forbid(unsafe_code)]

/// Authentication assurance attached to an actor-bound command.
#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub enum AuthenticationAssurance {
    /// Unauthenticated public audience; never sufficient for canonical writes.
    Aal0,
    /// Single-factor authenticated session.
    Aal1,
    /// Multi-factor or user-verifying credential.
    Aal2,
    /// Hardware-backed or enterprise-managed strong credential.
    Aal3,
    /// Deployment-defined high-assurance identity and workload evidence.
    Aal4,
}

/// The truthful provenance claim associated with an operation.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Attribution {
    /// The service associated the action with an authenticated account.
    Attributed,
    /// Aetherheim attested an actor-bound validated command.
    ServiceAttested,
    /// A user completed an explicit step-up approval.
    UserApproved,
    /// A user-controlled or enterprise-issued key signed the exact intent.
    UserSigned,
    /// Multiple authorised approvers satisfied a declared quorum.
    QuorumApproved,
    /// Imported source data named an author without cryptographic proof.
    ImportAttributed,
    /// A deterministic system process derived the result.
    SystemDerived,
    /// A named extension derived the result under a grant.
    PluginDerived,
    /// An AI worker produced an artifact not yet reviewed by a human.
    AiDerivedUnreviewed,
    /// A human reviewed an AI-derived artifact.
    AiDerivedReviewed,
}

/// Why an evidence or policy decision did not allow an operation.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Decision {
    /// The operation is allowed without additional constraints.
    Allow,
    /// The operation is allowed under explicit constraints.
    ConstrainedAllow,
    /// Protected fields must be redacted.
    Redact,
    /// A bound approval is required before continuing.
    ApprovalRequired,
    /// The operation is denied.
    Deny,
    /// More verified evidence is required before deciding.
    MoreEvidenceRequired,
}

impl Decision {
    /// Reports whether an operation may proceed immediately.
    #[must_use]
    pub const fn may_proceed(self) -> bool {
        matches!(self, Self::Allow | Self::ConstrainedAllow | Self::Redact)
    }
}

#[cfg(test)]
mod tests {
    use super::{Attribution, AuthenticationAssurance, Decision};

    #[test]
    fn assurance_order_is_monotonic() {
        assert!(AuthenticationAssurance::Aal0 < AuthenticationAssurance::Aal1);
        assert!(AuthenticationAssurance::Aal3 < AuthenticationAssurance::Aal4);
    }

    #[test]
    fn only_immediate_decisions_proceed() {
        assert!(Decision::Allow.may_proceed());
        assert!(Decision::Redact.may_proceed());
        assert!(!Decision::ApprovalRequired.may_proceed());
        assert!(!Decision::Deny.may_proceed());
    }

    #[test]
    fn imported_attribution_is_distinct_from_user_signature() {
        assert_ne!(Attribution::ImportAttributed, Attribution::UserSigned);
    }
}

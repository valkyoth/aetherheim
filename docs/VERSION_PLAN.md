# Aetherheim Version Plan

The complete version-by-version plan is maintained in
[RELEASE_PLAN.md](RELEASE_PLAN.md). That document is the authoritative version
plan and uses the required Goal, Deliverables, Verification, Exit criteria, and
pentest handoff stop for every milestone. The user-controlled individual or
cumulative workflow is documented in [release-workflow.md](release-workflow.md).

Version identities are intentionally allowed beyond `v0.99.0`; they are not
compressed or renumbered to fit an arbitrary band. `v1.0.0` remains the first
serious production release. Admission, implementation, live qualification,
independent domain state machines, platform packaging, and recovery are split
when they require separate evidence or rollback.

Post-1.0 numbering is also intentionally separated by product boundary:
`v1.1.0` through `v1.20.0` build and qualify dedicated native Android and iOS
client applications, while optional Skrifheim work begins at `v1.100.0` and
remains blocked by its own entry conditions. Android and iOS are not pre-1.0
server, worker, scheduler, database, or Rust-library embedding targets.

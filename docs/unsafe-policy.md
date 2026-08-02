# Unsafe Code Policy

The current workspace uses `#![forbid(unsafe_code)]` and denies unsafe code
through inherited lints. No current exception exists.

A future platform boundary may require unsafe Rust. It must receive a dedicated
crate and release with:

- a written impossibility/necessity analysis;
- smallest possible private unsafe surface;
- line-by-line safety invariants;
- safe public API and invalid-state tests;
- Miri, sanitizer, fuzz, platform, and failure evidence;
- independent review and coverage by the applicable green pentest report;
- no mixing with unrelated domain logic.

Unsafe code may not be introduced through generated or copied source to evade
this policy.

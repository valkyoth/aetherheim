# Current Status

Version 0.1.0 is in implementation and establishes only the repository and
portable contract foundation. The CLI provides help, version, and truthful
diagnostics. No CMS, network, storage, authentication, rendering, media,
extension, commerce, compliance, or Skrifheim runtime behavior is available.
The implemented CLI surface has a black-box smoke suite that launches the real
binary; future runtime/provider profiles must extend the same acceptance entry
point before support is claimed.

See [Release Plan](RELEASE_PLAN.md) for the implementation sequence and
[Security Controls](security-controls.md) for implemented versus required
controls. See [Acceptance Testing](acceptance-testing.md) for the mandatory
real-process and live-provider policy.

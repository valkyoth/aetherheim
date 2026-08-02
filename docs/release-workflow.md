# Simple Human-Controlled Release Workflow

Status: mandatory release process

The release process has one human decision-maker and no automatic tag or push.

## Normal Release

1. Codex implements the version, updates documentation and release notes, runs
   all required checks and executable acceptance profiles, and stops.
2. Codex tells the user that the candidate is ready for pentesting. No tag or
   push is created.
3. The user arranges the pentest.
4. If findings exist, the user places `PENTEST.md` at the repository root.
   Codex reads it, updates the permanent `security/pentest/vX.Y.Z.md` report,
   fixes the findings, adds regression/acceptance tests, runs the full gates,
   and removes the temporary root file. This loop repeats for new findings.
5. If the pentest is green, Codex records the result and tested commit in the
   permanent report, runs `scripts/release_gate.sh VERSION`, and commits the
   candidate and report. The project then waits for GitHub.
6. If GitHub reports a failure, the user tells Codex. Codex fixes it, updates
   the permanent pentest report with the post-pentest change, reruns all gates,
   commits again, and waits for GitHub again.
7. If GitHub is green, nothing further happens until the user explicitly tells
   Codex to tag and push. That instruction is the only tag/push authority.

`PENTEST.md` is temporary scratch, ignored by Git, and never becomes the
permanent record. Removing it after its contents and remediation status are
captured in the permanent report is an explicitly authorised cleanup step.
Known unresolved release-blocking findings always stop the workflow.

## Batched Pentest

Individual pentesting is the default. The user may explicitly authorise a
named batch of up to 15 versions to share one cumulative pentest.

The batch uses one file under `security/pentest/batches/`. It lists every
covered version explicitly, records the user's authorisation, and starts with
`Status: DEFERRED`. Each intermediate release truthfully links to that report;
it must not claim an individual pentest or PASS.

The final listed version stops for a pentest covering the complete change set
from the batch baseline through the final candidate, all shipped migrations,
supported upgrade paths, and the accumulated release artifacts. Findings use
the same temporary-root-file remediation loop. The batch report changes to
`Status: PASS` only after the cumulative pentest is green. A sixteenth release,
an unlisted release, or the final listed release with a deferred report fails
the gate.

The user's batch instruction is required each time; batching is never inferred
from previous releases. A batch does not hide known findings or weaken tests,
CI, audit, acceptance, documentation, or release-note requirements.

## Permanent Report Fields

An individual PASS report contains:

```text
Status: PASS
Mode: individual
Tested-Commit: <40 lowercase hexadecimal characters>
Tester: <name or organisation>
Scope: <tested surfaces and topology>
Date: <YYYY-MM-DD>
```

A batch report contains:

```text
Status: DEFERRED | PASS
Mode: batch
Covered-Versions: vX.Y.Z, vX.Y.Z, ...
Authorization: <user instruction and date/context>
Baseline: <tag or 40-character commit>
```

When a batch becomes PASS it also records `Tested-Commit`, `Tester`, `Scope`,
and `Date`. Both report forms maintain findings, remediations, retest results,
and post-pentest GitHub fixes without deleting history.

#!/usr/bin/env python3
"""Self-tests for release-plan milestone validation."""

from __future__ import annotations

import check_release_plan


def main() -> int:
    valid = """### v0.1.0 — Foundation
Status: planned.
Goal: Start.
Deliverables:
Verification:
Exit criteria:
`v0.1.0 implementation stop reached. Run pentest for this exact commit.`
"""
    assert check_release_plan.validate(valid) == []
    assert any("pentest stop" in error for error in check_release_plan.validate(valid.replace("Run pentest", "Skip pentest")))
    assert any("missing Goal:" in error for error in check_release_plan.validate(valid.replace("Goal:", "Aim:")))
    assert any("duplicate" in error for error in check_release_plan.validate(valid + valid))
    print("release plan validation tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

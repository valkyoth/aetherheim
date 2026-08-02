#!/usr/bin/env python3
"""Validate that every release milestone is a complete pentest handoff."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADING = re.compile(r"^### v([^ ]+) (?:—|-) .+$", re.MULTILINE)
REQUIRED = ("Status:", "Goal:", "Deliverables:", "Verification:", "Exit criteria:")


def validate(text: str) -> list[str]:
    errors: list[str] = []
    matches = list(HEADING.finditer(text))
    if not matches:
        return ["release plan contains no version milestones"]
    seen: set[str] = set()
    for index, match in enumerate(matches):
        version = match.group(1)
        if version in seen:
            errors.append(f"v{version}: duplicate milestone")
        seen.add(version)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end() : end]
        for label in REQUIRED:
            if label not in section:
                errors.append(f"v{version}: missing {label}")
        stop = f"`v{version} implementation stop reached. Run pentest for this exact commit.`"
        if stop not in section:
            errors.append(f"v{version}: missing exact pentest stop")
    return errors


def main() -> int:
    plan = Path(__file__).resolve().parents[1] / "docs/RELEASE_PLAN.md"
    errors = validate(plan.read_text(encoding="utf-8"))
    if errors:
        print("release plan violations:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("release plan milestone format ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

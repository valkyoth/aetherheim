#!/usr/bin/env python3
"""Validate local Markdown links without fetching remote resources."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing: list[str] = []
    for source in sorted(root.rglob("*.md")):
        if any(
            part in {".cargo-deny-advisory-dbs", ".git", "target"}
            for part in source.parts
        ):
            continue
        text = source.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            path = root / target.lstrip("/") if target.startswith("/") else source.parent / target
            if not path.exists():
                missing.append(f"{source.relative_to(root)} -> {raw}")
    if missing:
        print("missing Markdown link targets:", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("documentation links ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

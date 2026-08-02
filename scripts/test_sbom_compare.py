#!/usr/bin/env python3
"""Regression tests for semantic SPDX drift comparison."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import compare_sbom


def write_document(path: Path, version: str, reverse: bool) -> None:
    packages = [
        {"SPDXID": "SPDXRef-Package-aetherheim", "versionInfo": version},
        {"SPDXID": "SPDXRef-Package-core", "versionInfo": "0.1.0"},
    ]
    if reverse:
        packages.reverse()
    document = {
        "SPDXID": "SPDXRef-DOCUMENT",
        "creationInfo": {
            "created": "2026-08-02T00:00:01Z" if reverse else "2026-08-02T00:00:00Z",
            "creators": ["Tool: cargo-sbom"],
        },
        "documentNamespace": f"https://spdx.org/spdxdocs/{'second' if reverse else 'first'}",
        "packages": packages,
    }
    path.write_text(json.dumps(document), encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="aetherheim-sbom-") as directory:
        root = Path(directory)
        expected = root / "expected.json"
        reordered = root / "reordered.json"
        drifted = root / "drifted.json"
        write_document(expected, "0.1.0", reverse=False)
        write_document(reordered, "0.1.0", reverse=True)
        write_document(drifted, "0.2.0", reverse=True)
        assert compare_sbom.documents_match(expected, reordered)
        assert not compare_sbom.documents_match(expected, drifted)
    print("SBOM comparison tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Offline regression tests for admitted crate freshness selection."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_checker():
    script = Path(__file__).with_name("check_latest_crates.py")
    spec = importlib.util.spec_from_file_location("latest_crates", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load latest crate checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    checker = load_checker()
    assert checker.numeric_version("1.2.3") == (1, 2, 3)
    assert checker.numeric_version("1.2") is None
    metadata = {
        "versions": [
            {"num": "1.0.0", "yanked": False, "rust_version": "1.90"},
            {"num": "1.1.0", "yanked": True, "rust_version": "1.90"},
            {"num": "2.0.0-beta.1", "yanked": False, "rust_version": "1.90"},
            {"num": "2.0.0", "yanked": False, "rust_version": "1.98"},
        ]
    }
    assert checker.latest_compatible(metadata, (1, 97, 1)) == "1.0.0"
    assert checker.latest_compatible(metadata, (1, 98, 0)) == "2.0.0"
    try:
        checker.latest_compatible({"versions": []}, (1, 97, 1))
    except ValueError:
        pass
    else:
        raise AssertionError("empty metadata must fail")
    print("latest crate checker tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

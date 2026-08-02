#!/usr/bin/env python3
"""Self-tests for dependency admission and publication policy."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


def load_policy():
    script = Path(__file__).with_name("check_dependency_policy.py")
    spec = importlib.util.spec_from_file_location("dependency_policy", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load dependency policy module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def foundation(root: Path) -> None:
    write(
        root / "Cargo.toml",
        '[workspace]\nmembers=["crates/core"]\n[workspace.dependencies]\ncore={path="crates/core"}\n',
    )
    write(root / "dependency-admissions.toml", "version=1\n[crates]\n")
    write(
        root / "crates/core/Cargo.toml",
        '[package]\nname="core"\nversion="0.1.0"\npublish=false\n',
    )


def main() -> int:
    policy = load_policy()
    with tempfile.TemporaryDirectory(prefix="aetherheim-policy-") as directory:
        root = Path(directory)
        foundation(root)
        assert policy.validate(root) == []

        write(
            root / "crates/core/Cargo.toml",
            '[package]\nname="core"\nversion="0.1.0"\n[dependencies]\nserde="1.0.0"\n',
        )
        errors = policy.validate(root)
        assert any("publish = false" in error for error in errors)
        assert any("explicit dependency table" in error for error in errors)

        write(
            root / "crates/core/Cargo.toml",
            '[package]\nname="core"\nversion="0.1.0"\npublish=false\n[dependencies]\nserde={version="=1.0.228"}\n',
        )
        assert any("admission must be a table" in error for error in policy.validate(root))

        write(
            root / "dependency-admissions.toml",
            'version=1\n[crates.serde]\nversion="1.0.228"\npurpose="serialization"\nscope=["api"]\nlicense="MIT OR Apache-2.0"\nreviewed=2026-08-02\n',
        )
        assert policy.validate(root) == []

        write(
            root / "crates/core/Cargo.toml",
            '[package]\nname="core"\nversion="0.1.0"\npublish=false\n[dependencies]\nserde={git="https://example.invalid/serde",rev="abc"}\n',
        )
        assert any("git dependencies are prohibited" in error for error in policy.validate(root))

        foundation(root)
        write(
            root / "crates/core/Cargo.toml",
            '[package]\nname="core"\nversion="0.1.0"\npublish=false\n[dependencies]\nout={path="../../../outside"}\n',
        )
        assert any("escapes the workspace" in error for error in policy.validate(root))

        foundation(root)
        write(
            root / "crates/core/Cargo.toml",
            '[package]\nname="core"\nversion="0.1.0"\npublish=false\n[dependencies]\nzeroize={version="=1.8.2"}\n',
        )
        errors = policy.validate(root)
        assert any("zeroize is prohibited" in error for error in errors)

        foundation(root)
        write(
            root / "crates/core/Cargo.toml",
            '[package]\nname="core"\nversion="0.1.0"\npublish=false\n[dependencies]\nwipe={package="zeroize",version="=1.8.2"}\n',
        )
        errors = policy.validate(root)
        assert any("zeroize is prohibited" in error for error in errors)

        foundation(root)
        write(
            root / "Cargo.lock",
            'version = 4\n\n[[package]]\nname = "zeroize"\nversion = "1.8.2"\n',
        )
        errors = policy.validate(root)
        assert any("transitive crate zeroize is prohibited" in error for error in errors)
    print("dependency policy self-tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

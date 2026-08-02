#!/usr/bin/env python3
"""Check every admitted direct crates.io dependency against current releases."""

from __future__ import annotations

import importlib.util
import json
import re
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "valkyoth-aetherheim-dependency-check/0.1.0"
VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def load_policy():
    script = Path(__file__).with_name("check_dependency_policy.py")
    spec = importlib.util.spec_from_file_location("dependency_policy", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load dependency policy module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def numeric_version(value: str) -> tuple[int, int, int] | None:
    match = VERSION.fullmatch(value)
    if match is None:
        return None
    return tuple(int(part) for part in match.groups())


def crate_metadata(name: str) -> dict[str, object]:
    request = urllib.request.Request(
        f"https://crates.io/api/v1/crates/{name}",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
        raise RuntimeError(f"could not query crates.io metadata for {name}: {error}") from error


def latest_compatible(metadata: dict[str, object], rust: tuple[int, int, int]) -> str:
    candidates: list[tuple[tuple[int, int, int], str]] = []
    versions = metadata.get("versions")
    if not isinstance(versions, list):
        raise ValueError("crates.io response has no versions list")
    for entry in versions:
        if not isinstance(entry, dict) or entry.get("yanked"):
            continue
        number = entry.get("num")
        if not isinstance(number, str):
            continue
        parsed = numeric_version(number)
        if parsed is None:
            continue
        rust_version = entry.get("rust_version")
        if isinstance(rust_version, str):
            normalized = rust_version if rust_version.count(".") == 2 else f"{rust_version}.0"
            required = numeric_version(normalized)
            if required is None or required > rust:
                continue
        candidates.append((parsed, number))
    if not candidates:
        raise ValueError("crates.io response has no stable compatible version")
    return max(candidates)[1]


def main() -> int:
    policy = load_policy()
    errors = policy.validate(ROOT)
    if errors:
        raise SystemExit("dependency policy failed:\n- " + "\n- ".join(errors))
    dependencies = policy.external_dependencies(ROOT)
    if not dependencies:
        print("no external crates are currently admitted; freshness check is vacuous")
        return 0

    with (ROOT / "Cargo.toml").open("rb") as source:
        rust_text = tomllib.load(source)["workspace"]["package"]["rust-version"]
    rust = numeric_version(rust_text)
    if rust is None:
        raise ValueError(f"invalid workspace rust-version: {rust_text}")

    stale: list[str] = []
    for name, declared in sorted(dependencies.items()):
        latest = latest_compatible(crate_metadata(name), rust)
        if declared != latest:
            stale.append(f"{name}: declared={declared} latest-compatible={latest}")
        else:
            print(f"{name}: {declared} current")
    if stale:
        raise SystemExit("outdated admitted dependencies:\n- " + "\n- ".join(stale))
    print(f"all {len(dependencies)} admitted external crates are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Enforce reviewed minimal dependencies and disabled package publishing."""

from __future__ import annotations

import argparse
import datetime
import re
import sys
import tomllib
from pathlib import Path

DEPENDENCY_TABLES = {"dependencies", "dev-dependencies", "build-dependencies"}
IGNORED_PARTS = {".git", "target"}
EXACT_VERSION = re.compile(r"^=(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)$")
ADMISSION_FIELDS = {"version", "purpose", "scope", "license", "reviewed"}
FORBIDDEN_CRATES = {
    "zeroize": "use the reviewed sanitization crate and Aetherheim secret boundary",
}


def manifests(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("Cargo.toml")
        if not IGNORED_PARTS.intersection(path.relative_to(root).parts)
    )


def dependency_tables(value: object, name: str = ""):
    if not isinstance(value, dict):
        return
    if name in DEPENDENCY_TABLES:
        yield value
        return
    for child_name, child in value.items():
        yield from dependency_tables(child, child_name)


def inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def admissions(root: Path) -> tuple[dict[str, object], list[str]]:
    path = root / "dependency-admissions.toml"
    if not path.is_file():
        return {}, [f"{path}: missing dependency admission register"]
    with path.open("rb") as source:
        document = tomllib.load(source)
    crates = document.get("crates")
    if not isinstance(crates, dict):
        return {}, [f"{path}: [crates] table is required"]
    return crates, []


def external_dependencies(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for manifest in manifests(root):
        with manifest.open("rb") as source:
            document = tomllib.load(source)
        for table in dependency_tables(document):
            for name, specification in table.items():
                if not isinstance(specification, dict):
                    continue
                if specification.get("workspace") is True or "path" in specification:
                    continue
                version = specification.get("version")
                if isinstance(version, str):
                    match = EXACT_VERSION.fullmatch(version)
                    if match is not None:
                        result[name] = match.group(1)
    return result


def validate_admission(name: str, version: str, entry: object) -> list[str]:
    if not isinstance(entry, dict):
        return [f"dependency-admissions.toml: {name} admission must be a table"]
    errors = [
        f"dependency-admissions.toml: {name} missing {field}"
        for field in sorted(ADMISSION_FIELDS.difference(entry))
    ]
    if entry.get("version") != version:
        errors.append(f"dependency-admissions.toml: {name} version must be {version}")
    if not isinstance(entry.get("purpose"), str) or not entry.get("purpose"):
        errors.append(f"dependency-admissions.toml: {name} purpose must be non-empty")
    scope = entry.get("scope")
    if not isinstance(scope, list) or not scope or not all(isinstance(item, str) for item in scope):
        errors.append(f"dependency-admissions.toml: {name} scope must be a non-empty string list")
    if not isinstance(entry.get("license"), str) or not entry.get("license"):
        errors.append(f"dependency-admissions.toml: {name} license must be non-empty")
    if not isinstance(entry.get("reviewed"), datetime.date):
        errors.append(f"dependency-admissions.toml: {name} reviewed must be a TOML date")
    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    found = manifests(root)
    admitted, admission_errors = admissions(root)
    errors.extend(admission_errors)
    used_external: dict[str, str] = {}
    if not found:
        return errors + ["no Cargo.toml manifests found"]

    for manifest in found:
        with manifest.open("rb") as source:
            document = tomllib.load(source)
        package = document.get("package")
        if isinstance(package, dict) and package.get("publish") is not False:
            errors.append(f"{manifest}: package must set publish = false")

        for table in dependency_tables(document):
            for name, specification in table.items():
                package_name = (
                    specification.get("package", name)
                    if isinstance(specification, dict)
                    else name
                )
                if package_name in FORBIDDEN_CRATES:
                    errors.append(
                        f"{manifest}: {package_name} is prohibited; "
                        f"{FORBIDDEN_CRATES[package_name]}"
                    )
                    continue
                if isinstance(specification, dict) and specification.get("workspace") is True:
                    continue
                if isinstance(specification, dict) and isinstance(specification.get("path"), str):
                    dependency = manifest.parent / specification["path"]
                    if not inside(root, dependency):
                        errors.append(f"{manifest}: {name} path escapes the workspace")
                    continue
                if not isinstance(specification, dict):
                    errors.append(f"{manifest}: {name} must use an explicit dependency table")
                    continue
                if "git" in specification:
                    errors.append(f"{manifest}: {name} git dependencies are prohibited")
                    continue
                if "registry" in specification:
                    errors.append(f"{manifest}: {name} custom registries are prohibited")
                    continue
                version = specification.get("version")
                match = EXACT_VERSION.fullmatch(version) if isinstance(version, str) else None
                if match is None:
                    errors.append(f"{manifest}: {name} must pin an exact =X.Y.Z crates.io version")
                    continue
                normalized = match.group(1)
                previous = used_external.setdefault(name, normalized)
                if previous != normalized:
                    errors.append(f"{manifest}: {name} has conflicting versions {previous} and {normalized}")
                errors.extend(validate_admission(name, normalized, admitted.get(name)))

        for forbidden in ("patch", "replace"):
            if forbidden in document:
                errors.append(f"{manifest}: [{forbidden}] overrides are prohibited")

    for name in sorted(set(admitted).difference(used_external)):
        errors.append(f"dependency-admissions.toml: unused admission for {name}")
    vendor = root / "vendor"
    if vendor.exists():
        errors.append(f"{vendor}: vendored source requires a separate reviewed policy change")
    lockfile = root / "Cargo.lock"
    if lockfile.is_file():
        with lockfile.open("rb") as source:
            locked = tomllib.load(source)
        for package in locked.get("package", []):
            if isinstance(package, dict) and package.get("name") in FORBIDDEN_CRATES:
                name = package["name"]
                errors.append(
                    f"{lockfile}: transitive crate {name} is prohibited; "
                    f"{FORBIDDEN_CRATES[name]}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate(root)
    if errors:
        print("dependency/publication policy violations:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    count = len(external_dependencies(root))
    print(f"dependency policy ok: {count} reviewed external crates, publishing disabled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

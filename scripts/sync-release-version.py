#!/usr/bin/env python3
"""Write or validate the unscoped npm compatibility release identity."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "release/version.json"
GENERATED_TREE_PARTS = frozenset(
    {".git", ".venv", "_build", "build", "dist", "node_modules", "target", "venv"}
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def rewrite_candidate_tokens(patterns: tuple[str, ...], canonical: str) -> None:
    base, candidate = canonical.split("-rc.", 1)
    escaped = re.escape(base)
    for pattern in patterns:
        for target in ROOT.glob(pattern):
            relative = target.relative_to(ROOT)
            if not target.is_file() or GENERATED_TREE_PARTS.intersection(
                relative.parts
            ):
                continue
            source = target.read_text(encoding="utf-8")
            source = re.sub(rf"{escaped}-rc\.\d+", canonical, source)
            target.write_text(source, encoding="utf-8")


def write(model: dict) -> None:
    package_path = ROOT / "package.json"
    package = load(package_path)
    package["version"] = model["npm"]
    package["dependencies"] = model["dependencies"]
    package["publishConfig"]["tag"] = model["distTag"]
    dump(package_path, package)

    lock_path = ROOT / "package-lock.json"
    lock = load(lock_path)
    lock["version"] = model["npm"]
    root = lock["packages"][""]
    root["version"] = model["npm"]
    root["dependencies"] = model["dependencies"]
    dump(lock_path, lock)
    rewrite_candidate_tokens(
        ("README.md", "MIGRATION.md", "test/*.mjs"), model["canonical"]
    )


def validate(model: dict) -> list[str]:
    failures: list[str] = []
    package = load(ROOT / "package.json")
    lock = load(ROOT / "package-lock.json")
    if model["canonical"] != model["npm"]:
        failures.append("canonical and npm versions differ")
    if model.get("sourceTag") != f"v{model['canonical']}-release.1":
        failures.append("corrective source tag must be the append-only release.1 ref")
    if package["version"] != model["npm"] or lock["version"] != model["npm"]:
        failures.append("package or lock version is stale")
    if package["dependencies"] != model["dependencies"]:
        failures.append("scoped facade dependency is stale")
    if package.get("publishConfig", {}).get("tag") != "next":
        failures.append("release candidates must publish under next")
    if model.get("legacyLatest") != {
        "version": "2.0.4",
        "mustRemainUnchangedDuringRc": True,
    }:
        failures.append("legacy latest protection policy changed")
    release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    for marker in (
        "scripts/check-release-ref.py",
        "environment: github-release",
        "environment: npm",
    ):
        if marker not in release:
            failures.append(f"release workflow is missing {marker}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    model = load(MODEL_PATH)
    if args.write:
        write(model)
    failures = validate(model)
    for failure in failures:
        print(f"release-version error: {failure}", file=sys.stderr)
    if failures:
        return 1
    print(
        f"release versions agree with {model['canonical']}; legacy latest remains protected"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

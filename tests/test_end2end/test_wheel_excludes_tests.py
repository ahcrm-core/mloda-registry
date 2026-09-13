"""Root setuptools package discovery must not ship in-tree test packages in the workspace wheel."""

from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[import-not-found,unused-ignore]

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PYPROJECT = _REPO_ROOT / "pyproject.toml"
_PACKAGE_ROOT = _REPO_ROOT / "mloda"


def _package_name(tests_dir: Path) -> str:
    """Dotted package name for a tests directory under the included package tree."""
    return ".".join(tests_dir.relative_to(_REPO_ROOT).parts)


def _covered(package_name: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(package_name, pattern) for pattern in patterns)


def test_setuptools_find_excludes_every_in_tree_tests_package() -> None:
    """[tool.setuptools.packages.find] exclude must match every tests package under mloda/."""
    config = tomllib.loads(_PYPROJECT.read_text())
    setuptools = config["tool"]["setuptools"]
    find = setuptools["packages"]["find"]

    assert setuptools.get("include-package-data") is False, (
        "[tool.setuptools] include-package-data must be false so a stale SOURCES.txt "
        "cannot re-add excluded test modules as package data"
    )
    patterns = list(find.get("exclude") or [])
    assert "*.tests" in patterns
    assert "*.tests.*" in patterns

    tests_dirs = sorted(path for path in _PACKAGE_ROOT.rglob("tests") if path.is_dir())
    assert tests_dirs, "expected in-tree tests directories under mloda/"

    uncovered = [
        _package_name(path) for path in tests_dirs if not _covered(_package_name(path), patterns)
    ]
    assert not uncovered, (
        "setuptools exclude patterns do not cover these tests packages: " + ", ".join(uncovered)
    )

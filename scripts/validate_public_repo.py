from __future__ import annotations

import argparse
import re
import shutil
# Git metadata inspection uses one fixed argv command with shell disabled.
import subprocess  # nosec B404
from pathlib import Path
from typing import NamedTuple


class Issue(NamedTuple):
    path: str
    rule: str
    message: str


REQUIRED_FILES = {"README.md", "ARCHITECTURE.md", "SECURITY.md"}
FORBIDDEN_SUFFIXES = {
    ".db",
    ".env",
    ".jsonl",
    ".key",
    ".pem",
    ".pickle",
    ".pkl",
    ".sqlite",
    ".sqlite3",
}
SKIP_DIRS = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__", "htmlcov"}
SKIP_FILES = {".coverage"}
FORBIDDEN_PATH_PARTS = {
    ".codegraph",
    "graphify-out",
    "sources",
    "transcripts",
    "vault",
}
TEXT_SUFFIXES = {"", ".md", ".mmd", ".py", ".toml", ".txt", ".yaml", ".yml"}

_github_token = "gh" + r"[pousr]_[A-Za-z0-9]{20,}"
_model_token = "s" + r"k-[A-Za-z0-9_-]{20,}"
SECRET_PATTERN = re.compile(
    rf"(?:{_github_token}|{_model_token}|AKIA[0-9A-Z]{{16}}|BEGIN[ ]+(?:RSA[ ]+)?PRIVATE[ ]+KEY)",
    re.IGNORECASE,
)
LOCAL_PATH_PATTERN = re.compile(
    r"(?:\b[A-Z]:[\\/](?:Users|Documents[ ]and[ ]Settings)[\\/]|/(?:Users|home)/)",
    re.IGNORECASE,
)
EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)
NOREPLY_EMAIL_PATTERN = re.compile(
    r"^[A-Z0-9.+_-]+@users\.noreply\.github\.com$",
    re.IGNORECASE,
)
PRIVATE_CONTENT_PATHS = (
    "sources" + "/raw",
    "transcripts" + "/",
    "graphify" + "-out/",
    ".code" + "graph/",
)


def _visible_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        yield path, relative


def _git_metadata_issues(root: Path) -> list[Issue]:
    if not (root / ".git").exists():
        return []
    git_executable = shutil.which("git")
    if not git_executable:
        return [Issue(".git", "git-history", "Git metadata could not be inspected")]
    try:
        # The executable is resolved to an absolute path and no user text is code.
        result = subprocess.run(  # nosec B603
            [git_executable, "-C", str(root), "log", "--format=%ae%n%ce"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except OSError:
        return [Issue(".git", "git-history", "Git metadata could not be inspected")]
    if result.returncode:
        return [Issue(".git", "git-history", "Git metadata could not be inspected")]
    emails = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    return [
        Issue(".git", "git-email", "commit metadata must use a GitHub noreply address")
        for email in emails
        if not NOREPLY_EMAIL_PATTERN.fullmatch(email)
    ]


def scan_tree(root: Path) -> list[Issue]:
    root = root.resolve()
    issues = _git_metadata_issues(root)

    for required in sorted(REQUIRED_FILES):
        if not (root / required).is_file():
            issues.append(Issue(required, "required-file", "required public document is missing"))

    for path, relative in _visible_files(root):
        display = relative.as_posix()
        lowered_parts = {part.lower() for part in relative.parts}
        if lowered_parts & FORBIDDEN_PATH_PARTS:
            issues.append(Issue(display, "forbidden-path", "private artifact directory is not allowed"))
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            issues.append(Issue(display, "forbidden-file", "private artifact file type is not allowed"))
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            issues.append(Issue(display, "unexpected-file", "only reviewable text artifacts are allowed"))
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            issues.append(Issue(display, "utf8", "file is not readable UTF-8 text"))
            continue

        if SECRET_PATTERN.search(text):
            issues.append(Issue(display, "secret-pattern", "token or private-key pattern detected"))
        if LOCAL_PATH_PATTERN.search(text):
            issues.append(Issue(display, "local-path", "local home-directory path detected"))
        if EMAIL_PATTERN.search(text):
            issues.append(Issue(display, "email", "email-like identifier detected"))
        normalized = text.replace("\\", "/").lower()
        if any(fragment in normalized for fragment in PRIVATE_CONTENT_PATHS):
            issues.append(Issue(display, "private-content-path", "private runtime path detected"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the architecture-only public boundary")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    issues = scan_tree(root)
    if issues:
        for issue in issues:
            print(f"FAIL {issue.rule}: {issue.path} -- {issue.message}")
        return 1
    print("PASS public-boundary: no forbidden data, paths, secrets, or artifact types detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

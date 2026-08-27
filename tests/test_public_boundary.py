from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_public_repo.py"
SPEC = importlib.util.spec_from_file_location("validate_public_repo", SCRIPT)
if not SPEC or not SPEC.loader:
    raise RuntimeError("public boundary validator could not be loaded")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def _minimal_repo(root: Path) -> None:
    (root / "README.md").write_text("# Public architecture\n", encoding="utf-8")
    (root / "ARCHITECTURE.md").write_text("# Architecture\n", encoding="utf-8")
    (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")


def _commit_minimal_repo(root: Path, email: str) -> None:
    _minimal_repo(root)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Public Test"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", email], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-q", "-m", "test fixture"],
        check=True,
    )


class PublicBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_clean_architecture_repository_passes(self) -> None:
        _minimal_repo(self.root)

        self.assertEqual(validator.scan_tree(self.root), [])

    def test_windows_home_path_is_rejected(self) -> None:
        _minimal_repo(self.root)
        leaked_path = "".join(
            ["C", ":", "\\", "Users", "\\", "private", "\\", "note.md"]
        )
        (self.root / "docs.md").write_text(leaked_path, encoding="utf-8")

        issues = validator.scan_tree(self.root)

        self.assertTrue(any(issue.rule == "local-path" for issue in issues))

    def test_token_like_value_is_rejected_without_echoing_it(self) -> None:
        _minimal_repo(self.root)
        token = "".join(["g", "h", "p", "_", "A" * 36])
        (self.root / "docs.md").write_text(token, encoding="utf-8")

        issues = validator.scan_tree(self.root)

        self.assertTrue(any(issue.rule == "secret-pattern" for issue in issues))
        self.assertTrue(all(token not in issue.message for issue in issues))

    def test_email_like_identifier_is_rejected(self) -> None:
        _minimal_repo(self.root)
        address = "person" + "@" + "example.com"
        (self.root / "docs.md").write_text(address, encoding="utf-8")

        self.assertTrue(
            any(issue.rule == "email" for issue in validator.scan_tree(self.root))
        )

    def test_private_artifact_extensions_are_rejected(self) -> None:
        _minimal_repo(self.root)
        (self.root / "memory.sqlite").write_bytes(b"not a public artifact")

        self.assertTrue(
            any(
                issue.rule == "forbidden-file"
                for issue in validator.scan_tree(self.root)
            )
        )

    def test_tool_caches_are_ignored(self) -> None:
        _minimal_repo(self.root)
        cache = self.root / ".ruff_cache" / "version" / "entry"
        cache.parent.mkdir(parents=True)
        cache.write_bytes(b"\xff\xfe")

        self.assertEqual(validator.scan_tree(self.root), [])

    def test_private_directory_is_rejected(self) -> None:
        _minimal_repo(self.root)
        private_note = self.root / "vault" / "note.md"
        private_note.parent.mkdir()
        private_note.write_text("private", encoding="utf-8")

        self.assertTrue(
            any(issue.rule == "forbidden-path" for issue in validator.scan_tree(self.root))
        )

    def test_private_runtime_path_in_content_is_rejected(self) -> None:
        _minimal_repo(self.root)
        private_path = "sources" + "/raw/example"
        (self.root / "docs.md").write_text(private_path, encoding="utf-8")

        self.assertTrue(
            any(
                issue.rule == "private-content-path"
                for issue in validator.scan_tree(self.root)
            )
        )

    def test_non_utf8_text_is_rejected(self) -> None:
        _minimal_repo(self.root)
        (self.root / "docs.md").write_bytes(b"\xff\xfe")

        self.assertTrue(any(issue.rule == "utf8" for issue in validator.scan_tree(self.root)))

    def test_unexpected_binary_type_is_rejected(self) -> None:
        _minimal_repo(self.root)
        (self.root / "image.png").write_bytes(b"synthetic")

        self.assertTrue(
            any(issue.rule == "unexpected-file" for issue in validator.scan_tree(self.root))
        )

    def test_cli_returns_success_and_failure_without_echoing_secret(self) -> None:
        _minimal_repo(self.root)
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["validator", str(self.root)]):
            with contextlib.redirect_stdout(output):
                self.assertEqual(validator.main(), 0)
        self.assertIn("PASS public-boundary", output.getvalue())

        token = "".join(["g", "h", "p", "_", "B" * 36])
        (self.root / "docs.md").write_text(token, encoding="utf-8")
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["validator", str(self.root)]):
            with contextlib.redirect_stdout(output):
                self.assertEqual(validator.main(), 1)
        self.assertNotIn(token, output.getvalue())

    def test_missing_required_architecture_file_is_rejected(self) -> None:
        (self.root / "README.md").write_text("# Incomplete\n", encoding="utf-8")

        issues = validator.scan_tree(self.root)

        self.assertTrue(any(issue.rule == "required-file" for issue in issues))

    def test_published_contract_covers_loaded_stale_writers(self) -> None:
        repository = SCRIPT.parents[1]
        architecture = (repository / "ARCHITECTURE.md").read_text(encoding="utf-8")
        security = (repository / "SECURITY.md").read_text(encoding="utf-8")
        failures = (repository / "docs" / "failure-lessons.md").read_text(
            encoding="utf-8"
        )
        diagram = (repository / "diagrams" / "system.mmd").read_text(
            encoding="utf-8"
        )

        self.assertIn("writer epoch", architecture.lower())
        self.assertIn("tombstone", architecture.lower())
        self.assertIn("before semantic mutation", security.lower())
        self.assertIn("app restart", failures.lower())
        self.assertIn("Writer epoch gate", diagram)

    def test_published_evaluation_has_a_versioned_capture_slo(self) -> None:
        repository = SCRIPT.parents[1]
        evaluation = (repository / "docs" / "evaluation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("runtime contract version", evaluation.lower())
        self.assertIn("ten distinct sessions", evaluation.lower())
        self.assertIn("first active capture", evaluation.lower())
        self.assertIn("at least 95%", evaluation.lower())
        self.assertIn("at most two seconds", evaluation.lower())
        self.assertIn("complete latency samples", evaluation.lower())

    def test_published_contract_covers_grounded_notes_and_next_turn_feedback(self) -> None:
        repository = SCRIPT.parents[1]
        architecture = (repository / "ARCHITECTURE.md").read_text(encoding="utf-8")
        evaluation = (repository / "docs" / "evaluation.md").read_text(
            encoding="utf-8"
        )
        feedback = (repository / "docs" / "feedback-loop.md").read_text(
            encoding="utf-8"
        )
        failures = (repository / "docs" / "failure-lessons.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("declared authority", architecture.lower())
        self.assertIn("bounded excerpt", architecture.lower())
        self.assertIn("content-free note-use receipt", architecture.lower())
        self.assertIn("immediately previous turn", feedback.lower())
        self.assertIn("trusted direct-user", evaluation.lower())
        self.assertIn("tool-origin", evaluation.lower())
        self.assertIn("title-only recall", failures.lower())
        self.assertIn("rotate the writer epoch", failures.lower())

    def test_git_history_rejects_personal_author_email(self) -> None:
        _commit_minimal_repo(self.root, "person" + "@" + "example.com")

        issues = validator.scan_tree(self.root)

        self.assertTrue(any(issue.rule == "git-email" for issue in issues))

    def test_git_history_accepts_github_noreply_email(self) -> None:
        _commit_minimal_repo(
            self.root, "123+public" + "@" + "users.noreply.github.com"
        )

        self.assertEqual(validator.scan_tree(self.root), [])


if __name__ == "__main__":
    unittest.main()

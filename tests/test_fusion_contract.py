"""Public documentation regressions; these do not test the private runtime."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FusionContractTests(unittest.TestCase):
    def test_runtime_status_distinguishes_default_worker_and_optional_tools(self):
        text = (ROOT / "docs" / "runtime-status.md").read_text(encoding="utf-8")
        for phrase in (
            "configured worker is Claude",
            "Hermes is a tested alternative",
            "not a file-count watcher",
            "not independently reproducible from this repository",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_dashboard_bridge_does_not_claim_closed_loop_integration(self):
        text = (ROOT / "docs" / "brain-body-integration.md").read_text(encoding="utf-8")
        for phrase in (
            "hooks and memories disabled",
            "not yet a closed-loop integration",
            "project_revision",
            "idempotency_key",
            "does not grant direct-user authority",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_readme_does_not_claim_automatic_weight_training(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Evaluation changes the next retrieval decision", text)
        self.assertIn("not model-weight training", text)

    def test_relative_markdown_links_resolve(self):
        for file in ROOT.rglob("*.md"):
            if ".git" in file.parts:
                continue
            for raw in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", file.read_text(encoding="utf-8")):
                target = raw.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                with self.subTest(file=str(file.relative_to(ROOT)), target=target):
                    self.assertTrue((file.parent / target).is_file())


if __name__ == "__main__":
    unittest.main()

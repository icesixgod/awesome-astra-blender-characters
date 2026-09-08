"""Exercise committed-content checks with real Git history and GitHub event fixtures."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_whitespace.py"


class WhitespaceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.root / "no-hooks"))
        (self.repo / "old.md").write_text("Existing whitespace.   \n", encoding="utf-8")
        self.base = self.commit("base")
        (self.repo / "new.md").write_text("Clean change.\n", encoding="utf-8")
        self.clean = self.commit("clean")
        (self.repo / "new.md").write_text("New trailing whitespace.   \n", encoding="utf-8")
        self.bad = self.commit("bad")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True).strip()

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def check_event(self, name, event, head):
        path = self.root / "event.json"
        path.write_text(json.dumps(event), encoding="utf-8")
        env = dict(os.environ, GITHUB_EVENT_NAME=name, GITHUB_EVENT_PATH=str(path), GITHUB_SHA=head)
        return subprocess.run([sys.executable, str(SCRIPT)], cwd=self.repo, env=env,
                              capture_output=True, text=True)

    def test_push_checks_new_changes_without_rejecting_old_whitespace(self):
        clean = self.check_event("push", {"before": self.base}, self.clean)
        self.assertEqual(clean.returncode, 0, clean.stderr)
        bad = self.check_event("push", {"before": self.clean}, self.bad)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("new.md:1: trailing whitespace", bad.stdout)

    def test_first_push_checks_whole_tree(self):
        result = self.check_event("push", {"before": "0" * 40}, self.clean)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("old.md:1: trailing whitespace", result.stdout)

    def test_pull_request_checks_merge_base_to_head(self):
        result = self.check_event("pull_request", {"pull_request": {"base": {"sha": self.clean}}}, self.bad)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("new.md:1: trailing whitespace", result.stdout)
        self.assertNotIn("old.md:1: trailing whitespace", result.stdout)

    def test_manual_run_checks_whole_tree(self):
        result = self.check_event("workflow_dispatch", {}, self.clean)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("old.md:1: trailing whitespace", result.stdout)


if __name__ == "__main__":
    unittest.main()

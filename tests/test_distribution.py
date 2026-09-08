"""Exercise installation preservation and relocatable reference links in temporary folders."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import shutil
from unittest.mock import patch

from scripts import install as installer
from scripts.install import PACKAGE_FILES, SKILL_NAME, SOURCE
from scripts.validate import check_links


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def run_install(self, parent: Path, cwd: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/install.py"), "--destination", str(parent)],
            cwd=cwd, capture_output=True, text=True, check=False,
        )

    def test_install_from_another_directory_preserves_all_package_files(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory) / "skills with spaces"
            result = self.run_install(parent, Path(directory))
            self.assertEqual(result.returncode, 0, result.stderr)
            target = parent / SKILL_NAME
            expected = {Path(name): (SOURCE / name).read_bytes() for name in PACKAGE_FILES}
            actual = {p.relative_to(target): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(actual, expected)
            self.assertEqual((target / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
            for path in target.rglob("*.md"):
                self.assertEqual(check_links(path, target), [])

    def test_local_files_and_caches_are_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            shutil.copytree(SOURCE, source)
            extras = (".DS_Store", ".env", "scratch.blend", "notes.md", "__pycache__/cache.pyc")
            for name in extras:
                path = source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"private fixture")
            with patch.object(installer, "SOURCE", source):
                target = installer.install(root / "destination")
            actual = {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(actual, set(PACKAGE_FILES))
            for name in extras:
                self.assertFalse((target / name).exists())

    def test_source_symlinks_are_rejected_before_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            shutil.copytree(SOURCE, source)
            outside = root / "outside.txt"
            outside.write_text("private fixture", encoding="utf-8")
            try:
                (source / "linked.txt").symlink_to(outside)
            except OSError:
                self.skipTest("Symlink creation is unavailable")
            with patch.object(installer, "SOURCE", source):
                with self.assertRaises(ValueError):
                    installer.install(root / "destination")
            self.assertFalse((root / "destination").exists())

    def test_copy_failure_cleans_staging_and_allows_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            original_copy = shutil.copy2
            calls = 0

            def fail_second_copy(source, destination):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("simulated disk write failure")
                return original_copy(source, destination)

            with patch.object(installer.shutil, "copy2", side_effect=fail_second_copy):
                with self.assertRaises(OSError):
                    installer.install(parent)
            self.assertEqual(list(parent.iterdir()), [])
            target = installer.install(parent)
            self.assertTrue((target / "SKILL.md").is_file())

    def test_missing_reference_is_rejected_before_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            shutil.copytree(SOURCE, source)
            (source / "references/production-workflow.md").unlink()
            with patch.object(installer, "SOURCE", source):
                with self.assertRaises(FileNotFoundError):
                    installer.install(root / "destination")
            self.assertFalse((root / "destination").exists())

    def test_existing_install_is_not_modified(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            target = parent / SKILL_NAME
            target.mkdir()
            original = target / "SKILL.md"
            original.write_text("User's edited workflow", encoding="utf-8")
            result = self.run_install(parent, parent)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(original.read_text(encoding="utf-8"), "User's edited workflow")
            self.assertEqual(list(target.iterdir()), [original])

    def test_destination_inside_source_is_rejected_without_creating_it(self):
        parent = SOURCE / "installation-test-must-not-exist"
        self.assertFalse(parent.exists())
        result = self.run_install(parent, ROOT)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(parent.exists())

    def test_broken_destination_symlink_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            target = parent / SKILL_NAME
            missing = parent / "missing-user-directory"
            try:
                target.symlink_to(missing, target_is_directory=True)
            except OSError:
                self.skipTest("Symlink creation is unavailable")
            result = self.run_install(parent, parent)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(target.is_symlink())
            self.assertFalse(missing.exists())

    def test_reference_cannot_depend_on_a_file_outside_the_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            skill = parent / "skill"
            skill.mkdir()
            (parent / "private.md").write_text("Outside the package", encoding="utf-8")
            reference = skill / "SKILL.md"
            reference.write_text("[reference](../private.md)", encoding="utf-8")
            self.assertTrue(check_links(reference, skill))

    def test_missing_reference_heading_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory)
            reference = skill / "SKILL.md"
            reference.write_text("# Existing\n\n[reference](#missing)", encoding="utf-8")
            self.assertTrue(check_links(reference, skill))


if __name__ == "__main__":
    unittest.main()

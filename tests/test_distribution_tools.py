from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


publisher = load_module("publisher_under_test", ROOT / "scripts" / "publish_local_skills_to_repo.py")
scanner = load_module("scanner_under_test", ROOT / "scripts" / "scan_public_release.py")
syncer = load_module("syncer_under_test", ROOT / "scripts" / "sync_codex_skills.py")
updater = load_module(
    "updater_under_test",
    ROOT / "Skills" / "skills-update-folloze" / "scripts" / "update_folloze_skills.py",
)


def git(path: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


class PublisherPolicyTests(unittest.TestCase):
    def test_cli_requires_explicit_skill(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "publish_local_skills_to_repo.py")],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--skill", result.stderr)

    def test_refuses_symlink_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / "real" / "candidate"
            real.mkdir(parents=True)
            (real / "SKILL.md").write_text("---\nname: candidate\n---\n")
            source_root = root / "sources"
            source_root.mkdir()
            (source_root / "candidate").symlink_to(real, target_is_directory=True)
            with self.assertRaises(SystemExit):
                publisher.validate_source("candidate", source_root)

    def test_refuses_source_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source_root = Path(temp) / "sources"
            source_root.mkdir()
            with self.assertRaises(SystemExit):
                publisher.validate_source("../candidate", source_root)

    def test_requires_clean_non_main_branch(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            git(repo, "init", "-b", "main")
            git(repo, "config", "user.email", "tester@example.com")
            git(repo, "config", "user.name", "Test")
            (repo / "README.md").write_text("test\n")
            git(repo, "add", "README.md")
            git(repo, "commit", "-m", "initial")
            with self.assertRaises(SystemExit):
                publisher.require_pr_branch(repo)
            git(repo, "checkout", "-b", "codex/publication-test")
            self.assertEqual(publisher.require_pr_branch(repo), "codex/publication-test")
            (repo / "dirty.txt").write_text("dirty\n")
            with self.assertRaises(SystemExit):
                publisher.require_pr_branch(repo)

    def test_allowlist_is_fail_closed_by_default(self) -> None:
        policy = json.loads((ROOT / "publication-allowlist.json").read_text())
        self.assertEqual(policy["policy"], "fail-closed")
        self.assertEqual(publisher.approved_entries(policy), {})

    def test_publisher_has_no_push_operation(self) -> None:
        source = (ROOT / "scripts" / "publish_local_skills_to_repo.py").read_text()
        self.assertNotIn('"push"', source)
        self.assertNotIn("git push", source)


class PublicReleaseScannerTests(unittest.TestCase):
    def test_detects_secret_pii_and_machine_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "candidate.txt"
            path.write_text(
                "api_" + 'key="' + "abcdefghijklmnop" + '"\n'
                + "owner" + "@" + "company.invalid\n"
                + "/" + "Users/local-user/private/file\n"
            )
            kinds = {finding.kind for finding in scanner.scan_paths([path])}
            self.assertIn("generic secret assignment", kinds)
            self.assertIn("hardcoded email address or PII", kinds)
            self.assertIn("machine-specific home path", kinds)

    def test_ignores_documentation_domains(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "candidate.txt"
            path.write_text("operator@example.com\nchampion@acme.com\n")
            self.assertEqual(scanner.scan_paths([path]), [])


class SafeUpdaterTests(unittest.TestCase):
    def make_remote_and_clone(self, root: Path) -> tuple[Path, Path]:
        source = root / "source"
        source.mkdir()
        git(source, "init", "-b", "main")
        git(source, "config", "user.email", "tester@example.com")
        git(source, "config", "user.name", "Test")
        (source / "skills-manifest.json").write_text('{"skills": []}\n')
        git(source, "add", "skills-manifest.json")
        git(source, "commit", "-m", "initial")
        remote = root / "remote.git"
        subprocess.run(["git", "clone", "--bare", str(source), str(remote)], check=True, capture_output=True)
        clone = root / "development"
        subprocess.run(["git", "clone", str(remote), str(clone)], check=True, capture_output=True)
        return remote, clone

    def test_dirty_development_clone_uses_clean_clone_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote, development = self.make_remote_and_clone(root)
            dirty = development / "local-work.txt"
            dirty.write_text("preserve me\n")
            clean = root / "clean-sync"
            selected, cloned = updater.select_sync_repo(
                development,
                clean,
                str(remote),
                "main",
                False,
            )
            self.assertTrue(cloned)
            self.assertEqual(selected, clean)
            self.assertEqual(dirty.read_text(), "preserve me\n")
            self.assertTrue((clean / "skills-manifest.json").exists())

    def test_ahead_development_clone_uses_clean_clone_without_reset(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote, development = self.make_remote_and_clone(root)
            git(development, "config", "user.email", "tester@example.com")
            git(development, "config", "user.name", "Test")
            local_commit_file = development / "local-commit.txt"
            local_commit_file.write_text("preserve commit\n")
            git(development, "add", "local-commit.txt")
            git(development, "commit", "-m", "local only")
            original_head = git(development, "rev-parse", "HEAD")
            clean = root / "clean-sync"
            selected, cloned = updater.select_sync_repo(
                development,
                clean,
                str(remote),
                "main",
                False,
            )
            self.assertTrue(cloned)
            self.assertEqual(selected, clean)
            self.assertEqual(git(development, "rev-parse", "HEAD"), original_head)
            self.assertTrue(local_commit_file.exists())
            self.assertNotEqual(git(clean, "rev-parse", "HEAD"), original_head)

    def test_updater_source_is_pull_install_only(self) -> None:
        source = (ROOT / "Skills" / "skills-update-folloze" / "scripts" / "update_folloze_skills.py").read_text()
        self.assertNotIn("publish_local_skills", source)
        self.assertNotIn('"push"', source)
        automation = json.loads(
            (ROOT / "AutomationTemplates" / "folloze-skills-weekly-update" / "template.json").read_text()
        )["prompt"].lower()
        self.assertIn("do not discover", automation)
        self.assertIn("do not", automation)
        self.assertNotIn("push to origin", automation)


class InstallOwnershipTests(unittest.TestCase):
    def test_refuses_unmanaged_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            source = repo / "Skills" / "sample"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("---\nname: sample\n---\n")
            dest_root = root / "client" / "skills"
            dest = dest_root / "sample"
            dest.mkdir(parents=True)
            (dest / "user-file.txt").write_text("owned by user\n")
            with self.assertRaises(SystemExit):
                syncer.install_skill(source, dest, dest_root, repo, "copy", True, False)
            self.assertTrue((dest / "user-file.txt").exists())

    def test_copy_install_adds_management_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            source = repo / "Skills" / "sample"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("---\nname: sample\n---\n")
            dest_root = root / "client" / "skills"
            dest_root.mkdir(parents=True)
            dest = dest_root / "sample"
            syncer.install_skill(source, dest, dest_root, repo, "copy", True, False)
            self.assertTrue((dest / syncer.MANAGED_MARKER).exists())
            self.assertTrue(syncer.is_managed_destination(dest, repo))

    def test_dual_client_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "sync_codex_skills.py"),
                    "--repo-root",
                    str(ROOT),
                    "--client",
                    "both",
                    "--codex-dest",
                    str(root / "codex"),
                    "--claude-dest",
                    str(root / "claude"),
                    "--skill",
                    "folloze-brand-kit",
                    "--mode",
                    "copy",
                    "--dry-run",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertIn("client: codex", result.stdout)
            self.assertIn("client: claude", result.stdout)
            self.assertFalse((root / "codex").exists())
            self.assertFalse((root / "claude").exists())


if __name__ == "__main__":
    unittest.main()

"""Self-contained test suite for the investigating-repository-history skill.

Run from the skill root:

    python3 -m unittest tests.test_skill -v

or:

    python3 tests/test_skill.py
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
REFERENCES = ROOT / "references"


def run(cmd, cwd=None, timeout=60):
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


class TestSkillStructure(unittest.TestCase):
    def test_skill_md_exists(self):
        self.assertTrue((ROOT / "SKILL.md").exists())

    def test_required_scripts_exist(self):
        for name in ("history_context.py", "compact_pr.py", "validate_skill.py"):
            self.assertTrue((SCRIPTS / name).exists(), f"missing scripts/{name}")

    def test_required_references_exist(self):
        for name in ("ANOMALIES.md", "GH_CLI.md", "DECISION_ATOMS.md", "OUTPUT_SCHEMA.md", "EVALUATION.md"):
            self.assertTrue((REFERENCES / name).exists(), f"missing references/{name}")

    def test_assets_template_exists(self):
        self.assertTrue((ROOT / "assets" / "history-note-template.md").exists())

    def test_no_old_github_api_filename(self):
        self.assertFalse((REFERENCES / "GITHUB_API.md").exists(),
                         "Stale references/GITHUB_API.md should have been renamed to GH_CLI.md")


class TestFrontmatter(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_starts_with_frontmatter(self):
        self.assertTrue(self.text.startswith("---\n"))

    def _frontmatter(self):
        end = self.text.find("\n---", 4)
        return self.text[4:end]

    def test_required_fields(self):
        fm = self._frontmatter()
        self.assertRegex(fm, r"(?m)^name:\s*investigating-repository-history")
        self.assertRegex(fm, r"(?m)^description:\s*\S")

    def test_name_format(self):
        fm = self._frontmatter()
        m = re.search(r"(?m)^name:\s*(.+)$", fm)
        self.assertIsNotNone(m)
        name = m.group(1).strip().strip('"')
        self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)

    def test_description_length(self):
        fm = self._frontmatter()
        m = re.search(r"(?m)^description:\s*(.+)$", fm)
        self.assertIsNotNone(m)
        desc = m.group(1).strip().strip('"')
        self.assertGreater(len(desc), 60, "description too short")
        self.assertLessEqual(len(desc), 1024, "description exceeds 1024 chars")


class TestNoDirectGitHubAPI(unittest.TestCase):
    """The skill must access GitHub only through `gh`, not direct HTTP."""

    FORBIDDEN_PATTERNS = [
        r"api\.github\.com",
        r"\bimport\s+requests\b",
        r"from\s+requests\s",
        r"\bimport\s+httpx\b",
        r"\bimport\s+urllib\.request\b",
        r"from\s+urllib\.request\b",
        r"curl\s+[^\n]*api\.github\.com",
    ]

    def test_scripts_use_gh_cli_only(self):
        violations = []
        for py in SCRIPTS.glob("*.py"):
            content = py.read_text(encoding="utf-8")
            for pat in self.FORBIDDEN_PATTERNS:
                if re.search(pat, content):
                    violations.append(f"{py.name}: forbidden pattern '{pat}'")
        self.assertEqual(violations, [], "Direct GitHub API access detected:\n" + "\n".join(violations))

    def test_scripts_actually_invoke_gh(self):
        history = (SCRIPTS / "history_context.py").read_text(encoding="utf-8")
        compact = (SCRIPTS / "compact_pr.py").read_text(encoding="utf-8")
        self.assertIn('"gh", "api"', history, "history_context.py should call `gh api`")
        self.assertIn('"gh", "api"', compact, "compact_pr.py should call `gh api`")


class TestValidator(unittest.TestCase):
    def test_validate_skill_passes(self):
        proc = run([sys.executable, str(SCRIPTS / "validate_skill.py"), str(ROOT)])
        self.assertEqual(proc.returncode, 0, f"validate_skill.py failed:\nstdout:{proc.stdout}\nstderr:{proc.stderr}")
        self.assertIn("OK:", proc.stdout)


class TestScriptHelp(unittest.TestCase):
    def test_history_context_version(self):
        proc = run([sys.executable, str(SCRIPTS / "history_context.py"), "--version"])
        self.assertEqual(proc.returncode, 0)
        self.assertRegex(proc.stdout, r"history_context\.py \d+\.\d+\.\d+")

    def test_history_context_help(self):
        proc = run([sys.executable, str(SCRIPTS / "history_context.py"), "--help"])
        self.assertEqual(proc.returncode, 0)
        for sub in ("inspect", "commit-prs", "lineage"):
            self.assertIn(sub, proc.stdout)

    def test_compact_pr_help(self):
        proc = run([sys.executable, str(SCRIPTS / "compact_pr.py"), "--help"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--pr", proc.stdout)


@unittest.skipUnless(shutil.which("git"), "git not available")
class TestSmokeLocalOnly(unittest.TestCase):
    """Run history_context.py against a tiny on-disk git repo with --no-gh.

    No network calls; verifies that the local git pipeline produces a valid
    JSON report with the expected schema fields.
    """

    @classmethod
    def setUpClass(cls):
        import tempfile
        cls.tmpdir = Path(tempfile.mkdtemp(prefix="rhi-smoke-"))
        env = os.environ.copy()
        env["GIT_AUTHOR_NAME"] = "Test User"
        env["GIT_AUTHOR_EMAIL"] = "test@example.com"
        env["GIT_COMMITTER_NAME"] = "Test User"
        env["GIT_COMMITTER_EMAIL"] = "test@example.com"
        cls.env = env

        def git(*args):
            return subprocess.run(["git", *args], cwd=str(cls.tmpdir), env=env,
                                  text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        git("init", "-q", "-b", "main")
        git("config", "commit.gpgsign", "false")
        target = cls.tmpdir / "src" / "foo.py"
        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text("def hello():\n    return 1\n", encoding="utf-8")
        git("add", "src/foo.py")
        git("commit", "-q", "-m", "initial: add hello")

        # second commit with a guard to investigate
        target.write_text(
            "def hello():\n"
            "    # legacy compatibility check\n"
            "    if not isinstance(_ := 1, int):\n"
            "        raise TypeError(\"must be int\")\n"
            "    return 1\n",
            encoding="utf-8",
        )
        git("add", "src/foo.py")
        git("commit", "-q", "-m", "compat: enforce int return for legacy callers")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def test_inspect_no_gh_produces_valid_json(self):
        proc = run(
            [
                sys.executable, str(SCRIPTS / "history_context.py"), "inspect",
                "--repo-dir", str(self.tmpdir),
                "--path", "src/foo.py",
                "--start", "2", "--end", "4",
                "--question", "Can I remove this compatibility check?",
                "--no-gh",
                "--format", "json",
            ],
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0, f"non-zero exit:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        for key in ("schema_version", "scope", "evidence_completeness", "seed_commits", "risk", "unknowns"):
            self.assertIn(key, data, f"missing key '{key}' in report")
        self.assertEqual(data["evidence_completeness"]["github_prs"], "not_run")
        self.assertGreaterEqual(len(data["seed_commits"]), 1, "expected at least one seed commit from blame")
        # the second commit message contains 'compat' / 'legacy'
        summaries = " ".join(c.get("summary", "") for c in data["seed_commits"])
        self.assertIn("compat", summaries.lower())

    def test_inspect_no_gh_markdown_output(self):
        proc = run(
            [
                sys.executable, str(SCRIPTS / "history_context.py"), "inspect",
                "--repo-dir", str(self.tmpdir),
                "--path", "src/foo.py",
                "--start", "2", "--end", "4",
                "--no-gh",
                "--format", "markdown",
            ],
            timeout=120,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("History context report", proc.stdout)
        self.assertIn("Seed commits", proc.stdout)

    def test_commit_prs_subcommand_runs(self):
        """Regression: cmd_commit_prs used to crash on `args.no_gh` for non-inspect parsers."""
        proc = run(
            [
                sys.executable, str(SCRIPTS / "history_context.py"), "commit-prs",
                "--repo-dir", str(self.tmpdir),
                "--commit", "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
                "--github-repo", "test/repo",
                "--no-gh",
                "--format", "json",
            ],
            timeout=30,
        )
        # The temp repo has no GitHub remote, but with --github-repo + --no-gh
        # it should not raise AttributeError on `args.no_gh`.
        self.assertNotIn("'Namespace' object has no attribute 'no_gh'", proc.stderr)
        # Either we get a JSON envelope (gh fails per-commit, returns empty list)
        # or a clean RuntimeError, but never an AttributeError.
        self.assertNotIn("AttributeError", proc.stderr)

    def test_lineage_subcommand(self):
        proc = run(
            [
                sys.executable, str(SCRIPTS / "history_context.py"), "lineage",
                "--repo-dir", str(self.tmpdir),
                "--path", "src/foo.py",
                "--format", "json",
            ],
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, f"non-zero exit:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertIn("file_lineage", data)


if __name__ == "__main__":
    unittest.main(verbosity=2)

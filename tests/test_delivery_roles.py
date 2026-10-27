"""Packaging checks only; fresh-agent behavior results are recorded separately."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ROLES = ("lead", "conductor")


def markdown_links(path: Path) -> list[Path]:
    prose = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    return [
        path.parent / target.split("#")[0]
        for target in re.findall(r"\]\(([^)]+)\)", prose)
        if "://" not in target and not target.startswith("#")
    ]


class DeliveryRolePackagingTests(unittest.TestCase):
    def test_role_metadata_allows_natural_language_discovery(self) -> None:
        for role in ROLES:
            with self.subTest(role=role):
                path = SKILLS / role / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                frontmatter = text.split("---\n", 2)[1]
                self.assertIn(f"name: {role}\n", frontmatter)
                description = re.search(r"(?m)^description: (.+)$", frontmatter)
                self.assertIsNotNone(description)
                self.assertTrue(description[1].startswith("Use when"))
                self.assertLessEqual(len(description[1]), 1024)
                self.assertNotIn("disable-model-invocation: true", frontmatter)

    def test_both_roles_link_one_shared_contract(self) -> None:
        contract = (SKILLS / "lead/workflow.md").resolve()
        for role in ROLES:
            with self.subTest(role=role):
                links = [
                    p.resolve() for p in markdown_links(SKILLS / role / "SKILL.md")
                ]
                self.assertIn(contract, links)
        self.assertTrue(contract.is_file())
        self.assertFalse((SKILLS / "conductor/workflow.md").exists())
        self.assertFalse(contract.read_text(encoding="utf-8").startswith("---"))

    def test_all_role_bundle_links_resolve(self) -> None:
        for role in ROLES:
            for path in (SKILLS / role).rglob("*.md"):
                for target in markdown_links(path):
                    with self.subTest(source=path, target=target):
                        self.assertTrue(target.is_file())

    def test_roles_and_shared_contract_stay_small(self) -> None:
        for role in ROLES:
            text = (SKILLS / role / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(role=role):
                self.assertLess(len(text.split()), 500)
        contract = (SKILLS / "lead/workflow.md").read_text(encoding="utf-8")
        self.assertLess(len(contract.split()), 1100)

    def test_bundle_uses_existing_package_skill_root(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertIn("./skills", package["pi"]["skills"])
        for role in ROLES:
            self.assertTrue((SKILLS / role / "SKILL.md").is_file())

    def test_recursive_example_distinguishes_execution_cwd_from_creator(self) -> None:
        contract = (SKILLS / "lead/workflow.md").read_text(encoding="utf-8")
        # Removing this direction example reintroduces the observed confusion:
        # a Conductor refused to integrate a child into its assigned batch cwd.
        self.assertIn("Conductor integrates `tmp-b3-parser` into `tmp-b3`", contract)
        self.assertIn("Lead integrates `tmp-b3` into the Lead's line", contract)

    def test_manual_execution_workspace_names_its_integration_destination(self) -> None:
        contract = (SKILLS / "lead/workflow.md").read_text(encoding="utf-8")
        self.assertIn("Manual execution workspace", contract)
        self.assertIn("integration destination", contract)

    def test_shared_backlog_only_record_has_a_conductor_write_target(self) -> None:
        contract = (SKILLS / "lead/workflow.md").read_text(encoding="utf-8")
        self.assertIn("shared-backlog entry", contract)
        self.assertIn("linked batch record before dispatch", contract)

    def test_role_bundle_has_no_launch_scripts_or_machine_paths(self) -> None:
        for role in ROLES:
            for path in (SKILLS / role).rglob("*"):
                if path.is_file():
                    self.assertEqual(path.suffix, ".md", path)
                    text = path.read_text(encoding="utf-8")
                    self.assertNotRegex(text, r"[A-Z]:[/\\]|/home/|/Users/")
                    self.assertNotRegex(text, r"github-copilot/|claude-haiku-|gpt-6\.")

    def test_existing_mechanics_are_referenced_not_reimplemented(self) -> None:
        text = (SKILLS / "lead/workflow.md").read_text(encoding="utf-8")
        for dependency in (
            "delegating-independent-work",
            "using-zellij-with-intercom",
            "version-control-workflow",
            "project-structure",
        ):
            self.assertIn(dependency, text)
            self.assertTrue((SKILLS / dependency / "SKILL.md").is_file())
        self.assertIn("pi-subagents", text)
        self.assertIn("pi-intercom", text)

    def test_catalog_documents_both_explicit_entry_commands(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        usage = (ROOT / "docs/lead-conductor.md").read_text(encoding="utf-8")
        for role in ROLES:
            self.assertIn(f"`{role}`", readme)
            self.assertIn(f"/skill:{role}", usage)
        self.assertIn("together", usage)
        for target in markdown_links(ROOT / "docs/lead-conductor.md"):
            self.assertTrue(target.is_file(), target)

    def test_behavior_cases_have_explicit_rubrics(self) -> None:
        cases = json.loads(
            (ROOT / "tests/fixtures/delivery-role-scenarios.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(len(cases), 6)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in cases:
            self.assertIn(case["role"], (*ROLES, "both"))
            self.assertTrue(case["prompt"])
            self.assertGreaterEqual(len(case["expect"]), 2)


if __name__ == "__main__":
    unittest.main()

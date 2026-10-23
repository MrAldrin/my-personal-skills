"""Static packaging and local adaptation contracts for the imported skill set."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAMES = ("grill-me", "grill-with-docs", "grilling", "domain-modeling")


class GrillingSkillsTests(unittest.TestCase):
    def skill(self, name: str) -> str:
        return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")

    def test_frontmatter_and_catalog(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in NAMES:
            with self.subTest(name=name):
                content = self.skill(name)
                self.assertTrue(content.startswith("---\n"))
                self.assertIn(f"name: {name}\n", content)
                self.assertRegex(content, r"(?m)^description: .+")
                self.assertIn(f"`{name}`", readme)
                self.assertTrue((SKILLS / name / "agents/openai.yaml").is_file())

    def test_entry_point_dependencies_are_portable(self) -> None:
        for name, dependencies in {
            "grill-me": ("grilling",),
            "grill-with-docs": ("grilling", "domain-modeling"),
        }.items():
            content = self.skill(name)
            self.assertIn("disable-model-invocation: true", content)
            self.assertIn("read", content.lower())
            self.assertIn("in full with the file-reading tool", content)
            for dependency in dependencies:
                self.assertIn(f"../{dependency}/SKILL.md", content)
            self.assertNotIn("Call the Skill tool", content)

    def test_all_relative_markdown_links_resolve(self) -> None:
        for name in NAMES:
            for path in (SKILLS / name).glob("*.md"):
                # Format references contain fictional project links in fenced examples.
                prose = re.sub(r"```[^\n]*\n.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
                for target in re.findall(r"\]\(([^)]+)\)", prose):
                    if "://" not in target and not target.startswith("#"):
                        self.assertTrue((path.parent / target.split("#")[0]).is_file(), (path, target))

    def test_grilling_local_behavior(self) -> None:
        content = self.skill("grilling")
        for phrase in (
            "one question at a time", "recommended answer", "prerequisites",
            "delegation is authorized", "look up", "user confirms",
        ):
            self.assertIn(phrase, content)
        self.assertNotIn("Ask the whole frontier", content)
        self.assertIn("capturing an agreed glossary term inline", content)
        self.assertIn("Do not create or edit project files", self.skill("grill-me"))

    def test_domain_persistence_boundaries(self) -> None:
        content = self.skill("domain-modeling")
        for phrase in ("GLOSSARY-MAP.md", "Create files lazily", "all three", "Hard to reverse",
                       "Surprising without context", "real trade-off", "existing documentation conventions"):
            self.assertIn(phrase, content)
        self.assertTrue((SKILLS / "domain-modeling/GLOSSARY-FORMAT.md").is_file())
        self.assertTrue((SKILLS / "domain-modeling/ADR-FORMAT.md").is_file())

    def test_license_and_pinned_provenance(self) -> None:
        license_text = (ROOT / "licenses/mattpocock-skills-MIT.txt").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Matt Pocock", license_text)
        self.assertIn("Permission is hereby granted", license_text)
        provenance = (ROOT / "docs/grilling-skills.md").read_text(encoding="utf-8")
        self.assertIn("5beb35b040e3de97e54fa9e386d7e42d15c295c2", provenance)
        for name in NAMES:
            self.assertIn(name, provenance)


if __name__ == "__main__":
    unittest.main()

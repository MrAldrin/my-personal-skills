"""Static regression contracts; these do not replace a live shell exit test."""

import re
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / "skills"
LAUNCH = SKILLS / "launching-visible-agents"
ZELLIJ = SKILLS / "using-zellij"


def frontmatter_name(skill: Path) -> str:
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"(?m)^name: (\S+)$", text)
    assert match, skill
    return match.group(1)


class ZellijLaunchGuidanceTests(unittest.TestCase):
    def test_skill_names_match_directories(self) -> None:
        self.assertEqual(frontmatter_name(LAUNCH), "launching-visible-agents")
        self.assertEqual(frontmatter_name(ZELLIJ), "using-zellij")

    def test_new_tab_examples_start_normal_shell(self) -> None:
        content = (ZELLIJ / "commands.md").read_text(encoding="utf-8")
        commands = re.findall(
            r"(?m)^`?(zellij action new-tab [^\n`]+)", content, re.MULTILINE
        )
        self.assertGreaterEqual(len(commands), 2)
        for command in commands:
            self.assertNotIn(" -- ", command)
            self.assertNotIn("--close-on-exit", command)
            self.assertNotIn("--layout", command)

    def test_floating_job_pane_is_hidden_owned_and_not_stacked(self) -> None:
        content = (ZELLIJ / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "zellij action new-pane --tab-id <tab> --floating --no-focus --name <job> --cwd <dir> -- <command>",
            content,
        )
        self.assertIn("zellij action close-pane --pane-id <id>", content)
        self.assertIn("Do not use `--stacked`", content)
        self.assertIn("never as a hidden background process", content)
        commands = (ZELLIJ / "commands.md").read_text(encoding="utf-8")
        self.assertIn("--floating --no-focus", commands)
        self.assertIn("close-pane --pane-id", commands)

    def test_own_tab_and_tab_naming_rules_live_in_using_zellij(self) -> None:
        content = (ZELLIJ / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("ZELLIJ_PANE_ID", content)
        self.assertIn("list-panes --all --json", content)
        self.assertIn("tab_id", content)
        self.assertIn("`<project>-<task>`", content)
        self.assertIn("25 characters", content)
        self.assertIn("initials", content)

    def test_exact_pane_submission_and_shell_quoting(self) -> None:
        content = (LAUNCH / "commands.md").read_text(encoding="utf-8")
        self.assertIn("write-chars --pane-id terminal_123", content)
        self.assertIn("write --pane-id terminal_123 13", content)
        self.assertIn("Nushell", content)
        self.assertIn("PowerShell", content)
        self.assertIn("foreground", content)
        self.assertIn("windows-fullscreen-mouse/launch.mjs", content)
        self.assertIn("Linux/WSL", content)

    def test_skill_requires_shell_and_exit_verification(self) -> None:
        content = (LAUNCH / "SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "normal interactive",
            "shell prompt",
            "foreground",
            "stable",
            "disposable",
            "ping",
            "openProjectPaneIfMissing",
            "Closing the pane on Pi exit is not an equivalent substitute",
            "held-command",
            "Preserve",
        ):
            self.assertIn(phrase, content)
        self.assertIn("Do not replace", content)
        self.assertIn("--close-on-exit", content)

    def test_launch_skill_delegates_zellij_mechanics(self) -> None:
        content = (LAUNCH / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("../using-zellij/SKILL.md", content)
        self.assertNotIn("list-panes --all --json", content)


if __name__ == "__main__":
    unittest.main()

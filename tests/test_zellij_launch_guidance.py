"""Static regression contracts; these do not replace a live shell exit test."""

import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills/using-zellij-with-intercom"


class ZellijLaunchGuidanceTests(unittest.TestCase):
    def test_new_tab_examples_start_normal_shell(self) -> None:
        content = (SKILL / "commands.md").read_text(encoding="utf-8")
        commands = re.findall(r"(?m)^`?(zellij action new-tab [^\n`]+)", content, re.M)
        self.assertGreaterEqual(len(commands), 2)
        for command in commands:
            self.assertNotIn(" -- ", command)
            self.assertNotIn("--close-on-exit", command)
            self.assertNotIn("--layout", command)

    def test_exact_pane_submission_and_shell_quoting(self) -> None:
        content = (SKILL / "commands.md").read_text(encoding="utf-8")
        self.assertIn("write-chars --pane-id terminal_123", content)
        self.assertIn("write --pane-id terminal_123 13", content)
        self.assertIn("Nushell", content)
        self.assertIn("PowerShell", content)
        self.assertIn("foreground", content)
        self.assertIn("windows-fullscreen-mouse/launch.mjs", content)
        self.assertIn("Linux/WSL", content)

    def test_skill_requires_shell_and_exit_verification(self) -> None:
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for phrase in ("normal interactive", "shell prompt", "foreground", "stable", "disposable"):
            self.assertIn(phrase, content)
        self.assertIn("Do not replace", content)
        self.assertIn("--close-on-exit", content)


if __name__ == "__main__":
    unittest.main()

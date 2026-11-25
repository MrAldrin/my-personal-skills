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

    def test_shell_tab_examples_do_not_run_an_initial_command(self) -> None:
        content = (ZELLIJ / "commands.md").read_text(encoding="utf-8")
        commands = re.findall(r"(?m)^zellij action new-tab .+$", content)
        self.assertTrue(commands)
        for command in commands:
            self.assertIn("--no-focus", command)
            self.assertIn("--cwd", command)
            for option in (" -- ", "--close-on-exit", "--layout"):
                self.assertNotIn(option, command)
        self.assertNotIn("zellij action write", content)

    def test_floating_job_pane_uses_own_tab_without_focus(self) -> None:
        skill = (ZELLIJ / "SKILL.md").read_text(encoding="utf-8")
        commands = (ZELLIJ / "commands.md").read_text(encoding="utf-8")
        for content in (skill, commands):
            self.assertRegex(
                content, r"zellij action new-pane --tab-id \S+ --floating --no-focus"
            )
            self.assertIn("close-pane --pane-id", content)
        for rule in (
            "Do not use `--stacked`",
            "never as a hidden background process",
            "Never open a job pane in the user's focused tab",
        ):
            self.assertIn(rule, skill)

    def test_own_tab_and_tab_naming_rules_live_in_using_zellij(self) -> None:
        content = (ZELLIJ / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("ZELLIJ_PANE_ID", content)
        self.assertIn("list-panes --all --json", content)
        self.assertIn("tab_id", content)
        self.assertIn("`<project>-<task>`", content)
        self.assertIn("25 characters", content)
        self.assertIn("initials", content)

    def test_default_launch_uses_baton_for_both_harnesses(self) -> None:
        content = (LAUNCH / "commands.md").read_text(encoding="utf-8")
        default, _, _ = content.partition("## Native Windows Nushell exception")
        for agent in ("pi", "claude"):
            with self.subTest(agent=agent):
                self.assertRegex(
                    default, rf"(?m)^baton .* run .*--new-tab .*--agent {agent} --"
                )
        self.assertIn('baton send "$pane" "$prompt" && baton wait "$pane"', default)
        self.assertIn('baton read "$pane"', default)
        self.assertNotIn("zellij action", default)

    def test_raw_agent_input_is_only_for_the_nushell_exception(self) -> None:
        content = (LAUNCH / "commands.md").read_text(encoding="utf-8")
        _, marker, tail = content.partition("## Native Windows Nushell exception")
        self.assertTrue(marker)
        exception, _, rest = tail.partition("## Verify shell lifecycle")
        self.assertIn("does not have a Nushell quoting adapter", exception)
        self.assertIn("windows-fullscreen-mouse/launch.mjs", exception)
        for action in ("write-chars", "write"):
            command = f"zellij action {action} --pane-id terminal_123 "
            self.assertIn(command, exception)
            self.assertEqual(content.count(f"zellij action {action} "), 1)
        self.assertIn('baton close "$pane"', rest)
        self.assertIn("close-tab --tab-id <recorded-tab-id>", rest)

    def test_launch_requires_interactive_shell_and_peer_readiness(self) -> None:
        content = (LAUNCH / "SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "using-baton",
            "normal interactive shell first",
            "foreground child",
            "return to the shell prompt",
            "disposable tab",
            "two-way ping",
            "openProjectPaneIfMissing",
            "--close-on-exit",
            "matching claim in Beads",
        ):
            self.assertIn(phrase, content)
        self.assertNotIn("zellij action", content)

    def test_delivery_contract_distinguishes_wait_from_handoff(self) -> None:
        contract = (SKILLS / "lead" / "workflow.md").read_text(encoding="utf-8")
        for command in (
            "baton run --new-tab",
            "baton read",
            "baton send",
            "baton wait",
            "baton close",
        ):
            self.assertIn(command, contract)
        self.assertIn("verify the handoff on the bead", contract)
        self.assertIn("watch-goal.sh", contract)
        self.assertNotIn("zellij action", contract)


if __name__ == "__main__":
    unittest.main()

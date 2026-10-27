"""Opt-in live tests overwrite and restore clipboard text (not other formats).

Run on Windows: CLIPBOARD_LIVE_TESTS=1 uv run --no-project python -m unittest discover -s tests -p test_clipboard.py -v
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/copying-to-clipboard"


@unittest.skipUnless(os.environ.get("CLIPBOARD_LIVE_TESTS") == "1", "requires desktop clipboard")
class ClipboardTests(unittest.TestCase):
    def run_ps(self, command: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", "$ErrorActionPreference='Stop'; " + command],
            capture_output=True, check=True,
        )

    def test_windows_and_wsl_round_trip(self) -> None:
        self.assertTrue((SKILL / "copy.ps1").is_file(), "clipboard helper is missing")
        self.assertTrue((SKILL / "copy.sh").is_file(), "shell wrapper is missing")
        with tempfile.TemporaryDirectory(prefix="clipboard test '") as directory:
            directory = Path(directory)
            saved = directory / "previous.txt"
            source = directory / "message.txt"
            actual = directory / "actual.txt"
            quote = lambda path: "'" + str(path).replace("'", "''") + "'"
            self.run_ps(f"[IO.File]::WriteAllText({quote(saved)}, [string](Get-Clipboard -Raw), [Text.UTF8Encoding]::new($false))")
            try:
                for text in ("Hei æøå ÆØÅ «tilbud» 😀\nAndre linje", "no trailing newline", "CRLF\r\nnext\r\n"):
                    source.write_bytes(text.encode("utf-8"))
                    for environment in ("powershell", "git-bash", "wsl", "wsl-local"):
                        with self.subTest(environment=environment, text=text):
                            if environment == "powershell":
                                result = self.run_ps(f"& {quote(SKILL / 'copy.ps1')} -InputFile {quote(source)}")
                            elif environment == "git-bash":
                                result = subprocess.run(["bash", str(SKILL / "copy.sh"), str(source)], capture_output=True)
                            else:
                                def wsl_path(path: Path) -> str:
                                    return subprocess.check_output(["wsl.exe", "--exec", "wslpath", "-u", str(path)], text=True).strip()
                                if environment == "wsl":
                                    command = ["bash", wsl_path(SKILL / "copy.sh"), wsl_path(source)]
                                else:
                                    command = ["bash", "-c", 'f=$(mktemp); trap \'rm -f -- "$f"\' EXIT; cp -- "$2" "$f"; bash "$1" "$f"', "_", wsl_path(SKILL / "copy.sh"), wsl_path(source)]
                                result = subprocess.run(["wsl.exe", "--exec", *command], capture_output=True)
                            self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
                            self.run_ps(f"[IO.File]::WriteAllText({quote(actual)}, [string](Get-Clipboard -Raw), [Text.UTF8Encoding]::new($false))")
                            self.assertEqual(actual.read_bytes().decode("utf-8"), text)
            finally:
                self.run_ps(f"Set-Clipboard -Value ([IO.File]::ReadAllText({quote(saved)}, [Text.Encoding]::UTF8))")


if __name__ == "__main__":
    unittest.main()

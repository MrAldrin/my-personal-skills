---
name: copying-to-clipboard
description: >
  Use when the user explicitly asks to copy text to the clipboard, put a draft on the
  clipboard, or make an email, Teams message, or colleague request available via Ctrl+V.
---

# Copying to clipboard

- Use only on explicit request; drafting paste-ready text alone is not permission to overwrite the clipboard.
- Supports native Windows and WSL with Windows interop; Mint/Fedora are not yet supported.
- Write the requested text to a temporary UTF-8 file; keep its contents out of shell arguments.
- From Git Bash or WSL, run `bash <skill-dir>/copy.sh <text-file>`, quoting both paths.
- From PowerShell, run `powershell.exe -NoProfile -File <skill-dir>/copy.ps1 -InputFile <text-file>`, quoting both paths.
- The helper reads UTF-8, sets the Windows clipboard, verifies exact text through a UTF-8 file, and removes its verification file.
- Never trust PowerShell console rendering of æ, ø, å or «»: it can look corrupted while the clipboard is correct. Never omit UTF-8.
- Delete your temporary input file in a finally/trap cleanup, including on failure; never delete a user-owned source file.
- After exit code 0, say “Text is on the clipboard. Paste with Ctrl+V.” Do not reprint the whole text.
- On failure or an unsupported environment, report the limitation and offer a UTF-8 file instead; do not install tools or claim success.

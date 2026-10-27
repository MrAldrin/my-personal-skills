#!/usr/bin/env bash
set -euo pipefail
if [[ $# != 1 ]]; then
    echo "Usage: bash copy.sh <UTF-8 text file>" >&2
    exit 2
fi
helper="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/copy.ps1"
if command -v cygpath >/dev/null 2>&1; then
    helper="$(cygpath -w "$helper")"
    input="$(cygpath -w "$1")"
elif command -v wslpath >/dev/null 2>&1; then
    helper="$(wslpath -w "$helper")"
    input="$(wslpath -w "$(realpath -- "$1")")"
else
    echo "Supported only on native Windows (Git Bash) or WSL with Windows interop." >&2
    exit 2
fi
MSYS_NO_PATHCONV=1 powershell.exe -NoProfile -File "$helper" -InputFile "$input"

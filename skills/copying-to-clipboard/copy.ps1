param(
    [Parameter(Mandatory = $true)]
    [string]$InputFile
)
$ErrorActionPreference = 'Stop'
$text = Get-Content -LiteralPath $InputFile -Raw -Encoding UTF8
if ($null -eq $text -or $text.Length -eq 0) {
    throw 'Input must contain non-empty UTF-8 text.'
}
$verification = [IO.Path]::GetTempFileName()
try {
    Set-Clipboard -Value $text
    # The desktop clipboard can take a moment to become readable.
    for ($attempt = 0; $attempt -lt 10; $attempt++) {
        Start-Sleep -Milliseconds 100
        [IO.File]::WriteAllText($verification, [string](Get-Clipboard -Raw), [Text.UTF8Encoding]::new($false))
        if ([IO.File]::ReadAllText($verification, [Text.Encoding]::UTF8) -ceq $text) {
            Write-Output 'Text is on the clipboard. Paste with Ctrl+V.'
            exit 0
        }
    }
    throw 'Clipboard verification failed; do not claim the text was copied.'
}
finally {
    Remove-Item -LiteralPath $verification -Force
}

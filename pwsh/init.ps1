$toolsDir = Join-Path $PSScriptRoot 'tools'

if (-not $script:ToolsLoaded) {
    $script:ToolsLoaded = $true

    Get-ChildItem $toolsDir -Filter '*.ps1' |
        ForEach-Object { . $_.FullName }
}
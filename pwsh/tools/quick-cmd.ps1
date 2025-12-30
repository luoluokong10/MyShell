function uv-init {
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$ProjectName,

        [Parameter(Position = 1)]
        [string]$PythonVersion = "3.14",

        [Parameter(Position = 2)]
        [bool]$UseMirror = $true
    )

    uv init $ProjectName
    Set-Location $ProjectName

    uv python pin $PythonVersion

    if ($UseMirror) {
        @'

[[uv.index.tool]]
url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
'@ | Add-Content -Path "pyproject.toml"
    }

    uv sync
}
uv-init() {
    local project_name="$1"
    local python_version="${2:-3.14}"
    local use_mirror="${3:-true}"

    if [[ -z "$project_name" ]]; then
        echo "Usage: uv-init <project-name> [python-version] [use-mirror]" >&2
        return 1
    fi

    uv init "$project_name"
    cd "$project_name"

    uv python pin "$python_version"
    if [[ "$use_mirror" == "true" ]]; then
        cat >> pyproject.toml << 'EOF'

[[uv.index.tool]]
url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
EOF
    fi

    uv sync
}
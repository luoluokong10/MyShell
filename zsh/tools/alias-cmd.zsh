typeset -A ALIAS_MAP # local is equal to typeset
ALIAS_MAP=(
    mkdocs "uv run mkdocs serve --livereload"
    fs fastfetch
)

is_arch() {
    id=$(grep -oP '^ID=\K\S+' /etc/os-release | head -1)
    [[ $id == "arch" ]]
}

case "$(uname -s)" in
    Linux)
        if is_arch; then
            ALIAS_MAP+=(
                pls "sudo pacman -S"
            )
        fi
        ;;
    Darwin)
        ALIAS_MAP+=(
            pls "brew install"
        )
        ;;
esac

for name cmd in ${(kv)ALIAS_MAP}; do
    alias "$name=$cmd"
done
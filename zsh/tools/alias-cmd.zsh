typeset -A ALIAS_MAP # local is equal to typeset
ALIAS_MAP=(
    mkdocs "uv run mkdocs serve --livereload"
    fs fastfetch
)

for name cmd in ${(kv)ALIAS_MAP}; do
    alias "$name=$cmd"
done
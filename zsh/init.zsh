export OMZ="${HOME}/.config/zsh"

for config_file ("$OMZ"/config/*.zsh); do
    source "$config_file"
done

if [ -n "$ZSH_THEME" ]; then
    source "$OMZ/themes/$ZSH_THEME/$ZSH_THEME.zsh-theme"
fi
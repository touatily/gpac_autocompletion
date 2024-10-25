_gpac_completion() {
    # Get the whole command line
    local cur=${COMP_WORDS[COMP_CWORD]}
    local command_line="${COMP_LINE}"
    local cursor_position=$COMP_POINT


    # Get the directory where the current autocomplete script is located
    SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
    SCRIPTPATH="$SCRIPT_DIR/gpac_autocomplete.py"

    local all_completions
    all_completions=$(python3 "$SCRIPTPATH" "$cursor_position" \""$command_line"\")

    # Split the output based on newlines
    IFS=$'\n' read -r -d '' -a all_completions <<< "$all_completions"$'\0'

    # Filter completions to include only those starting with the current word
    COMPREPLY=("${all_completions[@]}")

    compopt -o nospace
}

complete -F _gpac_completion gpac

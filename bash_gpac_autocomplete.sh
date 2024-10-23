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
    code=$?

    # Split the output based on newlines
    IFS=$'\n' read -r -d '' -a all_completions <<< "$all_completions"$'\0'

    if [ $code -eq 1 ]; then
        # Remove special chars in $cur
        #cur=$(echo "$cur" | sed 's/[^a-zA-Z0-9_\-\./\~]//g')
        # Append default suggestions to the completions
        local IFS=$'\n'
        local file_suggestions=($(compgen -fd -- "$cur"))
        for i in "${!file_suggestions[@]}"; do
            file_suggestions[$i]=$(printf '%s' "${file_suggestions[$i]}" | sed 's/ /\\ /g')
            # Resolve tilde to home directory
            if [[ "${file_suggestions[$i]}" == \~/* ]]; then
                tmp="${HOME}${file_suggestions[$i]:1}"
            else
                tmp="${file_suggestions[$i]}"
            fi
            if [ -d "${tmp}" ]; then
                file_suggestions[$i]="${file_suggestions[$i]}/"
            else
                file_suggestions[$i]="${file_suggestions[$i]} "
            fi
        done

        all_completions=("${all_completions[@]}" "${file_suggestions[@]}")
    fi

    # Filter completions to include only those starting with the current word
    COMPREPLY=("${all_completions[@]}")

    compopt -o nospace
}

complete -F _gpac_completion gpac

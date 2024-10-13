#!/bin/bash

# Check if we're installing system-wide or user-specific
INSTALL_DIR=""

if [ "$(id -u)" = "0" ]; then
    # System-wide installation
    INSTALL_DIR="/etc/bash_completion.d/"
else
    # User-specific installation
    INSTALL_DIR="$HOME/.bash_completion.d/"
    mkdir -p "$INSTALL_DIR"
    
    # Add sourcing to .bashrc if not already there
    if ! grep -Fxq "source $HOME/.bash_completion.d/bash_gpac_autocomplete.sh" "$HOME/.bashrc"; then
        echo "source $HOME/.bash_completion.d/bash_gpac_autocomplete.sh" >> "$HOME/.bashrc"
    fi
fi

# Copy the autocompletion script
cp bash_gpac_autocomplete.sh "$INSTALL_DIR"
cp autocomplete/gpac_autocomplete.py "$INSTALL_DIR"

echo "Autocompletion script installed in $INSTALL_DIR"

# Reload the shell (optional)
source "$HOME/.bashrc"

echo "Autocompletion script successfully installed!"
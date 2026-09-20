#!/usr/bin/env bash 
set -euo pipefail

ACTION="${1:-}" 

case "$ACTION" in 
"install")
    echo "Installing dependencies..."
    if command -v apt >/dev/null 2>&1; then
        sudo apt update -y 
        command -v ninja >/dev/null 2>&1 || { sudo apt install -y ninja-build; }
    fi
    echo "Completed installing ninja-build."
    ;; 
"update")
    if [ -f "build/compile_commands.json" ]; then
        ln -sf build/compile_commands.json compile_commands.json
        echo "compile_commands.json linked successfully."
    else 
        echo "Not found compile_commands.json file in build directory. Please run './build.sh' command first."
    fi
    ;;
*)
    echo "Usage:"
    echo "  ./requirements.sh install  -> install ninja-build"
    echo "  ./requirements.sh update   -> create symlink for compile_commands.json"
    exit 1
    ;;
esac

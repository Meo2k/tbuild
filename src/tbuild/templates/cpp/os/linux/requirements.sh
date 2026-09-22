#!/usr/bin/env bash 
set -euo pipefail

ACTION="${1:-}" 

case "$ACTION" in 
"install")
    echo "Installing dependencies..."
    
    need_ninja=0
    need_cmake=0
    need_compiler=0

    command -v ninja >/dev/null 2>&1 || need_ninja=1
    command -v cmake >/dev/null 2>&1 || need_cmake=1
    (command -v g++ >/dev/null 2>&1 || command -v clang++ >/dev/null 2>&1) || need_compiler=1

    if [ "$need_ninja" -eq 0 ] && [ "$need_cmake" -eq 0 ] && [ "$need_compiler" -eq 0 ]; then
        echo "All dependencies (ninja, cmake, C++ compiler) are already installed."
    else
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update -y
            pkgs=""
            [ "$need_ninja" -eq 1 ] && pkgs="$pkgs ninja-build"
            [ "$need_cmake" -eq 1 ] && pkgs="$pkgs cmake"
            [ "$need_compiler" -eq 1 ] && pkgs="$pkgs build-essential"
            # shellcheck disable=SC2086
            sudo apt-get install -y $pkgs
        else
            echo "apt-get not found. This script supports Debian/Ubuntu/Mint."
            exit 1
        fi
    fi

    # Reload PATH & shell hash cache
    hash -r 2>/dev/null || true
    export PATH="/usr/local/bin:/usr/bin:$PATH"
    echo "Reloaded PATH and environment."
    echo "Completed dependencies installation."
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
    echo "  ./requirements.sh install  -> install ninja, cmake, and C++ compiler"
    echo "  ./requirements.sh update   -> create symlink for compile_commands.json"
    exit 1
    ;;
esac

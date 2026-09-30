#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"

case "$ACTION" in
"install")
    echo "Checking and installing dependencies..."

    need_python=0
    need_uv=0

    (command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1) || need_python=1
    command -v uv >/dev/null 2>&1 || need_uv=1

    if [ "$need_python" -eq 0 ] && [ "$need_uv" -eq 0 ]; then
        echo "All dependencies (Python, uv) are already installed."
    else
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update -y

            if [ "$need_python" -eq 1 ]; then
                echo "Installing Python..."
                sudo apt-get install -y python3 python3-pip python3-venv
            fi

            if [ "$need_uv" -eq 1 ]; then
                echo "Installing uv..."
                if ! command -v curl >/dev/null 2>&1; then
                    sudo apt-get install -y curl
                fi
                curl -LsSf https://astral.sh/uv/install.sh | sh
            fi
        else
            echo "apt-get not found. This script only supports Ubuntu/Debian."
            exit 1
        fi
    fi

    # Reload PATH & shell hash cache
    hash -r 2>/dev/null || true
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:/usr/local/bin:/usr/bin:$PATH"
    echo "Reloaded PATH and environment."
    echo "Completed dependencies installation."
    ;;

*)
    echo "Usage:"
    echo "  ./requirements.sh install  -> check and install Python and uv"
    exit 1
    ;;
esac

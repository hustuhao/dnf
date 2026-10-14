#!/usr/bin/env bash
# Use in Codex Cloud environment setup, or a Linux VM with apt.
# Installs analysis tools only: does NOT execute bundled game binaries.
set -euo pipefail

if ! command -v apt-get >/dev/null 2>&1; then
  echo "Expected an apt-based Linux environment. See cloud/README.md." >&2
  exit 2
fi

if [[ "$(id -u)" == "0" ]]; then
  apt-get update
  apt-get install -y --no-install-recommends binutils file gdb git graphviz jq python3 python3-venv ripgrep strace ca-certificates curl
elif command -v sudo >/dev/null 2>&1 && sudo -n true 2>/dev/null; then
  sudo -n apt-get update
  sudo -n apt-get install -y --no-install-recommends binutils file gdb git graphviz jq python3 python3-venv ripgrep strace ca-certificates curl
else
  echo "Cannot install system packages without root or passwordless sudo." >&2
  exit 3
fi

bash research/dungeon-sync/cloud/verify-env.sh

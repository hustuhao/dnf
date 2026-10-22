FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils file gdb git graphviz jq python3 python3-venv ripgrep \
    strace ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

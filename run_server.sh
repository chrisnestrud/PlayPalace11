#!/usr/bin/env bash
# PlayPalace Server Launcher for NixOS

cd "$(dirname "$0")/server"

nix-shell ../shell.nix --run "uv run python main.py $@"

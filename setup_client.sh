#!/usr/bin/env bash
# One-time setup: sync client dependencies (except wxPython which comes from Nix)

cd "$(dirname "$0")/client"

echo "Syncing client dependencies (using system wxPython)..."
nix-shell ../shell.nix --run "uv sync --no-install-project"

echo ""
echo "Setup complete! You can now run:"
echo "  ./run_client.sh"

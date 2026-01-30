#!/usr/bin/env bash
# Build PlayPalace distribution packages

set -e

echo "Building PlayPalace packages..."
echo "================================"

# Enter nix-shell for build environment
nix-shell --run '
  # Build server
  echo "Building server..."
  cd server
  uv sync --all-extras
  uv build
  cd ..
  
  # Build client  
  echo "Building client..."
  cd client
  uv sync
  uv build
  cd ..
  
  echo ""
  echo "Build complete!"
  echo "Packages created in:"
  echo "  server/dist/"
  echo "  client/dist/"
'

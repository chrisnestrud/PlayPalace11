#!/usr/bin/env bash
# PlayPalace Client Launcher for NixOS

cd "$(dirname "$0")/client"

nix-shell ../shell.nix --run '
  # Suppress GTK warnings for cleaner output
  export G_MESSAGES_DEBUG=""
  export GTK_DISABLE_GAIL_WARNING=1
  
  # Check if venv exists, create with system-site-packages if not
  if [ ! -d .venv ]; then
    echo "Creating virtual environment with system packages access..."
    python -m venv --system-site-packages .venv
    source .venv/bin/activate
    echo "Installing client dependencies (wxPython and speechd from system)..."
    pip install --quiet websockets accessible-output2 sound-lib platformdirs
  else
    source .venv/bin/activate
  fi
  
  # Run client (wxPython and speechd from system via PYTHONPATH)
  python client.py '"$@"'
'

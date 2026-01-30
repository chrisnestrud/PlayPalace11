{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    python311Packages.pip
    python311Packages.virtualenv
    python311Packages.wxpython
    python311Packages.websockets
    uv
    # Client dependencies
    gtk3
    portaudio
    libsndfile
    openal
    speechd
    # Build tools
    gcc
    pkg-config
  ];

  shellHook = ''
    export UV_SYSTEM_PYTHON=1
    echo "PlayPalace Development Environment"
    echo "=================================="
    echo "Python: $(python --version)"
    echo "uv: $(uv --version)"
    echo ""
    echo "To run the server:"
    echo "  ./run_server.sh"
    echo "  or: cd server && uv run python main.py"
    echo ""
    echo "To run the client:"
    echo "  ./run_client.sh"
    echo "  or: cd client && uv run python client.py"
    echo ""
    echo "Dependencies will be installed on first run."
  '';

  # Required for wxPython and audio on NixOS
  LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [
    pkgs.gtk3
    pkgs.portaudio
    pkgs.libsndfile
    pkgs.openal
  ]}";
  
  # Use system Python packages (wxPython from Nix)
  PYTHONPATH = "${pkgs.python311Packages.wxpython}/${pkgs.python311.sitePackages}";
}

# PlayPalace NixOS Build - Complete

## ✅ Build Status

**Server:** ✅ Fully functional  
**Client:** ✅ Functional (silent mode - no audio)

## Quick Start

### Start Server
```bash
./run_server.sh
```
Server starts on `ws://0.0.0.0:8000` by default.

### Start Client
```bash
./run_client.sh
```
Client starts in silent mode (no sound effects). All features work normally.

## What Was Built

### Distribution Packages
- `server/dist/playpalace_server-11.0.0-py3-none-any.whl` (637 KB)
- `client/dist/playpalace_client-11.0.0-py3-none-any.whl` (53 MB)

### NixOS Configuration
- `shell.nix` - Development environment with all dependencies
- `run_server.sh` - Server launcher (uses nix-shell)
- `run_client.sh` - Client launcher (uses nix-shell + venv)
- `build.sh` - Rebuild distribution packages
- `test_run.sh` - Quick verification test

### Documentation
- `NIXOS_SETUP.md` - Detailed NixOS-specific instructions
- `README.md` - General project documentation

## Technical Details

### Server
- Uses `uv` for dependency management
- All dependencies installed in nix-shell
- Starts immediately (no build time)

### Client  
- Uses system wxPython from Nix (avoids 30-min compile)
- Creates `.venv` with other dependencies (websockets, accessible-output2, sound-lib)
- Runs in silent mode when no audio device available
- Fully functional for gameplay testing

### Audio Issue
The client tries to initialize BASS audio library at import time. When no audio device is available (common on headless systems or without PulseAudio/PipeWire), it gracefully falls back to silent mode.

**To enable audio:**
1. Ensure PulseAudio or PipeWire is running
2. Verify with: `speaker-test -t wav -c 2`
3. Restart client

## Usage Examples

```bash
# Start server on custom port
./run_server.sh --port 9000

# Start server with SSL
./run_server.sh --ssl-cert cert.pem --ssl-key key.pem

# Run server tests
nix-shell --run "cd server && uv run pytest"

# Rebuild packages
./build.sh
```

## File Locations

All launcher scripts are in the root directory:
- `/home/alek/git/PlayPalace/run_server.sh`
- `/home/alek/git/PlayPalace/run_client.sh`
- `/home/alek/git/PlayPalace/build.sh`
- `/home/alek/git/PlayPalace/test_run.sh`

## Success Indicators

When everything works:
- Server: `Starting PlayPalace v11 server on ws://0.0.0.0:8000`
- Client: `Warning: Could not initialize audio output... Running in silent mode`
- Client shows login window and connects to server

## Next Steps

1. Start the server: `./run_server.sh`
2. Start the client: `./run_client.sh`  
3. Connect client to `localhost:8000`
4. Create account and play!

For audio, configure PulseAudio/PipeWire if needed (optional).

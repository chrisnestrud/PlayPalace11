# Web Client (Phase 1)

A minimal PlayPalace web POC implementing Phase 1 from `server/web.md`:
- connect + authorize
- server menu rendering + menu events
- `speak` history/live region output
- chat send/receive
- `play_sound` and `play_music`
- gameplay keybind packet sending

## Setup

1. Start the server:
   - `cd server && uv sync && uv run python main.py`
2. From repo root, serve static files so both `web-client/` and `client/packet_schema.json` are reachable:
   - `python3 -m http.server 8080`
3. Open:
   - `http://127.0.0.1:8080/web-client/`
4. Configure websocket target in `web-client/config.js` if needed.
5. Log in with username/password.

## Notes

- Audio is unlocked on the first user gesture (click/key press).
- Sound files are loaded from `/client/sounds/...`.
- While connected, Tab focus cycles only between menu, history, and chat input.

## Connection config

Edit `web-client/config.js`:

- `serverPort`: Override the websocket port on the current host.
  - Example for your setup: `serverPort: 7000`
- `serverUrl`: Full override (host + scheme + port), takes precedence.
  - Example: `serverUrl: "wss://playpalace.example.com:7000"`

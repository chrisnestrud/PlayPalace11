#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENDOR_DIR="${SCRIPT_DIR}/vendor"
LOG_DIR="${HOME:-/home/pi}/.playpalace"
LOG_PATH="${LOG_DIR}/btspeak_client_launcher.log"

cd "${REPO_ROOT}"
mkdir -p "${VENDOR_DIR}"
mkdir -p "${LOG_DIR}"
export PYTHONPATH="${VENDOR_DIR}:/BTSpeak/Python:${PYTHONPATH:-}"

{
  echo "-----"
  echo "start=$(date -Iseconds) user=$(id -un) cwd=$(pwd)"
  echo "python=$(command -v python3)"
  python3 - <<'PY'
import sys
print("sys.path[0]=", sys.path[0])
try:
    import btspeak_client
    print("btspeak_client=", getattr(btspeak_client, "__file__", "n/a"))
except Exception as exc:
    print("btspeak_client_import_error=", repr(exc))
PY
} >> "${LOG_PATH}"

# Announce startup before dependency checks and Python import work.
if [ -x /BTSpeak/bin/say-message ]; then
  /BTSpeak/bin/say-message -I "Please wait. Starting Play Palace client." >/dev/null 2>&1 || true
fi

if [ ! -d "${VENDOR_DIR}/websockets" ] && ! python3 -c "import websockets" >/dev/null 2>&1; then
  python3 -m pip install --quiet --target "${VENDOR_DIR}" websockets
fi

set +e
python3 -m btspeak_client.client >> "${LOG_PATH}" 2>&1
status=$?
set -e
echo "end=$(date -Iseconds) status=${status}" >> "${LOG_PATH}"
if [ "${status}" -ne 0 ] && [ -x /BTSpeak/bin/say-message ]; then
  /BTSpeak/bin/say-message -I "Play Palace client stopped unexpectedly. See btspeak client crash log." >/dev/null 2>&1 || true
fi
exit "${status}"

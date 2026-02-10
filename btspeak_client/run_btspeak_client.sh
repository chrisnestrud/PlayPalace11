#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENDOR_DIR="${SCRIPT_DIR}/vendor"

cd "${REPO_ROOT}"
mkdir -p "${VENDOR_DIR}"
export PYTHONPATH="${VENDOR_DIR}:/BTSpeak/Python:${PYTHONPATH:-}"

if ! python3 -c "import websockets" >/dev/null 2>&1; then
  python3 -m pip install --quiet --target "${VENDOR_DIR}" websockets
fi

exec python3 -m btspeak_client.client

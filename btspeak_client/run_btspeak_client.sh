#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

if command -v uv >/dev/null 2>&1; then
  exec uv run --project "${REPO_ROOT}/btspeak_client" python -m btspeak_client.client
fi

exec python3 -m btspeak_client.client

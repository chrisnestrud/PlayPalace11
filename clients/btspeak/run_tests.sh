#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "${SCRIPT_DIR}"
if [[ -n "${PYTHONPATH:-}" ]]; then
  export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"
else
  export PYTHONPATH="${SCRIPT_DIR}"
fi

exec uv run pytest "$@"

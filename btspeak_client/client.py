"""Entry point for the BTSpeak-native Play Palace client."""

from __future__ import annotations

import traceback
from datetime import datetime
from pathlib import Path


def main() -> int:
    try:
        from .runtime import BTSpeakClientRuntime

        runtime = BTSpeakClientRuntime()
        return runtime.run()
    except BaseException:
        log_dir = Path.home() / ".playpalace"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "btspeak_client_crash.log"
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"\n[{datetime.now().isoformat()}] Unhandled exception\n")
            fh.write(traceback.format_exc())
        raise


if __name__ == "__main__":
    raise SystemExit(main())

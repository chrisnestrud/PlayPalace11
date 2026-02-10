"""Entry point for the BTSpeak-native Play Palace client."""

from __future__ import annotations

from .runtime import BTSpeakClientRuntime


def main() -> int:
    runtime = BTSpeakClientRuntime()
    return runtime.run()


if __name__ == "__main__":
    raise SystemExit(main())

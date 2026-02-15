from __future__ import annotations

import pytest
from pathlib import Path


def test_main_runs_runtime(monkeypatch):
    import btspeak_client.runtime as runtime_mod
    from btspeak_client import client

    class FakeRuntime:
        def run(self):
            return 5

    monkeypatch.setattr(runtime_mod, "BTSpeakClientRuntime", FakeRuntime)

    assert client.main() == 5


def test_main_logs_exception(monkeypatch, tmp_path):
    import btspeak_client.runtime as runtime_mod
    from btspeak_client import client

    class FakeRuntime:
        def __init__(self):
            raise RuntimeError("boom")

    monkeypatch.setattr(runtime_mod, "BTSpeakClientRuntime", FakeRuntime)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    with pytest.raises(RuntimeError):
        client.main()

    log_path = tmp_path / ".playpalace" / "btspeak_client_crash.log"
    assert log_path.exists()
    text = log_path.read_text(encoding="utf-8")
    assert "Unhandled exception" in text

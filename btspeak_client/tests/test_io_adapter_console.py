from __future__ import annotations

import builtins
from pathlib import Path

from btspeak_client.io_adapter import ConsoleIO, ChoiceOption, BTSpeakIO


def test_console_choose_default_and_cancel(monkeypatch):
    io = ConsoleIO()
    inputs = iter(["", "q"])

    def fake_input(_prompt=""):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)

    options = [ChoiceOption("first", "First"), ChoiceOption("second", "Second")]
    assert io.choose("Prompt", options, default_key="second") == "second"
    assert io.choose("Prompt", options, default_key="first") is None


def test_console_choose_rejects_invalid(monkeypatch):
    io = ConsoleIO()
    inputs = iter(["x"])
    rejected = {"count": 0}

    def fake_input(_prompt=""):
        return next(inputs)

    def fake_rejected():
        rejected["count"] += 1

    monkeypatch.setattr(builtins, "input", fake_input)
    io.rejected_action = fake_rejected
    options = [ChoiceOption("first", "First")]
    assert io.choose("Prompt", options) is None
    assert rejected["count"] == 1


def test_console_request_text_read_only(monkeypatch):
    io = ConsoleIO()
    spoken = []

    def fake_speak(text, *, interrupt=False):
        spoken.append((text, interrupt))

    io.speak = fake_speak
    result = io.request_text("Prompt", default="value", read_only=True)
    assert result == "value"
    assert spoken == [("value", False)]


def test_console_request_text_multiline(monkeypatch):
    io = ConsoleIO()
    inputs = iter(["line1", "line2", "."])

    def fake_input(_prompt=""):
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)
    result = io.request_text("Prompt", multiline=True)
    assert result == "line1\nline2"


def test_console_request_text_password(monkeypatch):
    io = ConsoleIO()

    def fake_getpass(_prompt=""):
        return " secret "

    monkeypatch.setattr("btspeak_client.io_adapter.getpass", fake_getpass)
    assert io.request_text("Prompt", password=True) == "secret"


def test_btspeak_request_text_with_dialogs(monkeypatch, tmp_path):
    class FakeDialogs:
        def requestInput(self, prompt, password=False, initialText=None):
            return "  result  "

    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = FakeDialogs()
    io._use_dialogs_api = True
    io._debug_log_path = tmp_path / "log.txt"
    io._host = object()
    assert io.request_text("Prompt", default="") == "result"


def test_btspeak_request_text_multiline_uses_request_input(monkeypatch, tmp_path):
    class FakeDialogs:
        def requestInput(self, *args, **kwargs):
            return "multi line"

    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = FakeDialogs()
    io._use_dialogs_api = True
    io._debug_log_path = tmp_path / "log.txt"
    io._host = object()

    result = io.request_text("Prompt", default="seed", multiline=True)
    assert result == "multi line"


def test_btspeak_show_message_uses_dialog(monkeypatch, tmp_path):
    calls = {"shown": False}

    class FakeDialogs:
        def showMessage(self, text, wait=True):
            calls["shown"] = True

    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = FakeDialogs()
    io._use_dialogs_api = True
    io._debug_log_path = tmp_path / "log.txt"
    io._host = object()

    io.show_message("Hello", wait=False)
    assert calls["shown"] is True


def test_btspeak_choose_returns_none_on_exception(monkeypatch, tmp_path):
    class FakeDialogs:
        def requestChoice(self, *args, **kwargs):
            raise RuntimeError("boom")

    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = FakeDialogs()
    io._use_dialogs_api = True
    io._debug_log_path = tmp_path / "log.txt"
    io._host = object()

    options = [ChoiceOption("first", "First")]
    assert io.choose("Prompt", options) is None


def test_btspeak_view_long_text_falls_back_to_notify(monkeypatch, tmp_path):
    spoken = []

    class FakeDialogs:
        def viewLines(self, _lines):
            raise RuntimeError("boom")

    class FakeHost:
        def say(self, text, immediate=False):
            spoken.append((text, immediate))

    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = FakeDialogs()
    io._use_dialogs_api = True
    io._debug_log_path = tmp_path / "log.txt"
    io._host = FakeHost()

    io.view_long_text("Title", "Body")
    assert spoken == []


def test_btspeak_request_text_returns_none_without_dialogs(monkeypatch, tmp_path):
    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = object()
    io._use_dialogs_api = False
    io._debug_log_path = tmp_path / "log.txt"
    io._host = object()

    assert io.request_text("Prompt") is None


def test_btspeak_choose_returns_none_on_empty_options(tmp_path):
    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = object()
    io._use_dialogs_api = True
    io._debug_log_path = tmp_path / "log.txt"
    io._host = object()
    assert io.choose("Prompt", []) is None


def test_btspeak_request_text_read_only_uses_speak(tmp_path):
    spoken = []

    class FakeHost:
        def say(self, text, immediate=False):
            spoken.append((text, immediate))

    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = object()
    io._use_dialogs_api = False
    io._debug_log_path = tmp_path / "log.txt"
    io._host = FakeHost()

    assert io.request_text("Prompt", default="value", read_only=True) == "value"
    assert spoken == [("value", False)]


def test_btspeak_view_paged_text_returns_none_without_curses(tmp_path):
    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = object()
    io._use_dialogs_api = True
    io._debug_log_path = tmp_path / "log.txt"
    io._host = object()

    assert io.view_paged_text("Title", ["Line 1"]) is None


def test_btspeak_view_paged_text_returns_action(monkeypatch, tmp_path):
    import types

    class FakeDialogs:
        def cursesDialog(self, draw_fn):
            class FakeScreen:
                def getmaxyx(self):
                    return (5, 80)

                def clear(self):
                    return None

                def addstr(self, *_args):
                    return None

                def refresh(self):
                    return None

                def get_wch(self):
                    return "\x1b"

            return draw_fn(FakeScreen())

    class FakeHost:
        def say(self, text, immediate=False):
            return None

    fake_braille = types.SimpleNamespace(
        Dot1=1,
        Dot2=2,
        Dot3=4,
        Dot4=8,
        Dot5=16,
        Dot6=32,
        Dot7=64,
        Dot8=128,
        asciiToUnicodeDots=lambda _key: "dots7",
        dotsToUnicode=lambda _val: "dots7",
    )

    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = FakeDialogs()
    io._use_dialogs_api = True
    io._debug_log_path = tmp_path / "log.txt"
    io._host = FakeHost()

    import sys
    fake_btspeak = types.SimpleNamespace(braille=fake_braille)
    monkeypatch.setitem(sys.modules, "BTSpeak", fake_btspeak)
    monkeypatch.setitem(sys.modules, "BTSpeak.braille", fake_braille)

    assert io.view_paged_text("Title", ["Line 1", "Line 2"]) == "exit"

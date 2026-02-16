from __future__ import annotations

from btspeak_client.io_adapter import BTSpeakIO, ChoiceOption
from pathlib import Path


class FakeDialogs:
    def __init__(self, result):
        self._result = result

    def requestChoice(self, *args, **kwargs):
        return self._result


class FakeChoice:
    def __init__(self, key, label):
        self.key = key
        self.label = label


def make_io_with_result(result):
    io = BTSpeakIO.__new__(BTSpeakIO)
    io._dialogs = FakeDialogs(result)
    io._host = object()
    io._debug_log_path = Path("/tmp/btspeak_client_test.log")
    return io


def test_choose_falls_back_to_label_when_key_is_not_numeric():
    io = make_io_with_result(FakeChoice(key="x", label="Select identity"))
    options = [
        ChoiceOption("add_identity", "Add identity"),
        ChoiceOption("select_identity", "Select identity"),
    ]
    assert io.choose("Prompt", options) == "select_identity"


def test_choose_supports_one_based_index():
    io = make_io_with_result(FakeChoice(key=2, label="ignored"))
    options = [
        ChoiceOption("first", "First"),
        ChoiceOption("second", "Second"),
    ]
    assert io.choose("Prompt", options) == "second"


def test_choose_one_based_first_item_maps_to_first_option():
    io = make_io_with_result(FakeChoice(key=1, label="ignored"))
    options = [
        ChoiceOption("first", "First"),
        ChoiceOption("second", "Second"),
    ]
    assert io.choose("Prompt", options) == "first"


def test_choose_prefers_numeric_index_when_labels_duplicate():
    io = make_io_with_result(FakeChoice(key=2, label="alice"))
    options = [
        ChoiceOption("identity-1", "alice"),
        ChoiceOption("identity-2", "alice"),
    ]
    assert io.choose("Prompt", options) == "identity-2"


def test_choose_returns_none_when_dialog_returns_none():
    io = make_io_with_result(None)
    options = [ChoiceOption("first", "First")]
    assert io.choose("Prompt", options) is None


def test_choose_returns_none_when_label_not_found():
    io = make_io_with_result(FakeChoice(key="x", label="Unknown"))
    options = [
        ChoiceOption("first", "First"),
        ChoiceOption("second", "Second"),
    ]
    assert io.choose("Prompt", options) is None


def test_choose_returns_none_when_label_not_string():
    io = make_io_with_result(FakeChoice(key="x", label=None))
    options = [ChoiceOption("first", "First")]
    assert io.choose("Prompt", options) is None

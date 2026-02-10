from __future__ import annotations

from btspeak_client.io_adapter import BTSpeakIO, ChoiceOption


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
    return io


def test_choose_resolves_by_label_first():
    io = make_io_with_result(FakeChoice(key=99, label="Select identity"))
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


def test_choose_supports_zero_based_index():
    io = make_io_with_result(FakeChoice(key=0, label="ignored"))
    options = [
        ChoiceOption("first", "First"),
        ChoiceOption("second", "Second"),
    ]
    assert io.choose("Prompt", options) == "first"

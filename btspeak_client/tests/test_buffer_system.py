from __future__ import annotations

import time

from btspeak_client.buffer_system import BufferSystem


def test_add_item_creates_buffer_and_all():
    system = BufferSystem()
    system.create_buffer("all")

    original_time = time.time
    try:
        time.time = lambda: 123.45
        system.add_item("chats", "hello")
    finally:
        time.time = original_time

    assert "chats" in system.buffers
    assert len(system.buffers["chats"]) == 1
    assert len(system.buffers["all"]) == 1
    assert system.buffers["chats"][0]["text"] == "hello"
    assert system.buffers["chats"][0]["timestamp"] == 123.45


def test_buffer_navigation_does_not_wrap():
    system = BufferSystem()
    system.create_buffer("first")
    system.create_buffer("second")

    assert system.get_current_buffer_name() == "first"
    system.previous_buffer()
    assert system.get_current_buffer_name() == "first"
    system.next_buffer()
    assert system.get_current_buffer_name() == "second"
    system.next_buffer()
    assert system.get_current_buffer_name() == "second"
    system.first_buffer()
    assert system.get_current_buffer_name() == "first"
    system.last_buffer()
    assert system.get_current_buffer_name() == "second"


def test_move_in_buffer_and_current_item():
    system = BufferSystem()
    system.create_buffer("all")
    system.add_item("all", "oldest")
    system.add_item("all", "newest")

    assert system.get_current_item()["text"] == "newest"
    system.move_in_buffer("older")
    assert system.get_current_item()["text"] == "oldest"
    system.move_in_buffer("older")
    assert system.get_current_item()["text"] == "oldest"
    system.move_in_buffer("newer")
    assert system.get_current_item()["text"] == "newest"
    system.move_in_buffer("newer")
    assert system.get_current_item()["text"] == "newest"
    system.move_in_buffer("oldest")
    assert system.get_current_item()["text"] == "oldest"
    system.move_in_buffer("newest")
    assert system.get_current_item()["text"] == "newest"


def test_mute_and_clear_buffers():
    system = BufferSystem()
    system.create_buffer("all")
    system.add_item("all", "one")
    system.add_item("all", "two")

    assert system.is_muted("all") is False
    system.toggle_mute("all")
    assert system.is_muted("all") is True
    system.toggle_mute("all")
    assert system.is_muted("all") is False

    system.clear_buffer("all")
    assert system.get_buffer_info() == ("all", 0, 0)

    system.create_buffer("misc")
    system.add_item("misc", "hello")
    system.clear_all_buffers()
    assert system.buffers["all"] == []
    assert system.buffers["misc"] == []

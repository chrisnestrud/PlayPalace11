from __future__ import annotations

import json

from btspeak_client.config_manager import (
    ConfigManager,
    get_item_from_dict,
    set_item_in_dict,
    delete_item_from_dict,
)


def test_get_set_delete_item_helpers():
    data = {"a": {"b": {"c": 1}}}
    assert get_item_from_dict(data, "a/b") == {"c": 1}

    set_item_in_dict(data, "a/b/c", 2)
    assert data["a"]["b"]["c"] == 2

    set_item_in_dict(data, "a/b/d", 3, create_mode=True)
    assert data["a"]["b"]["d"] == 3

    deleted = delete_item_from_dict(data, "a/b/c")
    assert deleted is True
    assert "c" not in data["a"]["b"]

    delete_item_from_dict(data, "a/b/d")
    assert data == {}


def test_set_client_option_and_clear_override(tmp_path):
    cm = ConfigManager(base_path=tmp_path)
    server_id = cm.add_server(name="Main", host="localhost", port=8000)

    cm.set_client_option("audio/music_volume", 40)
    assert cm.profiles["client_options_defaults"]["audio"]["music_volume"] == 40

    cm.set_client_option("social/language_subscriptions/English", True, server_id=server_id, create_mode=True)
    assert cm.profiles["server_options"][server_id]["social"]["language_subscriptions"]["English"] is True

    cm.clear_server_override(server_id, "social/language_subscriptions/English")
    assert cm.profiles["server_options"][server_id] == {}


def test_server_url_normalizes_embedded_port(tmp_path):
    identities = {
        "last_server_id": None,
        "last_identity_id": None,
        "identities": {},
        "servers": {
            "server-1": {
                "server_id": "server-1",
                "name": "Main",
                "host": "example.com:9001",
                "port": 8000,
                "notes": "",
                "accounts": {},
            },
            "server-2": {
                "server_id": "server-2",
                "name": "Secure",
                "host": "wss://example.com:9443/game",
                "port": 8000,
                "notes": "",
                "accounts": {},
            },
        },
    }
    (tmp_path / "identities.json").write_text(json.dumps(identities), encoding="utf-8")

    cm = ConfigManager(base_path=tmp_path)
    assert cm.get_server_url("server-1") == "ws://example.com:9001"
    assert cm.get_server_url("server-2") == "wss://example.com:9443/game"


def test_profiles_migrate_and_save(tmp_path):
    profiles = {
        "client_options_defaults": {
            "social": {
                "chat_input_language": "Check",
                "language_subscriptions": {"Check": True},
            },
            "table_creations": {"Chess": True},
        },
        "servers": {
            "server-1": {
                "options_overrides": {
                    "social": {
                        "chat_input_language": "Check",
                        "language_subscriptions": {"Check": False},
                    },
                    "table_creations": {"Poker": True},
                }
            }
        },
    }
    (tmp_path / "option_profiles.json").write_text(json.dumps(profiles), encoding="utf-8")

    cm = ConfigManager(base_path=tmp_path)

    defaults = cm.profiles["client_options_defaults"]
    assert defaults["social"]["chat_input_language"] == "Czech"
    assert "Czech" in defaults["social"]["language_subscriptions"]
    assert "table_creations" not in defaults
    assert defaults["local_table"]["creation_notifications"]["Chess"] is True

    overrides = cm.profiles["server_options"]["server-1"]
    assert overrides["social"]["chat_input_language"] == "Czech"
    assert "Czech" in overrides["social"]["language_subscriptions"]
    assert "table_creations" not in overrides
    assert overrides["local_table"]["creation_notifications"]["Poker"] is True


def test_client_options_persist_and_reload(tmp_path):
    cm = ConfigManager(base_path=tmp_path)
    server_id = cm.add_server(name="Main", host="localhost", port=8000)

    cm.set_client_option("audio/music_volume", 40)
    cm.set_client_option(
        "social/language_subscriptions/English",
        True,
        server_id=server_id,
        create_mode=True,
    )

    cm_reloaded = ConfigManager(base_path=tmp_path)
    defaults = cm_reloaded.get_client_options()
    overrides = cm_reloaded.get_client_options(server_id)

    assert defaults["audio"]["music_volume"] == 40
    assert overrides["social"]["language_subscriptions"]["English"] is True

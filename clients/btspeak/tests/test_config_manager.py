from __future__ import annotations

from pathlib import Path

import pytest

from btspeak_client.config_manager import ConfigManager


def test_migrate_legacy_accounts_to_global_identities(tmp_path: Path):
    manager = ConfigManager(base_path=tmp_path)
    raw = {
        "servers": {
            "s1": {
                "accounts": {
                    "a1": {
                        "username": "alice",
                        "password": "pw1",
                        "email": "a@example.com",
                        "notes": "",
                    }
                }
            },
            "s2": {
                "accounts": {
                    "a2": {
                        "username": "alice",
                        "password": "pw1",
                        "email": "a@example.com",
                        "notes": "",
                    },
                    "a3": {
                        "username": "bob",
                        "password": "pw2",
                        "email": "",
                        "notes": "n",
                    },
                }
            },
        }
    }

    migrated, changed = manager._migrate_identity_records(raw)
    assert changed is True
    assert len(migrated["identities"]) == 2
    assert migrated["last_identity_id"] is not None


def test_migrate_keeps_existing_global_identities(tmp_path: Path):
    manager = ConfigManager(base_path=tmp_path)
    raw = {
        "identities": {
            "id1": {
                "identity_id": "id1",
                "username": "alice",
                "password": "pw",
                "email": "",
                "notes": "",
            }
        },
        "servers": {
            "s1": {
                "accounts": {
                    "a1": {
                        "username": "old",
                        "password": "old",
                        "email": "",
                        "notes": "",
                    }
                }
            }
        },
    }

    migrated, changed = manager._migrate_identity_records(raw)
    assert changed is False
    assert list(migrated["identities"].keys()) == ["id1"]


def test_add_identity_rejects_duplicate_username_case_insensitive(tmp_path: Path):
    manager = ConfigManager(base_path=tmp_path)
    manager.add_identity(username="Alice", password="pw1")

    with pytest.raises(ValueError, match="already exists"):
        manager.add_identity(username="alice", password="pw2")


def test_get_server_url_keeps_existing_port_in_host_url(tmp_path: Path):
    manager = ConfigManager(base_path=tmp_path)
    server_id = manager.add_server(name="Server", host="wss://example.com:443", port=8000)

    assert manager.get_server_url(server_id) == "wss://example.com:443"


def test_get_server_url_appends_port_when_missing_in_host_url(tmp_path: Path):
    manager = ConfigManager(base_path=tmp_path)
    server_id = manager.add_server(name="Server", host="wss://example.com", port=8000)

    assert manager.get_server_url(server_id) == "wss://example.com:8000"


def test_get_server_url_uses_embedded_port_when_stored_port_invalid(tmp_path: Path):
    manager = ConfigManager(base_path=tmp_path)
    server_id = manager.add_server(name="Server", host="wss://example.com:443", port=80008000)

    assert manager.get_server_url(server_id) == "wss://example.com:443"


def test_load_identities_normalizes_invalid_server_port(tmp_path: Path):
    path = tmp_path / "identities.json"
    path.write_text(
        """{
  "identities": {},
  "servers": {
    "s1": {
      "server_id": "s1",
      "name": "Server",
      "host": "wss://example.com",
      "port": 80008000,
      "notes": ""
    }
  },
  "last_server_id": null,
  "last_identity_id": null
}""",
        encoding="utf-8",
    )

    manager = ConfigManager(base_path=tmp_path)
    server = manager.get_server_by_id("s1")

    assert server is not None
    assert server["port"] == 8000

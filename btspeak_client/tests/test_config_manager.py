from __future__ import annotations

from pathlib import Path

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

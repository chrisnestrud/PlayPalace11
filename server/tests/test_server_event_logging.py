import logging
from types import SimpleNamespace

from server.core.server import Server
from server.core.tables.table import Table
from server.core.users.network_user import NetworkUser


class DummyConnection:
    async def send(self, _packet):
        return None


class DummyGame:
    def __init__(self):
        self._users = {}
        self.calls: list[tuple[str, str]] = []

    def get_player_by_id(self, player_id: str):
        return SimpleNamespace(id=player_id)

    def handle_event(self, player, packet: dict) -> None:
        self.calls.append((player.id, packet.get("type", "unknown")))


def _make_server(tmp_path, *, debug_events: bool = True) -> Server:
    return Server(
        host="127.0.0.1",
        port=0,
        db_path=str(tmp_path / "db.sqlite"),
        locales_dir="locales",
        config_path=tmp_path / "missing.toml",
        preload_locales=False,
        debug_events=debug_events,
    )


def _make_user(name: str = "alice") -> NetworkUser:
    return NetworkUser(name, "en", DummyConnection(), uuid=f"{name}-uuid", approved=True)


def test_forward_game_event_logs_phases(caplog, tmp_path):
    server = _make_server(tmp_path, debug_events=True)
    user = _make_user()
    table = Table(table_id="table-1", game_type="test_game", host=user.username)
    game = DummyGame()
    game._users[user.uuid] = user
    table._game = game

    packet = {"type": "menu", "menu_id": "turn_menu", "selection_id": "attack"}
    caplog.set_level(logging.DEBUG, "playpalace.events")

    server._forward_game_event(user, table, packet)

    assert game.calls == [(user.uuid, "menu")]
    records = [rec for rec in caplog.records if rec.name == "playpalace.events"]
    assert len(records) == 2
    phases = {rec.phase for rec in records}
    assert phases == {"dispatch", "complete"}
    dispatch = next(rec for rec in records if rec.phase == "dispatch")
    assert dispatch.menu_id == "turn_menu"
    assert dispatch.selection_id == "attack"
    assert dispatch.table_id == "table-1"
    complete = next(rec for rec in records if rec.phase == "complete")
    assert complete.duration_ms is not None
    assert complete.duration_ms >= 0

from __future__ import annotations

import asyncio

import btspeak_client.network_manager as nm_mod
import pytest
from btspeak_client.network_manager import CertificateInfo, NetworkManager, TLSUserDeclinedError


PACKET_TO_HANDLER = {
    "authorize_success": "on_authorize_success",
    "speak": "on_server_speak",
    "play_sound": "on_server_play_sound",
    "play_music": "on_server_play_music",
    "play_ambience": "on_server_play_ambience",
    "stop_ambience": "on_server_stop_ambience",
    "add_playlist": "on_server_add_playlist",
    "start_playlist": "on_server_start_playlist",
    "remove_playlist": "on_server_remove_playlist",
    "get_playlist_duration": "on_server_get_playlist_duration",
    "menu": "on_server_menu",
    "request_input": "on_server_request_input",
    "clear_ui": "on_server_clear_ui",
    "game_list": "on_server_game_list",
    "disconnect": "on_server_disconnect",
    "update_options_lists": "on_update_options_lists",
    "open_client_options": "on_open_client_options",
    "open_server_options": "on_open_server_options",
    "table_create": "on_table_create",
    "pong": "on_server_pong",
    "chat": "on_receive_chat",
    "server_status": "on_server_status",
    "stop_music": "on_server_stop_music",
}


class RecordingHandler:
    def __init__(self):
        self.calls = []
        for method in PACKET_TO_HANDLER.values():
            setattr(self, method, self._build_handler(method))

    def _build_handler(self, name):
        def handler(packet):
            self.calls.append((name, packet.get("type")))

        return handler

    def add_history(self, *args, **kwargs):
        return None


def test_handle_packet_dispatches_handlers(monkeypatch):
    handler = RecordingHandler()
    manager = NetworkManager(handler)

    monkeypatch.setattr(nm_mod, "validate_incoming", lambda packet: None)

    for packet_type in PACKET_TO_HANDLER:
        manager._handle_packet({"type": packet_type})

    assert len(handler.calls) == len(PACKET_TO_HANDLER)
    assert {name for name, _ in handler.calls} == set(PACKET_TO_HANDLER.values())


def test_send_packet_requires_connection():
    manager = NetworkManager(RecordingHandler())
    assert manager.send_packet({"type": "ping"}) is False


def test_tls_failure_declined_raises_and_does_not_store(monkeypatch):
    class Handler(RecordingHandler):
        server_id = "server-1"

        def __init__(self):
            super().__init__()
            self.saved = None
            self.config_manager = self

        def set_trusted_certificate(self, server_id, cert_info):
            self.saved = (server_id, cert_info)

        def get_trusted_certificate(self, server_id):
            return None

    handler = Handler()
    manager = NetworkManager(handler, trust_prompt=lambda info: False)
    cert = CertificateInfo(
        host="example.com",
        common_name="example.com",
        sans=("example.com",),
        issuer="ca",
        valid_from="now",
        valid_to="later",
        fingerprint="AA",
        fingerprint_hex="AA",
        pem="PEM",
        matches_host=True,
    )
    async def fake_fetch(url):
        return cert

    monkeypatch.setattr(manager, "_fetch_certificate_info", fake_fetch)

    with pytest.raises(TLSUserDeclinedError):
        asyncio.run(manager._handle_tls_failure("wss://example.com"))
    assert handler.saved is None


def test_tls_failure_accepts_and_stores(monkeypatch):
    class Handler(RecordingHandler):
        server_id = "server-1"

        def __init__(self):
            super().__init__()
            self.saved = None
            self.config_manager = self

        def set_trusted_certificate(self, server_id, cert_info):
            self.saved = (server_id, cert_info)

        def get_trusted_certificate(self, server_id):
            return {"fingerprint": "AA"}

    handler = Handler()
    manager = NetworkManager(handler, trust_prompt=lambda info: True)
    cert = CertificateInfo(
        host="example.com",
        common_name="example.com",
        sans=("example.com",),
        issuer="ca",
        valid_from="now",
        valid_to="later",
        fingerprint="AA",
        fingerprint_hex="AA",
        pem="PEM",
        matches_host=True,
    )

    async def fake_connect(url, ssl=None):
        class FakeTransport:
            def get_extra_info(self, _):
                return None

        class FakeWS:
            transport = FakeTransport()

            async def close(self):
                return None

        return FakeWS()

    async def fake_fetch(url):
        return cert

    monkeypatch.setattr(manager, "_fetch_certificate_info", fake_fetch)
    monkeypatch.setattr(manager, "_verify_pinned_certificate", lambda ws: asyncio.sleep(0))
    monkeypatch.setattr(nm_mod, "connect", fake_connect)

    ws = asyncio.run(manager._handle_tls_failure("wss://example.com"))
    assert ws is not None
    assert handler.saved is not None

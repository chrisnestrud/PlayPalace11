from __future__ import annotations

import asyncio

import pytest
from jsonschema import ValidationError as SchemaValidationError

import btspeak_client.network_manager as net_mod
from btspeak_client.network_manager import CertificateInfo, NetworkManager


class DummyEventHandler:
    def __init__(self):
        self.history = []
        self.debug = []
        self.server_id = "server-1"
        self.config_manager = None

    def add_history(self, message, buffer_name):
        self.history.append((message, buffer_name))

    def _debug_log(self, message):
        self.debug.append(message)


class DummyConfigManager:
    def __init__(self):
        self.trusted = {}

    def get_trusted_certificate(self, server_id):
        return self.trusted.get(server_id)

    def set_trusted_certificate(self, server_id, entry):
        self.trusted[server_id] = entry


def test_format_packet_for_debug_redacts_and_truncates():
    handler = DummyEventHandler()
    nm = NetworkManager(handler)
    packet = {"type": "authorize", "password": "secret", "token": "abc", "data": "x" * 500}
    rendered = nm._format_packet_for_debug(packet, max_len=80)
    assert "***" in rendered
    assert "secret" not in rendered
    assert rendered.endswith("...")


def test_validate_outgoing_and_incoming_emit_activity(monkeypatch):
    handler = DummyEventHandler()
    nm = NetworkManager(handler)

    def fake_outgoing(_packet):
        raise SchemaValidationError("bad outgoing")

    def fake_incoming(_packet):
        raise SchemaValidationError("bad incoming")

    monkeypatch.setattr(net_mod, "validate_outgoing", fake_outgoing)
    monkeypatch.setattr(net_mod, "validate_incoming", fake_incoming)

    assert nm._validate_outgoing_packet({"type": "x"}) is False
    assert nm._validate_incoming_packet({"type": "x"}) is False
    assert "Blocked invalid outgoing packet" in handler.history[0][0]
    assert "Ignored invalid server packet" in handler.history[1][0]


def test_prepare_tls_if_needed_mismatch_emits_activity(monkeypatch):
    class Handler(DummyEventHandler):
        def __init__(self):
            super().__init__()
            self.config_manager = self
            self.trusted = {"server-1": {"fingerprint": "OLD"}}

        def get_trusted_certificate(self, server_id):
            return self.trusted.get(server_id)

        def set_trusted_certificate(self, server_id, entry):
            self.trusted[server_id] = entry

    handler = Handler()
    cert = CertificateInfo(
        host="example.com",
        common_name="example.com",
        sans=("example.com",),
        issuer="ca",
        valid_from="now",
        valid_to="later",
        fingerprint="BB",
        fingerprint_hex="BB",
        pem="PEM",
        matches_host=True,
    )
    manager = NetworkManager(handler, trust_prompt=lambda info: False)
    monkeypatch.setattr(manager, "_run_coroutine_sync", lambda coro: (coro.close(), cert)[1])

    assert manager.prepare_tls_if_needed("wss://example.com") is False
    assert any("Trusted certificate changed" in message for message, _ in handler.history)


def test_open_connection_mismatch_emits_activity(monkeypatch):
    class Handler(DummyEventHandler):
        def __init__(self):
            super().__init__()
            self.config_manager = type(
                "Cfg",
                (),
                {"get_trusted_certificate": lambda _self, _sid: {"fingerprint": "OLD"}},
            )()

    handler = Handler()
    manager = NetworkManager(handler)

    async def fake_handle_tls(_url):
        raise net_mod.TLSUserDeclinedError()

    monkeypatch.setattr(
        manager,
        "_connect_with_trusted_certificate",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(net_mod.ssl.SSLError("mismatch")),
    )
    monkeypatch.setattr(manager, "_handle_tls_failure", fake_handle_tls)

    with pytest.raises(net_mod.TLSUserDeclinedError):
        asyncio.run(manager._open_connection("wss://example.com"))
    assert any("Trusted certificate changed" in message for message, _ in handler.history)


def test_handle_packet_dispatches(monkeypatch):
    handler = DummyEventHandler()
    nm = NetworkManager(handler)
    called = {}

    def on_server_menu(packet):
        called["packet"] = packet

    handler.on_server_menu = on_server_menu
    monkeypatch.setattr(net_mod, "validate_incoming", lambda _packet: None)
    nm._handle_packet({"type": "menu", "items": []})
    assert called["packet"]["type"] == "menu"


def test_send_packet_requires_connection(monkeypatch):
    handler = DummyEventHandler()
    nm = NetworkManager(handler)
    assert nm.send_packet({"type": "ping"}) is False

    sent = {}

    class FakeWS:
        def send(self, message):
            sent["message"] = message
            return message

    def fake_run(coro, loop):
        sent["loop"] = loop
        return object()

    monkeypatch.setattr(asyncio, "run_coroutine_threadsafe", fake_run)
    monkeypatch.setattr(net_mod, "validate_outgoing", lambda _packet: None)
    nm.connected = True
    nm.ws = FakeWS()
    nm.loop = object()

    assert nm.send_packet({"type": "ping"}) is True
    assert "ping" in sent["message"]


def test_prepare_tls_if_needed_trusted_entry(monkeypatch):
    handler = DummyEventHandler()
    handler.config_manager = DummyConfigManager()
    handler.config_manager.trusted["server-1"] = {"fingerprint": "AA"}
    nm = NetworkManager(handler)

    assert nm.prepare_tls_if_needed("wss://example.com") is True


def test_prepare_tls_if_needed_trust_prompt(monkeypatch):
    handler = DummyEventHandler()
    handler.config_manager = DummyConfigManager()

    cert_info = CertificateInfo(
        host="example.com",
        common_name="example.com",
        sans=("example.com",),
        issuer="ca",
        valid_from="now",
        valid_to="later",
        fingerprint="AA:BB",
        fingerprint_hex="AABB",
        pem="pem",
        matches_host=True,
    )

    def fake_run(coro):
        if asyncio.iscoroutine(coro):
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()
        return coro

    nm = NetworkManager(handler, trust_prompt=lambda info: True)
    async def fake_fetch(_url):
        return cert_info
    monkeypatch.setattr(nm, "_fetch_certificate_info", fake_fetch)
    monkeypatch.setattr(nm, "_run_coroutine_sync", fake_run)
    monkeypatch.setattr(nm, "_probe_default_tls_connection", lambda _url: False)

    assert nm.prepare_tls_if_needed("wss://example.com") is True
    assert handler.config_manager.get_trusted_certificate("server-1") is not None


def test_build_certificate_info_and_host_match():
    handler = DummyEventHandler()
    nm = NetworkManager(handler)
    cert_dict = {
        "subject": ((("commonName", "example.com"),),),
        "issuer": ((("organizationName", "Test CA"),),),
        "subjectAltName": (("DNS", "alt.example.com"), ("DNS", "example.com")),
        "notBefore": "yesterday",
        "notAfter": "tomorrow",
    }
    info = nm._build_certificate_info(cert_dict, "AABBCC", "pem", "example.com")
    assert info.common_name == "example.com"
    assert info.matches_host is True
    assert info.fingerprint == "AA:BB:CC"


def test_get_server_host_handles_none():
    handler = DummyEventHandler()
    nm = NetworkManager(handler)
    assert nm._get_server_host(None) == ""


def test_extract_peer_certificate_missing_transport():
    handler = DummyEventHandler()
    nm = NetworkManager(handler)
    assert nm._extract_peer_certificate(None) == (None, None, None)


def test_extract_peer_certificate_with_ssl_object(monkeypatch):
    handler = DummyEventHandler()
    nm = NetworkManager(handler)

    class FakeSSL:
        def getpeercert(self, binary_form=False):
            if binary_form:
                return b"abc"
            return {"subject": (), "issuer": ()}

    class FakeTransport:
        def get_extra_info(self, key):
            if key == "ssl_object":
                return FakeSSL()
            return None

    class FakeWS:
        transport = FakeTransport()

    monkeypatch.setattr(net_mod.ssl, "DER_cert_to_PEM_cert", lambda _der: "pem")

    fingerprint_hex, cert_dict, pem = nm._extract_peer_certificate(FakeWS())
    assert pem == "pem"
    assert fingerprint_hex is not None
    assert cert_dict is not None


def test_verify_pinned_certificate_mismatch_closes(monkeypatch):
    handler = DummyEventHandler()
    handler.config_manager = DummyConfigManager()
    handler.config_manager.trusted["server-1"] = {"fingerprint": "DEADBEEF"}
    nm = NetworkManager(handler)

    closed = {"called": False}

    class FakeWS:
        async def close(self):
            closed["called"] = True

    monkeypatch.setattr(
        nm,
        "_extract_peer_certificate",
        lambda _ws: ("AABB", {"subject": ()}, "pem"),
    )

    with pytest.raises(net_mod.ssl.SSLError):
        asyncio.run(nm._verify_pinned_certificate(FakeWS()))
    assert closed["called"] is True


def test_probe_default_tls_connection(monkeypatch):
    handler = DummyEventHandler()
    nm = NetworkManager(handler)

    class FakeWS:
        async def close(self):
            return None

    async def fake_connect(_url, ssl=None):
        return FakeWS()

    monkeypatch.setattr(net_mod, "connect", fake_connect)
    assert nm._probe_default_tls_connection("wss://example.com") is True

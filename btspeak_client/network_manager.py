"""Non-wx network manager for BTSpeak runtime."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import ssl
import tempfile
import threading
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

import websockets
from jsonschema import ValidationError as SchemaValidationError
from websockets.asyncio.client import connect

from .packet_validator import validate_incoming, validate_outgoing


class TLSUserDeclinedError(Exception):
    """Raised when the user declines to trust a presented TLS certificate."""


@dataclass
class CertificateInfo:
    host: str
    common_name: str
    sans: tuple[str, ...]
    issuer: str
    valid_from: str
    valid_to: str
    fingerprint: str
    fingerprint_hex: str
    pem: str
    matches_host: bool


class NetworkManager:
    """Manages WebSocket connection to Play Palace server."""

    def __init__(
        self,
        event_handler,
        *,
        scheduler: Callable[[Callable, tuple, dict], None] | None = None,
        trust_prompt: Callable[[CertificateInfo], bool] | None = None,
    ):
        self.event_handler = event_handler
        self.scheduler = scheduler or (lambda fn, args, kwargs: fn(*args, **kwargs))
        self.trust_prompt = trust_prompt

        self.ws = None
        self.connected = False
        self.username = None
        self.thread = None
        self.loop = None
        self.should_stop = False
        self.server_url = None
        self.server_id = None
        self._validation_errors = 0

    def _defer(self, callback: Callable, *args, **kwargs):
        self.scheduler(callback, args, kwargs)

    def _emit_activity(self, message: str):
        add_history = getattr(self.event_handler, "add_history", None)
        if callable(add_history):
            self._defer(add_history, message, "activity")

    def _debug(self, message: str) -> None:
        debug_log = getattr(self.event_handler, "_debug_log", None)
        if callable(debug_log):
            self._defer(debug_log, message)

    def _format_packet_for_debug(self, packet: dict, *, max_len: int = 400) -> str:
        redacted_keys = {"password", "token", "auth", "authorization"}
        scrubbed: dict = {}
        for key, value in packet.items():
            if key in redacted_keys:
                scrubbed[key] = "***"
            else:
                scrubbed[key] = value
        try:
            rendered = json.dumps(scrubbed, ensure_ascii=True, default=str)
        except Exception:
            rendered = repr(scrubbed)
        if len(rendered) > max_len:
            rendered = rendered[: max_len - 3] + "..."
        return rendered

    def _validate_outgoing_packet(self, packet: dict) -> bool:
        try:
            validate_outgoing(packet)
            return True
        except SchemaValidationError as exc:
            self._validation_errors += 1
            self._emit_activity(
                f"Blocked invalid outgoing packet #{self._validation_errors}: {exc.message}"
            )
            return False

    def _validate_incoming_packet(self, packet: dict) -> bool:
        try:
            validate_incoming(packet)
            return True
        except SchemaValidationError as exc:
            self._validation_errors += 1
            self._emit_activity(
                f"Ignored invalid server packet #{self._validation_errors}: {exc.message}"
            )
            return False

    def connect(self, server_url, username, password):
        try:
            if self.thread and self.thread.is_alive():
                self.should_stop = True
                self.thread.join(timeout=2.0)

            self.username = username
            self.should_stop = False
            self.server_url = server_url
            self.server_id = getattr(self.event_handler, "server_id", None)

            self.thread = threading.Thread(
                target=self._run_async_loop,
                args=(server_url, username, password),
                daemon=True,
            )
            self.thread.start()
            return True
        except Exception:
            import traceback

            traceback.print_exc()
            return False

    def _run_async_loop(self, server_url, username, password):
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(
                self._connect_and_listen(server_url, username, password)
            )
        except Exception:
            import traceback

            traceback.print_exc()
        finally:
            if self.loop:
                self.loop.close()

    async def _connect_and_listen(self, server_url, username, password):
        websocket = None
        try:
            self._debug(f"net: opening connection url={server_url!r}")
            websocket = await self._open_connection(server_url)
            self.ws = websocket
            self.connected = True

            self._debug("net: sending authorize packet")
            await self._send_authorize(websocket, username, password)

            while not self.should_stop:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    try:
                        packet = json.loads(message)
                    except json.JSONDecodeError as exc:
                        self._debug(f"net: invalid json from server: {exc!r}")
                        raise
                    self._defer(self._handle_packet, packet)
                except asyncio.TimeoutError:
                    continue
                except websockets.exceptions.ConnectionClosed as exc:
                    self._debug(
                        "net: connection closed "
                        f"code={getattr(exc, 'code', None)!r} "
                        f"reason={getattr(exc, 'reason', None)!r}"
                    )
                    break
        except TLSUserDeclinedError:
            self._emit_activity("TLS certificate was not trusted; connection aborted.")
            self._debug("net: tls certificate not trusted")
        except Exception:
            import traceback

            traceback.print_exc()
        finally:
            self._debug(f"net: closing connection should_stop={self.should_stop!r}")
            self.connected = False
            self.ws = None
            if websocket:
                try:
                    await websocket.close()
                except Exception:
                    pass
            if not self.should_stop:
                on_connection_lost = getattr(self.event_handler, "on_connection_lost", None)
                if callable(on_connection_lost):
                    self._defer(on_connection_lost)

    async def _send_authorize(self, websocket, username, password):
        packet = {
            "type": "authorize",
            "username": username,
            "password": password,
            "major": 11,
            "minor": 0,
            "patch": 0,
        }
        if not self._validate_outgoing_packet(packet):
            raise RuntimeError("Client refused to send invalid authorize packet.")
        await websocket.send(json.dumps(packet))

    async def _open_connection(self, server_url: str):
        if not server_url.startswith("wss://"):
            self._debug("net: using insecure websocket (ws)")
            return await connect(server_url)

        trust_entry = self._get_trusted_certificate_entry()
        if trust_entry:
            self._debug("net: using stored trusted certificate")
            return await self._connect_with_trusted_certificate(server_url, trust_entry)

        try:
            self._debug("net: trying default TLS verification")
            websocket = await connect(server_url, ssl=self._build_default_ssl_context())
            await self._verify_pinned_certificate(websocket)
            return websocket
        except ssl.SSLCertVerificationError:
            self._debug("net: default TLS verification failed")
            raise TLSUserDeclinedError()

    def _build_default_ssl_context(self) -> ssl.SSLContext:
        return ssl.create_default_context()

    async def _connect_with_trusted_certificate(self, server_url: str, trust_entry: dict):
        """Connect with verification disabled and pin to stored fingerprint."""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        websocket = await connect(server_url, ssl=context)
        await self._verify_pinned_certificate(websocket)
        return websocket

    async def _handle_tls_failure(self, server_url: str):
        cert_info = await self._fetch_certificate_info(server_url)
        if cert_info is None:
            raise TLSUserDeclinedError()

        trust = False
        if self.trust_prompt:
            trust = bool(self.trust_prompt(cert_info))
        if not trust:
            raise TLSUserDeclinedError()

        self._store_trusted_certificate(cert_info)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        websocket = await connect(server_url, ssl=context)
        await self._verify_pinned_certificate(websocket)
        return websocket

    def prepare_tls_if_needed(self, server_url: str) -> bool:
        if not server_url.startswith("wss://"):
            return True

        if self._get_trusted_certificate_entry():
            return True

        try:
            if self._probe_default_tls_connection(server_url):
                return True
        except Exception:
            return True

        cert_info = self._run_coroutine_sync(self._fetch_certificate_info(server_url))
        if cert_info is None:
            return False

        trust = False
        if self.trust_prompt:
            trust = bool(self.trust_prompt(cert_info))
        if not trust:
            return False

        self._store_trusted_certificate(cert_info)
        return True

    def _probe_default_tls_connection(self, server_url: str) -> bool:
        async def probe():
            websocket = await connect(server_url, ssl=self._build_default_ssl_context())
            try:
                return True
            finally:
                await websocket.close()

        try:
            return bool(self._run_coroutine_sync(probe()))
        except ssl.SSLCertVerificationError:
            return False

    @staticmethod
    def _run_coroutine_sync(coroutine):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coroutine)
        finally:
            loop.close()

    async def _verify_pinned_certificate(self, websocket):
        fingerprint_hex, cert_dict, pem = self._extract_peer_certificate(websocket)
        entry = self._get_trusted_certificate_entry()
        if not entry:
            return

        expected = str(entry.get("fingerprint", "")).upper()
        if not fingerprint_hex or expected != fingerprint_hex.upper():
            await websocket.close()
            raise ssl.SSLError("Trusted certificate fingerprint mismatch.")

    async def _fetch_certificate_info(self, server_url: str) -> CertificateInfo | None:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        websocket = None
        try:
            websocket = await connect(server_url, ssl=context)
            fingerprint_hex, cert_dict, pem = self._extract_peer_certificate(websocket)
            if not fingerprint_hex or not pem:
                return None
            host = self._get_server_host(server_url)
            return self._build_certificate_info(cert_dict or {}, fingerprint_hex, pem, host)
        except Exception:
            return None
        finally:
            if websocket:
                try:
                    await websocket.close()
                except Exception:
                    pass

    def _store_trusted_certificate(self, cert_info: CertificateInfo) -> None:
        manager = getattr(self.event_handler, "config_manager", None)
        server_id = getattr(self.event_handler, "server_id", None)
        if not manager or not server_id:
            return
        manager.set_trusted_certificate(
            server_id,
            {
                "fingerprint": cert_info.fingerprint_hex,
                "pem": cert_info.pem,
                "host": cert_info.host,
                "common_name": cert_info.common_name,
            },
        )

    def _get_trusted_certificate_entry(self) -> dict | None:
        manager = getattr(self.event_handler, "config_manager", None)
        server_id = getattr(self.event_handler, "server_id", None)
        if not manager or not server_id:
            return None
        return manager.get_trusted_certificate(server_id)

    def _extract_peer_certificate(self, websocket):
        if not websocket or not websocket.transport:
            return None, None, None
        ssl_obj = websocket.transport.get_extra_info("ssl_object")
        if not ssl_obj:
            return None, None, None
        der_bytes = ssl_obj.getpeercert(binary_form=True)
        cert_dict = ssl_obj.getpeercert()
        pem = ssl.DER_cert_to_PEM_cert(der_bytes) if der_bytes else None

        if cert_dict is None and pem:
            cert_dict = self._decode_certificate_dict(pem)

        if not der_bytes or cert_dict is None:
            return None, cert_dict, None
        fingerprint_hex = hashlib.sha256(der_bytes).hexdigest().upper()
        return fingerprint_hex, cert_dict, pem

    def _decode_certificate_dict(self, pem: str) -> dict | None:
        tmp_path = None
        try:
            tmp = tempfile.NamedTemporaryFile("w", delete=False)
            tmp.write(pem)
            tmp.flush()
            tmp_path = tmp.name
            tmp.close()
            return ssl._ssl._test_decode_cert(tmp_path)
        except Exception:
            return None
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

    def _build_certificate_info(
        self, cert_dict, fingerprint_hex: str, pem: str, host: str
    ) -> CertificateInfo:
        subject = cert_dict.get("subject", ())
        issuer = cert_dict.get("issuer", ())

        common_name = ""
        for part in subject:
            for key, value in part:
                if key == "commonName":
                    common_name = value

        sans = tuple(
            value
            for kind, value in cert_dict.get("subjectAltName", ())
            if kind.lower() == "dns"
        )

        issuer_text = ", ".join(
            f"{key}={value}" for part in issuer for key, value in part
        )

        host_lower = host.lower()
        matches = common_name.lower() == host_lower or host_lower in {s.lower() for s in sans}

        display_fp = ":".join(
            fingerprint_hex[index : index + 2]
            for index in range(0, len(fingerprint_hex), 2)
        )

        return CertificateInfo(
            host=host,
            common_name=common_name,
            sans=sans,
            issuer=issuer_text,
            valid_from=cert_dict.get("notBefore", ""),
            valid_to=cert_dict.get("notAfter", ""),
            fingerprint=display_fp,
            fingerprint_hex=fingerprint_hex,
            pem=pem,
            matches_host=matches,
        )

    def _get_server_host(self, server_url: str) -> str:
        try:
            return urlparse(server_url).hostname or ""
        except Exception:
            return ""

    def disconnect(self, wait=False, timeout=3.0):
        self.should_stop = True
        self.connected = False

        if self.ws and self.loop:
            try:
                asyncio.run_coroutine_threadsafe(self.ws.close(), self.loop)
            except Exception:
                pass

        if wait and self.thread and self.thread.is_alive():
            self.thread.join(timeout=timeout)

    def send_packet(self, packet):
        if not self.connected or not self.ws or not self.loop:
            return False

        if not self._validate_outgoing_packet(packet):
            return False

        try:
            self._debug(
                "net: send packet "
                f"type={packet.get('type')!r} "
                f"payload={self._format_packet_for_debug(packet)}"
            )
            message = json.dumps(packet)
            asyncio.run_coroutine_threadsafe(self.ws.send(message), self.loop)
            return True
        except Exception:
            import traceback

            traceback.print_exc()
            self.connected = False
            on_connection_lost = getattr(self.event_handler, "on_connection_lost", None)
            if callable(on_connection_lost):
                self._defer(on_connection_lost)
            return False

    def _handle_packet(self, packet):
        if not self._validate_incoming_packet(packet):
            return

        packet_type = packet.get("type")
        self._debug(
            "net: recv packet "
            f"type={packet_type!r} "
            f"payload={self._format_packet_for_debug(packet)}"
        )

        handlers = {
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

        handler_name = handlers.get(packet_type)
        if not handler_name:
            return
        handler = getattr(self.event_handler, handler_name, None)
        if callable(handler):
            handler(packet)

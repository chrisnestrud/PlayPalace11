"""Single-loop BTSpeak client runtime."""

from __future__ import annotations

import time
from threading import Event
from dataclasses import dataclass
from typing import Callable

from .audio_manager import AudioManager
from .buffer_system import BufferSystem
from .config_manager import ConfigManager
from .io_adapter import BTSpeakIO, ChoiceOption, ConsoleIO, IOAdapter
from .network_manager import CertificateInfo, NetworkManager


@dataclass(frozen=True)
class Credentials:
    identity_id: str
    server_id: str
    server_url: str
    username: str
    password: str


class BTSpeakClientRuntime:
    """Main state machine for the BTSpeak client."""

    def __init__(
        self,
        *,
        io: IOAdapter | None = None,
        config_manager: ConfigManager | None = None,
        network_factory: Callable[..., NetworkManager] | None = None,
    ):
        self.io = io or self._build_default_io()
        self.config_manager = config_manager or ConfigManager()
        self.server_id: str | None = None
        self.identity_id: str | None = None
        self.connected = False
        self.running = True
        self._awaiting_authorization = False
        self._authorize_success = False
        self._authorize_event = Event()

        self.network = (
            network_factory(self, trust_prompt=self._prompt_trust_decision)
            if network_factory
            else NetworkManager(self, trust_prompt=self._prompt_trust_decision)
        )

        self.current_menu_id: str | None = None
        self.current_menu_items: list[dict] = []
        self.pending_input_id: str | None = None
        self._ping_start_time: float | None = None

        self.client_options: dict = {}
        self.buffer_system = BufferSystem()
        self.audio_manager = AudioManager()
        for name in ("all", "table", "chats", "activity", "misc"):
            self.buffer_system.create_buffer(name)

    def _build_default_io(self) -> IOAdapter:
        try:
            return BTSpeakIO()
        except Exception:
            return ConsoleIO()

    def _prompt_trust_decision(self, cert_info: CertificateInfo) -> bool:
        lines = [
            "Untrusted certificate.",
            f"Host: {cert_info.host}",
            f"Common name: {cert_info.common_name or '(none)'}",
            f"Fingerprint: {cert_info.fingerprint}",
        ]
        self.io.notify(" ".join(lines))
        choice = self.io.choose(
            "Trust this certificate for this server?",
            [ChoiceOption("yes", "Yes"), ChoiceOption("no", "No")],
            default_key="no",
        )
        return choice == "yes"

    def run(self) -> int:
        while self.running:
            identities = self.config_manager.get_all_identities()
            menu_options = [ChoiceOption("add_identity", "Add identity")]
            if identities:
                menu_options.append(ChoiceOption("remove_identity", "Remove identity"))
                menu_options.append(ChoiceOption("select_identity", "Select identity"))
            menu_options.append(ChoiceOption("exit", "Exit"))

            action = self.io.choose(
                "Identity menu",
                menu_options,
            )
            if action in (None, "exit"):
                self.running = False
                break

            if action == "add_identity":
                self._add_identity_flow()
            elif action == "remove_identity":
                self._remove_identity_flow()
            elif action == "select_identity":
                identity_id = self._select_identity_flow()
                if identity_id:
                    self._identity_server_menu(identity_id)

        self.network.disconnect(wait=True)
        return 0

    def _add_identity_flow(self):
        username = (self.io.request_text("Username", default="") or "").strip()
        if not username:
            self.io.notify("Username is required.")
            return

        password = self.io.request_text("Password", default="", password=True) or ""
        if not password:
            self.io.notify("Password is required.")
            return

        email = self.io.request_text("Email (optional)", default="") or ""
        notes = self.io.request_text("Notes (optional)", default="") or ""

        identity_id = self.config_manager.add_identity(
            username=username,
            password=password,
            email=email,
            notes=notes,
        )
        self.config_manager.set_last_identity(identity_id)
        self.io.notify("Identity added.")

    def _remove_identity_flow(self):
        identities = self.config_manager.get_all_identities()
        if not identities:
            self.io.notify("No identities to remove.")
            return

        identity_id = self._select_identity("Remove which identity?")
        if not identity_id:
            return

        confirm = self.io.choose(
            "Remove this identity?",
            [ChoiceOption("yes", "Yes"), ChoiceOption("back", "Back")],
            default_key="back",
        )
        if confirm != "yes":
            return
        self.config_manager.delete_identity(identity_id)
        self.io.notify("Identity removed.")

    def _select_identity(self, prompt: str) -> str | None:
        identities = self.config_manager.get_all_identities()
        if not identities:
            self.io.notify("No identities available.")
            return None

        last_identity = self.config_manager.get_last_identity_id()
        options = []
        for identity_id, identity in identities.items():
            username = identity.get("username", "Unknown")
            email = identity.get("email", "")
            label = f"{username} ({email})" if email else username
            options.append(ChoiceOption(identity_id, label))
        options.append(ChoiceOption("back", "Back"))

        choice = self.io.choose(prompt, options, default_key=last_identity)
        if not choice or choice == "back":
            return None
        return choice

    def _select_identity_flow(self) -> str | None:
        identity_id = self._select_identity("Select identity")
        if not identity_id:
            return None
        self.config_manager.set_last_identity(identity_id)
        return identity_id

    def _identity_server_menu(self, identity_id: str):
        while self.running:
            identity = self.config_manager.get_identity_by_id(identity_id)
            if not identity:
                self.io.notify("Identity no longer exists.")
                return

            label = identity.get("username", "Identity")
            servers = self.config_manager.get_all_servers()
            menu_options = [ChoiceOption("add_server", "Add server")]
            if servers:
                menu_options.append(ChoiceOption("remove_server", "Remove server"))
                menu_options.append(ChoiceOption("connect_server", "Connect to server"))
            menu_options.append(ChoiceOption("back", "Back"))

            action = self.io.choose(
                f"Server menu for {label}",
                menu_options,
            )
            if action in (None, "back"):
                return
            if action == "add_server":
                self._add_server_flow()
            elif action == "remove_server":
                self._remove_server_flow()
            elif action == "connect_server":
                credentials = self._build_credentials(identity_id)
                if credentials and self._attempt_connection(credentials):
                    self._session_loop()

    def _add_server_flow(self):
        name = (self.io.request_text("Server name", default="") or "").strip()
        if not name:
            self.io.notify("Server name is required.")
            return

        host = (self.io.request_text("Host (e.g. ws://host or wss://host)", default="") or "").strip()
        if not host:
            self.io.notify("Host is required.")
            return

        port_text = (self.io.request_text("Port", default="8000") or "8000").strip()
        try:
            port = int(port_text)
        except ValueError:
            self.io.notify("Port must be a number.")
            return

        notes = self.io.request_text("Notes (optional)", default="") or ""
        self.config_manager.add_server(name=name, host=host, port=port, notes=notes)
        self.io.notify("Server added.")

    def _select_server(self, prompt: str) -> str | None:
        servers = self.config_manager.get_all_servers()
        if not servers:
            self.io.notify("No servers available.")
            return None

        last_server = self.config_manager.get_last_server_id()
        options = []
        for server_id, server in servers.items():
            name = server.get("name", "Unknown Server")
            host = server.get("host", "")
            port = server.get("port", 8000)
            options.append(ChoiceOption(server_id, f"{name} ({host}:{port})"))
        options.append(ChoiceOption("back", "Back"))
        choice = self.io.choose(prompt, options, default_key=last_server)
        if not choice or choice == "back":
            return None
        return choice

    def _remove_server_flow(self):
        server_id = self._select_server("Remove which server?")
        if not server_id:
            return

        confirm = self.io.choose(
            "Remove this server?",
            [ChoiceOption("yes", "Yes"), ChoiceOption("back", "Back")],
            default_key="back",
        )
        if confirm != "yes":
            return
        self.config_manager.delete_server(server_id)
        self.io.notify("Server removed.")

    def _build_credentials(self, identity_id: str) -> Credentials | None:
        identity = self.config_manager.get_identity_by_id(identity_id)
        if not identity:
            self.io.notify("Identity no longer exists.")
            return None

        server_id = self._select_server("Connect to which server?")
        if not server_id:
            return None

        self.config_manager.set_last_server(server_id)
        self.config_manager.set_last_identity(identity_id)

        server_url = self.config_manager.get_server_url(server_id)
        if not server_url:
            self.io.notify("Selected server has no URL.")
            return None

        return Credentials(
            identity_id=identity_id,
            server_id=server_id,
            server_url=server_url,
            username=identity.get("username", ""),
            password=identity.get("password", ""),
        )

    def _attempt_connection(self, credentials: Credentials) -> bool:
        self.identity_id = credentials.identity_id
        self.server_id = credentials.server_id
        self.client_options = self.config_manager.get_client_options(self.server_id)
        self.connected = False
        self._authorize_success = False
        self._awaiting_authorization = True
        self._authorize_event.clear()

        started = self.network.connect(
            credentials.server_url,
            credentials.username,
            credentials.password,
        )
        if not started:
            self._awaiting_authorization = False
            self.io.notify("Failed to start network connection.")
            return False

        self.io.notify("Connecting...")
        authorized = self._authorize_event.wait(timeout=15.0)
        self._awaiting_authorization = False
        if not authorized or not self._authorize_success:
            self.network.disconnect(wait=True)
            self.io.notify("Connection failed.")
            return False
        return True

    def _session_loop(self):
        self.io.notify("Connected. Enter /help for commands.")
        while self.running and self.connected:
            line = self.io.request_text("Message or command", default="")
            if line is None:
                self.network.disconnect(wait=True)
                self.connected = False
                break
            self._handle_user_input(line)

    def _handle_user_input(self, raw_line: str) -> None:
        line = raw_line.strip()
        if not line:
            return

        if self.pending_input_id:
            payload = {"type": "editbox", "text": line, "input_id": self.pending_input_id}
            self.pending_input_id = None
            self.network.send_packet(payload)
            return

        if not line.startswith("/"):
            self.network.send_packet(
                {
                    "type": "chat",
                    "convo": "local",
                    "message": line,
                    "language": self.client_options.get("social", {}).get(
                        "chat_input_language", "Other"
                    ),
                }
            )
            return

        command, _, rest = line.partition(" ")
        command = command.lower()
        rest = rest.strip()

        if command == "/quit":
            self.running = False
            return
        if command == "/help":
            self.io.notify(
                "Commands: /quit /ping /online /online_games /select N /escape /local MSG /global MSG"
            )
            return
        if command == "/ping":
            self._ping_start_time = time.time()
            self.network.send_packet({"type": "ping"})
            return
        if command == "/online":
            self.network.send_packet({"type": "list_online"})
            return
        if command == "/online_games":
            self.network.send_packet({"type": "list_online_with_games"})
            return
        if command == "/escape":
            self.network.send_packet({"type": "escape", "menu_id": self.current_menu_id})
            return
        if command in ("/local", "/global"):
            if not rest:
                self.io.rejected_action()
                return
            self.network.send_packet(
                {
                    "type": "chat",
                    "convo": "global" if command == "/global" else "local",
                    "message": rest,
                    "language": self.client_options.get("social", {}).get(
                        "chat_input_language", "Other"
                    ),
                }
            )
            return
        if command == "/select":
            if not rest.isdigit():
                self.io.rejected_action()
                return
            selection = int(rest)
            item_id = None
            if 1 <= selection <= len(self.current_menu_items):
                item_id = self.current_menu_items[selection - 1].get("id")
            payload = {
                "type": "menu",
                "menu_id": self.current_menu_id,
                "selection": selection,
            }
            if item_id:
                payload["selection_id"] = item_id
            self.network.send_packet(payload)
            return

        self.io.rejected_action()

    def add_history(self, text: str, buffer_name: str = "misc") -> None:
        self.buffer_system.add_item(buffer_name, text)
        if not self.buffer_system.is_muted(buffer_name):
            self.io.notify(text)

    def on_connection_lost(self):
        self.connected = False
        if self._awaiting_authorization:
            self._authorize_success = False
            self._authorize_event.set()
        self.io.notify("Connection lost.")

    def on_authorize_success(self, packet):
        self.connected = True
        if self._awaiting_authorization:
            self._authorize_success = True
            self._authorize_event.set()
        self.io.notify(f"Authorized as {packet.get('username', '')}.")

    def on_server_speak(self, packet):
        text = packet.get("text", "")
        buffer_name = packet.get("buffer") or "misc"
        if text:
            self.add_history(text, buffer_name)

    def on_server_play_sound(self, packet):
        name = packet.get("name", "")
        played = self.audio_manager.play_sound(
            name,
            volume=int(packet.get("volume", 100)),
            pan=int(packet.get("pan", 0)),
            pitch=int(packet.get("pitch", 100)),
        )
        if not played:
            self.io.notify(f"Sound unavailable: {name}")

    def on_server_play_music(self, packet):
        name = packet.get("name", "")
        played = self.audio_manager.play_music(name, looping=bool(packet.get("looping", True)))
        if not played:
            self.io.notify(f"Music unavailable: {name}")

    def on_server_stop_music(self, packet):
        self.audio_manager.stop_music()

    def on_server_play_ambience(self, packet):
        played = self.audio_manager.play_ambience(
            packet.get("intro"),
            packet.get("loop", ""),
            packet.get("outro"),
        )
        if not played:
            self.io.notify("Ambience unavailable.")

    def on_server_stop_ambience(self, packet):
        self.audio_manager.stop_ambience()

    def on_server_add_playlist(self, packet):
        self.audio_manager.add_playlist(
            playlist_id=packet.get("playlist_id", ""),
            tracks=list(packet.get("tracks", [])),
            audio_type=packet.get("audio_type", "music"),
            shuffle_tracks=bool(packet.get("shuffle_tracks", False)),
            repeats=int(packet.get("repeats", 1)),
            auto_start=bool(packet.get("auto_start", True)),
        )

    def on_server_start_playlist(self, packet):
        self.audio_manager.start_playlist(packet.get("playlist_id", ""))

    def on_server_remove_playlist(self, packet):
        self.audio_manager.remove_playlist(packet.get("playlist_id", ""))

    def on_server_get_playlist_duration(self, packet):
        request_id = packet.get("request_id")
        playlist_id = packet.get("playlist_id")
        self.network.send_packet(
            {
                "type": "playlist_duration_response",
                "request_id": request_id,
                "playlist_id": playlist_id,
                "duration_type": packet.get("duration_type", "total"),
                "duration": 0,
            }
        )

    def on_server_menu(self, packet):
        self.current_menu_id = packet.get("menu_id")
        self.current_menu_items = []

        rendered = []
        for item in packet.get("items", []):
            if isinstance(item, str):
                data = {"text": item, "id": None}
            else:
                data = {"text": item.get("text", ""), "id": item.get("id")}
            self.current_menu_items.append(data)
            rendered.append(data["text"])

        if rendered:
            listing = "; ".join(f"{i+1}. {text}" for i, text in enumerate(rendered))
            self.io.notify(f"Menu {self.current_menu_id}: {listing}")

    def on_server_request_input(self, packet):
        self.pending_input_id = packet.get("input_id")
        prompt = packet.get("prompt", "Input")
        default_value = packet.get("default_value", "")

        response = self.io.request_text(
            prompt,
            default=default_value,
            multiline=packet.get("multiline", False),
            read_only=packet.get("read_only", False),
        )
        if response is None:
            return

        self.network.send_packet(
            {
                "type": "editbox",
                "text": response,
                "input_id": self.pending_input_id,
            }
        )
        self.pending_input_id = None

    def on_server_clear_ui(self, packet):
        self.io.notify("UI cleared.")

    def on_server_game_list(self, packet):
        games = [entry.get("name", "") for entry in packet.get("games", [])]
        if games:
            self.io.notify("Games: " + ", ".join(games))

    def on_server_disconnect(self, packet):
        message = packet.get("message") or "Server requested disconnect."
        self.io.notify(message)
        self.connected = False
        if self._awaiting_authorization:
            self._authorize_success = False
            self._authorize_event.set()
        if not packet.get("reconnect", False):
            return

    def on_update_options_lists(self, packet):
        self.io.notify("Options lists updated.")

    def on_open_client_options(self, packet):
        self.io.notify("Client options dialog requested (not implemented in BTSpeak client).")

    def on_open_server_options(self, packet):
        self.io.notify("Server options dialog requested (not implemented in BTSpeak client).")

    def on_table_create(self, packet):
        self.io.notify(f"Table created by {packet.get('host', '')} for {packet.get('game', '')}.")

    def on_server_pong(self, packet):
        if self._ping_start_time is None:
            return
        elapsed_ms = int((time.time() - self._ping_start_time) * 1000)
        self._ping_start_time = None
        self.io.notify(f"Ping: {elapsed_ms}ms")

    def on_receive_chat(self, packet):
        convo = packet.get("convo", "local")
        sender = packet.get("sender", "")
        message = packet.get("message", "")
        self.add_history(f"[{convo}] {sender}: {message}", "chats")

    def on_server_status(self, packet):
        mode = packet.get("mode", "unknown")
        retry = packet.get("retry_after")
        message = packet.get("message")
        parts = [f"Server status: {mode}"]
        if retry:
            parts.append(f"retry after {retry}s")
        if message:
            parts.append(message)
        self.io.notify(". ".join(parts))

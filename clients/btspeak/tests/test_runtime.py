from __future__ import annotations

import time

from btspeak_client.io_adapter import IOAdapter
from btspeak_client.runtime import BTSpeakClientRuntime
from btspeak_client.network_manager import CertificateInfo


class FakeIO(IOAdapter):
    def __init__(self, *, choices=None, inputs=None):
        self.choices = list(choices or [])
        self.inputs = list(inputs or [])
        self.messages: list[str] = []
        self.rejected = 0
        self.option_history: list[tuple[str, list[str]]] = []
        self.default_history: list[tuple[str, str | None]] = []

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        self.messages.append(text)

    def show_message(self, text: str, *, wait: bool = True) -> None:
        self.messages.append(text)

    def choose(self, prompt, options, *, default_key=None, show_cancel=True):
        assert options
        self.option_history.append((prompt, [option.key for option in options]))
        self.default_history.append((prompt, default_key))
        if self.choices:
            return self.choices.pop(0)
        return default_key or options[0].key

    def request_text(self, prompt, *, default="", password=False, multiline=False, read_only=False):
        if self.inputs:
            return self.inputs.pop(0)
        return None

    def rejected_action(self) -> None:
        self.rejected += 1


class FakeConfigManager:
    def __init__(self):
        self.identities = {
            "identity-1": {
                "identity_id": "identity-1",
                "username": "alice",
                "password": "secret",
                "email": "",
                "notes": "",
            }
        }
        self.servers = {
            "server-1": {
                "server_id": "server-1",
                "name": "Main",
                "host": "localhost",
                "port": 8000,
                "notes": "",
            }
        }
        self.last_identity_id = "identity-1"
        self.last_server_id = "server-1"
        self.profiles = {
            "client_options_defaults": {
                "audio": {"music_volume": 20, "ambience_volume": 20},
                "social": {
                    "mute_global_chat": False,
                    "mute_table_chat": False,
                    "include_language_filters_for_table_chat": False,
                    "chat_input_language": "English",
                    "language_subscriptions": {},
                },
                "interface": {"play_typing_sounds": True},
                "local_table": {"creation_notifications": {}},
            },
            "server_options": {"server-1": {}},
        }
        self.set_option_calls: list[tuple[str, object, str | None, bool]] = []

    def get_all_identities(self):
        return self.identities

    def get_identity_by_id(self, identity_id):
        return self.identities.get(identity_id)

    def get_last_identity_id(self):
        return self.last_identity_id

    def set_last_identity(self, identity_id):
        self.last_identity_id = identity_id

    def add_identity(self, username, password, email="", notes=""):
        identity_id = f"identity-{len(self.identities) + 1}"
        self.identities[identity_id] = {
            "identity_id": identity_id,
            "username": username,
            "password": password,
            "email": email,
            "notes": notes,
        }
        return identity_id

    def delete_identity(self, identity_id):
        self.identities.pop(identity_id, None)

    def get_all_servers(self):
        return self.servers

    def get_last_server_id(self):
        return self.last_server_id

    def set_last_server(self, server_id):
        self.last_server_id = server_id

    def add_server(self, name, host, port, notes=""):
        server_id = f"server-{len(self.servers) + 1}"
        self.servers[server_id] = {
            "server_id": server_id,
            "name": name,
            "host": host,
            "port": port,
            "notes": notes,
        }
        return server_id

    def delete_server(self, server_id):
        self.servers.pop(server_id, None)

    def get_server_url(self, server_id):
        server = self.servers.get(server_id)
        if not server:
            return None
        host = server["host"]
        port = server["port"]
        if "://" in host:
            scheme, host_only = host.split("://", 1)
            return f"{scheme}://{host_only}:{port}"
        return f"ws://{host}:{port}"

    def get_client_options(self, server_id):
        defaults = self.profiles["client_options_defaults"]
        social_defaults = defaults["social"]
        local_defaults = defaults["local_table"]
        audio_defaults = defaults["audio"]
        interface_defaults = defaults["interface"]
        overrides = self.profiles.get("server_options", {}).get(server_id, {})
        social = dict(social_defaults)
        social.update(overrides.get("social", {}))
        local_table = dict(local_defaults)
        local_table.update(overrides.get("local_table", {}))
        audio = dict(audio_defaults)
        audio.update(overrides.get("audio", {}))
        interface = dict(interface_defaults)
        interface.update(overrides.get("interface", {}))
        return {"social": social, "local_table": local_table, "audio": audio, "interface": interface}

    def set_client_option(self, key_path, value, server_id=None, create_mode=False):
        self.set_option_calls.append((key_path, value, server_id, create_mode))
        overrides = self.profiles.setdefault("server_options", {}).setdefault(server_id, {})
        scope = overrides
        parts = key_path.split("/")
        for part in parts[:-1]:
            scope = scope.setdefault(part, {})
        scope[parts[-1]] = value

    def save_profiles(self):
        return None

    def set_trusted_certificate(self, server_id, cert_info):
        return None

    def get_trusted_certificate(self, server_id):
        return None


class FakeNetworkManager:
    def __init__(self, event_handler, **kwargs):
        self.event_handler = event_handler
        self.sent_packets: list[dict] = []
        self.disconnect_calls = 0
        self.connected = True
        self.loop = object()
        self.ws = object()
        self.connect_mode = "success"
        self.prepare_tls_ok = True

    def prepare_tls_if_needed(self, server_url):
        return self.prepare_tls_ok

    def connect(self, server_url, username, password):
        if self.connect_mode == "startup_fail":
            return False
        if self.connect_mode == "auth_fail":
            self.event_handler.on_connection_lost()
            return True

        self.event_handler.on_authorize_success({"type": "authorize_success", "username": username})
        return True

    def send_packet(self, packet):
        self.sent_packets.append(packet)
        return True

    def disconnect(self, wait=False, timeout=3.0):
        self.disconnect_calls += 1


def make_runtime(io: FakeIO):
    network_holder = {}
    config = FakeConfigManager()

    def factory(event_handler, **kwargs):
        manager = FakeNetworkManager(event_handler, **kwargs)
        network_holder["manager"] = manager
        return manager

    runtime = BTSpeakClientRuntime(
        io=io,
        config_manager=config,
        network_factory=factory,
    )
    return runtime, network_holder, config


def test_top_menu_exit_returns_cleanly():
    io = FakeIO(choices=["exit"])
    runtime, holder, _ = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert holder["manager"].disconnect_calls == 1


def test_top_menu_cancel_exits_client():
    io = FakeIO(choices=[None, "exit"])
    runtime, holder, _ = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert holder["manager"].disconnect_calls == 1
    assert io.option_history[0][0] == "Identity menu"
    assert len(io.option_history) == 1


def test_run_connects_and_sends_chat_commands():
    io = FakeIO(
        choices=["select_identity", "identity-1", "connect_server", "server-1", "back", "exit"],
        inputs=["/ping", "hello world", None],
    )
    runtime, holder, _ = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    packets = holder["manager"].sent_packets
    assert packets[0] == {"type": "ping"}
    assert packets[1]["type"] == "chat"
    assert packets[1]["message"] == "hello world"


def test_connect_failure_returns_to_server_menu():
    io = FakeIO(
        choices=["select_identity", "identity-1", "connect_server", "server-1", "back", "exit"],
    )
    runtime, holder, _ = make_runtime(io)
    holder["manager"].connect_mode = "auth_fail"

    rc = runtime.run()

    assert rc == 0
    assert any("Connection failed." in message for message in io.messages)


def test_connect_canceled_when_tls_not_trusted():
    io = FakeIO(
        choices=["select_identity", "identity-1", "connect_server", "server-1", "back", "exit"],
    )
    runtime, holder, _ = make_runtime(io)
    holder["manager"].prepare_tls_ok = False

    rc = runtime.run()

    assert rc == 0
    assert any("Connection canceled." in message for message in io.messages)


def test_add_and_remove_identity_flows():
    io = FakeIO(
        choices=["add_identity", "remove_identity", "identity-2", "yes", "exit"],
        inputs=["bob", "pw", "", ""],
    )
    runtime, _, config = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert "identity-2" not in config.identities


def test_add_identity_io_failure_does_not_crash_runtime():
    class BrokenInputIO(FakeIO):
        def request_text(self, prompt, *, default="", password=False, multiline=False, read_only=False):
            raise RuntimeError("dialog failure")

    io = BrokenInputIO(choices=["add_identity", "exit"])
    runtime, _, _ = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert any(message.startswith("Unable to add identity:") for message in io.messages)


def test_add_identity_baseexception_does_not_crash_runtime():
    class BrokenInputIO(FakeIO):
        def request_text(self, prompt, *, default="", password=False, multiline=False, read_only=False):
            raise KeyboardInterrupt()

    io = BrokenInputIO(choices=["add_identity", "exit"])
    runtime, _, _ = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert any(message.startswith("Unable to add identity:") for message in io.messages)


def test_menu_selection_uses_selection_id_when_available():
    io = FakeIO()
    runtime, holder, _ = make_runtime(io)

    runtime.current_menu_id = "main"
    runtime.current_menu_items = [{"text": "Play", "id": "play"}, {"text": "Exit", "id": "exit"}]
    runtime._handle_user_input("/select 2")

    assert holder["manager"].sent_packets[-1] == {
        "type": "menu",
        "menu_id": "main",
        "selection": 2,
        "selection_id": "exit",
    }


def test_request_input_immediately_returns_editbox():
    io = FakeIO(inputs=["typed value"])
    runtime, holder, _ = make_runtime(io)

    runtime.on_server_request_input(
        {
            "type": "request_input",
            "input_id": "field-1",
            "prompt": "Type something",
            "default_value": "",
            "multiline": False,
            "read_only": False,
        }
    )

    assert holder["manager"].sent_packets[-1] == {
        "type": "editbox",
        "text": "typed value",
        "input_id": "field-1",
    }


def test_request_input_cancel_clears_pending_input():
    io = FakeIO(inputs=[None])
    runtime, holder, _ = make_runtime(io)

    runtime.on_server_request_input(
        {
            "type": "request_input",
            "input_id": "field-1",
            "prompt": "Type something",
            "default_value": "",
            "multiline": False,
            "read_only": False,
        }
    )

    assert runtime.pending_input_id is None
    assert holder["manager"].sent_packets == []


def test_disconnect_packet_does_not_force_app_exit():
    io = FakeIO()
    runtime, _, _ = make_runtime(io)

    runtime.running = True
    runtime.on_server_disconnect({"type": "disconnect", "reconnect": False, "message": "bye"})

    assert runtime.running is True
    assert any("bye" in message for message in io.messages)


def test_sound_packet_calls_audio_manager():
    io = FakeIO()
    runtime, _, _ = make_runtime(io)

    class AudioStub:
        def __init__(self):
            self.calls = []

        def play_sound(self, name, volume=100, pan=0, pitch=100):
            self.calls.append((name, volume, pan, pitch))
            return True

    runtime.audio_manager = AudioStub()
    runtime.on_server_play_sound(
        {"type": "play_sound", "name": "open.ogg", "volume": 80, "pan": 5, "pitch": 110}
    )

    assert runtime.audio_manager.calls == [("open.ogg", 80, 5, 110)]


def test_disconnect_and_stop_audio_helper():
    io = FakeIO()
    runtime, holder, _ = make_runtime(io)

    class AudioStopStub:
        def __init__(self):
            self.calls = 0

        def stop_all_audio(self):
            self.calls += 1

    audio = AudioStopStub()
    runtime.audio_manager = audio
    runtime.connected = True

    runtime._disconnect_and_stop_audio()

    assert runtime.connected is False
    assert holder["manager"].disconnect_calls == 1
    assert audio.calls == 1


def test_session_loop_btspeak_select_command_uses_options_list(monkeypatch):
    io = FakeIO(choices=["menu:1"])
    runtime, holder, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True
    runtime.current_menu_id = "main"
    runtime.current_menu_items = [
        {"text": "Play", "id": "play"},
        {"text": "Back", "id": "back"},
    ]

    import btspeak_client.runtime as runtime_mod

    monkeypatch.setattr(runtime_mod, "BTSpeakIO", FakeIO)

    class AudioStopStub:
        def stop_all_audio(self):
            return None

    runtime.audio_manager = AudioStopStub()

    def fake_sleep(_seconds):
        runtime._menu_refresh_requested = True
        runtime._menu_version += 1
        if io.choices:
            return
        runtime.running = False

    monkeypatch.setattr(time, "sleep", fake_sleep)

    runtime._session_loop()

    assert holder["manager"].sent_packets[0] == {
        "type": "menu",
        "menu_id": "main",
        "selection": 1,
        "selection_id": "play",
    }
    prompts = [prompt for prompt, _ in io.option_history]
    assert "Session options" in prompts
    session_options = [options for prompt, options in io.option_history if prompt == "Session options"]
    assert session_options
    assert "menu:1" in session_options[0]
    assert "client_options" in session_options[0]
    assert "review_buffer" in session_options[0]
    assert "client_commands" in session_options[0]
    assert session_options[0][-1] == "disconnect"


def test_session_menu_hides_disconnect_when_logout_present(monkeypatch):
    io = FakeIO(choices=["menu:1"])
    runtime, _, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True
    runtime.current_menu_id = "main"
    runtime.current_menu_items = [
        {"text": "Play", "id": "play"},
        {"text": "Logout", "id": "logout"},
    ]

    import btspeak_client.runtime as runtime_mod

    monkeypatch.setattr(runtime_mod, "BTSpeakIO", FakeIO)

    def fake_sleep(_seconds):
        runtime._menu_refresh_requested = True
        runtime._menu_version += 1
        if io.choices:
            return
        runtime.running = False

    monkeypatch.setattr(time, "sleep", fake_sleep)

    runtime._session_loop()

    session_options = [options for prompt, options in io.option_history if prompt == "Session options"]
    assert session_options
    assert "disconnect" not in session_options[0]


def test_session_menu_orders_back_before_logout(monkeypatch):
    io = FakeIO(choices=["menu:1"])
    runtime, _, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True
    runtime.current_menu_id = "main"
    runtime.current_menu_items = [
        {"text": "Play", "id": "play"},
        {"text": "Logout", "id": "logout"},
        {"text": "Back", "id": "back"},
    ]

    import btspeak_client.runtime as runtime_mod

    monkeypatch.setattr(runtime_mod, "BTSpeakIO", FakeIO)

    def fake_sleep(_seconds):
        runtime._menu_refresh_requested = True
        runtime._menu_version += 1
        if io.choices:
            return
        runtime.running = False

    monkeypatch.setattr(time, "sleep", fake_sleep)

    runtime._session_loop()

    session_options = [options for prompt, options in io.option_history if prompt == "Session options"]
    assert session_options
    assert session_options[0][-2] == "back"
    assert session_options[0][-1] == "menu:2"


def test_session_menu_defaults_to_previous_selection(monkeypatch):
    io = FakeIO(choices=["menu:2", "menu:2"])
    runtime, _, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True
    runtime.current_menu_id = "main"
    runtime.current_menu_items = [
        {"text": "Play", "id": "play"},
        {"text": "Options", "id": "options"},
    ]

    import btspeak_client.runtime as runtime_mod

    monkeypatch.setattr(runtime_mod, "BTSpeakIO", FakeIO)

    def fake_sleep(_seconds):
        runtime._menu_refresh_requested = True
        runtime._menu_version += 1
        if io.choices:
            return
        runtime.running = False

    monkeypatch.setattr(time, "sleep", fake_sleep)

    runtime._session_loop()

    defaults = [default for prompt, default in io.default_history if prompt == "Session options"]
    assert defaults
    assert defaults[0] == "menu:1"
    assert defaults[-1] == "menu:2"


def test_table_menu_adds_key_help(monkeypatch):
    io = FakeIO(choices=["table_help"])
    runtime, _, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True
    runtime.current_menu_id = "turn_menu"
    runtime.current_menu_items = [{"text": "Start game", "id": "start_game"}]

    import btspeak_client.runtime as runtime_mod

    monkeypatch.setattr(runtime_mod, "BTSpeakIO", FakeIO)

    viewed = []

    def fake_view(title, text):
        viewed.append((title, text))
        runtime.running = False

    io.view_long_text = fake_view

    runtime._session_loop()

    session_options = [options for prompt, options in io.option_history if prompt == "Session options"]
    assert session_options
    assert "table_help" in session_options[0]
    assert viewed


def test_keybind_without_args_shows_help():
    io = FakeIO()
    runtime, _, _ = make_runtime(io)
    shown = []

    def fake_view(title, text):
        shown.append((title, text))

    io.view_long_text = fake_view

    runtime._handle_user_input("/keybind")

    assert shown


def test_session_loop_btspeak_review_buffers_uses_long_view(monkeypatch):
    io = FakeIO(choices=["review_buffer", "chats", "back", "back", "disconnect"])
    runtime, holder, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True
    runtime.current_menu_id = "main"
    runtime.current_menu_items = [{"text": "Play", "id": "play"}]
    runtime.add_history("hello chat", "chats")
    long_views = []

    def capture_long_view(title, text):
        long_views.append((title, text))

    io.view_long_text = capture_long_view
    io.view_paged_text = lambda *args, **kwargs: None

    import btspeak_client.runtime as runtime_mod

    monkeypatch.setattr(runtime_mod, "BTSpeakIO", FakeIO)

    class AudioStopStub:
        def stop_all_audio(self):
            return None

    runtime.audio_manager = AudioStopStub()

    runtime._session_loop()

    assert long_views
    assert holder["manager"].disconnect_calls == 1


def test_session_loop_btspeak_cancel_session_options_disconnects(monkeypatch):
    io = FakeIO(choices=[None, "disconnect"])
    runtime, holder, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True
    runtime.current_menu_items = [{"text": "Play", "id": "play"}]

    import btspeak_client.runtime as runtime_mod

    monkeypatch.setattr(runtime_mod, "BTSpeakIO", FakeIO)

    class AudioStopStub:
        def stop_all_audio(self):
            return None

    runtime.audio_manager = AudioStopStub()
    runtime._session_loop()

    assert runtime.connected is False
    assert holder["manager"].disconnect_calls == 1
    assert any("Session menu unavailable. Staying connected." in message for message in io.messages)


def test_session_loop_console_cancel_disconnects():
    io = FakeIO(inputs=[None])
    runtime, holder, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True

    runtime._session_loop()

    assert runtime.connected is False
    assert holder["manager"].disconnect_calls == 1


def test_select_identity_when_empty_shows_message_and_returns():
    io = FakeIO(choices=["select_identity", "exit"])
    runtime, _, config = make_runtime(io)
    config.identities = {}

    rc = runtime.run()

    assert rc == 0
    assert any("No identities available." in message for message in io.messages)


def test_remove_identity_with_back_does_not_delete():
    io = FakeIO(choices=["remove_identity", "identity-1", "back", "exit"])
    runtime, _, config = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert "identity-1" in config.identities


def test_add_server_invalid_port_keeps_state():
    io = FakeIO(
        choices=["select_identity", "identity-1", "add_server", "back", "exit"],
        inputs=["Server X", "localhost", "abc"],
    )
    runtime, _, config = make_runtime(io)
    before = len(config.servers)

    rc = runtime.run()

    assert rc == 0
    assert len(config.servers) == before
    assert any("Port must be a number." in message for message in io.messages)


def test_add_server_blank_port_rejected():
    io = FakeIO(
        choices=["select_identity", "identity-1", "add_server", "back", "exit"],
        inputs=["Server X", "localhost", ""],
    )
    runtime, _, config = make_runtime(io)
    before = len(config.servers)

    rc = runtime.run()

    assert rc == 0
    assert len(config.servers) == before
    assert any("Port is required." in message for message in io.messages)


def test_add_server_out_of_range_port_rejected():
    io = FakeIO(
        choices=["select_identity", "identity-1", "add_server", "back", "exit"],
        inputs=["Server X", "localhost", "70000"],
    )
    runtime, _, config = make_runtime(io)
    before = len(config.servers)

    rc = runtime.run()

    assert rc == 0
    assert len(config.servers) == before
    assert any("Port must be between 1 and 65535." in message for message in io.messages)


def test_remove_server_confirm_back_keeps_server():
    io = FakeIO(
        choices=["select_identity", "identity-1", "remove_server", "server-1", "back", "back", "exit"]
    )
    runtime, _, config = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert "server-1" in config.servers


def test_remove_server_confirm_yes_deletes_server():
    io = FakeIO(
        choices=["select_identity", "identity-1", "remove_server", "server-1", "yes", "back", "exit"]
    )
    runtime, _, config = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert "server-1" not in config.servers


def test_chat_and_select_input_validation_rejected_count():
    io = FakeIO()
    runtime, _, _ = make_runtime(io)

    runtime._handle_user_input("/local")
    runtime._handle_user_input("/select nope")

    assert io.rejected == 2


def test_unknown_slash_command_passthrough():
    io = FakeIO()
    runtime, holder, _ = make_runtime(io)

    runtime._handle_user_input("/custom foo bar")

    assert holder["manager"].sent_packets[-1] == {
        "type": "slash_command",
        "command": "custom",
        "args": "foo bar",
    }


def test_keybind_command_sends_keybind_with_menu_context():
    io = FakeIO()
    runtime, holder, _ = make_runtime(io)
    runtime.current_menu_id = "turn_menu"
    runtime.current_menu_items = [{"text": "Roll", "id": "roll"}]
    runtime.current_menu_selection_id = "roll"

    runtime._handle_user_input("/keybind f1 ctrl shift")

    assert holder["manager"].sent_packets[-1] == {
        "type": "keybind",
        "key": "f1",
        "control": True,
        "alt": False,
        "shift": True,
        "menu_id": "turn_menu",
        "menu_index": 1,
        "menu_item_id": "roll",
    }


def test_clear_ui_stops_audio_and_removes_playlists():
    io = FakeIO()
    runtime, _, _ = make_runtime(io)

    class AudioStub:
        def __init__(self):
            self.removed = 0
            self.stopped = 0

        def remove_all_playlists(self):
            self.removed += 1

        def stop_all_audio(self):
            self.stopped += 1

    audio = AudioStub()
    runtime.audio_manager = audio
    runtime.current_menu_id = "main"
    runtime.current_menu_items = [{"text": "Play", "id": "play"}]

    runtime.on_server_clear_ui({"type": "clear_ui"})

    assert runtime.current_menu_id is None
    assert runtime.current_menu_items == []
    assert audio.removed == 1
    assert audio.stopped == 1


def test_update_options_lists_updates_profiles_and_sends_client_options():
    io = FakeIO()
    runtime, holder, config = make_runtime(io)
    runtime.connected = True
    runtime.server_id = "server-1"

    runtime.on_update_options_lists(
        {
            "type": "update_options_lists",
            "games": [{"name": "Farkle"}, {"name": "Liar's Dice"}],
            "languages": {"en": "English", "es": "Spanish"},
        }
    )

    creation_defaults = config.profiles["client_options_defaults"]["local_table"]["creation_notifications"]
    assert creation_defaults["Farkle"] is True
    assert creation_defaults["Liar's Dice"] is True
    last_packet = holder["manager"].sent_packets[-1]
    assert last_packet["type"] == "client_options"
    assert "options" in last_packet


def test_receive_chat_respects_global_mute():
    io = FakeIO()
    runtime, _, _ = make_runtime(io)
    runtime.client_options = {
        "social": {
            "mute_global_chat": True,
            "mute_table_chat": False,
            "include_language_filters_for_table_chat": False,
            "chat_input_language": "English",
            "language_subscriptions": {},
        }
    }

    class AudioStub:
        def play_sound(self, *args, **kwargs):
            return True

    runtime.audio_manager = AudioStub()
    runtime.on_receive_chat(
        {
            "type": "chat",
            "convo": "global",
            "sender": "other",
            "message": "hi there",
            "language": "English",
        }
    )

    assert not any("[global] other: hi there" in message for message in io.messages)


def test_pending_request_input_line_sends_editbox_only():
    io = FakeIO()
    runtime, holder, _ = make_runtime(io)
    runtime.pending_input_id = "field-xyz"

    runtime._handle_user_input("typed now")

    assert holder["manager"].sent_packets[-1] == {
        "type": "editbox",
        "text": "typed now",
        "input_id": "field-xyz",
    }


def test_identity_menu_hides_remove_and_select_when_empty():
    io = FakeIO(choices=["exit"])
    runtime, _, config = make_runtime(io)
    config.identities = {}

    rc = runtime.run()

    assert rc == 0
    first_prompt, first_options = io.option_history[0]
    assert first_prompt == "Identity menu"
    assert first_options == ["add_identity", "exit"]


def test_identity_menu_shows_select_first_when_identities_exist():
    io = FakeIO(choices=["exit"])
    runtime, _, _ = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    first_prompt, first_options = io.option_history[0]
    assert first_prompt == "Identity menu"
    assert first_options == ["select_identity", "remove_identity", "add_identity", "exit"]


def test_select_identity_defaults_to_last_identity():
    io = FakeIO(choices=["select_identity", "back", "exit"])
    runtime, _, config = make_runtime(io)
    config.identities["identity-2"] = {
        "identity_id": "identity-2",
        "username": "bob",
        "password": "secret",
        "email": "",
        "notes": "",
    }
    config.last_identity_id = "identity-2"

    rc = runtime.run()

    assert rc == 0
    defaults = [default for prompt, default in io.default_history if prompt == "Select identity"]
    assert defaults and defaults[-1] == "identity-2"


def test_server_menu_hides_remove_and_connect_when_no_servers():
    io = FakeIO(choices=["select_identity", "back", "exit"])
    runtime, _, config = make_runtime(io)
    config.servers = {}

    rc = runtime.run()

    assert rc == 0
    server_prompt, server_options = next(
        entry for entry in io.option_history if entry[0].startswith("Server menu for ")
    )
    assert server_options == ["add_server", "back"]


def test_server_menu_shows_select_server_first_when_servers_exist():
    io = FakeIO(choices=["select_identity", "back", "exit"])
    runtime, _, _ = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    server_prompt, server_options = next(
        entry for entry in io.option_history if entry[0].startswith("Server menu for ")
    )
    assert server_options == ["connect_server", "remove_server", "add_server", "back"]


def test_select_server_defaults_to_last_server():
    io = FakeIO(choices=["select_identity", "connect_server", "back", "back", "exit"])
    runtime, _, config = make_runtime(io)
    config.servers["server-2"] = {
        "server_id": "server-2",
        "name": "Backup",
        "host": "localhost",
        "port": 9000,
        "notes": "",
    }
    config.last_server_id = "server-2"

    rc = runtime.run()

    assert rc == 0
    defaults = [default for prompt, default in io.default_history if prompt == "Connect to which server?"]
    assert defaults and defaults[-1] == "server-2"


def test_select_identity_shows_identity_list_then_enters_server_menu():
    io = FakeIO(choices=["select_identity", "identity-1", "back", "exit"])
    runtime, _, config = make_runtime(io)
    config.identities["identity-2"] = {
        "identity_id": "identity-2",
        "username": "bob",
        "password": "secret",
        "email": "",
        "notes": "",
    }

    rc = runtime.run()

    assert rc == 0
    assert ("Select identity", ["identity-1", "identity-2", "back"]) in io.option_history
    assert any(prompt.startswith("Server menu for ") for prompt, _ in io.option_history)


def test_single_identity_auto_selected():
    io = FakeIO(choices=["select_identity", "back", "exit"])
    runtime, _, config = make_runtime(io)
    config.identities = {
        "identity-1": {
            "identity_id": "identity-1",
            "username": "admin",
            "password": "secret",
            "email": "",
            "notes": "",
        }
    }

    rc = runtime.run()

    assert rc == 0
    prompts = [prompt for prompt, _ in io.option_history]
    assert "Select identity" not in prompts


def test_single_server_auto_selected():
    io = FakeIO(choices=["select_identity", "identity-1", "connect_server", "back", "exit"])
    runtime, _, config = make_runtime(io)
    config.servers = {
        "server-1": {
            "server_id": "server-1",
            "name": "Solo",
            "host": "localhost",
            "port": 8000,
            "notes": "",
        }
    }

    rc = runtime.run()

    assert rc == 0
    prompts = [prompt for prompt, _ in io.option_history]
    assert "Connect to which server?" not in prompts


def test_prompt_trust_decision_uses_io_choose():
    io = FakeIO(choices=["trust"])
    runtime, _, _ = make_runtime(io)
    cert = CertificateInfo(
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

    assert runtime._prompt_trust_decision(cert) is True


def test_set_client_option_updates_config_and_sends_packet():
    io = FakeIO(choices=["exit"])
    runtime, holder, config = make_runtime(io)
    runtime.server_id = "server-1"
    runtime.connected = True

    class AudioStub:
        def __init__(self):
            self.music = []
            self.ambience = []

        def set_music_volume(self, value):
            self.music.append(value)

        def set_ambience_volume(self, value):
            self.ambience.append(value)

    runtime.audio_manager = AudioStub()

    runtime._set_client_option_value(("audio", "music_volume"), 80)

    assert config.set_option_calls[-1] == ("audio/music_volume", 80, "server-1", True)
    last_packet = holder["manager"].sent_packets[-1]
    assert last_packet["type"] == "client_options"
    assert last_packet["options"]["audio"]["music_volume"] == 80
    assert runtime.audio_manager.music[-1] == 80


def test_session_menu_waits_for_new_menu_when_unchanged(monkeypatch):
    class CountingIO(FakeIO):
        def __init__(self, *, choices=None, inputs=None):
            super().__init__(choices=choices, inputs=inputs)
            self.choose_calls = 0

        def choose(self, prompt, options, *, default_key=None, show_cancel=True):
            self.choose_calls += 1
            return super().choose(prompt, options, default_key=default_key, show_cancel=show_cancel)

    import btspeak_client.runtime as runtime_mod

    monkeypatch.setattr(runtime_mod, "BTSpeakIO", CountingIO)

    io = CountingIO(choices=["menu:1"])
    runtime, holder, _ = make_runtime(io)
    runtime.connected = True
    runtime.running = True
    runtime.current_menu_id = "main"
    runtime.current_menu_items = [{"text": "Play", "id": "play"}]
    runtime._menu_version = 1
    runtime._menu_refresh_requested = True

    def fake_sleep(_seconds):
        runtime.running = False

    monkeypatch.setattr(time, "sleep", fake_sleep)

    runtime._session_loop()

    assert io.choose_calls == 1

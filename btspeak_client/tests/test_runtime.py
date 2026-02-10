from __future__ import annotations

from btspeak_client.io_adapter import IOAdapter
from btspeak_client.runtime import BTSpeakClientRuntime


class FakeIO(IOAdapter):
    def __init__(self, *, choices=None, inputs=None):
        self.choices = list(choices or [])
        self.inputs = list(inputs or [])
        self.messages: list[str] = []
        self.rejected = 0
        self.option_history: list[tuple[str, list[str]]] = []

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        self.messages.append(text)

    def choose(self, prompt, options, *, default_key=None):
        assert options
        self.option_history.append((prompt, [option.key for option in options]))
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
        return {"social": {"chat_input_language": "English"}}

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


def test_add_and_remove_identity_flows():
    io = FakeIO(
        choices=["add_identity", "remove_identity", "identity-2", "yes", "exit"],
        inputs=["bob", "pw", "", ""],
    )
    runtime, _, config = make_runtime(io)

    rc = runtime.run()

    assert rc == 0
    assert "identity-2" not in config.identities


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


def test_server_menu_hides_remove_and_connect_when_no_servers():
    io = FakeIO(choices=["select_identity", "identity-1", "back", "exit"])
    runtime, _, config = make_runtime(io)
    config.servers = {}

    rc = runtime.run()

    assert rc == 0
    server_prompt, server_options = next(
        entry for entry in io.option_history if entry[0].startswith("Server menu for ")
    )
    assert server_options == ["add_server", "back"]

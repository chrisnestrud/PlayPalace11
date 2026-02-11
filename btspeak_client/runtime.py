"""Single-loop BTSpeak client runtime."""

from __future__ import annotations

import time
from threading import Event
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
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
        self.current_menu_selection_id: str | None = None
        self.current_menu_position: int | None = None
        self.current_menu_escape_behavior: str = "keybind"
        self.pending_input_id: str | None = None
        self._ping_start_time: float | None = None
        self._last_audio_activity: float = 0.0
        self._last_buffer_choice: str = "all"
        self._menu_version: int = 0
        self._menu_refresh_requested: bool = True
        self._last_menu_choice_by_id: dict[str, str] = {}

        self.client_options: dict = {}
        self.server_options: dict = {}
        self._current_credentials: Credentials | None = None
        self.buffer_system = BufferSystem()
        self.audio_manager = AudioManager()
        for name in ("all", "table", "chats", "activity", "misc"):
            self.buffer_system.create_buffer(name)

        self._debug_log_path = Path.home() / ".playpalace" / "btspeak_client_debug.log"

    def _build_default_io(self) -> IOAdapter:
        try:
            return BTSpeakIO()
        except BaseException:
            return ConsoleIO()

    def _debug_log(self, message: str) -> None:
        try:
            self._debug_log_path.parent.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().isoformat()
            with self._debug_log_path.open("a", encoding="utf-8") as fh:
                fh.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass

    def _safe_notify(self, message: str) -> None:
        try:
            self.io.notify(message)
        except BaseException as exc:
            self._debug_log(f"notify failed: {exc!r}")

    def _safe_message(self, message: str, *, wait: bool = True) -> None:
        try:
            if hasattr(self.io, "show_message"):
                self.io.show_message(message, wait=wait)
            else:
                self.io.notify(message)
        except BaseException as exc:
            self._debug_log(f"show_message failed: {exc!r}")

    def _start_activity(self) -> None:
        try:
            if hasattr(self.io, "start_activity_indicator"):
                self.io.start_activity_indicator()
        except BaseException as exc:
            self._debug_log(f"start activity failed: {exc!r}")

    def _stop_activity(self) -> None:
        try:
            if hasattr(self.io, "stop_activity_indicator"):
                self.io.stop_activity_indicator()
        except BaseException as exc:
            self._debug_log(f"stop activity failed: {exc!r}")

    def _safe_choose(
        self,
        prompt: str,
        options: list[ChoiceOption],
        *,
        default_key: str | None = None,
        show_cancel: bool = True,
    ) -> str | None:
        try:
            choice = self.io.choose(
                prompt, options, default_key=default_key, show_cancel=show_cancel
            )
            self._debug_log(f"choose: prompt={prompt!r} result={choice!r}")
            return choice
        except BaseException as exc:
            self._debug_log(f"choose failed for {prompt!r}: {exc!r}")
            return None

    def _confirm(
        self,
        question: str,
        *,
        default_yes: bool = False,
        yes_label: str = "Yes",
        no_label: str = "No",
    ) -> bool:
        choice = self._safe_choose(
            question,
            [ChoiceOption("yes", yes_label), ChoiceOption("no", no_label)],
            default_key="yes" if default_yes else "no",
        )
        return choice == "yes"

    def _show_instruction_dialog(self, heading: str, instruction: str) -> None:
        self.io.view_long_text(heading, instruction)

    def _mark_audio_activity(self) -> None:
        self._last_audio_activity = time.time()

    @staticmethod
    def _extract_hotkey(label: str) -> str | None:
        for char in label:
            if char.isalnum():
                return char.lower()
        return None

    def _format_menu_choice_options(self) -> list[ChoiceOption]:
        key_counts: dict[str, int] = {}
        for item in self.current_menu_items:
            hotkey = self._extract_hotkey(item.get("text", ""))
            if hotkey:
                key_counts[hotkey] = key_counts.get(hotkey, 0) + 1

        options: list[ChoiceOption] = []
        for index, item in enumerate(self.current_menu_items, start=1):
            text = item.get("text", "")
            hotkey = self._extract_hotkey(text)
            if hotkey and key_counts.get(hotkey, 0) == 1:
                label = f"{text}, {hotkey}"
            else:
                label = text
            options.append(ChoiceOption(f"menu:{index}", label))
        options.append(ChoiceOption("back", "Back"))
        return options

    def _menu_has_logout(self) -> bool:
        for item in self.current_menu_items:
            item_id = str(item.get("id") or "").strip().lower()
            text = str(item.get("text") or "").strip().lower()
            if item_id in {"logout", "log_out", "log-out"}:
                return True
            if "logout" in text or "log out" in text:
                return True
        return False

    def _menu_has_back(self) -> bool:
        for item in self.current_menu_items:
            item_id = str(item.get("id") or "").strip().lower()
            text = str(item.get("text") or "").strip().lower()
            if item_id == "back" or text == "back":
                return True
        return False

    def _is_table_menu(self) -> bool:
        menu_id = (self.current_menu_id or "").lower()
        return "turn_menu" in menu_id or "table_menu" in menu_id

    def _build_key_emulation_help(self) -> str:
        help_lines: list[str] = []
        help_path = Path("/BTSpeak/Help/keyboard-emulation")
        if help_path.exists():
            try:
                for line in help_path.read_text(encoding="utf-8").splitlines():
                    if "Function Key:" in line:
                        help_lines.append(line.strip())
                        break
            except Exception as exc:
                self._debug_log(f"key emulation help read failed: {exc!r}")

        help_lines.append(
            "F-keys: Function Key chord (dots 2-3-5) then letter A for F1 through L for F12."
        )
        help_lines.append("Example: F3 is Function Key chord then letter C.")
        help_lines.append("Escape key: dots 2-6 (low E).")
        help_lines.append("Examples: /keybind b (bot), /keybind f3 (toggle spectator).")
        return "\n".join(help_lines)

    def _show_key_help(self) -> None:
        body = self._build_key_emulation_help()
        self.io.view_long_text("Key emulation help", body)

    def _build_ordered_session_options(self) -> list[ChoiceOption]:
        menu_options = self._format_menu_choice_options()
        back_option = None
        logout_option = None
        for option in list(menu_options):
            if option.key == "back":
                back_option = option
                menu_options.remove(option)
                break
        for option in list(menu_options):
            if option.key.startswith("menu:"):
                index = int(option.key.split(":", 1)[1])
                item = self.current_menu_items[index - 1]
                item_id = str(item.get("id") or "").strip().lower()
                text = str(item.get("text") or "").strip().lower()
                if item_id in {"logout", "log_out", "log-out"} or "logout" in text or "log out" in text:
                    logout_option = option
                    menu_options.remove(option)
                    break

        extras = [
            ChoiceOption("client_options", "Client options, o"),
            ChoiceOption("review_buffer", "Review buffers, b"),
            ChoiceOption("client_commands", "Client commands, c"),
            ChoiceOption("key_help", "Key emulation help, h"),
        ]
        if self._is_table_menu():
            extras.append(ChoiceOption("table_help", "Table key help (H-chord), h"))

        combined = list(menu_options) + extras

        if back_option:
            combined.append(back_option)
        if logout_option:
            combined.append(logout_option)
        elif not self._menu_has_logout():
            combined.append(ChoiceOption("disconnect", "Log out, z"))
        return combined

    @staticmethod
    def _format_choice_options_with_hotkeys(options: list[ChoiceOption]) -> list[ChoiceOption]:
        key_counts: dict[str, int] = {}
        for option in options:
            hotkey = BTSpeakClientRuntime._extract_hotkey(option.label)
            if hotkey:
                key_counts[hotkey] = key_counts.get(hotkey, 0) + 1

        formatted: list[ChoiceOption] = []
        for option in options:
            label = option.label
            hotkey = BTSpeakClientRuntime._extract_hotkey(label)
            if hotkey and key_counts.get(hotkey, 0) == 1:
                label = f"{label}, {hotkey}"
            formatted.append(ChoiceOption(option.key, label))
        return formatted

    def _send_menu_selection(self, selection: int) -> None:
        payload = {
            "type": "menu",
            "menu_id": self.current_menu_id,
            "selection": selection,
        }
        item_id = self.current_menu_items[selection - 1].get("id")
        if item_id:
            payload["selection_id"] = item_id
        self.network.send_packet(payload)

    def _open_client_options_menu(self) -> None:
        if not self.server_id:
            self.io.notify("No server selected.")
            return
        self.client_options = self.config_manager.get_client_options(self.server_id)

        options = [
            ChoiceOption("music_volume", "Music volume, m"),
            ChoiceOption("ambience_volume", "Ambience volume, a"),
            ChoiceOption("typing_sounds", "Typing sounds, t"),
            ChoiceOption("mute_global", "Mute global chat, g"),
            ChoiceOption("mute_table", "Mute table chat, l"),
            ChoiceOption("chat_language", "Chat input language, h"),
            ChoiceOption("back", "Back"),
        ]

        while True:
            choice = self._safe_choose("Client options", options, default_key="back")
            if not choice or choice == "back":
                return

            if choice in ("music_volume", "ambience_volume"):
                label = "Music volume" if choice == "music_volume" else "Ambience volume"
                path = ("audio", "music_volume") if choice == "music_volume" else ("audio", "ambience_volume")
                volume_choice = self._safe_choose(
                    label,
                    [
                        ChoiceOption("0", "Off"),
                        ChoiceOption("10", "10%"),
                        ChoiceOption("20", "20%"),
                        ChoiceOption("40", "40%"),
                        ChoiceOption("60", "60%"),
                        ChoiceOption("80", "80%"),
                        ChoiceOption("100", "100%"),
                        ChoiceOption("back", "Back"),
                    ],
                    default_key="100",
                )
                if not volume_choice or volume_choice == "back":
                    continue
                self._set_client_option_value(path, int(volume_choice))
                self.io.notify("Option updated.")
                continue

            if choice in ("typing_sounds", "mute_global", "mute_table"):
                label_map = {
                    "typing_sounds": "Typing sounds",
                    "mute_global": "Mute global chat",
                    "mute_table": "Mute table chat",
                }
                path_map = {
                    "typing_sounds": ("interface", "play_typing_sounds"),
                    "mute_global": ("social", "mute_global_chat"),
                    "mute_table": ("social", "mute_table_chat"),
                }
                toggle_choice = self._safe_choose(
                    label_map[choice],
                    [
                        ChoiceOption("true", "On"),
                        ChoiceOption("false", "Off"),
                        ChoiceOption("back", "Back"),
                    ],
                    default_key="true",
                )
                if toggle_choice == "back" or not toggle_choice:
                    continue
                self._set_client_option_value(path_map[choice], toggle_choice == "true")
                self.io.notify("Option updated.")
                continue

            if choice == "chat_language":
                social = self.client_options.get("social", {})
                lang_map = social.get("language_subscriptions", {})
                languages = list(lang_map.keys()) if isinstance(lang_map, dict) else []
                if not languages:
                    self.io.notify("No languages are available.")
                    continue
                lang_options = [ChoiceOption(lang, lang) for lang in languages]
                lang_options.append(ChoiceOption("back", "Back"))
                selected = self._safe_choose("Chat input language", lang_options, default_key="back")
                if not selected or selected == "back":
                    continue
                self._set_client_option_value(("social", "chat_input_language"), selected)
                self.io.notify("Option updated.")
                continue

    def _select_server_menu_command(self) -> bool:
        if not self.current_menu_items:
            self.io.notify("No server menu options are currently available.")
            return False

        default_key = None
        if self.current_menu_selection_id:
            for index, item in enumerate(self.current_menu_items, start=1):
                if item.get("id") == self.current_menu_selection_id:
                    default_key = f"menu:{index}"
                    break
        if default_key is None and self.current_menu_position is not None:
            position = self.current_menu_position + 1
            if 1 <= position <= len(self.current_menu_items):
                default_key = f"menu:{position}"

        choice = self._safe_choose(
            "Select a command",
            self._format_menu_choice_options(),
            default_key=default_key,
        )
        if not choice or choice == "back" or not choice.startswith("menu:"):
            return False

        selection = int(choice.split(":", 1)[1])
        payload = {
            "type": "menu",
            "menu_id": self.current_menu_id,
            "selection": selection,
        }
        item_id = self.current_menu_items[selection - 1].get("id")
        if item_id:
            payload["selection_id"] = item_id
        self.network.send_packet(payload)
        return True

    def _review_buffer(self) -> None:
        buffer_order = ["all", "table", "chats", "activity", "misc"]
        buffer_labels = {
            "all": "All",
            "table": "Table",
            "chats": "Chats",
            "activity": "Activity",
            "misc": "Misc",
        }
        shortcut_map = {
            "all": "a",
            "table": "t",
            "chats": "c",
            "activity": "y",
            "misc": "m",
        }
        options = [
            ChoiceOption(key, f"{buffer_labels[key]}, {shortcut_map[key]}")
            for key in buffer_order
        ]
        options.append(ChoiceOption("back", "Back"))
        choice = self._safe_choose(
            "Select buffer to review",
            options,
            default_key=self._last_buffer_choice or "all",
        )
        if not choice or choice == "back":
            return
        self._last_buffer_choice = choice

        try:
            current_index = buffer_order.index(choice)
        except ValueError:
            current_index = 0
        self._review_buffer_ring(buffer_order, buffer_labels, current_index)

    def _review_buffer_ring(
        self,
        buffer_order: list[str],
        buffer_labels: dict[str, str],
        start_index: int,
    ) -> None:
        current_index = start_index
        while True:
            key = buffer_order[current_index]
            items = self.buffer_system.buffers.get(key, [])
            lines = [item.get("text", "") for item in items if item.get("text")]
            if not lines:
                self.io.notify(f"{buffer_labels[key]} buffer is empty.")
            else:
                action = None
                if hasattr(self.io, "view_paged_text"):
                    try:
                        action = self.io.view_paged_text(
                            f"{buffer_labels[key]} buffer",
                            lines,
                            page_size=30,
                        )
                    except BaseException:
                        action = None
                if action == "prev_buffer":
                    current_index = (current_index - 1) % len(buffer_order)
                    continue
                if action == "next_buffer":
                    current_index = (current_index + 1) % len(buffer_order)
                    continue
                if action == "exit":
                    return
                if action is None:
                    self._review_buffer_pages(f"{buffer_labels[key]} buffer", lines)

            choice = self._safe_choose(
                "Buffer navigation",
                [
                    ChoiceOption("prev", "Previous buffer (Dot-7)"),
                    ChoiceOption("next", "Next buffer (Dot-8)"),
                    ChoiceOption("back", "Back (Z-chord)"),
                ],
                default_key="next",
            )
            if not choice or choice == "back":
                return
            if choice == "prev":
                current_index = (current_index - 1) % len(buffer_order)
            elif choice == "next":
                current_index = (current_index + 1) % len(buffer_order)
            else:
                return

    def _review_buffer_pages(self, title: str, lines: list[str], *, page_size: int = 30) -> None:
        if not lines:
            return
        if hasattr(self.io, "view_paged_text"):
            try:
                if self.io.view_paged_text(title, lines, page_size=page_size):
                    return
            except BaseException:
                pass
        total_lines = len(lines)
        total_pages = (total_lines + page_size - 1) // page_size
        page_index = 0
        while True:
            start = page_index * page_size
            end = min(total_lines, start + page_size)
            header = f"{title} (Page {page_index + 1} of {total_pages})"
            body = "\n".join(lines[start:end])
            self.io.view_long_text(header, body)

            options = [ChoiceOption("next", "Next page (Dot-8)"), ChoiceOption("back", "Back (Z-chord)")]
            if page_index > 0:
                options.insert(0, ChoiceOption("prev", "Previous page (Dot-7)"))
            choice = self._safe_choose("Buffer navigation", options, default_key="next")
            if not choice or choice == "back":
                return
            if choice == "next":
                if page_index + 1 >= total_pages:
                    self.io.notify("End of buffer.")
                else:
                    page_index += 1
            elif choice == "prev":
                if page_index == 0:
                    self.io.notify("Start of buffer.")
                else:
                    page_index -= 1
            else:
                return

    def _prompt_trust_decision(self, cert_info: CertificateInfo) -> bool:
        lines = [
            f"Host: {cert_info.host}",
            f"Common name: {cert_info.common_name or '(none)'}",
            f"Subject alt names: {', '.join(cert_info.sans) if cert_info.sans else '(none)'}",
            f"Issuer: {cert_info.issuer or '(unknown)'}",
            f"Valid from: {cert_info.valid_from or '(unknown)'}",
            f"Valid to: {cert_info.valid_to or '(unknown)'}",
            f"Host match: {'yes' if cert_info.matches_host else 'no'}",
            f"Fingerprint: {cert_info.fingerprint}",
        ]
        details = "\n".join(lines)

        try:
            self.io.view_long_text("Untrusted certificate", details)
        except BaseException as exc:
            self._debug_log(f"cert details failed: {exc!r}")
            self._safe_notify(details)

        choice = self._safe_choose(
            "Trust this certificate? Select an option and press Enter.",
            [
                ChoiceOption("trust", "Trust certificate"),
                ChoiceOption("decline", "Decline"),
            ],
            default_key="decline",
        )
        return choice == "trust"

    def run(self) -> int:
        self._debug_log("run: start")
        while self.running:
            identities = self.config_manager.get_all_identities()
            self._debug_log(f"run: identities={len(identities)}")
            if identities:
                menu_options = [
                    ChoiceOption("select_identity", "Select identity"),
                    ChoiceOption("remove_identity", "Remove identity"),
                    ChoiceOption("add_identity", "Add identity"),
                ]
            else:
                menu_options = [ChoiceOption("add_identity", "Add identity")]
            menu_options.append(ChoiceOption("exit", "Exit"))

            if len(identities) == 1:
                identity = next(iter(identities.values()))
                username = identity.get("username", "Identity")
                menu_options[0] = ChoiceOption("select_identity", f"Select identity, {username}")
            menu_options = self._format_choice_options_with_hotkeys(menu_options)

            action = self._safe_choose(
                "Identity menu",
                menu_options,
            )
            self._debug_log(f"run: selected action={action!r}")
            if action is None:
                self.running = False
                break
            if action == "exit":
                self.running = False
                break

            try:
                if action == "add_identity":
                    self._add_identity_flow()
                elif action == "remove_identity":
                    self._remove_identity_flow()
                elif action == "select_identity":
                    identity_id = self._select_identity_flow()
                    if identity_id:
                        self._identity_server_menu(identity_id)
            except BaseException as exc:
                self._debug_log(f"main menu action {action!r} failed: {exc!r}")
                self._safe_notify("Client error. Returning to menu.")

        self.network.disconnect(wait=True)
        self._debug_log("run: stop")
        return 0

    def _add_identity_flow(self):
        self._debug_log("add_identity: start")
        try:
            self._debug_log("add_identity: request username")
            username = (self.io.request_text("Username", default="") or "").strip()
            if not username:
                self._debug_log("add_identity: username missing")
                self._safe_notify("Username is required.")
                return

            self._debug_log("add_identity: request password")
            password = self.io.request_text("Password", default="", password=True) or ""
            if not password:
                self._debug_log("add_identity: password missing")
                self._safe_notify("Password is required.")
                return

            self._debug_log("add_identity: request email")
            email = self.io.request_text("Email (optional)", default="") or ""
            self._debug_log("add_identity: request notes")
            notes = self.io.request_text("Notes (optional)", default="") or ""

            self._debug_log("add_identity: save identity")
            identity_id = self.config_manager.add_identity(
                username=username,
                password=password,
                email=email,
                notes=notes,
            )
        except ValueError as exc:
            self._debug_log(f"add_identity: value error {exc!r}")
            self._safe_notify(str(exc))
            return
        except BaseException as exc:
            self._debug_log(f"add_identity: base exception {exc!r}")
            self._safe_notify(f"Unable to add identity: {exc}")
            return
        self.config_manager.set_last_identity(identity_id)
        self._debug_log(f"add_identity: success {identity_id}")
        self._safe_notify("Identity added.")

    def _remove_identity_flow(self):
        identities = self.config_manager.get_all_identities()
        if not identities:
            self.io.notify("No identities to remove.")
            return

        identity_id = self._select_identity("Remove which identity?")
        if not identity_id:
            return

        self._show_instruction_dialog(
            "Remove identity confirmation",
            "Press Enter on Dismiss, then choose Yes to remove the identity or Back to cancel.",
        )
        if not self._confirm("Remove this identity?", default_yes=False, yes_label="Yes", no_label="Back"):
            return
        self.config_manager.delete_identity(identity_id)
        self.io.notify("Identity removed.")

    def _select_identity(self, prompt: str) -> str | None:
        identities = self.config_manager.get_all_identities()
        if not identities:
            self.io.notify("No identities available.")
            return None
        if len(identities) == 1:
            identity_id, identity = next(iter(identities.items()))
            username = identity.get("username", "Unknown")
            self.io.notify(f"Selected identity: {username}.")
            return identity_id

        default_key = self.config_manager.get_last_identity_id()
        options = []
        for identity_id, identity in identities.items():
            username = identity.get("username", "Unknown")
            email = identity.get("email", "")
            if email:
                label = f"{username} ({email})"
            else:
                label = username
            options.append(ChoiceOption(identity_id, label))
        options.append(ChoiceOption("back", "Back"))

        options = self._format_choice_options_with_hotkeys(options)
        choice = self._safe_choose(prompt, options, default_key=default_key)
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
            if self.connected:
                self._disconnect_and_stop_audio()
            identity = self.config_manager.get_identity_by_id(identity_id)
            if not identity:
                self.io.notify("Identity no longer exists.")
                return

            label = identity.get("username", "Identity")
            servers = self.config_manager.get_all_servers()
            single_server_name = None
            if len(servers) == 1:
                single_server_name = next(iter(servers.values())).get("name", "Server")
            if servers:
                menu_options = [
                    ChoiceOption(
                        "connect_server",
                        f"Select server, {single_server_name}"
                        if single_server_name
                        else "Select server",
                    ),
                    ChoiceOption("remove_server", "Remove server"),
                    ChoiceOption("add_server", "Add server"),
                ]
            else:
                menu_options = [ChoiceOption("add_server", "Add server")]
            menu_options.append(ChoiceOption("back", "Back"))
            menu_options = self._format_choice_options_with_hotkeys(menu_options)

            action = self._safe_choose(
                f"Server menu for {label}",
                menu_options,
            )
            self._debug_log(f"server_menu: identity={identity_id} action={action!r}")
            if action in (None, "back"):
                if self.connected:
                    self._disconnect_and_stop_audio()
                return
            try:
                if action == "add_server":
                    self._add_server_flow()
                elif action == "remove_server":
                    self._remove_server_flow()
                elif action == "connect_server":
                    credentials = self._build_credentials(identity_id)
                    if credentials and self._attempt_connection(credentials):
                        self._session_loop()
            except BaseException as exc:
                self._debug_log(f"server menu action {action!r} failed: {exc!r}")
                self._safe_notify("Client error. Returning to server menu.")

    def _add_server_flow(self):
        name = (self.io.request_text("Server name", default="") or "").strip()
        if not name:
            self.io.notify("Server name is required.")
            return

        host = (self.io.request_text("Host (e.g. wss://host or host)", default="") or "").strip()
        if not host:
            self.io.notify("Host is required.")
            return

        port_value = self.io.request_text("Port (default 8000)", default="8000")
        if port_value is None:
            return
        port_text = port_value.strip()
        if not port_text:
            self.io.notify("Port is required.")
            return
        try:
            port = int(port_text)
        except ValueError:
            self.io.notify("Port must be a number.")
            return
        if not 1 <= port <= 65535:
            self.io.notify("Port must be between 1 and 65535.")
            return

        notes = self.io.request_text("Notes (optional)", default="") or ""
        self.config_manager.add_server(name=name, host=host, port=port, notes=notes)
        self.io.notify("Server added.")

    def _select_server(self, prompt: str) -> str | None:
        servers = self.config_manager.get_all_servers()
        if not servers:
            self.io.notify("No servers available.")
            return None

        default_key = self.config_manager.get_last_server_id()
        options = []
        for server_id, server in servers.items():
            name = server.get("name", "Unknown Server")
            options.append(ChoiceOption(server_id, name))
        options.append(ChoiceOption("back", "Back"))
        options = self._format_choice_options_with_hotkeys(options)
        choice = self._safe_choose(prompt, options, default_key=default_key)
        if not choice or choice == "back":
            return None
        return choice

    def _remove_server_flow(self):
        server_id = self._select_server("Remove which server?")
        self._debug_log(f"remove_server: selected={server_id!r}")
        if not server_id:
            return

        self._show_instruction_dialog(
            "Remove server confirmation",
            "Press Enter on Dismiss, then choose Yes to remove the server or Back to cancel.",
        )
        confirmed = self._confirm("Remove this server?", default_yes=False, yes_label="Yes", no_label="Back")
        self._debug_log(f"remove_server: confirm={confirmed!r}")
        if not confirmed:
            return
        before = len(self.config_manager.get_all_servers())
        self.config_manager.delete_server(server_id)
        after = len(self.config_manager.get_all_servers())
        self._debug_log(f"remove_server: before={before} after={after} removed={before != after}")
        self.io.notify("Server removed.")

    def _build_credentials(self, identity_id: str) -> Credentials | None:
        identity = self.config_manager.get_identity_by_id(identity_id)
        if not identity:
            self.io.notify("Identity no longer exists.")
            return None

        servers = self.config_manager.get_all_servers()
        if not servers:
            self.io.notify("No servers available.")
            return None
        if len(servers) == 1:
            server_id, server = next(iter(servers.items()))
            server_name = server.get("name", "Server")
            self.io.notify(f"Selected server: {server_name}.")
        else:
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
        self._current_credentials = credentials
        self._debug_log(
            "connect: start "
            f"identity={credentials.identity_id} server={credentials.server_id} "
            f"url={credentials.server_url!r} username={credentials.username!r}"
        )
        self.identity_id = credentials.identity_id
        self.server_id = credentials.server_id
        self.client_options = self.config_manager.get_client_options(self.server_id)
        self.connected = False
        self._authorize_success = False
        self._awaiting_authorization = True
        self._authorize_event.clear()

        self._debug_log("connect: prepare_tls_if_needed")
        if not self.network.prepare_tls_if_needed(credentials.server_url):
            self._awaiting_authorization = False
            self._safe_message("Connection canceled.", wait=False)
            self._debug_log("connect: tls preparation canceled")
            return False

        self._debug_log("connect: start network thread")
        started = self.network.connect(
            credentials.server_url,
            credentials.username,
            credentials.password,
        )
        if not started:
            self._awaiting_authorization = False
            self.io.notify("Failed to start network connection.")
            self._debug_log("connect: network start failed")
            return False

        self._safe_message("Connecting...", wait=False)
        self._start_activity()
        self._debug_log("connect: waiting for authorize event")
        authorized = self._authorize_event.wait(timeout=15.0)
        self._stop_activity()
        self._awaiting_authorization = False
        self._debug_log(
            f"connect: authorize event={authorized!r} success={self._authorize_success!r} connected={self.connected!r}"
        )
        if not authorized or not self._authorize_success:
            self.network.disconnect(wait=True)
            self.io.notify("Connection failed.")
            self._debug_log("connect: failed")
            return False
        self._debug_log("connect: success")
        return True

    def _send_client_options_to_server(self) -> None:
        if not self.connected:
            return
        if not self.server_id:
            return
        options = self.config_manager.get_client_options(self.server_id)
        self.client_options = options
        self._apply_audio_options(options)
        self.network.send_packet({"type": "client_options", "options": options})

    @staticmethod
    def _humanize_option_name(name: str) -> str:
        return str(name).replace("_", " ").strip().capitalize()

    @staticmethod
    def _get_nested_mapping(root: dict, path: tuple[str, ...]) -> dict:
        scope = root
        for key in path:
            next_scope = scope.get(key)
            if not isinstance(next_scope, dict):
                return {}
            scope = next_scope
        return scope

    def _set_client_option_value(self, path: tuple[str, ...], value) -> None:
        key_path = "/".join(path)
        if not self.server_id:
            return
        self.config_manager.set_client_option(
            key_path,
            value,
            server_id=self.server_id,
            create_mode=True,
        )
        self.client_options = self.config_manager.get_client_options(self.server_id)
        self._apply_audio_options(self.client_options)
        self._send_client_options_to_server()

    def _apply_audio_options(self, options: dict) -> None:
        audio = options.get("audio") if isinstance(options, dict) else None
        if not isinstance(audio, dict):
            return
        try:
            self.audio_manager.set_music_volume(int(audio.get("music_volume", 100)))
        except Exception as exc:
            self._debug_log(f"audio option apply music failed: {exc!r}")
        try:
            self.audio_manager.set_ambience_volume(int(audio.get("ambience_volume", 100)))
        except Exception as exc:
            self._debug_log(f"audio option apply ambience failed: {exc!r}")

    def _edit_scalar_option(self, label: str, current_value):
        if isinstance(current_value, bool):
            choice = self._safe_choose(
                f"{label} is currently {'on' if current_value else 'off'}.",
                [
                    ChoiceOption("true", "Set on"),
                    ChoiceOption("false", "Set off"),
                    ChoiceOption("back", "Back"),
                ],
                default_key="true" if current_value else "false",
            )
            if choice == "true":
                return True
            if choice == "false":
                return False
            return None

        if isinstance(current_value, int):
            entered = self.io.request_text(label, default=str(current_value))
            if entered is None:
                return None
            entered = entered.strip()
            if not entered:
                return None
            try:
                return int(entered)
            except ValueError:
                self.io.notify("Value must be a number.")
                return None

        entered = self.io.request_text(label, default=str(current_value))
        if entered is None:
            return None
        return entered

    def _edit_mapping_options(
        self,
        *,
        title: str,
        root: dict,
        path: tuple[str, ...],
        editable: bool,
        save_callback: Callable[[tuple[str, ...], object], None] | None = None,
    ) -> None:
        while self.running:
            scope = self._get_nested_mapping(root, path)
            if not scope:
                self.io.notify("No options available.")
                return

            option_entries: list[tuple[str, object]] = list(scope.items())
            options: list[ChoiceOption] = []
            for key, value in option_entries:
                label_name = self._humanize_option_name(key)
                if isinstance(value, dict):
                    label = f"{label_name}"
                else:
                    label = f"{label_name}: {value}"
                options.append(ChoiceOption(key, label))
            options.append(ChoiceOption("back", "Back"))

            choice = self._safe_choose(title, options, default_key="back")
            if not choice or choice == "back":
                return

            selected_value = scope.get(choice)
            if isinstance(selected_value, dict):
                self._edit_mapping_options(
                    title=self._humanize_option_name(choice),
                    root=root,
                    path=path + (choice,),
                    editable=editable,
                    save_callback=save_callback,
                )
                continue

            if not editable or save_callback is None:
                self.io.notify("This option is read-only.")
                continue

            updated = self._edit_scalar_option(self._humanize_option_name(choice), selected_value)
            if updated is None:
                continue
            save_callback(path + (choice,), updated)
            self.io.notify("Option updated.")

    def _open_client_options_editor(self) -> None:
        if not self.server_id:
            self.io.notify("No server selected.")
            return
        self.client_options = self.config_manager.get_client_options(self.server_id)
        self._edit_mapping_options(
            title="Client options",
            root=self.client_options,
            path=(),
            editable=True,
            save_callback=self._set_client_option_value,
        )

    def _open_server_options_viewer(self) -> None:
        if not self.server_options:
            self.io.notify("No server options are available.")
            return
        self._edit_mapping_options(
            title="Server options",
            root=self.server_options,
            path=(),
            editable=False,
            save_callback=None,
        )

    def _update_options_lists(self, packet: dict) -> bool:
        if not self.server_id:
            return False
        profiles = self.config_manager.profiles
        defaults = profiles.setdefault("client_options_defaults", {})
        local_table = defaults.setdefault("local_table", {})
        creation_defaults = local_table.setdefault("creation_notifications", {})
        social_defaults = defaults.setdefault("social", {})
        lang_defaults = social_defaults.setdefault("language_subscriptions", {})

        server_options = profiles.setdefault("server_options", {})
        server_overrides = server_options.setdefault(self.server_id, {})
        server_local = server_overrides.setdefault("local_table", {})
        creation_overrides = server_local.setdefault("creation_notifications", {})
        server_social = server_overrides.setdefault("social", {})
        lang_overrides = server_social.setdefault("language_subscriptions", {})

        changed = False

        games = packet.get("games") or []
        for game in games:
            name = game.get("name") if isinstance(game, dict) else str(game)
            if not name:
                continue
            if name not in creation_defaults:
                creation_defaults[name] = True
                changed = True
            if name not in creation_overrides:
                creation_overrides[name] = True
                changed = True

        languages = packet.get("languages") or {}
        if isinstance(languages, list):
            language_names = [str(code) for code in languages]
        else:
            language_names = [str(name) for name in languages.values()]
        if language_names:
            new_default = {name: lang_defaults.get(name, False) for name in language_names}
            if list(new_default.keys()) != list(lang_defaults.keys()):
                social_defaults["language_subscriptions"] = new_default
                changed = True

            new_override = {name: lang_overrides.get(name, False) for name in language_names}
            if list(new_override.keys()) != list(lang_overrides.keys()):
                server_social["language_subscriptions"] = new_override
                changed = True

        if changed:
            self.config_manager.save_profiles()
        return changed

    def _build_menu_context(self) -> tuple[int | None, str | None]:
        menu_index = None
        menu_item_id = self.current_menu_selection_id

        if menu_item_id:
            for index, item in enumerate(self.current_menu_items, start=1):
                if item.get("id") == menu_item_id:
                    menu_index = index
                    break

        if menu_index is None and self.current_menu_position is not None:
            candidate = self.current_menu_position + 1
            if 1 <= candidate <= len(self.current_menu_items):
                menu_index = candidate
                item_id = self.current_menu_items[candidate - 1].get("id")
                if item_id:
                    menu_item_id = item_id

        return menu_index, menu_item_id

    def _session_loop(self):
        self._safe_message("Connected.", wait=False)
        waiting_announced = False
        last_session_choice: str | None = None
        menu_failures = 0
        last_menu_notice = 0.0
        last_menu_version_shown = -1
        while self.running and self.connected:
            if isinstance(self.io, BTSpeakIO):
                if time.time() - self._last_audio_activity < 2.0:
                    time.sleep(0.05)
                    continue
                if not self.current_menu_items:
                    self._debug_log("session: waiting for server menu (no items)")
                    if not waiting_announced:
                        self._safe_message("Connected. Waiting for server menu options.", wait=False)
                        waiting_announced = True
                    time.sleep(0.05)
                    continue

                waiting_announced = False
                if not self._menu_refresh_requested and self._menu_version == last_menu_version_shown:
                    time.sleep(0.05)
                    continue
                self._debug_log(
                    f"session: opening menu id={self.current_menu_id!r} items={len(self.current_menu_items)}"
                )
                menu_version = self._menu_version
                self._menu_refresh_requested = False
                combined_options = self._build_ordered_session_options()
                default_choice = None
                if self.current_menu_id:
                    default_choice = self._last_menu_choice_by_id.get(self.current_menu_id)
                if default_choice is None:
                    for option in combined_options:
                        if option.key.startswith("menu:"):
                            default_choice = option.key
                            break
                action = self._safe_choose(
                    "Session options",
                    combined_options,
                    default_key=default_choice or last_session_choice,
                    show_cancel=False,
                )
                if action is None:
                    menu_failures += 1
                    self._debug_log(f"session: session menu canceled or failed count={menu_failures}")
                    self._menu_refresh_requested = True
                    now = time.time()
                    if now - last_menu_notice > 2.0:
                        self.io.notify("Session menu unavailable. Staying connected.")
                        last_menu_notice = now
                    time.sleep(0.2)
                    continue
                menu_failures = 0
                if action.startswith("menu:"):
                    last_session_choice = action
                    if self.current_menu_id:
                        self._last_menu_choice_by_id[self.current_menu_id] = action
                    last_menu_version_shown = menu_version
                    selection = int(action.split(":", 1)[1])
                    self._send_menu_selection(selection)
                    continue
                if action == "disconnect":
                    self._debug_log("session: session menu requested disconnect")
                    self._disconnect_and_stop_audio()
                    break
                if action == "review_buffer":
                    last_session_choice = action
                    self._review_buffer()
                    self._menu_refresh_requested = True
                    continue
                if action == "client_options":
                    last_session_choice = action
                    self._open_client_options_menu()
                    self._menu_refresh_requested = True
                    continue
                if action == "client_commands":
                    last_session_choice = action
                    command = self._choose_session_command()
                    if command:
                        self._handle_user_input(command)
                    self._menu_refresh_requested = True
                    continue
                if action == "key_help":
                    last_session_choice = action
                    self._show_key_help()
                    self._menu_refresh_requested = True
                    last_menu_version_shown = menu_version
                    time.sleep(0.2)
                    continue
                if action == "table_help":
                    last_session_choice = action
                    self._show_key_help()
                    self._menu_refresh_requested = True
                    last_menu_version_shown = menu_version
                    time.sleep(0.2)
                    continue

            self.io.notify("Connected. Enter /help for commands.")
            line = self.io.request_text("Message or command", default="")
            if line is None:
                if isinstance(self.io, BTSpeakIO):
                    continue
                self._disconnect_and_stop_audio()
                break
            self._handle_user_input(line)

    def _choose_session_command(self) -> str | None:
        choice = self._safe_choose(
            "Select a client command",
            [
                ChoiceOption("ping", "Ping"),
                ChoiceOption("online", "List online users"),
                ChoiceOption("online_games", "List online users with games"),
                ChoiceOption("escape", "Escape current menu"),
                ChoiceOption("local", "Local chat message"),
                ChoiceOption("global", "Global chat message"),
                ChoiceOption("help", "Help"),
                ChoiceOption("key_help", "Key emulation help"),
                ChoiceOption("quit", "Quit client"),
                ChoiceOption("back", "Back"),
            ],
            default_key="back",
        )
        if choice in (None, "back"):
            return None
        if choice == "key_help":
            self._show_key_help()
            return None
        if choice in ("local", "global"):
            text = self.io.request_text("Message text", default="")
            if not text:
                return None
            return f"/{choice} {text}"
        return f"/{choice}"

    def _disconnect_and_stop_audio(self) -> None:
        self._debug_log("disconnect: stopping network and audio")
        self.network.disconnect(wait=True)
        self.connected = False
        self.current_menu_id = None
        self.current_menu_items = []
        self.current_menu_selection_id = None
        self.current_menu_position = None
        try:
            self.audio_manager.stop_all_audio()
        except Exception:
            self.audio_manager.stop_music()
            self.audio_manager.stop_ambience()

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
                "Commands: /quit /ping /online /online_games /select N /escape /keybind KEY [ctrl alt shift] /keyhelp /local MSG /global MSG"
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
        if command in ("/keybind", "/key"):
            if not rest:
                self._show_key_help()
                return
            parts = [part.lower() for part in rest.split() if part]
            key = parts[0]
            modifiers = set(parts[1:])
            menu_index, menu_item_id = self._build_menu_context()
            payload = {
                "type": "keybind",
                "key": key,
                "control": "ctrl" in modifiers or "control" in modifiers,
                "alt": "alt" in modifiers,
                "shift": "shift" in modifiers,
                "menu_id": self.current_menu_id,
                "menu_index": menu_index,
                "menu_item_id": menu_item_id,
            }
            self.network.send_packet(payload)
            return

        if command.startswith("/"):
            self.network.send_packet(
                {
                    "type": "slash_command",
                    "command": command[1:],
                    "args": rest,
                }
            )
            return
        self.io.rejected_action()

    def add_history(self, text: str, buffer_name: str = "misc") -> None:
        self.buffer_system.add_item(buffer_name, text)
        if not self.buffer_system.is_muted(buffer_name):
            self.io.notify(text)

    def on_connection_lost(self):
        self._debug_log("event: connection_lost")
        self.connected = False
        self.current_menu_id = None
        self.current_menu_items = []
        self.current_menu_selection_id = None
        self.current_menu_position = None
        if self._awaiting_authorization:
            self._authorize_success = False
            self._authorize_event.set()
        self._safe_message("Connection lost.", wait=False)

    def on_authorize_success(self, packet):
        self._debug_log(f"authorize_success: packet={packet!r}")
        self.connected = True
        if self._awaiting_authorization:
            self._authorize_success = True
            self._authorize_event.set()
        self._safe_message(f"Authorized as {packet.get('username', '')}.", wait=False)

    def on_server_speak(self, packet):
        text = packet.get("text", "")
        buffer_name = packet.get("buffer") or "misc"
        if text:
            self._mark_audio_activity()
            self.add_history(text, buffer_name)

    def on_server_play_sound(self, packet):
        name = packet.get("name", "")
        self._mark_audio_activity()
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
        self._mark_audio_activity()
        played = self.audio_manager.play_music(name, looping=bool(packet.get("looping", True)))
        if not played:
            self.io.notify(f"Music unavailable: {name}")

    def on_server_stop_music(self, packet):
        self.audio_manager.stop_music()

    def on_server_play_ambience(self, packet):
        self._mark_audio_activity()
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
        self._debug_log(
            "event: server_menu "
            f"menu_id={packet.get('menu_id')!r} "
            f"items={len(packet.get('items', []) or [])!r} "
            f"selection_id={packet.get('selection_id')!r} "
            f"position={packet.get('position')!r}"
        )
        try:
            labels = []
            for item in packet.get("items", [])[:10]:
                if isinstance(item, str):
                    labels.append(item)
                elif isinstance(item, dict):
                    labels.append(str(item.get("text", "")))
            if labels:
                rendered = ", ".join(labels)
                if len(packet.get("items", [])) > 10:
                    rendered += ", ..."
                self._debug_log(f"event: server_menu items=[{rendered}]")
        except Exception:
            pass
        self.current_menu_id = packet.get("menu_id")
        self.current_menu_items = []
        self.current_menu_selection_id = packet.get("selection_id")
        self.current_menu_position = packet.get("position")
        self.current_menu_escape_behavior = packet.get("escape_behavior", "keybind")
        self._menu_version += 1
        self._menu_refresh_requested = True

        for item in packet.get("items", []):
            if isinstance(item, str):
                data = {"text": item, "id": None}
            else:
                data = {"text": item.get("text", ""), "id": item.get("id")}
            self.current_menu_items.append(data)
        if self.current_menu_items:
            self.io.notify("Server menu updated. Use Select a command.")

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
            self.pending_input_id = None
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
        self.current_menu_id = None
        self.current_menu_items = []
        self.current_menu_selection_id = None
        self.current_menu_position = None
        self.audio_manager.remove_all_playlists()
        self.audio_manager.stop_all_audio()
        self.io.notify("UI cleared.")

    def on_server_game_list(self, packet):
        games = [entry.get("name", "") for entry in packet.get("games", [])]
        if games:
            self.io.notify("Games: " + ", ".join(games))

    def on_server_disconnect(self, packet):
        self._debug_log(f"event: server_disconnect packet={packet!r}")
        message = packet.get("message") or "Server requested disconnect."
        should_reconnect = bool(packet.get("reconnect", False))
        retry_after = packet.get("retry_after")
        return_to_login = bool(packet.get("return_to_login", False))
        status_mode = packet.get("status_mode")
        self._safe_message(message, wait=False)
        self.connected = False
        self.current_menu_id = None
        self.current_menu_items = []
        self.current_menu_selection_id = None
        self.current_menu_position = None
        self.audio_manager.stop_all_audio()
        if self._awaiting_authorization:
            self._authorize_success = False
            self._authorize_event.set()
        if return_to_login:
            self.io.notify("Disconnected. Returning to identity menu.")
            return
        if not should_reconnect or not self._current_credentials:
            return
        delay_seconds = 3
        if retry_after is not None:
            try:
                delay_seconds = max(1, int(retry_after))
            except (TypeError, ValueError):
                delay_seconds = 3
        if status_mode:
            self.io.notify(f"Server status is {status_mode}.")
        self.io.notify(f"Reconnecting in {delay_seconds} seconds...")
        time.sleep(delay_seconds)
        if not self.running:
            return
        self._authorize_success = False
        self._awaiting_authorization = True
        self._authorize_event.clear()
        started = self.network.connect(
            self._current_credentials.server_url,
            self._current_credentials.username,
            self._current_credentials.password,
        )
        if not started:
            self._awaiting_authorization = False
            self.io.notify("Reconnect failed.")
            return
        self.io.notify("Reconnecting...")
        authorized = self._authorize_event.wait(timeout=15.0)
        self._awaiting_authorization = False
        if not authorized or not self._authorize_success:
            self.network.disconnect(wait=True)
            self.io.notify("Reconnect failed.")
            return
        self.io.notify("Reconnected.")

    def on_update_options_lists(self, packet):
        self._update_options_lists(packet)
        self.client_options = self.config_manager.get_client_options(self.server_id)
        self._send_client_options_to_server()
        self._safe_message("Options lists updated.", wait=False)

    def on_open_client_options(self, packet):
        packet_options = packet.get("options")
        if isinstance(packet_options, dict) and packet_options:
            self.client_options = packet_options
        self._open_client_options_editor()
        self._send_client_options_to_server()

    def on_open_server_options(self, packet):
        options = packet.get("options")
        self.server_options = options if isinstance(options, dict) else {}
        self._open_server_options_viewer()

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
        language = packet.get("language", "Other")
        social = self.client_options.get("social", {})
        username = ""
        if self._current_credentials:
            username = self._current_credentials.username
        same_user = bool(sender) and sender == username

        if not same_user:
            input_language = social.get("chat_input_language", "Other")
            include_table_filter = bool(social.get("include_language_filters_for_table_chat", False))
            apply_filter = convo == "global" or (convo == "local" and include_table_filter)
            if apply_filter and language != input_language:
                subscriptions = social.get("language_subscriptions", {})
                if subscriptions and not subscriptions.get(language, False):
                    return

        should_mute = (
            (convo == "global" and bool(social.get("mute_global_chat", False)))
            or (convo == "local" and bool(social.get("mute_table_chat", False)))
        )

        text = f"[{convo}] {sender}: {message}"
        self.buffer_system.add_item("chats", text)
        if should_mute and not same_user:
            return

        sound_name = "chatlocal.ogg" if convo == "local" else "chat.ogg"
        self.audio_manager.play_sound(sound_name)
        if username and username.lower() in message.lower():
            self.audio_manager.play_sound("mention.ogg")
        if not self.buffer_system.is_muted("chats"):
            self.io.notify(text)

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
        if command in ("/keyhelp", "/keys"):
            self._show_key_help()
            return

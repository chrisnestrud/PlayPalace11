"""Input/output adapters for BTSpeak and testable console fallbacks."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from getpass import getpass
from pathlib import Path
from typing import Sequence

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ChoiceOption:
    """Selectable option used by the login/menu prompts."""

    key: str
    label: str


class IOAdapter:
    """Abstract UI surface for runtime prompts and announcements."""

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        raise NotImplementedError

    def notify(self, text: str) -> None:
        self.speak(text)

    def show_message(self, text: str, *, wait: bool = True) -> None:
        self.notify(text)

    def choose(
        self,
        prompt: str,
        options: Sequence[ChoiceOption],
        *,
        default_key: str | None = None,
        show_cancel: bool = True,
    ) -> str | None:
        raise NotImplementedError

    def request_text(
        self,
        prompt: str,
        *,
        default: str = "",
        password: bool = False,
        multiline: bool = False,
        read_only: bool = False,
    ) -> str | None:
        raise NotImplementedError

    def view_long_text(self, title: str, text: str) -> None:
        self.notify(f"{title}\n\n{text}")

    def view_paged_text(self, title: str, lines: Sequence[str], *, page_size: int = 30) -> str | None:
        return None

    def rejected_action(self) -> None:
        return


class ConsoleIO(IOAdapter):
    """Fallback terminal I/O when BTSpeak libraries are unavailable."""

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        print(text)

    def show_message(self, text: str, *, wait: bool = True) -> None:
        print(text)

    def choose(
        self,
        prompt: str,
        options: Sequence[ChoiceOption],
        *,
        default_key: str | None = None,
        show_cancel: bool = True,
    ) -> str | None:
        if not options:
            return None

        print(prompt)
        for index, option in enumerate(options, start=1):
            marker = "*" if option.key == default_key else " "
            print(f"{marker} {index}. {option.label}")

        try:
            if show_cancel:
                raw = input("Select number (blank=default, q=cancel): ").strip()
            else:
                raw = input("Select number (blank=default): ").strip()
        except EOFError:
            return None
        if show_cancel and raw.lower() == "q":
            return None
        if not raw:
            if default_key is not None:
                return default_key
            return options[0].key
        if not raw.isdigit():
            self.rejected_action()
            return None

        selected = int(raw)
        if selected < 1 or selected > len(options):
            self.rejected_action()
            return None
        return options[selected - 1].key

    def request_text(
        self,
        prompt: str,
        *,
        default: str = "",
        password: bool = False,
        multiline: bool = False,
        read_only: bool = False,
    ) -> str | None:
        if read_only:
            self.speak(default)
            return default

        if multiline:
            self.speak(f"{prompt} (finish with a single '.' line)")
            lines: list[str] = []
            while True:
                line = input()
                if line == ".":
                    break
                lines.append(line)
            return "\n".join(lines)

        rendered = f"{prompt}"
        if default:
            rendered = f"{rendered} [{default}]"
        rendered = f"{rendered}: "

        if password:
            try:
                value = getpass(rendered)
            except EOFError:
                return None
        else:
            try:
                value = input(rendered)
            except EOFError:
                return None

        value = value.strip()
        return value if value else default


class BTSpeakIO(IOAdapter):
    """BTSpeak-backed I/O adapter using dialogs and host speech output."""

    def __init__(self):
        from BTSpeak import dialogs, host

        # Ensure BTSpeak helper commands resolve against the BTSpeak installation,
        # not this git repository.
        if hasattr(host, "_repositoryRoot"):
            host._repositoryRoot = "/BTSpeak"

        self._dialogs = dialogs
        self._host = host
        self._use_dialog_commands = False
        self._debug_log_path = Path.home() / ".playpalace" / "btspeak_client_debug.log"
        self._use_dialogs_api = hasattr(self._dialogs, "requestInput")

    def _debug_log(self, message: str) -> None:
        try:
            self._debug_log_path.parent.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().isoformat()
            with self._debug_log_path.open("a", encoding="utf-8") as fh:
                fh.write(f"[{timestamp}] {message}\n")
        except OSError as exc:
            logger.debug("Unable to write BTSpeak debug log: %s", exc)

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        self._host.say(text, immediate=interrupt)

    def show_message(self, text: str, *, wait: bool = True) -> None:
        if hasattr(self._dialogs, "showMessage"):
            try:
                self._dialogs.showMessage(text, wait=wait)
                return
            except BaseException as exc:
                self._debug_log(f"dialog: showMessage failed exc={exc!r}")
        self.notify(text)

    def start_activity_indicator(self) -> None:
        if hasattr(self._dialogs, "startActivityIndicator"):
            try:
                self._dialogs.startActivityIndicator()
            except BaseException as exc:
                self._debug_log(f"dialog: startActivityIndicator failed exc={exc!r}")

    def stop_activity_indicator(self) -> None:
        if hasattr(self._dialogs, "stopActivityIndicator"):
            try:
                self._dialogs.stopActivityIndicator()
            except BaseException as exc:
                self._debug_log(f"dialog: stopActivityIndicator failed exc={exc!r}")

    def choose(
        self,
        prompt: str,
        options: Sequence[ChoiceOption],
        *,
        default_key: str | None = None,
        show_cancel: bool = True,
    ) -> str | None:
        if not options:
            return None

        self._debug_log("dialog: requestChoice via dialogs API")
        labels = [option.label for option in options]
        default_value = None
        if default_key is not None:
            for index, option in enumerate(options, start=1):
                if option.key == default_key:
                    default_value = index
                    break
        try:
            choice = self._dialogs.requestChoice(
                labels,
                message=prompt,
                default=default_value,
                allowEmptyChoice=show_cancel,
                okayLabel="Select",
                cancelLabel="Back" if show_cancel else None,
                showCancelButton=show_cancel,
            )
        except BaseException as exc:
            self._debug_log(f"dialog: requestChoice raised exc={exc!r}")
            return None
        if choice is None:
            self._debug_log("dialog: requestChoice returned None")
            return None
        try:
            index = int(choice.key)
        except (TypeError, ValueError):
            index = None
        if index is not None and 1 <= index <= len(options):
            self._debug_log(f"dialog: requestChoice selected index={index}")
            return options[index - 1].key
        selected_label = getattr(choice, "label", None)
        if not isinstance(selected_label, str):
            self._debug_log("dialog: requestChoice returned non-string label")
            return None
        for option in options:
            if option.label == selected_label:
                self._debug_log(f"dialog: requestChoice selected label={selected_label!r}")
                return option.key
        self._debug_log("dialog: requestChoice selection not matched")
        return None

    def request_text(
        self,
        prompt: str,
        *,
        default: str = "",
        password: bool = False,
        multiline: bool = False,
        read_only: bool = False,
    ) -> str | None:
        if read_only:
            self.speak(default)
            return default

        if self._use_dialogs_api and hasattr(self._dialogs, "requestInput"):
            try:
                value = self._dialogs.requestInput(
                    prompt,
                    password=password,
                    initialText=default or None,
                )
            except BaseException as exc:
                self._debug_log(f"dialog: requestInput failed exc={exc!r}")
                return None
            if value is None:
                return None
            return value if multiline else value.strip()
        return None

    def view_long_text(self, title: str, text: str) -> None:
        if self._use_dialogs_api and hasattr(self._dialogs, "viewLines"):
            try:
                lines = [f"{title}", "", *text.splitlines()]
                self._dialogs.viewLines(lines)
                return
            except BaseException as exc:
                self._debug_log(f"dialog: viewLines failed exc={exc!r}")
                return
        self.notify(f"{title}\n\n{text}")

    def view_paged_text(self, title: str, lines: Sequence[str], *, page_size: int = 30) -> str | None:
        if not hasattr(self._dialogs, "cursesDialog"):
            return None
        if not hasattr(self._host, "say"):
            return None
        if not lines:
            return None
        from BTSpeak import braille
        import curses

        total_lines = len(lines)
        page_index = 0

        def draw_page(stdscr):
            nonlocal page_index
            max_y, max_x = stdscr.getmaxyx()
            usable_lines = max(1, max_y - 2)
            page_len = min(page_size, usable_lines)
            total_pages = (total_lines + page_len - 1) // page_len
            while True:
                start = page_index * page_len
                end = min(total_lines, start + page_len)
                header = (
                    f"{title} (Page {page_index + 1} of {total_pages}) "
                    "Up/Down=Page Dot-1-2-3=First Dot-4-5-6=Last Dot-7=Prev buffer "
                    "Dot-8=Next buffer Z-chord=Exit"
                )
                stdscr.clear()
                stdscr.addstr(0, 0, header[: max_x - 1])
                for idx, line in enumerate(lines[start:end], start=1):
                    if idx >= max_y:
                        break
                    stdscr.addstr(idx, 0, str(line)[: max_x - 1])
                stdscr.refresh()

                key = stdscr.get_wch()
                if key == chr(27):
                    return "exit"
                if key == curses.KEY_UP:
                    if page_index > 0:
                        page_index -= 1
                    continue
                if key == curses.KEY_DOWN:
                    if page_index + 1 < total_pages:
                        page_index += 1
                    continue
                uckey = braille.asciiToUnicodeDots(key)
                if uckey == braille.dotsToUnicode(braille.Dot1 | braille.Dot2 | braille.Dot3):
                    page_index = 0
                    continue
                if uckey == braille.dotsToUnicode(braille.Dot4 | braille.Dot5 | braille.Dot6):
                    page_index = max(0, total_pages - 1)
                    continue
                if uckey == braille.dotsToUnicode(braille.Dot7):
                    return "prev_buffer"
                if uckey == braille.dotsToUnicode(braille.Dot8):
                    return "next_buffer"

        try:
            return self._dialogs.cursesDialog(draw_page)
        except BaseException as exc:
            self._debug_log(f"dialog: paged view failed exc={exc!r}")
            return None

    def rejected_action(self) -> None:
        self._host.playRejectedAction()


__all__ = ["BTSpeakIO", "ChoiceOption", "ConsoleIO", "IOAdapter"]

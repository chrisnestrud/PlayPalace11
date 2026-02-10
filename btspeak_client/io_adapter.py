"""Input/output adapters for BTSpeak and testable console fallbacks."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from getpass import getpass
import tempfile
from pathlib import Path
from typing import Sequence


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

    def choose(
        self,
        prompt: str,
        options: Sequence[ChoiceOption],
        *,
        default_key: str | None = None,
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

    def rejected_action(self) -> None:
        return


class ConsoleIO(IOAdapter):
    """Fallback terminal I/O when BTSpeak libraries are unavailable."""

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        print(text)

    def choose(
        self,
        prompt: str,
        options: Sequence[ChoiceOption],
        *,
        default_key: str | None = None,
    ) -> str | None:
        if not options:
            return None

        print(prompt)
        for index, option in enumerate(options, start=1):
            marker = "*" if option.key == default_key else " "
            print(f"{marker} {index}. {option.label}")

        try:
            raw = input("Select number (blank=default, q=cancel): ").strip()
        except EOFError:
            return None
        if raw.lower() == "q":
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
        self._use_dialog_commands = True

    def speak(self, text: str, *, interrupt: bool = False) -> None:
        self._host.say(text, immediate=interrupt)

    def choose(
        self,
        prompt: str,
        options: Sequence[ChoiceOption],
        *,
        default_key: str | None = None,
    ) -> str | None:
        if not options:
            return None

        if getattr(self, "_use_dialog_commands", False):
            command = [
                "/BTSpeak/bin/request-choice",
                "-m",
                prompt,
                "-O",
                "Select",
                "-C",
                "Cancel",
                "-E",
            ]
            for index, option in enumerate(options, start=1):
                if option.key == default_key:
                    command.extend(["-d", str(index)])
                    break
            command.extend(option.label for option in options)
            try:
                completed = subprocess.run(
                    command,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            except subprocess.TimeoutExpired:
                completed = None
            except BaseException:
                completed = None
            if completed and completed.returncode == 0:
                output = completed.stdout.strip()
                if output:
                    token = output.split(" ", 1)[0]
                    if token == "0":
                        return None
                    if token.isdigit():
                        index = int(token)
                        if 1 <= index <= len(options):
                            return options[index - 1].key

        labels = [option.label for option in options]
        default_label = None
        for option in options:
            if option.key == default_key:
                default_label = option.label
                break
        try:
            choice = self._dialogs.requestChoice(
                labels,
                message=prompt,
                default=default_label,
                allowEmptyChoice=True,
                okayLabel="Select",
                cancelLabel="Cancel",
            )
        except BaseException:
            return None
        if choice is None:
            return None
        try:
            index = int(choice.key)
        except (TypeError, ValueError):
            index = None
        if index is not None and 1 <= index <= len(options):
            return options[index - 1].key
        selected_label = getattr(choice, "label", None)
        if not isinstance(selected_label, str):
            return None
        for option in options:
            if option.label == selected_label:
                return option.key
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

        command = ["/BTSpeak/bin/request-input"]
        if password:
            command.append("-p")
        if default:
            command.extend(["-d", default])
        command.extend(["-O", "Send", "-C", "Cancel", prompt])

        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return None
        except BaseException:
            return None
        if completed.returncode != 0:
            return None
        value = completed.stdout
        if multiline:
            return value
        return value.strip()

    def view_long_text(self, title: str, text: str) -> None:
        fd, path = tempfile.mkstemp(prefix="btspeak_client_", suffix=".txt")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(f"{title}\n\n{text}\n")
            completed = subprocess.run(
                ["/BTSpeak/bin/view-file", str(Path(path))],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if completed.returncode != 0:
                self.notify(f"{title}\n\n{text}")
        except subprocess.TimeoutExpired:
            self.notify(f"{title}\n\n{text}")
        except BaseException:
            self.notify(f"{title}\n\n{text}")
        finally:
            try:
                Path(path).unlink(missing_ok=True)
            except BaseException:
                pass

    def rejected_action(self) -> None:
        self._host.playRejectedAction()


__all__ = ["BTSpeakIO", "ChoiceOption", "ConsoleIO", "IOAdapter"]

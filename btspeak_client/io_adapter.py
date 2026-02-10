"""Input/output adapters for BTSpeak and testable console fallbacks."""

from __future__ import annotations

from dataclasses import dataclass
from getpass import getpass
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

        labels = [option.label for option in options]
        default_label = None
        for option in options:
            if option.key == default_key:
                default_label = option.label
                break

        choice = self._dialogs.requestChoice(
            labels,
            message=prompt,
            default=default_label,
            allowEmptyChoice=True,
            okayLabel="Select",
            cancelLabel="Cancel",
        )
        if choice is None:
            return None

        # Resolve by returned label first for robustness across dialog backends.
        selected_label = getattr(choice, "label", None)
        if isinstance(selected_label, str):
            for option in options:
                if option.label == selected_label:
                    return option.key

        # Fall back to numeric key. Some environments return 0-based indices,
        # others return 1-based indices.
        index = int(choice.key)
        if 0 <= index < len(options):
            return options[index].key
        if 1 <= index <= len(options):
            return options[index - 1].key
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
        value = self._dialogs.requestInput(
            prompt=prompt,
            password=password,
            initialText=default,
            showCancelButton=True,
            okayLabel="Send",
            cancelLabel="Cancel",
            message=prompt,
        )
        if value is None:
            return None
        if read_only:
            self.speak(value)
            return value
        if multiline:
            return value
        return value.strip()

    def rejected_action(self) -> None:
        self._host.playRejectedAction()


__all__ = ["BTSpeakIO", "ChoiceOption", "ConsoleIO", "IOAdapter"]

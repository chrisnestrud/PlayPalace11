"""Mixin for synchronized, paced table announcement timelines."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..games.base import Player
    from ..users.base import User


class TimelineMixin:
    """Schedule and process synchronized speech timelines.

    Expected Game attributes:
        scheduled_timeline_events: list entries
        sound_scheduler_tick: int
        players: list[Player]
        get_user(player) -> User | None
    """

    def schedule_timeline_speech(
        self,
        text: str,
        delay_ticks: int = 0,
        buffer: str = "table",
        *,
        player_ids: list[str] | None = None,
        only_spectators: bool = False,
        include_spectators: bool = True,
        tag: str = "",
    ) -> None:
        target_tick = self.sound_scheduler_tick + max(0, delay_ticks)
        self.scheduled_timeline_events.append(
            [
                target_tick,
                text,
                buffer,
                player_ids if player_ids is not None else [],
                only_spectators,
                include_spectators,
                tag,
            ]
        )

    def cancel_timeline(self, tag: str) -> None:
        if not tag:
            return
        self.scheduled_timeline_events = [
            event for event in self.scheduled_timeline_events if event[6] != tag
        ]

    def process_scheduled_timeline_events(self) -> None:
        current_tick = self.sound_scheduler_tick
        remaining = []
        for event in self.scheduled_timeline_events:
            (
                target_tick,
                text,
                buffer,
                player_ids,
                only_spectators,
                include_spectators,
                _tag,
            ) = event
            if target_tick > current_tick:
                remaining.append(event)
                continue

            ids_filter = set(player_ids) if player_ids else None
            for player in self.players:
                if ids_filter is not None and player.id not in ids_filter:
                    continue
                if only_spectators and not player.is_spectator:
                    continue
                if not include_spectators and player.is_spectator:
                    continue
                user = self.get_user(player)
                if user:
                    user.speak(text, buffer)
        self.scheduled_timeline_events = remaining


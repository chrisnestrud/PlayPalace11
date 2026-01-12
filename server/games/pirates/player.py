"""
Player dataclass for Pirates of the Lost Seas.

Contains player state including position, score, gems, and references to
the leveling system and skill manager.

Inherits from Player which has DataClassJSONMixin, so this class is serializable.
All fields are either primitive types or serializable dataclasses (LevelingSystem).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..base import Player
from .leveling import LevelingSystem

if TYPE_CHECKING:
    from .skills import SkillManager


@dataclass
class PiratesPlayer(Player):
    """
    Player state for Pirates of the Lost Seas.

    Skills are managed via the game's skill_manager dict, not stored on the player.
    Leveling is managed via the _leveling field which is serialized.

    The game object is NEVER stored on this class - it is only passed as a
    parameter to methods. This ensures the player remains serializable.
    """

    position: int = 0
    score: int = 0
    gems: list[int] = field(default_factory=list)

    # Leveling system (serialized - has DataClassJSONMixin)
    _leveling: LevelingSystem = field(default=None)  # type: ignore

    # Skill manager is stored on the game object, not on the player
    # This avoids circular references and keeps the player serializable

    def __post_init__(self):
        """Initialize the leveling system if not set."""
        if self._leveling is None:
            self._leveling = LevelingSystem(user_id=self.id)

    @property
    def leveling(self) -> LevelingSystem:
        """Get the leveling system for this player."""
        return self._leveling

    @property
    def level(self) -> int:
        """Shortcut to get the player's level."""
        return self._leveling.level

    @property
    def xp(self) -> int:
        """Shortcut to get the player's XP."""
        return self._leveling.xp

    def add_gem(self, gem_type: int, gem_value: int) -> None:
        """Add a gem to the player's collection and update score."""
        self.gems.append(gem_type)
        self.score += gem_value

    def remove_gem(self, gem_index: int) -> int | None:
        """Remove and return a gem at the given index, or None if invalid."""
        if 0 <= gem_index < len(self.gems):
            return self.gems.pop(gem_index)
        return None

    def has_gems(self) -> bool:
        """Check if the player has any gems."""
        return len(self.gems) > 0

    def recalculate_score(self, get_gem_value: callable) -> None:
        """Recalculate score from current gems using the provided value function."""
        self.score = sum(get_gem_value(gem) for gem in self.gems)

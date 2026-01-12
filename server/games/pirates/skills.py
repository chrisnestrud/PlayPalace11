"""
Skill System for Pirates of the Lost Seas.

Skills are dataclasses that encapsulate all skill-related state and logic.
This replaces the scattered player variables (sword_active, portal_cooldown, etc.)
with a clean, object-oriented design.

All skill classes inherit from DataClassJSONMixin to ensure serializability.
The skill_type field acts as a discriminator for polymorphic deserialization.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Annotated, Union
import random

from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.config import BaseConfig
from mashumaro.types import Discriminator

if TYPE_CHECKING:
    from .game import PiratesGame
    from .player import PiratesPlayer


@dataclass
class Skill(ABC, DataClassJSONMixin):
    """
    Base class for all skills in Pirates of the Lost Seas.

    Skills encapsulate their own state (cooldowns, active duration, uses)
    and provide methods to check availability and execute actions.

    The game object is NEVER stored - it is only passed as a parameter to methods.
    This ensures the skill remains serializable.
    """

    class Config(BaseConfig):
        discriminator = Discriminator(
            field="skill_type",
            include_subtypes=True,
        )

    user_id: str
    skill_type: str = ""  # Discriminator field - set by each subclass
    name: str = ""
    description: str = ""
    required_level: int = 0

    @abstractmethod
    def can_perform(self, game: "PiratesGame", player: "PiratesPlayer") -> tuple[bool, str | None]:
        """
        Check if this skill can be performed.

        Returns:
            Tuple of (can_perform, reason_if_not).
            If can_perform is False, reason_if_not explains why.
        """
        ...

    @abstractmethod
    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """
        Execute the skill action.

        Returns:
            "end_turn" to end the player's turn, "continue" to keep turn active.
        """
        ...

    def on_turn_start(self, game: "PiratesGame", player: "PiratesPlayer") -> None:
        """Called at the start of the player's turn. Override to update timers."""
        pass

    def get_menu_label(self) -> str:
        """Get the label for the skill menu. Override for dynamic labels."""
        return self.name

    def is_unlocked(self, player: "PiratesPlayer") -> bool:
        """Check if the player's level is high enough for this skill."""
        return player.level >= self.required_level


@dataclass
class CooldownSkill(Skill):
    """Base class for skills with a cooldown."""

    cooldown: int = 0
    max_cooldown: int = 0

    def is_on_cooldown(self) -> bool:
        """Check if the skill is currently on cooldown."""
        return self.cooldown > 0

    def start_cooldown(self) -> None:
        """Start the cooldown timer."""
        self.cooldown = self.max_cooldown

    def tick_cooldown(self) -> None:
        """Reduce cooldown by 1 (called at turn start)."""
        if self.cooldown > 0:
            self.cooldown -= 1

    def on_turn_start(self, game: "PiratesGame", player: "PiratesPlayer") -> None:
        """Tick the cooldown at turn start."""
        self.tick_cooldown()


@dataclass
class BuffSkill(CooldownSkill):
    """Base class for skills that provide a temporary buff."""

    active: int = 0
    duration: int = 0

    def is_active(self) -> bool:
        """Check if the buff is currently active."""
        return self.active > 0

    def activate(self) -> None:
        """Activate the buff and start cooldown."""
        self.active = self.duration
        self.start_cooldown()

    def tick_active(self) -> bool:
        """
        Reduce active duration by 1.

        Returns:
            True if the buff just expired.
        """
        if self.active > 0:
            self.active -= 1
            return self.active == 0
        return False

    def on_turn_start(self, game: "PiratesGame", player: "PiratesPlayer") -> None:
        """Tick both active duration and cooldown at turn start."""
        if self.tick_active():
            game.broadcast_l(
                "pirates-buff-expired",
                player=player.name,
                skill=self.name
            )
        self.tick_cooldown()

    def can_perform(self, game: "PiratesGame", player: "PiratesPlayer") -> tuple[bool, str | None]:
        """Check if the buff skill can be activated."""
        if not self.is_unlocked(player):
            return False, f"Requires level {self.required_level}"
        if self.is_active():
            return False, f"{self.name} is already active ({self.active} turns remaining)"
        if self.is_on_cooldown():
            return False, f"{self.name} is on cooldown ({self.cooldown} turns)"
        return True, None

    def get_menu_label(self) -> str:
        """Get dynamic menu label showing status."""
        if self.is_active():
            return f"{self.name} (active: {self.active} turns)"
        if self.is_on_cooldown():
            return f"{self.name} (cooldown: {self.cooldown} turns)"
        return f"{self.name} (activate)"


# =============================================================================
# Concrete Skill Implementations
# =============================================================================


@dataclass
class CannonballSkill(Skill):
    """
    Cannonball Shot - Attack a player within range.

    Always available from the start.
    """

    def __post_init__(self):
        self.skill_type = "cannonball"
        self.name = "Cannonball Shot"
        self.description = "Fire a cannonball at a player within 5 tiles (10 with Double Devastation)."
        self.required_level = 0

    def can_perform(self, game: "PiratesGame", player: "PiratesPlayer") -> tuple[bool, str | None]:
        """Always available if it's the player's turn."""
        if game.current_player != player:
            return False, "Not your turn"
        return True, None

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Handled by the game's cannonball attack logic."""
        return game.handle_cannonball_attack(player)


@dataclass
class SailorsInstinctSkill(Skill):
    """
    Sailor's Instinct - Show map sector information.

    Unlocked at level 10.
    """

    def __post_init__(self):
        self.skill_type = "instinct"
        self.name = "Sailor's Instinct"
        self.description = "Shows map sector information and charted status."
        self.required_level = 10

    def can_perform(self, game: "PiratesGame", player: "PiratesPlayer") -> tuple[bool, str | None]:
        if not self.is_unlocked(player):
            return False, f"Requires level {self.required_level}"
        return True, None

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Show map information to the player."""
        sound_num = random.randint(1, 2)
        game.play_sound(f"game_pirates/instinct{sound_num}.ogg", volume=60)

        ocean_index = (player.position - 1) // 10
        ocean_name = game.selected_oceans[ocean_index] if ocean_index < len(game.selected_oceans) else "Unknown"

        lines = [
            f"Your position: {player.position} in {ocean_name}",
            "",
            "Map Sectors:"
        ]

        for sector in range(1, 9):
            sector_start = (sector - 1) * 5 + 1
            sector_end = sector * 5
            charted_count = sum(
                1 for i in range(sector_start, sector_end + 1)
                if game.charted_tiles.get(i, False)
            )

            if charted_count == 5:
                status = "Fully charted"
            elif charted_count > 0:
                status = f"Partially charted ({charted_count}/5)"
            else:
                status = "Uncharted"

            lines.append(f"Sector {sector} ({sector_start}-{sector_end}): {status}")

        game.status_box(player, lines)
        return "continue"


@dataclass
class PortalSkill(CooldownSkill):
    """
    Portal - Teleport to an ocean occupied by another player.

    Unlocked at level 25. Cooldown: 3 turns.
    """

    def __post_init__(self):
        self.skill_type = "portal"
        self.name = "Portal"
        self.description = "Teleport to a random position in an ocean occupied by another player."
        self.required_level = 25
        self.max_cooldown = 3

    def can_perform(self, game: "PiratesGame", player: "PiratesPlayer") -> tuple[bool, str | None]:
        if not self.is_unlocked(player):
            return False, f"Requires level {self.required_level}"
        if self.is_on_cooldown():
            return False, f"Portal is on cooldown ({self.cooldown} turns)"
        return True, None

    def get_menu_label(self) -> str:
        if self.is_on_cooldown():
            return f"Portal (cooldown: {self.cooldown} turns)"
        return "Portal (teleport to occupied ocean)"

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Teleport to an ocean with other players."""
        return game.handle_portal(player, self)


@dataclass
class GemSeekerSkill(Skill):
    """
    Gem Seeker - Reveal the location of one uncollected gem.

    Unlocked at level 40. Limited to 3 uses per game.
    """

    uses_remaining: int = 3

    def __post_init__(self):
        self.skill_type = "gem_seeker"
        self.name = "Gem Seeker"
        self.description = "Reveals the location of one uncollected gem. Limited to 3 uses per game."
        self.required_level = 40

    def can_perform(self, game: "PiratesGame", player: "PiratesPlayer") -> tuple[bool, str | None]:
        if not self.is_unlocked(player):
            return False, f"Requires level {self.required_level}"
        if self.uses_remaining <= 0:
            return False, "No uses remaining"
        return True, None

    def get_menu_label(self) -> str:
        if self.uses_remaining <= 0:
            return "Gem Seeker (no uses remaining)"
        return f"Gem Seeker ({self.uses_remaining} uses left)"

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Reveal a gem location."""
        self.uses_remaining -= 1

        sound_num = random.randint(1, 2)
        game.play_sound(f"game_pirates/gemseeker{sound_num}.ogg", volume=60)

        # Find the first uncollected gem
        for pos, gem_type in game.gem_positions.items():
            if gem_type != -1:
                from .gems import GEM_NAMES
                gem_name = GEM_NAMES.get(gem_type, "unknown gem")
                user = game.get_user(player)
                if user:
                    user.speak_l(
                        "pirates-gem-seeker-reveal",
                        gem=gem_name,
                        position=pos,
                        uses=self.uses_remaining
                    )
                break

        return "continue"


@dataclass
class SwordFighterSkill(BuffSkill):
    """
    Sword Fighter - +4 attack bonus for 3 turns.

    Unlocked at level 60. Duration: 3 turns. Cooldown: 8 turns.
    """

    attack_bonus: int = 4

    def __post_init__(self):
        self.skill_type = "sword_fighter"
        self.name = "Sword Fighter"
        self.description = "Grants +4 attack bonus for 3 turns."
        self.required_level = 60
        self.max_cooldown = 8
        self.duration = 3

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Activate the sword fighter buff."""
        self.activate()
        game.play_sound("game_pirates/swordfighter.ogg", volume=60)

        user = game.get_user(player)
        if user:
            user.speak_l("pirates-sword-fighter-activated", turns=self.active)
        game.broadcast_l("pirates-skill-activated", player=player.name, skill=self.name, exclude=player)

        return "end_turn"


@dataclass
class PushSkill(BuffSkill):
    """
    Push - +3 defense bonus for 4 turns.

    Unlocked at level 75. Duration: 4 turns. Cooldown: 8 turns.
    """

    defense_bonus: int = 3

    def __post_init__(self):
        self.skill_type = "push"
        self.name = "Push"
        self.description = "Grants +3 defense bonus for 4 turns."
        self.required_level = 75
        self.max_cooldown = 8
        self.duration = 4

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Activate the push buff."""
        self.activate()
        sound_num = random.randint(1, 2)
        game.play_sound(f"game_pirates/push{sound_num}.ogg", volume=60)

        user = game.get_user(player)
        if user:
            user.speak_l("pirates-push-activated", turns=self.active)
        game.broadcast_l("pirates-skill-activated", player=player.name, skill=self.name, exclude=player)

        return "end_turn"


@dataclass
class SkilledCaptainSkill(BuffSkill):
    """
    Skilled Captain - +2 attack and +2 defense for 4 turns.

    Unlocked at level 90. Duration: 4 turns. Cooldown: 8 turns.
    """

    attack_bonus: int = 2
    defense_bonus: int = 2

    def __post_init__(self):
        self.skill_type = "skilled_captain"
        self.name = "Skilled Captain"
        self.description = "Grants +2 attack and +2 defense for 4 turns."
        self.required_level = 90
        self.max_cooldown = 8
        self.duration = 4

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Activate the skilled captain buff."""
        self.activate()
        game.play_sound("game_pirates/skilledcaptain.ogg", volume=60)

        user = game.get_user(player)
        if user:
            user.speak_l("pirates-skilled-captain-activated", turns=self.active)
        game.broadcast_l("pirates-skill-activated", player=player.name, skill=self.name, exclude=player)

        return "end_turn"


@dataclass
class BattleshipSkill(CooldownSkill):
    """
    Battleship - Fire two cannonballs in one turn.

    Unlocked at level 125. Cooldown: 2 turns.
    """

    def __post_init__(self):
        self.skill_type = "battleship"
        self.name = "Battleship"
        self.description = "Fire two cannonballs in one turn."
        self.required_level = 125
        self.max_cooldown = 2

    def can_perform(self, game: "PiratesGame", player: "PiratesPlayer") -> tuple[bool, str | None]:
        if not self.is_unlocked(player):
            return False, f"Requires level {self.required_level}"
        if self.is_on_cooldown():
            return False, f"Battleship is on cooldown ({self.cooldown} turns)"

        # Check if double devastation is active (incompatible)
        skill_manager = game.get_skill_manager(player)
        if skill_manager:
            dd_skill = skill_manager.get_skill(DoubleDevastationSkill)
            if dd_skill and dd_skill.is_active():
                return False, "Cannot use Battleship while Double Devastation is active"

        # Check if there are targets in range
        targets = game.get_targets_in_range(player)
        if not targets:
            return False, "No targets in range"

        return True, None

    def get_menu_label(self) -> str:
        if self.is_on_cooldown():
            return f"Battleship (cooldown: {self.cooldown} turns)"
        return "Battleship (fire extra shot)"

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Fire two cannonballs."""
        self.start_cooldown()
        return game.handle_battleship(player)


@dataclass
class DoubleDevastationSkill(BuffSkill):
    """
    Double Devastation - Increases cannon range to 10 tiles for 3 turns.

    Unlocked at level 200. Duration: 3 turns. Cooldown: 10 turns.
    """

    range_bonus: int = 5  # Adds 5 to base range of 5

    def __post_init__(self):
        self.skill_type = "double_devastation"
        self.name = "Double Devastation"
        self.description = "Increases cannon range to 10 tiles for 3 turns."
        self.required_level = 200
        self.max_cooldown = 10
        self.duration = 3

    def do_action(self, game: "PiratesGame", player: "PiratesPlayer") -> str:
        """Activate the double devastation buff."""
        self.activate()
        game.play_sound("game_pirates/doubledevastation.ogg", volume=60)

        user = game.get_user(player)
        if user:
            user.speak_l("pirates-double-devastation-activated", turns=self.active)
        game.broadcast_l("pirates-skill-activated", player=player.name, skill=self.name, exclude=player)

        return "end_turn"


# =============================================================================
# Skill Manager
# =============================================================================

# Type alias for all concrete skill types (for polymorphic serialization)
AnySkill = Annotated[
    Union[
        CannonballSkill,
        SailorsInstinctSkill,
        PortalSkill,
        GemSeekerSkill,
        SwordFighterSkill,
        PushSkill,
        SkilledCaptainSkill,
        BattleshipSkill,
        DoubleDevastationSkill,
    ],
    Discriminator(field="skill_type", include_subtypes=True),
]


@dataclass
class SkillManager(DataClassJSONMixin):
    """
    Manages all skills for a player.

    Replaces the scattered skill-related variables on the player object.
    This class is fully serializable via mashumaro.

    The game object is NEVER stored - it is only passed as a parameter to methods.
    """

    user_id: str
    skills: dict[str, AnySkill] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize all skills for this player."""
        if not self.skills:
            self._init_skills()

    def _init_skills(self) -> None:
        """Create all skill instances."""
        self.skills = {
            "cannonball": CannonballSkill(user_id=self.user_id),
            "instinct": SailorsInstinctSkill(user_id=self.user_id),
            "portal": PortalSkill(user_id=self.user_id),
            "gem_seeker": GemSeekerSkill(user_id=self.user_id),
            "sword_fighter": SwordFighterSkill(user_id=self.user_id),
            "push": PushSkill(user_id=self.user_id),
            "skilled_captain": SkilledCaptainSkill(user_id=self.user_id),
            "battleship": BattleshipSkill(user_id=self.user_id),
            "double_devastation": DoubleDevastationSkill(user_id=self.user_id),
        }

    def get_skill(self, skill_type: type) -> Skill | None:
        """Get a skill by its type."""
        for skill in self.skills.values():
            if isinstance(skill, skill_type):
                return skill
        return None

    def get_skill_by_name(self, name: str) -> Skill | None:
        """Get a skill by its internal name."""
        return self.skills.get(name)

    def on_turn_start(self, game: "PiratesGame", player: "PiratesPlayer") -> None:
        """Called at the start of the player's turn to update all skill timers."""
        for skill in self.skills.values():
            skill.on_turn_start(game, player)

    def get_available_skills(self, game: "PiratesGame", player: "PiratesPlayer") -> list[tuple[str, Skill]]:
        """Get list of (name, skill) tuples for skills that are unlocked."""
        result = []
        for name, skill in self.skills.items():
            if skill.is_unlocked(player):
                result.append((name, skill))
        return result

    def get_attack_bonus(self) -> int:
        """Calculate total attack bonus from active buffs."""
        bonus = 0
        sword = self.get_skill(SwordFighterSkill)
        if sword and isinstance(sword, SwordFighterSkill) and sword.is_active():
            bonus += sword.attack_bonus
        captain = self.get_skill(SkilledCaptainSkill)
        if captain and isinstance(captain, SkilledCaptainSkill) and captain.is_active():
            bonus += captain.attack_bonus
        return bonus

    def get_defense_bonus(self) -> int:
        """Calculate total defense bonus from active buffs."""
        bonus = 0
        push = self.get_skill(PushSkill)
        if push and isinstance(push, PushSkill) and push.is_active():
            bonus += push.defense_bonus
        captain = self.get_skill(SkilledCaptainSkill)
        if captain and isinstance(captain, SkilledCaptainSkill) and captain.is_active():
            bonus += captain.defense_bonus
        return bonus

    def get_attack_range(self) -> int:
        """Get the current attack range (base 5, or 10 with Double Devastation)."""
        base_range = 5
        dd = self.get_skill(DoubleDevastationSkill)
        if dd and isinstance(dd, DoubleDevastationSkill) and dd.is_active():
            return base_range + dd.range_bonus
        return base_range

    def is_double_devastation_active(self) -> bool:
        """Check if double devastation buff is active."""
        dd = self.get_skill(DoubleDevastationSkill)
        return dd is not None and isinstance(dd, DoubleDevastationSkill) and dd.is_active()

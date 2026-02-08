"""Hangin' with Friends implementation."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json
import gzip
import math
import random
import string

from ..base import Game, GameOptions, Player
from ..registry import register_game
from ...game_utils.action_guard_mixin import ActionGuardMixin
from ...game_utils.actions import Action, ActionSet, EditboxInput, MenuInput, Visibility
from ...game_utils.bot_helper import BotHelper
from ...game_utils.poker_timer import PokerTurnTimer
from ...game_utils.game_result import GameResult, PlayerResult
from ...game_utils.options import BoolOption, IntOption, MenuOption, option_field
from ...messages.localization import Localization
from ...ui.keybinds import KeybindState

LETTER_SCORES = {
    "E": 1,
    "A": 1,
    "I": 1,
    "O": 1,
    "N": 1,
    "R": 1,
    "T": 1,
    "L": 1,
    "S": 1,
    "U": 1,
    "D": 2,
    "G": 2,
    "B": 3,
    "C": 3,
    "M": 3,
    "P": 3,
    "F": 4,
    "H": 4,
    "V": 4,
    "W": 4,
    "Y": 4,
    "K": 5,
    "J": 8,
    "X": 8,
    "Q": 10,
    "Z": 10,
}

DEFAULT_WORDS = [
    "apple",
    "apron",
    "badge",
    "baker",
    "beach",
    "blaze",
    "board",
    "bonus",
    "brave",
    "brick",
    "bring",
    "cable",
    "candy",
    "chair",
    "chase",
    "clear",
    "cloud",
    "coast",
    "crate",
    "dance",
    "dream",
    "eager",
    "earth",
    "fable",
    "flame",
    "float",
    "focus",
    "frame",
    "friend",
    "frost",
    "globe",
    "grace",
    "grape",
    "green",
    "happy",
    "house",
    "jolly",
    "laugh",
    "light",
    "lucky",
    "magic",
    "maple",
    "melon",
    "metal",
    "music",
    "north",
    "ocean",
    "party",
    "pearl",
    "piano",
    "pilot",
    "planet",
    "plaza",
    "point",
    "power",
    "pride",
    "prize",
    "queen",
    "quick",
    "radio",
    "raven",
    "river",
    "robot",
    "royal",
    "score",
    "shape",
    "shine",
    "shore",
    "smile",
    "spark",
    "spice",
    "spoon",
    "sport",
    "sprout",
    "stack",
    "stone",
    "story",
    "storm",
    "sugar",
    "sunny",
    "swing",
    "table",
    "tiger",
    "toast",
    "track",
    "travel",
    "vivid",
    "voice",
    "water",
    "whale",
    "wheat",
    "zebra",
]

# Weighted rack pool (roughly English frequency).
LETTER_POOL = (
    "EEEEEEEEEEEE"
    "AAAAAAAAA"
    "IIIIIIIII"
    "OOOOOOOO"
    "NNNNNN"
    "RRRRRR"
    "TTTTTT"
    "LLLL"
    "SSSS"
    "UUUU"
    "DDDD"
    "GGG"
    "BBCCMMPP"
    "FFHHVVWWYY"
    "K"
    "JX"
    "QZ"
)

BOT_DIFFICULTY_CHOICES = ["easy", "medium", "hard", "extreme"]
BOT_DIFFICULTY_LABELS = {
    "easy": "hwf-bot-difficulty-easy",
    "medium": "hwf-bot-difficulty-medium",
    "hard": "hwf-bot-difficulty-hard",
    "extreme": "hwf-bot-difficulty-extreme",
}
DICTIONARY_MODE_CHOICES = ["strict", "rack-only", "off"]
DICTIONARY_MODE_LABELS = {
    "strict": "hwf-dictionary-mode-strict",
    "rack-only": "hwf-dictionary-mode-rack-only",
    "off": "hwf-dictionary-mode-off",
}
BOT_GUESS_AGGRESSION_CHOICES = ["safe", "balanced", "risky"]
BOT_GUESS_AGGRESSION_LABELS = {
    "safe": "hwf-bot-guess-safe",
    "balanced": "hwf-bot-guess-balanced",
    "risky": "hwf-bot-guess-risky",
}
PACING_PROFILE_CHOICES = ["fast", "normal", "slow"]
PACING_PROFILE_LABELS = {
    "fast": "hwf-pacing-fast",
    "normal": "hwf-pacing-normal",
    "slow": "hwf-pacing-slow",
}

WORD_LIST_CHOICES = ["words", "american-english-huge"]
WORD_LIST_LABELS = {
    "words": "hwf-word-list-words",
    "american-english-huge": "hwf-word-list-american-english-huge",
}

PAIRING_STRATEGY_CHOICES = [
    "winner_fair",
    "round_robin",
    "weighted_fair",
    "winner_cap",
    "host_queue",
    "performance",
]
PAIRING_STRATEGY_LABELS = {
    "winner_fair": "hwf-pairing-winner-fair",
    "round_robin": "hwf-pairing-round-robin",
    "weighted_fair": "hwf-pairing-weighted-fair",
    "winner_cap": "hwf-pairing-winner-cap",
    "host_queue": "hwf-pairing-host-queue",
    "performance": "hwf-pairing-performance",
}
WORD_LIST_FILES = {
    "words": "words.txt.gz",
    "american-english-huge": "american-english-huge.txt.gz",
}

SOUNDS = {
    "lava": "game_hangin_with_friends/bg_lava5.ogg",
    "click": "game_hangin_with_friends/click.ogg",
    "music": "game_hangin_with_friends/music_lavascene1.ogg",
    "avatar": "game_hangin_with_friends/sfx_avatarpicker3.ogg",
    "balloon": "game_hangin_with_friends/sfx_balloonflyoff3_250ms.ogg",
    "shuffle": "game_hangin_with_friends/sfx_bloopshuffle5.ogg",
    "buy_points": "game_hangin_with_friends/sfx_buypoints1.ogg",
    "click2": "game_hangin_with_friends/sfx_click2.ogg",
    "drop": "game_hangin_with_friends/sfx_dropbloop.ogg",
    "enter_wheel": "game_hangin_with_friends/sfx_entermissions.ogg",
    "lose": "game_hangin_with_friends/sfx_gamelost1.ogg",
    "win": "game_hangin_with_friends/sfx_gamewon1.ogg",
    "history_correct": "game_hangin_with_friends/sfx_historycorrect1.ogg",
    "history_incorrect": "game_hangin_with_friends/sfx_historyincorrect1.ogg",
    "level_up": "game_hangin_with_friends/sfx_levelup1.ogg",
    "level_up_missions": "game_hangin_with_friends/sfx_levelupmissions.ogg",
    "lifeline_bounce": "game_hangin_with_friends/sfx_lifeline_bounce.ogg",
    "lifeline_slide": "game_hangin_with_friends/sfx_lifeline_slide.ogg",
    "menu_close": "game_hangin_with_friends/sfx_menuclose3.ogg",
    "menu_open": "game_hangin_with_friends/sfx_menuopen3.ogg",
    "popup": "game_hangin_with_friends/sfx_missioncompletepopup.ogg",
    "multiplier": "game_hangin_with_friends/sfx_multiplybadge4_1s.ogg",
    "pickup": "game_hangin_with_friends/sfx_pickupbloop1.ogg",
    "roulette": "game_hangin_with_friends/sfx_roulette4.ogg",
    "roulette_ping": "game_hangin_with_friends/sfx_roulette4_ping.ogg",
    "score_flyup": "game_hangin_with_friends/sfx_scoreflyup5_pointscharge.ogg",
    "submit_invalid": "game_hangin_with_friends/sfx_submitwordinvalid6.ogg",
    "submit_valid": "game_hangin_with_friends/sfx_submitwordvalid4_3.ogg",
    "use_lifeline": "game_hangin_with_friends/sfx_uselifeline1.ogg",
}

CORRECT_SEQUENCE_SOUNDS = [
    "game_hangin_with_friends/sfx_correctsequence1_1.ogg",
    "game_hangin_with_friends/sfx_correctsequence1_2.ogg",
    "game_hangin_with_friends/sfx_correctsequence1_3.ogg",
    "game_hangin_with_friends/sfx_correctsequence1_4.ogg",
    "game_hangin_with_friends/sfx_correctsequence1_5.ogg",
    "game_hangin_with_friends/sfx_correctsequence1_6.ogg",
    "game_hangin_with_friends/sfx_correctsequence1_7.ogg",
    "game_hangin_with_friends/sfx_correctsequence1_8.ogg",
]

INCORRECT_SEQUENCE_SOUNDS = [
    "game_hangin_with_friends/sfx_incorrectsequence1_1.ogg",
    "game_hangin_with_friends/sfx_incorrectsequence1_2.ogg",
    "game_hangin_with_friends/sfx_incorrectsequence1_3.ogg",
    "game_hangin_with_friends/sfx_incorrectsequence1_4.ogg",
    "game_hangin_with_friends/sfx_incorrectsequence1_5.ogg",
    "game_hangin_with_friends/sfx_incorrectsequence1_6.ogg",
    "game_hangin_with_friends/sfx_incorrectsequence1_7.ogg",
    "game_hangin_with_friends/sfx_incorrectsequence1_8noballoon.ogg",
]

WHEEL_OUTCOMES = [
    "coin_bonus",
    "extra_guess",
    "fewer_guess",
    "double_points",
    "lifeline_reveal",
    "lifeline_remove",
    "lifeline_retry",
    "nothing",
]

VOWELS = {"a", "e", "i", "o", "u"}
MODIFIER_ORDER = ("double_letter", "triple_letter", "double_word", "triple_word")
MODIFIER_LABELS = {
    "double_letter": "double letter",
    "triple_letter": "triple letter",
    "double_word": "double word",
    "triple_word": "triple word",
}
PACING_TICKS = {
    "fast": {
        "turn_transition": 8,
        "board_token_step": 5,
        "post_board_pause": 6,
        "guess_result_pause": 4,
        "round_end_pause": 10,
    },
    "normal": {
        "turn_transition": 10,
        "board_token_step": 6,
        "post_board_pause": 8,
        "guess_result_pause": 6,
        "round_end_pause": 12,
    },
    "slow": {
        "turn_transition": 13,
        "board_token_step": 8,
        "post_board_pause": 10,
        "guess_result_pause": 8,
        "round_end_pause": 16,
    },
}


@dataclass
class HanginWithFriendsPlayer(Player):
    """Player state for Hangin' with Friends."""

    balloons_remaining: int = 5
    score: int = 0
    coins: int = 0
    level: int = 1
    correct_streak: int = 0
    wrong_streak: int = 0
    lifeline_reveal: int = 0
    lifeline_remove: int = 0
    lifeline_retry: int = 0
    retry_shield_active: bool = False


@dataclass
class HanginWithFriendsOptions(GameOptions):
    """Config options for Hangin' with Friends."""

    starting_balloons: int = option_field(
        IntOption(
            default=5,
            min_val=1,
            max_val=10,
            value_key="count",
            label="hwf-set-starting-balloons",
            prompt="hwf-enter-starting-balloons",
            change_msg="hwf-option-changed-starting-balloons",
        )
    )
    rack_size: int = option_field(
        IntOption(
            default=12,
            min_val=8,
            max_val=20,
            value_key="count",
            label="hwf-set-rack-size",
            prompt="hwf-enter-rack-size",
            change_msg="hwf-option-changed-rack-size",
        )
    )
    min_word_length: int = option_field(
        IntOption(
            default=3,
            min_val=2,
            max_val=8,
            value_key="count",
            label="hwf-set-min-word-length",
            prompt="hwf-enter-min-word-length",
            change_msg="hwf-option-changed-min-word-length",
        )
    )
    max_word_length: int = option_field(
        IntOption(
            default=8,
            min_val=3,
            max_val=12,
            value_key="count",
            label="hwf-set-max-word-length",
            prompt="hwf-enter-max-word-length",
            change_msg="hwf-option-changed-max-word-length",
        )
    )
    base_wrong_guesses: int = option_field(
        IntOption(
            default=2,
            min_val=0,
            max_val=10,
            value_key="count",
            label="hwf-set-base-wrong-guesses",
            prompt="hwf-enter-base-wrong-guesses",
            change_msg="hwf-option-changed-base-wrong-guesses",
        )
    )
    word_list: str = option_field(
        MenuOption(
            default="words",
            choices=WORD_LIST_CHOICES,
            value_key="mode",
            label="hwf-set-word-list",
            prompt="hwf-select-word-list",
            change_msg="hwf-option-changed-word-list",
            choice_labels=WORD_LIST_LABELS,
        )
    )
    max_rounds: int = option_field(
        IntOption(
            default=0,
            min_val=0,
            max_val=500,
            value_key="count",
            label="hwf-set-max-rounds",
            prompt="hwf-enter-max-rounds",
            change_msg="hwf-option-changed-max-rounds",
        )
    )
    max_score: int = option_field(
        IntOption(
            default=0,
            min_val=0,
            max_val=500,
            value_key="score",
            label="hwf-set-max-score",
            prompt="hwf-enter-max-score",
            change_msg="hwf-option-changed-max-score",
        )
    )
    round_timer_seconds: int = option_field(
        IntOption(
            default=0,
            min_val=0,
            max_val=600,
            value_key="seconds",
            label="hwf-set-round-timer",
            prompt="hwf-enter-round-timer",
            change_msg="hwf-option-changed-round-timer",
        )
    )
    pairing_strategy: str = option_field(
        MenuOption(
            default="winner_fair",
            choices=PAIRING_STRATEGY_CHOICES,
            value_key="mode",
            label="hwf-set-pairing-strategy",
            prompt="hwf-select-pairing-strategy",
            change_msg="hwf-option-changed-pairing-strategy",
            choice_labels=PAIRING_STRATEGY_LABELS,
        )
    )
    default_bot_difficulty: str = option_field(
        MenuOption(
            default="medium",
            choices=BOT_DIFFICULTY_CHOICES,
            value_key="mode",
            label="hwf-set-default-bot-difficulty",
            prompt="hwf-select-default-bot-difficulty",
            change_msg="hwf-option-changed-default-bot-difficulty",
            choice_labels=BOT_DIFFICULTY_LABELS,
        )
    )
    dictionary_mode: str = option_field(
        MenuOption(
            default="rack-only",
            choices=DICTIONARY_MODE_CHOICES,
            value_key="mode",
            label="hwf-set-dictionary-mode",
            prompt="hwf-select-dictionary-mode",
            change_msg="hwf-option-changed-dictionary-mode",
            choice_labels=DICTIONARY_MODE_LABELS,
        )
    )
    spectators_see_all_actions: bool = option_field(
        BoolOption(
            default=True,
            value_key="enabled",
            label="hwf-toggle-spectators-see-all-actions",
            change_msg="hwf-option-changed-spectators-see-all-actions",
        )
    )
    bot_guess_aggression: str = option_field(
        MenuOption(
            default="balanced",
            choices=BOT_GUESS_AGGRESSION_CHOICES,
            value_key="mode",
            label="hwf-set-bot-guess-aggression",
            prompt="hwf-select-bot-guess-aggression",
            change_msg="hwf-option-changed-bot-guess-aggression",
            choice_labels=BOT_GUESS_AGGRESSION_LABELS,
        )
    )
    pacing_profile: str = option_field(
        MenuOption(
            default="normal",
            choices=PACING_PROFILE_CHOICES,
            value_key="mode",
            label="hwf-set-pacing-profile",
            prompt="hwf-select-pacing-profile",
            change_msg="hwf-option-changed-pacing-profile",
            choice_labels=PACING_PROFILE_LABELS,
        )
    )


@dataclass
@register_game
class HanginWithFriendsGame(ActionGuardMixin, Game):
    """Turn-based Hangman variant where players alternate setter/guesser roles."""

    players: list[HanginWithFriendsPlayer] = field(default_factory=list)
    options: HanginWithFriendsOptions = field(default_factory=HanginWithFriendsOptions)

    phase: str = "lobby"  # lobby, choose_word, guessing, round_end, game_end
    setter_id: str = ""
    guesser_id: str = ""
    tile_rack: list[str] = field(default_factory=list)
    secret_word: str = ""
    masked_word: str = ""
    guessed_letters: list[str] = field(default_factory=list)
    wrong_guesses: int = 0
    max_wrong_guesses: int = 0
    rng_seed: int = 0
    bot_difficulties: dict[str, str] = field(default_factory=dict)
    wheel_result: str = ""
    round_points_multiplier: int = 1
    lava_next_tick: int = 0
    participant_ids: list[str] = field(default_factory=list)
    board_modifiers: dict[int, str] = field(default_factory=dict)
    round_resume_tick: int = 0
    last_match_end_message: str = ""
    last_eliminated_names: list[str] = field(default_factory=list)
    last_round_winner_id: str = ""
    last_played_round: dict[str, int] = field(default_factory=dict)
    has_played_ids: list[str] = field(default_factory=list)
    round_robin_index: int = 0
    host_queue_index: int = 0
    winner_streak_id: str = ""
    winner_streak_count: int = 0
    timer: PokerTurnTimer = field(default_factory=PokerTurnTimer)
    timer_warning_played: bool = False

    def __post_init__(self):
        super().__post_init__()
        self._dictionary_words: tuple[str, ...] = tuple(DEFAULT_WORDS)
        self._dictionary_loaded: bool = False
        self._modifier_chances_by_length: dict[int, dict[str, float]] = {}
        self._load_modifier_chances()

    def rebuild_runtime_state(self) -> None:
        """Rebuild runtime-only state after load."""
        self._dictionary_words = tuple(DEFAULT_WORDS)
        self._dictionary_loaded = False
        self._modifier_chances_by_length = {}
        self._load_modifier_chances()

    @classmethod
    def get_name(cls) -> str:
        return "Hangin' with Friends"

    @classmethod
    def get_type(cls) -> str:
        return "hangin_with_friends"

    @classmethod
    def get_category(cls) -> str:
        return "category-word-games"

    @classmethod
    def get_min_players(cls) -> int:
        return 1

    @classmethod
    def get_max_players(cls) -> int:
        return 8

    def create_player(
        self, player_id: str, name: str, is_bot: bool = False
    ) -> HanginWithFriendsPlayer:
        return HanginWithFriendsPlayer(id=player_id, name=name, is_bot=is_bot)

    def create_turn_action_set(self, player: HanginWithFriendsPlayer) -> ActionSet:
        action_set = ActionSet(name="turn")

        action_set.add(
            Action(
                id="choose_word",
                label="Choose word",
                handler="_action_choose_word",
                is_enabled="_is_choose_word_enabled",
                is_hidden="_is_choose_word_hidden",
                input_request=EditboxInput(
                    prompt="hwf-prompt-enter-word",
                    bot_input="_bot_choose_word_input",
                ),
            )
        )

        for letter in string.ascii_lowercase:
            action_set.add(
                Action(
                    id=f"guess_letter_{letter}",
                    label=f"Guess {letter.upper()}",
                    handler="_action_guess_letter",
                    is_enabled="_is_guess_letter_enabled",
                    is_hidden="_is_guess_letter_hidden",
                    get_label="_get_guess_letter_label",
                )
            )

        action_set.add(
            Action(
                id="lifeline_reveal",
                label="Use reveal lifeline",
                handler="_action_lifeline_reveal",
                is_enabled="_is_lifeline_reveal_enabled",
                is_hidden="_is_lifeline_reveal_hidden",
            )
        )
        action_set.add(
            Action(
                id="lifeline_remove",
                label="Use remove-strike lifeline",
                handler="_action_lifeline_remove",
                is_enabled="_is_lifeline_remove_enabled",
                is_hidden="_is_lifeline_remove_hidden",
            )
        )
        action_set.add(
            Action(
                id="lifeline_retry",
                label="Use retry-shield lifeline",
                handler="_action_lifeline_retry",
                is_enabled="_is_lifeline_retry_enabled",
                is_hidden="_is_lifeline_retry_hidden",
            )
        )
        return action_set

    def create_lobby_action_set(self, player: Player) -> ActionSet:
        """Add bot-difficulty management action to lobby."""
        action_set = super().create_lobby_action_set(player)
        user = self.get_user(player)
        locale = user.locale if user else "en"
        action_set.add(
            Action(
                id="set_bot_difficulty",
                label=Localization.get(locale, "hwf-set-bot-difficulty"),
                handler="_action_set_bot_difficulty",
                is_enabled="_is_set_bot_difficulty_enabled",
                is_hidden="_is_set_bot_difficulty_hidden",
                input_request=MenuInput(
                    prompt="hwf-select-bot-difficulty",
                    options="_per_bot_difficulty_options",
                ),
            )
        )
        return action_set

    def create_standard_action_set(self, player: Player) -> ActionSet:
        action_set = super().create_standard_action_set(player)
        user = self.get_user(player)
        locale = user.locale if user else "en"
        local_actions = [
            Action(
                id="read_board",
                label="Read board",
                handler="_action_read_board",
                is_enabled="_is_read_status_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_letters_available",
                label="Letters available",
                handler="_action_read_letters_available",
                is_enabled="_is_read_status_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_letters_used",
                label="Letters used",
                handler="_action_read_letters_used",
                is_enabled="_is_read_status_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_all_boards",
                label="Read all boards",
                handler="_action_read_all_boards",
                is_enabled="_is_read_all_boards_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_wheel_outcome",
                label="Wheel outcome",
                handler="_action_read_wheel_outcome",
                is_enabled="_is_read_status_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_current_score",
                label="Current score",
                handler="_action_read_current_score",
                is_enabled="_is_read_status_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_current_balloons",
                label="Current balloons",
                handler="_action_read_current_balloons",
                is_enabled="_is_read_status_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_round_status",
                label="Round status",
                handler="_action_read_round_status",
                is_enabled="_is_read_status_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_board_modifiers",
                label="Board modifiers",
                handler="_action_read_board_modifiers",
                is_enabled="_is_read_status_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="read_rack",
                label="Rack letters",
                handler="_action_read_rack",
                is_enabled="_is_read_rack_enabled",
                is_hidden="_is_read_status_hidden",
            ),
            Action(
                id="check_turn_timer",
                label=Localization.get(locale, "poker-check-turn-timer"),
                handler="_action_check_turn_timer",
                is_enabled="_is_check_turn_timer_enabled",
                is_hidden="_is_read_status_hidden",
            ),
        ]
        for action in reversed(local_actions):
            action_set.add(action)
            if action.id in action_set._order:
                action_set._order.remove(action.id)
            action_set._order.insert(0, action.id)
        return action_set

    def setup_keybinds(self) -> None:
        super().setup_keybinds()
        self.define_keybind("c", "Choose word", ["choose_word"], state=KeybindState.ACTIVE)
        self.define_keybind("1", "Reveal lifeline", ["lifeline_reveal"], state=KeybindState.ACTIVE)
        self.define_keybind("2", "Remove strike lifeline", ["lifeline_remove"], state=KeybindState.ACTIVE)
        self.define_keybind("3", "Retry shield lifeline", ["lifeline_retry"], state=KeybindState.ACTIVE)
        self.define_keybind("b", "Read board", ["read_board"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("a", "Letters available", ["read_letters_available"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("u", "Letters used", ["read_letters_used"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("shift+b", "Read all boards", ["read_all_boards"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("w", "Wheel outcome", ["read_wheel_outcome"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("p", "Current score", ["read_current_score"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("l", "Current balloons", ["read_current_balloons"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("r", "Round status", ["read_round_status"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("m", "Board modifiers", ["read_board_modifiers"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("k", "Rack letters", ["read_rack"], state=KeybindState.ACTIVE, include_spectators=True)
        self.define_keybind("shift+t", "Turn timer", ["check_turn_timer"], state=KeybindState.ACTIVE, include_spectators=True)

    def on_start(self) -> None:
        self.status = "playing"
        self.game_active = True
        self.round = 0
        self.phase = "lobby"
        self.round_resume_tick = 0
        self.last_match_end_message = ""
        self.last_eliminated_names = []
        self.last_round_winner_id = ""
        self.last_played_round = {}
        self.has_played_ids = []
        self.round_robin_index = 0
        self.host_queue_index = 0
        self.winner_streak_id = ""
        self.winner_streak_count = 0
        self.timer.clear()
        self.timer_warning_played = False

        active_players = self.get_active_players()
        self.participant_ids = [p.id for p in active_players]
        self._team_manager.team_mode = "individual"
        self._team_manager.setup_teams([p.name for p in active_players])

        self.set_turn_players(active_players)
        for player in active_players:
            player.balloons_remaining = self.options.starting_balloons
            player.score = 0
            player.coins = 0
            player.level = 1
            player.correct_streak = 0
            player.wrong_streak = 0
            player.lifeline_reveal = 0
            player.lifeline_remove = 0
            player.lifeline_retry = 0
            player.retry_shield_active = False

        if self.rng_seed == 0:
            self.rng_seed = random.randint(1, 2_147_483_647)
        self._load_dictionary()
        self._sync_bot_difficulty_overrides()

        self.play_music(SOUNDS["music"])
        self._schedule_next_lava_ambience(initial=True)
        self._start_round()

    def on_tick(self) -> None:
        super().on_tick()
        self.process_scheduled_sounds()
        self._maybe_play_lava_ambience()
        if self.round_resume_tick > 0 and self.sound_scheduler_tick >= self.round_resume_tick and self.phase == "round_end":
            self.round_resume_tick = 0
            self._start_round()
        if self.timer.tick():
            self._handle_turn_timeout()
        self._maybe_play_timer_warning()
        BotHelper.on_tick(self)

    def _pacing_ticks(self, key: str) -> int:
        profile = self.options.pacing_profile
        if profile not in PACING_TICKS:
            profile = "normal"
        return PACING_TICKS[profile].get(key, 0)

    def _cancel_board_readout_audio(self) -> None:
        self.scheduled_sounds = [
            sound_event
            for sound_event in self.scheduled_sounds
            if len(sound_event) < 2 or sound_event[1] != SOUNDS["click2"]
        ]

    def _clear_round_timeline(self) -> None:
        self.cancel_timeline("hwf-board-readout")
        self.cancel_timeline("hwf-round-flow")
        self._cancel_board_readout_audio()

    def prestart_validate(self) -> list[str]:
        errors = super().prestart_validate()
        if self.options.min_word_length > self.options.max_word_length:
            errors.append("hwf-error-min-length-greater-than-max")
        if self.options.rack_size < self.options.max_word_length:
            errors.append("hwf-error-rack-smaller-than-max-length")
        return errors

    def _schedule_next_lava_ambience(self, initial: bool = False) -> None:
        jitter = random.randint(80, 180) if initial else random.randint(140, 320)
        self.lava_next_tick = self.sound_scheduler_tick + jitter

    def _maybe_play_lava_ambience(self) -> None:
        if self.sound_scheduler_tick < self.lava_next_tick:
            return
        self.play_sound(SOUNDS["lava"], volume=55)
        self._schedule_next_lava_ambience()

    def _start_round(self) -> None:
        if self._check_match_end():
            return

        self._clear_round_timeline()
        self.round += 1
        self.last_eliminated_names = []
        players = self._get_round_eligible_players()
        if len(players) < 1:
            return
        self.set_turn_players(players)

        if len(players) == 1:
            self._start_solo_round(players[0])
            return

        setter, guesser = self._select_round_pair(players)

        self.setter_id = setter.id
        self.guesser_id = guesser.id
        self.tile_rack = self._generate_rack(self.round)
        self.secret_word = ""
        self.masked_word = ""
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong_guesses = 0
        self.wheel_result = ""
        self.round_points_multiplier = 1
        setter.retry_shield_active = False
        guesser.retry_shield_active = False
        self._mark_players_as_played(setter, guesser)

        self.phase = "choose_word"
        self.current_player = setter

        intro_text = f"Round {self.round}. {setter.name} is choosing a word, {guesser.name} will guess."
        intro_delay = max(self._pacing_ticks("turn_transition"), 6)
        self.schedule_sound(SOUNDS["menu_open"], delay_ticks=0)
        self.schedule_sound(SOUNDS["avatar"], delay_ticks=2, volume=70)
        self.schedule_sound(SOUNDS["shuffle"], delay_ticks=4, volume=85)
        self._schedule_round_intro(intro_text, delay_ticks=intro_delay)
        # Spectator boards are available via hotkeys instead of auto speech.

        BotHelper.jolt_bot_for_speech(
            setter,
            delay_ticks=intro_delay,
            speech_ticks=self.estimate_speech_ticks(intro_text),
            post_pause_ticks=self._pacing_ticks("post_board_pause"),
            min_ticks=max(2, self._pacing_ticks("guess_result_pause")),
        )

        self.rebuild_all_menus()

    def _start_solo_round(self, player: HanginWithFriendsPlayer) -> None:
        self._clear_round_timeline()
        self.setter_id = player.id
        self.guesser_id = player.id
        self.tile_rack = self._generate_rack(self.round)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong_guesses = 0
        self.wheel_result = ""
        self.round_points_multiplier = 1
        player.retry_shield_active = False

        candidates = self._get_words_for_rack()
        if candidates:
            self.secret_word = self._select_bot_word_by_difficulty(
                candidates, self.options.default_bot_difficulty
            )
        else:
            rack_letters = self.tile_rack[: self.options.max_word_length]
            fallback = "".join(rack_letters[: self.options.min_word_length]).lower()
            self.secret_word = fallback if fallback else "aaa"
        self._initialize_board(self.secret_word)
        self.max_wrong_guesses = self.options.base_wrong_guesses + len(self.secret_word)

        self.phase = "guessing"
        self.current_player = player

        intro_text = f"Round {self.round}. Solo mode: {player.name} is guessing."
        intro_delay = max(self._pacing_ticks("turn_transition"), 6)
        self.schedule_sound(SOUNDS["menu_open"], delay_ticks=0)
        self.schedule_sound(SOUNDS["shuffle"], delay_ticks=2, volume=85)
        self._schedule_round_intro(intro_text, delay_ticks=intro_delay)
        self._spin_wheel(player)
        selected_text = (
            f"Word selected. The word has {len(self.secret_word)} letters. "
            f"Wrong guesses allowed: {self.max_wrong_guesses}."
        )
        self.schedule_timeline_speech(
            selected_text,
            delay_ticks=self._pacing_ticks("turn_transition"),
            buffer="table",
            include_spectators=True,
            tag="hwf-round-flow",
        )
        board_end_delay = self._announce_guess_state(
            delay_ticks=self._pacing_ticks("turn_transition")
        )
        self._start_turn_timer()

        BotHelper.jolt_bot_for_speech(
            player,
            delay_ticks=board_end_delay,
            speech_ticks=self.estimate_speech_ticks(selected_text),
            post_pause_ticks=self._pacing_ticks("post_board_pause"),
            min_ticks=max(2, self._pacing_ticks("guess_result_pause")),
        )
        self.rebuild_all_menus()

    def _select_round_pair(
        self, eligible: list[HanginWithFriendsPlayer]
    ) -> tuple[HanginWithFriendsPlayer, HanginWithFriendsPlayer]:
        if len(eligible) == 1:
            return (eligible[0], eligible[0])
        host_player = next((p for p in eligible if p.name == self.host), None)
        if self.round == 1:
            setter = host_player if host_player else eligible[0]
            guesser = self._pick_random_other(eligible, setter.id)
            return (setter, guesser)
        if len(eligible) == 2 and self.setter_id and self.guesser_id:
            setter = self.get_player_by_id(self.guesser_id)
            guesser = self.get_player_by_id(self.setter_id)
            if isinstance(setter, HanginWithFriendsPlayer) and isinstance(guesser, HanginWithFriendsPlayer):
                if setter in eligible and guesser in eligible:
                    return (setter, guesser)

        strategy = self.options.pairing_strategy
        if strategy == "round_robin":
            return self._pair_round_robin(eligible)
        if strategy == "weighted_fair":
            return self._pair_weighted_fair(eligible)
        if strategy == "winner_cap":
            return self._pair_winner_cap(eligible)
        if strategy == "host_queue":
            return self._pair_host_queue(eligible)
        if strategy == "performance":
            return self._pair_performance(eligible)
        return self._pair_winner_fair(eligible)

    # action guards
    def _is_choose_word_enabled(self, player: Player) -> str | None:
        error = self.guard_turn_action_enabled(player)
        if error:
            return error
        if self.phase != "choose_word" or player.id != self.setter_id:
            return "action-not-available"
        return None

    def _is_choose_word_hidden(self, player: Player) -> Visibility:
        return self.turn_action_visibility(player, extra_condition=self.phase == "choose_word" and player.id == self.setter_id)

    def _is_guess_letter_enabled(self, player: Player, action_id: str) -> str | None:
        error = self.guard_turn_action_enabled(player)
        if error:
            return error
        if self.phase != "guessing" or player.id != self.guesser_id:
            return "action-not-available"
        letter = action_id.rsplit("_", 1)[-1]
        if letter in self.guessed_letters:
            return "action-not-available"
        return None

    def _is_read_status_enabled(self, player: Player) -> str | None:
        if self.status != "playing":
            return "action-not-playing"
        if not self.secret_word:
            return "action-not-available"
        return None

    def _is_read_status_hidden(self, player: Player) -> Visibility:
        return Visibility.HIDDEN

    def _is_read_rack_enabled(self, player: Player) -> str | None:
        if self.status != "playing":
            return "action-not-playing"
        if not self.tile_rack:
            return "action-not-available"
        if player.id == self.setter_id:
            return None
        if player.is_spectator and self.options.spectators_see_all_actions:
            return None
        return "action-not-available"

    def _is_check_turn_timer_enabled(self, player: Player) -> str | None:
        if self.status != "playing":
            return "action-not-playing"
        return None

    def _is_read_all_boards_enabled(self, player: Player) -> str | None:
        if self.status != "playing":
            return "action-not-playing"
        if not self._get_participant_players():
            return "action-not-available"
        if player.is_spectator and not self.options.spectators_see_all_actions:
            return "action-not-available"
        return None

    def _is_guess_letter_hidden(self, player: Player, action_id: str) -> Visibility:
        letter = action_id.rsplit("_", 1)[-1]
        return self.turn_action_visibility(
            player,
            extra_condition=(self.phase == "guessing" and player.id == self.guesser_id and letter not in self.guessed_letters),
        )

    def _is_guesser_turn_enabled(self, player: Player) -> str | None:
        error = self.guard_turn_action_enabled(player)
        if error:
            return error
        if self.phase != "guessing" or player.id != self.guesser_id:
            return "action-not-available"
        return None

    def _is_set_bot_difficulty_enabled(self, player: Player) -> str | None:
        if self.status != "waiting":
            return "action-game-in-progress"
        if player.name != self.host:
            return "action-not-host"
        if not any(p.is_bot for p in self.players):
            return "action-no-bots"
        return None

    def _is_set_bot_difficulty_hidden(self, player: Player) -> Visibility:
        if self.status != "waiting" or player.name != self.host:
            return Visibility.HIDDEN
        return Visibility.VISIBLE if any(p.is_bot for p in self.players) else Visibility.HIDDEN

    def _is_lifeline_reveal_enabled(self, player: Player) -> str | None:
        error = self._is_guesser_turn_enabled(player)
        if error:
            return error
        return None if isinstance(player, HanginWithFriendsPlayer) and player.lifeline_reveal > 0 else "action-not-available"

    def _is_lifeline_reveal_hidden(self, player: Player) -> Visibility:
        cond = isinstance(player, HanginWithFriendsPlayer) and player.lifeline_reveal > 0
        return self.turn_action_visibility(player, extra_condition=self.phase == "guessing" and player.id == self.guesser_id and cond)

    def _is_lifeline_remove_enabled(self, player: Player) -> str | None:
        error = self._is_guesser_turn_enabled(player)
        if error:
            return error
        if not isinstance(player, HanginWithFriendsPlayer) or player.lifeline_remove <= 0:
            return "action-not-available"
        if self.wrong_guesses <= 0:
            return "action-not-available"
        return None

    def _is_lifeline_remove_hidden(self, player: Player) -> Visibility:
        cond = isinstance(player, HanginWithFriendsPlayer) and player.lifeline_remove > 0 and self.wrong_guesses > 0
        return self.turn_action_visibility(player, extra_condition=self.phase == "guessing" and player.id == self.guesser_id and cond)

    def _is_lifeline_retry_enabled(self, player: Player) -> str | None:
        error = self._is_guesser_turn_enabled(player)
        if error:
            return error
        if not isinstance(player, HanginWithFriendsPlayer) or player.lifeline_retry <= 0:
            return "action-not-available"
        if player.retry_shield_active:
            return "action-not-available"
        return None

    def _is_lifeline_retry_hidden(self, player: Player) -> Visibility:
        cond = isinstance(player, HanginWithFriendsPlayer) and player.lifeline_retry > 0 and not player.retry_shield_active
        return self.turn_action_visibility(player, extra_condition=self.phase == "guessing" and player.id == self.guesser_id and cond)

    def _get_guess_letter_label(self, player: Player, action_id: str) -> str:
        letter = action_id.rsplit("_", 1)[-1]
        return f"Guess {letter.upper()}"

    # actions
    def _action_choose_word(self, player: Player, input_value: str, action_id: str) -> None:
        self.play_sound(SOUNDS["click"])
        word = self._normalize_word(input_value)
        user = self.get_user(player)
        if word is None:
            self.play_sound(SOUNDS["submit_invalid"])
            if user:
                user.speak("Word must contain letters only.", "table")
            return

        if not (self.options.min_word_length <= len(word) <= self.options.max_word_length):
            self.play_sound(SOUNDS["submit_invalid"])
            if user:
                user.speak(f"Word must be {self.options.min_word_length}-{self.options.max_word_length} letters.", "table")
            return

        if self.options.dictionary_mode != "off" and not self._word_uses_rack(word):
            self.play_sound(SOUNDS["submit_invalid"])
            if user:
                user.speak("Word must use only the rack letters.", "table")
            return

        if self.options.dictionary_mode == "strict" and self._dictionary_loaded and word not in self._dictionary_words:
            self.play_sound(SOUNDS["submit_invalid"])
            if user:
                user.speak("Word must be in the dictionary for strict mode.", "table")
            return

        self.secret_word = word
        self._initialize_board(word)
        self.max_wrong_guesses = self.options.base_wrong_guesses + len(word)

        guesser = self.get_player_by_id(self.guesser_id)
        setter = self.get_player_by_id(self.setter_id)
        if guesser is None or setter is None:
            return

        self.play_sound(SOUNDS["submit_valid"])
        self.play_sound(SOUNDS["menu_close"])
        self._spin_wheel(guesser)

        self._clear_round_timeline()
        self.phase = "guessing"
        self.current_player = guesser
        selected_text = (
            f"Word selected. The word has {len(word)} letters. "
            f"Wrong guesses allowed: {self.max_wrong_guesses}."
        )
        self.schedule_timeline_speech(
            selected_text,
            delay_ticks=self._pacing_ticks("turn_transition"),
            buffer="table",
            include_spectators=True,
            tag="hwf-round-flow",
        )
        self._broadcast_private_to_spectators(f"Secret word chosen by {setter.name}: {self.secret_word.upper()}")
        board_end_delay = self._announce_guess_state(
            delay_ticks=self._pacing_ticks("turn_transition")
        )
        self._start_turn_timer()

        BotHelper.jolt_bot_for_speech(
            guesser,
            delay_ticks=board_end_delay,
            speech_ticks=self.estimate_speech_ticks(selected_text),
            post_pause_ticks=self._pacing_ticks("post_board_pause"),
            min_ticks=max(2, self._pacing_ticks("guess_result_pause")),
        )
        self.rebuild_all_menus()

    def _action_guess_letter(self, player: Player, action_id: str) -> None:
        self.play_sound(SOUNDS["click2"], volume=80)
        letter = action_id.rsplit("_", 1)[-1]
        self._resolve_letter_guess(letter)

    def _action_read_board(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        user.speak(self._format_board_summary())

    def _action_read_letters_available(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        available = self._available_letters()
        if available:
            letters = ", ".join(letter.upper() for letter in available)
            user.speak(f"Available letters: {letters}.")
        else:
            user.speak("Available letters: none.")

    def _action_read_letters_used(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        used = sorted(set(self.guessed_letters))
        if used:
            letters = ", ".join(letter.upper() for letter in used)
            user.speak(f"Used letters: {letters}.")
        else:
            user.speak("Used letters: none.")

    def _action_read_all_boards(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        players = [p for p in self._get_participant_players() if not p.is_spectator]
        if not players:
            user.speak("No boards available.")
            return
        lines = [self._format_player_board_line(p) for p in sorted(players, key=lambda p: p.name.lower())]
        user.speak(" ".join(lines))

    def _action_read_wheel_outcome(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        user.speak(self._format_wheel_outcome())

    def _action_read_current_score(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        if isinstance(player, HanginWithFriendsPlayer):
            user.speak(f"{player.name} score {player.score}.")
        else:
            user.speak("No score available.")

    def _action_read_current_balloons(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        if isinstance(player, HanginWithFriendsPlayer):
            user.speak(f"{player.name} balloons {player.balloons_remaining}.")
        else:
            user.speak("No balloons available.")

    def _action_read_round_status(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        user.speak(self._format_round_status())

    def _action_read_board_modifiers(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        user.speak(self._format_board_modifiers_summary())

    def _action_read_rack(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        if player.id != self.setter_id and not (player.is_spectator and self.options.spectators_see_all_actions):
            user.speak("Rack not available.")
            return
        if not self.tile_rack:
            user.speak("Rack not available.")
            return
        scored = [f"{letter.upper()}({LETTER_SCORES.get(letter.upper(), 0)})" for letter in self.tile_rack]
        rack_text = ", ".join(scored)
        user.speak(f"Rack letters: {rack_text}.")

    def _action_check_turn_timer(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        remaining = self.timer.seconds_remaining()
        if remaining <= 0:
            user.speak_l("poker-timer-disabled")
            return
        user.speak_l("poker-timer-remaining", seconds=remaining)

    def _format_score_line_brief(self, player: HanginWithFriendsPlayer) -> str:
        return f"{player.name} score {player.score}, balloons {player.balloons_remaining}"

    def _format_score_line_detailed(self, player: HanginWithFriendsPlayer) -> str:
        return (
            f"{player.name} score {player.score}, balloons {player.balloons_remaining}, "
            f"coins {player.coins}, reveal {player.lifeline_reveal}, "
            f"remove {player.lifeline_remove}, retry {player.lifeline_retry}."
        )

    def _format_player_board_line(self, player: HanginWithFriendsPlayer) -> str:
        return (
            f"{player.name} board: score {player.score}, balloons {player.balloons_remaining}, "
            f"coins {player.coins}, reveal {player.lifeline_reveal}, "
            f"remove {player.lifeline_remove}, retry {player.lifeline_retry}."
        )

    def _action_check_scores(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        players = [p for p in self._get_participant_players() if not p.is_spectator]
        if not players:
            user.speak_l("no-scores-available")
            return
        lines = [self._format_score_line_brief(p) for p in sorted(players, key=lambda p: p.name.lower())]
        text = ". ".join(lines)
        if text and not text.endswith("."):
            text += "."
        user.speak(text)

    def _action_check_scores_detailed(self, player: Player, action_id: str) -> None:
        user = self.get_user(player)
        if not user:
            return
        players = [p for p in self._get_participant_players() if not p.is_spectator]
        if not players:
            self.status_box(player, ["No scores available."])
            return
        lines = [self._format_score_line_detailed(p) for p in sorted(players, key=lambda p: p.name.lower())]
        self.status_box(player, lines)

    def _action_lifeline_reveal(self, player: Player, action_id: str) -> None:
        if not isinstance(player, HanginWithFriendsPlayer) or player.lifeline_reveal <= 0:
            return
        hidden_positions = [idx for idx, ch in enumerate(self.masked_word) if ch == "_"]
        if not hidden_positions:
            return
        target_idx = random.choice(hidden_positions)
        target_letter = self.secret_word[target_idx]

        player.lifeline_reveal -= 1
        self.play_sound(SOUNDS["use_lifeline"])
        self.play_sound(SOUNDS["lifeline_slide"])
        self._resolve_letter_guess(target_letter, from_lifeline=True)

    def _action_lifeline_remove(self, player: Player, action_id: str) -> None:
        if not isinstance(player, HanginWithFriendsPlayer) or player.lifeline_remove <= 0:
            return
        if self.wrong_guesses <= 0:
            return
        player.lifeline_remove -= 1
        mistakes_before = max(0, self.max_wrong_guesses - self.wrong_guesses)
        self.wrong_guesses = max(0, self.wrong_guesses - 1)
        mistakes_after = max(0, self.max_wrong_guesses - self.wrong_guesses)
        self.play_sound(SOUNDS["use_lifeline"])
        self.play_sound(SOUNDS["lifeline_bounce"])
        self._maybe_broadcast_mistakes_left_change(mistakes_before, mistakes_after)
        self.rebuild_all_menus()

    def _action_lifeline_retry(self, player: Player, action_id: str) -> None:
        if not isinstance(player, HanginWithFriendsPlayer) or player.lifeline_retry <= 0:
            return
        if player.retry_shield_active:
            return
        player.lifeline_retry -= 1
        player.retry_shield_active = True
        self.play_sound(SOUNDS["use_lifeline"])
        self.play_sound(SOUNDS["lifeline_bounce"])
        self.rebuild_all_menus()

    def _action_set_bot_difficulty(self, player: Player, value: str, action_id: str) -> None:
        try:
            bot_name, difficulty = value.split("|", 1)
        except ValueError:
            return
        bot = next((p for p in self.players if p.is_bot and p.name == bot_name), None)
        if bot is None:
            return
        selected = self._normalize_bot_difficulty(difficulty)
        self.bot_difficulties[bot.id] = selected
        self.play_sound(SOUNDS["click"])
        self.broadcast(f"{bot.name} bot difficulty set to {selected}.")
        self.rebuild_all_menus()

    # round mechanics
    def _spin_wheel(self, guesser: HanginWithFriendsPlayer) -> None:
        self.play_sound(SOUNDS["enter_wheel"])
        self.play_sound(SOUNDS["roulette"])
        self.schedule_sound(SOUNDS["roulette_ping"], delay_ticks=8)
        self.schedule_sound(SOUNDS["roulette_ping"], delay_ticks=16)
        self.schedule_sound(SOUNDS["roulette_ping"], delay_ticks=24)

        rng = random.Random(self.rng_seed + (self.round * 997) + len(self.secret_word))
        outcome = rng.choice(WHEEL_OUTCOMES)
        self.wheel_result = outcome
        self.play_sound(SOUNDS["drop"])
        mistakes_before = max(0, self.max_wrong_guesses - self.wrong_guesses)

        if outcome == "coin_bonus":
            guesser.coins += 10
            self.play_sound(SOUNDS["buy_points"])
            self.play_sound(SOUNDS["pickup"])
        elif outcome == "extra_guess":
            self.max_wrong_guesses += 1
            self.play_sound(SOUNDS["pickup"])
        elif outcome == "fewer_guess":
            self.max_wrong_guesses = max(1, self.max_wrong_guesses - 1, self.wrong_guesses)
            self.play_sound(SOUNDS["drop"])
        elif outcome == "double_points":
            self.round_points_multiplier = 2
            self.play_sound(SOUNDS["multiplier"])
        elif outcome == "lifeline_reveal":
            guesser.lifeline_reveal += 1
            self.play_sound(SOUNDS["pickup"])
            self.play_sound(SOUNDS["lifeline_slide"])
        elif outcome == "lifeline_remove":
            guesser.lifeline_remove += 1
            self.play_sound(SOUNDS["pickup"])
            self.play_sound(SOUNDS["lifeline_bounce"])
        elif outcome == "lifeline_retry":
            guesser.lifeline_retry += 1
            self.play_sound(SOUNDS["pickup"])
            self.play_sound(SOUNDS["lifeline_bounce"])
        else:
            self.play_sound(SOUNDS["click2"])
        mistakes_after = max(0, self.max_wrong_guesses - self.wrong_guesses)
        self._maybe_broadcast_mistakes_left_change(mistakes_before, mistakes_after)

    def _resolve_letter_guess(self, letter: str, from_lifeline: bool = False) -> None:
        guesser = self.get_player_by_id(self.guesser_id)
        if not isinstance(guesser, HanginWithFriendsPlayer):
            return
        if letter in self.guessed_letters:
            return

        self.guessed_letters.append(letter)

        if letter in self.secret_word:
            masked = list(self.masked_word)
            for idx, char in enumerate(self.secret_word):
                if char == letter:
                    masked[idx] = char
            self.masked_word = "".join(masked)
            guesser.correct_streak += 1
            guesser.wrong_streak = 0
            self.play_sound(SOUNDS["history_correct"])
            self.play_sound(CORRECT_SEQUENCE_SOUNDS[min(guesser.correct_streak, 8) - 1])
            guess_text = f"Correct. {letter.upper()} is in the word."
            if not from_lifeline:
                self.broadcast(guess_text)

            if "_" not in self.masked_word:
                self._resolve_round(guesser_solved=True)
                return
        else:
            self._apply_wrong_guess(guesser)
            guess_text = f"Wrong. {letter.upper()} is not in the word."
            self.broadcast(guess_text)
            if self.wrong_guesses >= self.max_wrong_guesses:
                self._resolve_round(guesser_solved=False)
                return

        if letter in self.secret_word and not from_lifeline:
            board_end_delay = self._announce_guess_state(
                delay_ticks=self._pacing_ticks("guess_result_pause")
            )
        else:
            board_end_delay = self._pacing_ticks("guess_result_pause")
        BotHelper.jolt_bot_for_speech(
            guesser,
            delay_ticks=board_end_delay,
            speech_ticks=self.estimate_speech_ticks(guess_text if "guess_text" in locals() else ""),
            post_pause_ticks=self._pacing_ticks("post_board_pause"),
            min_ticks=max(2, self._pacing_ticks("guess_result_pause")),
        )
        if self.phase == "guessing":
            self._start_turn_timer()
        self.rebuild_all_menus()

    def _apply_wrong_guess(self, guesser: HanginWithFriendsPlayer) -> None:
        if guesser.retry_shield_active:
            guesser.retry_shield_active = False
            self.play_sound(SOUNDS["lifeline_bounce"])
            self.play_sound(SOUNDS["history_incorrect"])
            self.broadcast("Retry shield blocked the strike.")
            return

        self.wrong_guesses += 1
        guesser.wrong_streak += 1
        guesser.correct_streak = 0
        self.play_sound(SOUNDS["history_incorrect"])
        index = min(guesser.wrong_streak, 8) - 1
        self.play_sound(INCORRECT_SEQUENCE_SOUNDS[index])

    def _resolve_round(self, guesser_solved: bool) -> None:
        setter = self.get_player_by_id(self.setter_id)
        guesser = self.get_player_by_id(self.guesser_id)
        if not isinstance(setter, HanginWithFriendsPlayer) or not isinstance(guesser, HanginWithFriendsPlayer):
            return

        self._clear_round_timeline()
        self.phase = "round_end"
        self.timer.clear()
        word_points = self._score_word_with_board_modifiers(self.secret_word)
        points = word_points * self.round_points_multiplier
        if guesser_solved:
            setter.balloons_remaining -= 1
            self._award_score(guesser, points)
            self.play_sound(CORRECT_SEQUENCE_SOUNDS[7])
            self.play_sound(SOUNDS["balloon"])
            result_text = f"{guesser.name} guessed the winning word: {self.secret_word.capitalize()} with {points} points."
            self.broadcast(result_text)
            self.last_round_winner_id = guesser.id
            if self.winner_streak_id == guesser.id:
                self.winner_streak_count += 1
            else:
                self.winner_streak_id = guesser.id
                self.winner_streak_count = 1
        else:
            guesser.balloons_remaining -= 1
            self._award_score(setter, points)
            self.play_sound(INCORRECT_SEQUENCE_SOUNDS[7])
            self.play_sound(SOUNDS["balloon"])
            result_text = f"{setter.name} set the winning word: {self.secret_word.capitalize()} with {points} points."
            self.broadcast(result_text)
            self.last_round_winner_id = setter.id
            if self.winner_streak_id == setter.id:
                self.winner_streak_count += 1
            else:
                self.winner_streak_id = setter.id
                self.winner_streak_count = 1

        eliminated_texts = self._eliminate_players_without_balloons(speak=False)

        if self._check_match_end():
            return
        round_end_texts = [result_text, *eliminated_texts]
        text_pause_ticks = sum(
            self.estimate_speech_ticks(msg) + self._pacing_ticks("post_board_pause")
            for msg in round_end_texts
        )
        self.round_resume_tick = (
            self.sound_scheduler_tick
            + self._pacing_ticks("round_end_pause")
            + text_pause_ticks
        )

    def _award_score(self, player: HanginWithFriendsPlayer, points: int) -> None:
        player.score += points
        player.coins += points * 2
        self.play_sound(SOUNDS["score_flyup"])
        self.play_sound(SOUNDS["buy_points"])
        self._check_level_up(player)

    def _check_level_up(self, player: HanginWithFriendsPlayer) -> None:
        target_level = 1 + (player.score // 5)
        if target_level <= player.level:
            return
        player.level = target_level
        self.play_sound(SOUNDS["level_up"])
        self.play_sound(SOUNDS["level_up_missions"])
        self.play_sound(SOUNDS["popup"])
        # Level ups are discoverable via hotkeys/status.

    def _available_letters(self) -> list[str]:
        guessed = set(self.guessed_letters)
        return [letter for letter in string.ascii_lowercase if letter not in guessed]

    def _pick_random_rack_letter(self) -> str | None:
        rack_letters = [c for c in self.tile_rack if c not in self.guessed_letters]
        if rack_letters:
            return random.choice(rack_letters)
        available = self._available_letters()
        return random.choice(available) if available else None

    def _format_board_summary(self) -> str:
        masked = self._spoken_board()
        modifiers = self._format_board_modifiers_compact()
        if modifiers:
            return f"Board: {masked}. Modifiers: {modifiers}."
        return f"Board: {masked}."

    def _format_board_modifiers_compact(self) -> str:
        if not self.board_modifiers:
            return ""
        by_kind: dict[str, list[int]] = {kind: [] for kind in MODIFIER_ORDER}
        for pos, kind in self.board_modifiers.items():
            if kind in by_kind:
                by_kind[kind].append(pos)

        def format_positions(positions: list[int]) -> str:
            if not positions:
                return ""
            parts = [str(p) for p in sorted(positions)]
            if len(parts) == 1:
                return parts[0]
            if len(parts) == 2:
                return f"{parts[0]} and {parts[1]}"
            return ", ".join(parts[:-1]) + f", and {parts[-1]}"

        lines: list[str] = []
        mapping = {
            "double_letter": "double letter",
            "triple_letter": "triple letter",
            "double_word": "double word",
            "triple_word": "triple word",
        }
        for kind in MODIFIER_ORDER:
            positions = by_kind.get(kind, [])
            if not positions:
                continue
            lines.append(f"{mapping[kind]} on {format_positions(positions)}")
        return "; ".join(lines)

    def _format_wheel_outcome(self) -> str:
        if not self.wheel_result:
            return "Wheel outcome not set."
        mapping = {
            "coin_bonus": "Wheel outcome: coin bonus.",
            "extra_guess": "Wheel outcome: extra guess.",
            "fewer_guess": "Wheel outcome: one fewer guess.",
            "double_points": "Wheel outcome: double points.",
            "lifeline_reveal": "Wheel outcome: reveal lifeline.",
            "lifeline_remove": "Wheel outcome: remove-strike lifeline.",
            "lifeline_retry": "Wheel outcome: retry-shield lifeline.",
            "none": "Wheel outcome: no bonus.",
        }
        return mapping.get(self.wheel_result, f"Wheel outcome: {self.wheel_result}.")

    def _format_round_status(self) -> str:
        setter = self.get_player_by_id(self.setter_id)
        guesser = self.get_player_by_id(self.guesser_id)
        parts = [f"Round {self.round}", f"phase {self.phase}"]
        if self.current_player:
            parts.append(f"current player {self.current_player.name}")
        if setter:
            parts.append(f"setter {setter.name}")
        if guesser:
            parts.append(f"guesser {guesser.name}")
        if self.secret_word:
            parts.append(f"word length {len(self.secret_word)}")
        if self.max_wrong_guesses > 0:
            mistakes_left = max(0, self.max_wrong_guesses - self.wrong_guesses)
            parts.append(f"mistakes left {mistakes_left}")
        if self.phase in {"round_end", "game_end"} and self.secret_word:
            points = self._score_word_with_board_modifiers(self.secret_word)
            total = points * self.round_points_multiplier
            parts.append(f"round points {points} x{self.round_points_multiplier} total {total}")
        if self.last_eliminated_names:
            eliminated = ", ".join(self.last_eliminated_names)
            parts.append(f"eliminated {eliminated}")
        if self.phase == "game_end" and getattr(self, "last_match_end_message", ""):
            parts.append(self.last_match_end_message)
        return ". ".join(parts) + "."

    def _maybe_broadcast_mistakes_left_change(self, before: int, after: int) -> None:
        if before == after:
            return
        if after < before and before - after == 1:
            return
        self.broadcast(f"Mistakes left: {after}.")

    def _pair_winner_fair(
        self, eligible: list[HanginWithFriendsPlayer]
    ) -> tuple[HanginWithFriendsPlayer, HanginWithFriendsPlayer]:
        carry = self.get_player_by_id(self.last_round_winner_id)
        if not isinstance(carry, HanginWithFriendsPlayer) or carry not in eligible:
            setter = self._pick_least_recent(eligible, exclude_id="")
            guesser = self._pick_least_recent(eligible, exclude_id=setter.id)
            return (setter, guesser)
        if carry.id == self.setter_id:
            setter = carry
            guesser = self._pick_fair_opponent(eligible, setter.id)
        else:
            guesser = carry
            setter = self._pick_fair_opponent(eligible, guesser.id)
        return (setter, guesser)

    def _pair_round_robin(
        self, eligible: list[HanginWithFriendsPlayer]
    ) -> tuple[HanginWithFriendsPlayer, HanginWithFriendsPlayer]:
        order = self._get_pairing_order(eligible)
        if not order:
            return (eligible[0], eligible[0])
        idx = self.round_robin_index % len(order)
        setter = self._get_player_by_id_or_fallback(order[idx], eligible)
        guesser = self._get_player_by_id_or_fallback(order[(idx + 1) % len(order)], eligible)
        self.round_robin_index = (idx + 1) % len(order)
        return (setter, guesser)

    def _pair_weighted_fair(
        self, eligible: list[HanginWithFriendsPlayer]
    ) -> tuple[HanginWithFriendsPlayer, HanginWithFriendsPlayer]:
        weights = {p.id: self._weight_for_player(p.id) for p in eligible}
        setter = self._weighted_choice(eligible, weights)
        guesser_pool = [p for p in eligible if p.id != setter.id]
        guesser = self._weighted_choice(guesser_pool, weights)
        return (setter, guesser)

    def _pair_winner_cap(
        self, eligible: list[HanginWithFriendsPlayer]
    ) -> tuple[HanginWithFriendsPlayer, HanginWithFriendsPlayer]:
        cap = 2
        if self.winner_streak_id and self.winner_streak_count >= cap:
            setter = self._pick_least_recent(eligible, exclude_id="")
            guesser = self._pick_least_recent(eligible, exclude_id=setter.id)
            return (setter, guesser)
        return self._pair_winner_fair(eligible)

    def _pair_host_queue(
        self, eligible: list[HanginWithFriendsPlayer]
    ) -> tuple[HanginWithFriendsPlayer, HanginWithFriendsPlayer]:
        order = self._get_pairing_order(eligible)
        if not order:
            return (eligible[0], eligible[0])
        if self.round == 1 and self.host:
            host_id = next((p.id for p in eligible if p.name == self.host), order[0])
            self.host_queue_index = (order.index(host_id) + 1) % len(order)
            setter = self._get_player_by_id_or_fallback(host_id, eligible)
            guesser = self._pick_random_other(eligible, setter.id)
            return (setter, guesser)
        idx = self.host_queue_index % len(order)
        setter = self._get_player_by_id_or_fallback(order[idx], eligible)
        guesser = self._get_player_by_id_or_fallback(order[(idx + 1) % len(order)], eligible)
        self.host_queue_index = (idx + 1) % len(order)
        return (setter, guesser)

    def _pair_performance(
        self, eligible: list[HanginWithFriendsPlayer]
    ) -> tuple[HanginWithFriendsPlayer, HanginWithFriendsPlayer]:
        ranked = sorted(eligible, key=lambda p: (p.score, p.balloons_remaining))
        guesser = ranked[0]
        setter = ranked[-1] if ranked[-1].id != guesser.id else ranked[0]
        if setter.id == guesser.id and len(ranked) > 1:
            setter = ranked[-1]
        return (setter, guesser)

    def _pick_fair_opponent(
        self, eligible: list[HanginWithFriendsPlayer], exclude_id: str
    ) -> HanginWithFriendsPlayer:
        candidates = [p for p in eligible if p.id != exclude_id]
        if not candidates:
            return self._get_player_by_id_or_fallback(exclude_id, eligible)
        never_played = [p for p in candidates if p.id not in self.has_played_ids]
        if never_played:
            return random.choice(never_played)
        return self._pick_least_recent(candidates, exclude_id="")

    def _pick_least_recent(
        self, eligible: list[HanginWithFriendsPlayer], exclude_id: str
    ) -> HanginWithFriendsPlayer:
        candidates = [p for p in eligible if p.id != exclude_id] or eligible
        min_round = min(self.last_played_round.get(p.id, 0) for p in candidates)
        tied = [p for p in candidates if self.last_played_round.get(p.id, 0) == min_round]
        return random.choice(tied)

    def _weight_for_player(self, player_id: str) -> int:
        last_round = self.last_played_round.get(player_id, 0)
        return max(1, self.round - last_round)

    def _weighted_choice(
        self,
        candidates: list[HanginWithFriendsPlayer],
        weights: dict[str, int],
    ) -> HanginWithFriendsPlayer:
        total = sum(weights.get(p.id, 1) for p in candidates)
        if total <= 0:
            return random.choice(candidates)
        roll = random.uniform(0, total)
        upto = 0.0
        for p in candidates:
            upto += weights.get(p.id, 1)
            if roll <= upto:
                return p
        return candidates[-1]

    def _get_pairing_order(self, eligible: list[HanginWithFriendsPlayer]) -> list[str]:
        if self.participant_ids:
            order = [pid for pid in self.participant_ids if any(p.id == pid for p in eligible)]
            if order:
                return order
        return [p.id for p in eligible]

    def _get_player_by_id_or_fallback(
        self, player_id: str, eligible: list[HanginWithFriendsPlayer]
    ) -> HanginWithFriendsPlayer:
        player = self.get_player_by_id(player_id)
        if isinstance(player, HanginWithFriendsPlayer) and player in eligible:
            return player
        return eligible[0]

    def _pick_random_other(
        self, eligible: list[HanginWithFriendsPlayer], exclude_id: str
    ) -> HanginWithFriendsPlayer:
        candidates = [p for p in eligible if p.id != exclude_id]
        return random.choice(candidates) if candidates else eligible[0]

    def _mark_players_as_played(
        self, setter: HanginWithFriendsPlayer, guesser: HanginWithFriendsPlayer
    ) -> None:
        if setter.id not in self.has_played_ids:
            self.has_played_ids.append(setter.id)
        if guesser.id not in self.has_played_ids:
            self.has_played_ids.append(guesser.id)
        self.last_played_round[setter.id] = self.round
        self.last_played_round[guesser.id] = self.round

    def _announce_guess_state(self, *, delay_ticks: int = 0) -> int:
        total_board_ticks = self._schedule_board_readout(delay_ticks=delay_ticks)
        summary_delay = total_board_ticks + self._pacing_ticks("post_board_pause")
        summary_text = self._format_board_summary()
        self.schedule_timeline_speech(
            summary_text,
            delay_ticks=summary_delay,
            buffer="table",
            include_spectators=True,
            tag="hwf-board-readout",
        )
        # Spectator boards are available via hotkeys instead of auto speech.
        return summary_delay + self.estimate_speech_ticks(summary_text)

    def _announce_balloons(self) -> str:
        parts = [f"{p.name}: {p.balloons_remaining} balloons" for p in self._get_participant_players()]
        line = " | ".join(parts)
        self.broadcast(line)
        return line

    def _check_match_end(self) -> bool:
        players = self._get_participant_players()
        if not players:
            return False

        ranked = sorted(players, key=lambda p: (p.score, p.balloons_remaining), reverse=True)
        winner = ranked[0]
        contenders = [p for p in players if p.balloons_remaining > 0]

        if len(players) == 1 and players[0].balloons_remaining <= 0:
            self._finish_with_winner(
                winner,
                f"{winner.name} ran out of balloons. Match over.",
            )
            return True

        if self.options.max_score > 0 and winner.score >= self.options.max_score:
            self._finish_with_winner(winner, f"Score limit {self.options.max_score} reached. {winner.name} wins the match.")
            return True

        if self.options.max_rounds > 0 and self.round >= self.options.max_rounds:
            self._finish_with_winner(winner, f"Round limit {self.options.max_rounds} reached. {winner.name} wins the match.")
            return True

        if len(players) > 1 and len(contenders) <= 1:
            if contenders:
                self._finish_with_winner(
                    contenders[0],
                    f"All but one player ran out of balloons. {contenders[0].name} wins the match.",
                )
            else:
                self._finish_with_winner(
                    winner,
                    f"All players ran out of balloons. {winner.name} wins the match by score.",
                )
            return True

        return False

    def _broadcast_private_to_spectators(
        self, text: str, *, delay_ticks: int = 0, tag: str = ""
    ) -> None:
        if not self.options.spectators_see_all_actions:
            return
        if delay_ticks > 0:
            self.schedule_timeline_speech(
                text,
                delay_ticks=delay_ticks,
                buffer="table",
                only_spectators=True,
                tag=tag,
            )
            return
        for player in self.players:
            if player.is_spectator:
                user = self.get_user(player)
                if user:
                    user.speak(text, "table")

    def _broadcast_spectator_player_boards(self, *, delay_ticks: int = 0) -> None:
        if not self.options.spectators_see_all_actions:
            return
        for participant in self._get_participant_players():
            if participant.is_spectator:
                continue
            self._broadcast_private_to_spectators(
                f"{participant.name} board: score {participant.score}, balloons {participant.balloons_remaining}, "
                f"coins {participant.coins}, reveal {participant.lifeline_reveal}, "
                f"remove {participant.lifeline_remove}, retry {participant.lifeline_retry}.",
                delay_ticks=delay_ticks,
                tag="hwf-board-readout",
            )

    def _get_participant_players(self) -> list[HanginWithFriendsPlayer]:
        if self.participant_ids:
            out: list[HanginWithFriendsPlayer] = []
            for pid in self.participant_ids:
                p = self.get_player_by_id(pid)
                if isinstance(p, HanginWithFriendsPlayer):
                    out.append(p)
            if out:
                return out
        return [p for p in self.players if isinstance(p, HanginWithFriendsPlayer)]

    def _get_round_eligible_players(self) -> list[HanginWithFriendsPlayer]:
        return [
            p
            for p in self._get_participant_players()
            if not p.is_spectator and p.balloons_remaining > 0
        ]

    def _eliminate_players_without_balloons(self, *, speak: bool = True) -> list[str]:
        eliminated_messages: list[str] = []
        for p in self._get_participant_players():
            if p.balloons_remaining > 0 or p.is_spectator:
                continue
            p.is_spectator = True
            self.last_eliminated_names.append(p.name)
            message = f"{p.name} is eliminated and now spectating."
            if speak:
                self.broadcast(message)
            eliminated_messages.append(message)
        return eliminated_messages

    def _finish_with_winner(self, winner: HanginWithFriendsPlayer, message: str) -> None:
        self._clear_round_timeline()
        self.timer.clear()
        self.phase = "game_end"
        self.last_match_end_message = message
        self.broadcast("Match over.")
        for p in self.get_active_players():
            user = self.get_user(p)
            if not user:
                continue
            if p.id == winner.id:
                user.play_sound(SOUNDS["win"])
            else:
                user.play_sound(SOUNDS["lose"])
        self.finish_game()

    def _start_turn_timer(self) -> None:
        seconds = self.options.round_timer_seconds
        if seconds <= 0:
            self.timer.clear()
            return
        self.timer.start(seconds)
        self.timer_warning_played = False

    def _maybe_play_timer_warning(self) -> None:
        seconds = self.options.round_timer_seconds
        if seconds < 20 or seconds <= 0:
            return
        if self.timer_warning_played:
            return
        if self.timer.seconds_remaining() == 5:
            self.timer_warning_played = True
            self.play_sound(SOUNDS["click2"], volume=40)

    def _handle_turn_timeout(self) -> None:
        if self.phase != "guessing":
            return
        player = self.get_player_by_id(self.guesser_id)
        if not isinstance(player, HanginWithFriendsPlayer):
            return
        letter = self._pick_random_rack_letter()
        if not letter:
            return
        self._resolve_letter_guess(letter)

    # bot logic
    def bot_think(self, player: HanginWithFriendsPlayer) -> str | None:
        if self.phase == "choose_word" and player.id == self.setter_id:
            return "choose_word"
        if self.phase != "guessing" or player.id != self.guesser_id:
            return None

        # use lifelines first if needed
        if player.lifeline_remove > 0 and self.wrong_guesses >= max(1, self.max_wrong_guesses - 1):
            return "lifeline_remove"
        if player.lifeline_retry > 0 and not player.retry_shield_active and self.wrong_guesses >= max(1, self.max_wrong_guesses - 2):
            return "lifeline_retry"
        unknown_count = self.masked_word.count("_")
        if player.lifeline_reveal > 0 and unknown_count >= 4:
            return "lifeline_reveal"

        candidates = self._get_candidate_words()
        difficulty = self._effective_bot_difficulty(player)
        if difficulty == "easy":
            letter = self._easy_pick_letter()
        elif difficulty == "medium":
            letter = self._best_guess_letter(candidates)
        elif difficulty == "hard":
            letter = self._best_pick_letter_elimination(candidates)
        else:
            letter = self._best_pick_letter_entropy(candidates)
        if not letter:
            for char in string.ascii_lowercase:
                if char not in self.guessed_letters:
                    letter = char
                    break
        return f"guess_letter_{letter}" if letter else None

    def _bot_choose_word_input(self, player: Player) -> str:
        candidates = self._get_words_for_rack()
        if not candidates:
            rack_letters = self.tile_rack[: self.options.max_word_length]
            return "".join(rack_letters[: self.options.min_word_length])
        return self._select_bot_word_by_difficulty(candidates, self._effective_bot_difficulty(player))

    def _get_words_for_rack(self) -> list[str]:
        return [w for w in self._dictionary_words if self._word_uses_rack(w)]

    def _get_candidate_words(self) -> list[str]:
        if not self.secret_word:
            return []
        return self._get_words_matching_row(
            words=self._dictionary_words,
            row=self.masked_word,
            tried_letters=set(self.guessed_letters),
        )

    def _word_matches_row(self, word: str, row: str) -> bool:
        if len(word) != len(row):
            return False
        for idx, val in enumerate(row):
            if val in ("_", "?"):
                continue
            if word[idx] != val:
                return False
        return True

    def _get_strike_letters(self, row: str, tried_letters: set[str]) -> set[str]:
        row_letters = {ch for ch in row if ch not in ("_", "?")}
        return {letter for letter in tried_letters if letter not in row_letters}

    def _get_words_matching_row(
        self, words: tuple[str, ...] | list[str], row: str, tried_letters: set[str]
    ) -> list[str]:
        strike_letters = self._get_strike_letters(row=row, tried_letters=tried_letters)
        out: list[str] = []
        for word in words:
            if not self._word_matches_row(word=word, row=row):
                continue
            if any(letter in word for letter in strike_letters):
                continue
            out.append(word)
        return out

    def _get_letter_frequencies(
        self, words: list[str], row: str, tried_letters: set[str]
    ) -> dict[str, int]:
        strike_letters = self._get_strike_letters(row=row, tried_letters=tried_letters)
        letters_on_row = {letter for letter in row if letter not in ("_", "?")}
        freqs: dict[str, int] = {}
        for word in words:
            for letter in set(word):
                if letter in letters_on_row or letter in strike_letters:
                    continue
                freqs[letter] = freqs.get(letter, 0) + 1
        return freqs

    def _best_guess_letter(self, candidates: list[str]) -> str | None:
        freqs: dict[str, int] = {}
        guessed_set = set(self.guessed_letters)
        for word in candidates:
            for char in set(word):
                if char in guessed_set:
                    continue
                freqs[char] = freqs.get(char, 0) + 1
        if not freqs:
            return None
        return max(freqs.items(), key=lambda kv: (kv[1], kv[0]))[0]

    def _easy_pick_letter(self) -> str | None:
        return self._pick_random_rack_letter()

    def _best_pick_letter_elimination(self, candidates: list[str]) -> str | None:
        if not candidates:
            return None
        freqs = self._get_letter_frequencies(
            words=candidates,
            row=self.masked_word,
            tried_letters=set(self.guessed_letters),
        )
        if not freqs:
            return None
        return max(freqs.items(), key=lambda kv: (kv[1], kv[0]))[0]

    def _best_pick_letter_entropy(self, candidates: list[str]) -> str | None:
        if not candidates:
            return None
        total = len(candidates)
        if total == 0:
            return None
        guessed = set(self.guessed_letters)
        best_letter: str | None = None
        best_score = -1
        for letter in string.ascii_lowercase:
            if letter in guessed:
                continue
            present = sum(1 for word in candidates if letter in word)
            absent = total - present
            score = min(present, absent)
            if score > best_score or (score == best_score and best_letter and letter > best_letter):
                best_score = score
                best_letter = letter
        return best_letter

    def _debug_best_pick(self) -> dict[str, str | int | None]:
        candidates = self._get_candidate_words()
        return {
            "candidate_count": len(candidates),
            "easy": self._easy_pick_letter(),
            "medium": self._best_guess_letter(candidates),
            "hard": self._best_pick_letter_elimination(candidates),
            "extreme": self._best_pick_letter_entropy(candidates),
        }

    def _score_word(self, word: str) -> int:
        return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)

    def _select_bot_word_by_difficulty(self, candidates: list[str], difficulty: str | None = None) -> str:
        ranked = sorted(candidates, key=lambda w: (self._score_word(w), len(w), w))
        bucketed = self._build_score_buckets(ranked)
        selected = self._normalize_bot_difficulty(difficulty or self.options.default_bot_difficulty)
        bucket_index = {"easy": 0, "medium": 1, "hard": 2, "extreme": 3}[selected]
        return bucketed[bucket_index][-1]

    def _build_score_buckets(self, ranked: list[str]) -> list[list[str]]:
        n = len(ranked)
        if n == 0:
            return [[], [], [], []]

        boundaries = [0, math.ceil(n * 0.25), math.ceil(n * 0.5), math.ceil(n * 0.75), n]
        buckets = [ranked[boundaries[i] : boundaries[i + 1]] for i in range(4)]

        for idx in range(4):
            if buckets[idx]:
                continue
            left = idx - 1
            right = idx + 1
            while left >= 0 or right <= 3:
                if left >= 0 and buckets[left]:
                    buckets[idx] = buckets[left]
                    break
                if right <= 3 and buckets[right]:
                    buckets[idx] = buckets[right]
                    break
                left -= 1
                right += 1

        return buckets

    def _normalize_bot_difficulty(self, value: str) -> str:
        normalized = value.strip().lower()
        return normalized if normalized in {"easy", "medium", "hard", "extreme"} else "medium"

    def _effective_bot_difficulty(self, player: Player) -> str:
        self._sync_bot_difficulty_overrides()
        if player.is_bot and player.id in self.bot_difficulties:
            return self._normalize_bot_difficulty(self.bot_difficulties[player.id])
        return self._normalize_bot_difficulty(self.options.default_bot_difficulty)

    def _sync_bot_difficulty_overrides(self) -> None:
        bot_ids = {p.id for p in self.players if p.is_bot}
        stale = [pid for pid in self.bot_difficulties if pid not in bot_ids]
        for pid in stale:
            self.bot_difficulties.pop(pid, None)

        default = self._normalize_bot_difficulty(self.options.default_bot_difficulty)
        for pid in bot_ids:
            self.bot_difficulties.setdefault(pid, default)

    def _per_bot_difficulty_options(self, player: Player) -> list[str]:
        self._sync_bot_difficulty_overrides()
        options: list[str] = []
        for bot in [p for p in self.players if p.is_bot]:
            for difficulty in BOT_DIFFICULTY_CHOICES:
                options.append(f"{bot.name}|{difficulty}")
        return options

    def _action_add_bot(self, player: Player, bot_name: str, action_id: str) -> None:
        super()._action_add_bot(player, bot_name, action_id)
        self._sync_bot_difficulty_overrides()

    def _action_remove_bot(self, player: Player, action_id: str) -> None:
        super()._action_remove_bot(player, action_id)
        self._sync_bot_difficulty_overrides()

    # utility
    def _generate_rack(self, round_number: int) -> list[str]:
        rng = random.Random(self.rng_seed + (round_number * 7919))
        return [rng.choice(LETTER_POOL).lower() for _ in range(self.options.rack_size)]

    def _format_positions(self, positions: list[int]) -> str:
        if not positions:
            return "none"
        return ", ".join(str(pos) for pos in sorted(positions))

    def _load_modifier_chances(self) -> None:
        config_path = Path(__file__).with_name("modifier_chances_by_length.json")
        if not config_path.exists():
            return
        try:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        parsed: dict[int, dict[str, float]] = {}
        for length_str, payload in raw.items():
            try:
                length = int(length_str)
            except (TypeError, ValueError):
                continue
            if length < 1 or not isinstance(payload, dict):
                continue
            row: dict[str, float] = {}
            for key in MODIFIER_ORDER:
                value = payload.get(key, 0.0)
                try:
                    row[key] = max(0.0, min(100.0, float(value)))
                except (TypeError, ValueError):
                    row[key] = 0.0
            parsed[length] = row
        self._modifier_chances_by_length = parsed

    def _modifier_chances_for_length(self, length: int) -> dict[str, float]:
        if length in self._modifier_chances_by_length:
            return self._modifier_chances_by_length[length]
        if not self._modifier_chances_by_length:
            return {
                "double_letter": 10.67,
                "triple_letter": 7.56,
                "double_word": 5.33,
                "triple_word": 3.56,
            }
        nearest = min(self._modifier_chances_by_length.keys(), key=lambda k: abs(k - length))
        return self._modifier_chances_by_length[nearest]

    def _roll_board_modifiers(self, word: str) -> dict[int, str]:
        chances = self._modifier_chances_for_length(len(word))
        modifiers: dict[int, str] = {}
        for idx in range(1, len(word) + 1):
            for kind in MODIFIER_ORDER:
                chance = chances.get(kind, 0.0)
                if random.random() * 100.0 < chance:
                    modifiers[idx] = kind
                    break
        return modifiers

    def _initialize_board(self, word: str) -> None:
        self.secret_word = word
        self.masked_word = "".join("_" for _ in word)
        self.board_modifiers = self._roll_board_modifiers(word)
        for idx in range(len(word) - 1, -1, -1):
            if word[idx] in VOWELS:
                self.masked_word = (
                    self.masked_word[:idx] + word[idx] + self.masked_word[idx + 1 :]
                )
                if word[idx] not in self.guessed_letters:
                    self.guessed_letters.append(word[idx])
                break

    def _format_board_modifiers_summary(self) -> str:
        compact = self._format_board_modifiers_compact()
        return f"Board modifiers: {compact}." if compact else "Board modifiers: none."

    def _score_word_with_board_modifiers(self, word: str) -> int:
        if not word:
            return 1

        subtotal = 0
        word_mult = 1
        for idx, letter in enumerate(word, start=1):
            letter_mult = 1
            kind = self.board_modifiers.get(idx)
            if kind == "double_letter":
                letter_mult *= 2
            if kind == "triple_letter":
                letter_mult *= 3
            subtotal += LETTER_SCORES.get(letter.upper(), 0) * letter_mult
            if kind == "double_word":
                word_mult *= 2
            if kind == "triple_word":
                word_mult *= 3
        return max(1, subtotal * word_mult)

    def _word_uses_rack(self, word: str) -> bool:
        rack_counts = Counter(self.tile_rack)
        word_counts = Counter(word)
        return all(rack_counts.get(letter, 0) >= count for letter, count in word_counts.items())

    def _normalize_word(self, value: str) -> str | None:
        word = value.strip().lower()
        return word if word.isalpha() else None

    def _spoken_board(self) -> str:
        """Format board for speech with comma-separated positions."""
        parts: list[str] = []
        for ch in self.masked_word:
            token = "blank" if ch == "_" else ch.lower()
            parts.append(token)
        return ", ".join(parts)

    def _spoken_board_tokens(self) -> list[str]:
        return [token.strip() for token in self._spoken_board().split(",")]

    def _schedule_board_readout(self, *, delay_ticks: int = 0) -> int:
        self.cancel_timeline("hwf-board-readout")
        board_text = self._format_board_summary()
        if not board_text:
            return delay_ticks
        self.schedule_timeline_speech(
            board_text,
            delay_ticks=delay_ticks,
            buffer="table",
            include_spectators=True,
            tag="hwf-board-readout",
        )
        return delay_ticks + self.estimate_speech_ticks(board_text)

    def _schedule_round_intro(self, text: str, *, delay_ticks: int | None = None) -> None:
        self.cancel_timeline("hwf-round-flow")
        self.schedule_timeline_speech(
            text,
            delay_ticks=self._pacing_ticks("turn_transition") if delay_ticks is None else delay_ticks,
            buffer="table",
            include_spectators=True,
            tag="hwf-round-flow",
        )

    def _load_dictionary(self) -> None:
        if self._dictionary_loaded:
            return
        selected = (
            self.options.word_list
            if self.options.word_list in WORD_LIST_CHOICES
            else "words"
        )
        filename = WORD_LIST_FILES[selected]
        candidate_paths = [
            Path(__file__).with_name("word_lists") / filename,
            Path("/tmp/hanging") / filename.replace(".gz", ""),
        ]
        loaded: list[str] = []
        for path in candidate_paths:
            if not path.exists():
                continue
            loaded = self._read_words(path)
            if loaded:
                break

        self._dictionary_words = tuple(loaded) if loaded else tuple(DEFAULT_WORDS)
        self._dictionary_loaded = True

    def _read_words(self, path: Path) -> list[str]:
        words: set[str] = set()
        max_words = 250000
        if path.suffix == ".gz":
            fp_ctx = gzip.open(path, "rt", encoding="utf-8", errors="ignore")
        else:
            fp_ctx = path.open("rt", encoding="utf-8", errors="ignore")
        with fp_ctx as fp:
            for line in fp:
                word = line.strip().lower()
                if not word.isalpha():
                    continue
                if not (self.options.min_word_length <= len(word) <= self.options.max_word_length):
                    continue
                words.add(word)
                if len(words) >= max_words:
                    break
        return sorted(words)

    def build_game_result(self) -> GameResult:
        players = self._get_participant_players()
        winner = max(players, key=lambda p: (p.score, p.balloons_remaining), default=None)
        return GameResult(
            game_type=self.get_type(),
            timestamp=datetime.now().isoformat(),
            duration_ticks=self.sound_scheduler_tick,
            player_results=[
                PlayerResult(
                    player_id=p.id,
                    player_name=p.name,
                    is_bot=p.is_bot,
                    is_virtual_bot=getattr(p, "is_virtual_bot", False),
                )
                for p in players
            ],
            custom_data={
                "winner_name": winner.name if winner else None,
                "rounds_played": self.round,
                "scores": {p.name: p.score for p in players},
                "balloons": {p.name: p.balloons_remaining for p in players},
                "coins": {p.name: p.coins for p in players},
                "wheel_result": self.wheel_result,
            },
        )

    def format_end_screen(self, result: GameResult, locale: str) -> list[str]:
        lines = [Localization.get(locale, "game-final-scores-header")]
        balloons = result.custom_data.get("balloons", {})
        scores = result.custom_data.get("scores", {})
        coins = result.custom_data.get("coins", {})
        for name in sorted(scores.keys()):
            lines.append(
                f"{name}: score {scores.get(name, 0)}, balloons {balloons.get(name, 0)}, coins {coins.get(name, 0)}"
            )
        winner = result.custom_data.get("winner_name")
        if winner:
            lines.append(f"Winner: {winner}")
        return lines

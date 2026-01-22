"""
Bot AI for Texas Hold'em.

Lightweight strategy based on preflop hand strength, position, stack size,
and postflop hand category.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...game_utils.poker_evaluator import best_hand
from .state import order_after_button

if TYPE_CHECKING:
    from .game import HoldemGame, HoldemPlayer


def bot_think(game: "HoldemGame", player: "HoldemPlayer") -> str | None:
    if game.current_player != player or not game.betting:
        return None

    to_call = game.betting.amount_to_call(player.id)
    can_raise = game.betting.can_raise()
    stack_bb = player.chips / max(1, game.current_big_blind or 1)
    position = _position_index(game, player)

    if len(game.community) < 3:
        strength = _preflop_strength(player)
        return _decide_preflop(strength, to_call, can_raise, stack_bb, position)

    score = None
    if len(player.hand) + len(game.community) >= 5:
        score, _ = best_hand(player.hand + game.community)
    return _decide_postflop(score, to_call, can_raise, stack_bb, position)


def _position_index(game: "HoldemGame", player: "HoldemPlayer") -> int:
    active = [p for p in game.get_active_players() if isinstance(p, type(player)) and not p.folded]
    active_ids = [p.id for p in active]
    order = order_after_button(active_ids, game.table_state.get_button_id(active_ids))
    if not order or player.id not in order:
        return 0
    return order.index(player.id)


def _preflop_strength(player: "HoldemPlayer") -> int:
    if len(player.hand) < 2:
        return 0
    ranks = sorted([_rank_value(c.rank) for c in player.hand], reverse=True)
    suited = player.hand[0].suit == player.hand[1].suit
    pair = ranks[0] == ranks[1]
    high, low = ranks
    gap = high - low
    broadway = high >= 10 and low >= 10

    if pair and high >= 11:
        return 4  # premium pair
    if (high == 14 and low >= 13) or (pair and high >= 9):
        return 3  # AK, QQ+, or medium pair
    if suited and (broadway or gap == 1):
        return 2  # suited broadway or connectors
    if high == 14 and low >= 10:
        return 2  # strong ace
    if pair:
        return 1  # small pair
    if suited and high >= 10:
        return 1
    return 0


def _decide_preflop(
    strength: int,
    to_call: int,
    can_raise: bool,
    stack_bb: float,
    position: int,
) -> str:
    late_position = position >= 2
    if to_call == 0:
        if can_raise and strength >= 2 and stack_bb >= 6:
            return "raise"
        return "call"
    if strength >= 3:
        if can_raise and stack_bb >= 8 and to_call <= stack_bb * 2:
            return "raise"
        return "call"
    if strength == 2:
        if to_call <= stack_bb and (late_position or stack_bb <= 10):
            return "call"
        return "fold"
    if strength == 1:
        if to_call <= max(1, stack_bb * 0.5) and late_position:
            return "call"
        return "fold"
    if to_call <= max(1, stack_bb * 0.2) and late_position:
        return "call"
    return "fold"


def _decide_postflop(
    score: tuple[int, tuple[int, ...]] | None,
    to_call: int,
    can_raise: bool,
    stack_bb: float,
    position: int,
) -> str:
    late_position = position >= 2
    if to_call == 0:
        if score and score[0] >= 2 and can_raise and stack_bb >= 6:
            return "raise"
        return "call"
    if score and score[0] >= 4:
        return "raise" if can_raise and stack_bb >= 6 else "call"
    if score and score[0] >= 2:
        if to_call <= max(1, stack_bb * 2):
            return "call"
        return "fold"
    if score and score[0] >= 1:
        if to_call <= max(1, stack_bb) and late_position:
            return "call"
        return "fold"
    if to_call <= max(1, stack_bb * 0.5) and late_position:
        return "call"
    return "fold"


def _rank_value(rank: int) -> int:
    return 14 if rank == 1 else rank

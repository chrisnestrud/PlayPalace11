# 1-4-24 (Midnight) game messages
# Note: Common messages like round-start, turn-start, target-score are in games.ftl

# Game info
game-name-midnight = 1-4-24
midnight-category = Игре са Коцкама

# Actions
midnight-roll = Бацајте коцке
midnight-keep-die = Задржите { $value }
midnight-bank = Потврдите

# Game events
midnight-turn-start = Ред играча { $player }.
midnight-you-rolled = Бацили сте: { $dice }.
midnight-player-rolled = { $player } је бацио: { $dice }.

# Keeping dice
midnight-you-keep = Задржавате { $die }.
midnight-player-keeps = { $player } задржава { $die }.
midnight-you-unkeep = Отпуштате { $die }.
midnight-player-unkeeps = { $player } отпушта { $die }.

# Turn status
midnight-you-have-kept = Задржане коцке: { $kept }. Преостала бацања: { $remaining }.
midnight-player-has-kept = { $player } је задржао: { $kept }. { $remaining } коцки преостало.

# Scoring
midnight-you-scored = Освојили сте { $score } поена.
midnight-scored = { $player } је освојио { $score } поена.
midnight-you-disqualified = Немате и 1 и 4. Дисквалификовани сте!
midnight-player-disqualified = { $player } нема и 1 и 4. Дисквалификован!

# Round results
midnight-round-winner = { $player } побеђује рунду!
midnight-round-tie = Рунда нерешена између { $players }.
midnight-all-disqualified = Сви играчи дисквалификовани! Нема победника ове рунде.

# Game winner
midnight-game-winner = { $player } побеђује игру са { $wins } победа у рундама!
midnight-game-tie = Нерешено! { $players } сваки је освојио { $wins } рунди.

# Options
midnight-set-rounds = Рунди за играње: { $rounds }
midnight-enter-rounds = Унесите број рунди за играње:
midnight-option-changed-rounds = Рунди за играње промењено на { $rounds }

# Disabled reasons
midnight-need-to-roll = Морате прво бацити коцке.
midnight-no-dice-to-keep = Нема доступних коцки за задржавање.
midnight-must-keep-one = Морате задржати најмање једну коцку по бацању.
midnight-must-roll-first = Морате прво бацити коцке.
midnight-keep-all-first = Морате задржати све коцке пре потврђивања.

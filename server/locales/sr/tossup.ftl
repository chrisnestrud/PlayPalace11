# Toss Up game messages
# Note: Common messages like round-start, turn-start, target-score are in games.ftl

# Game info
game-name-tossup = Бацање горе
tossup-category = Игре са коцкицама

# Actions
tossup-roll-first = Баци { $count } коцкица
tossup-roll-remaining = Баци преостале { $count } коцкице
tossup-bank = Сачувај { $points } поена

# Game events
tossup-turn-start = Потез играча { $player }. Резултат: { $score }
tossup-you-roll = Бацио си: { $results }.
tossup-player-rolls = { $player } је бацио: { $results }.

# Turn status
tossup-you-have-points = Поени потеза: { $turn_points }. Преостало коцкица: { $dice_count }.
tossup-player-has-points = { $player } има { $turn_points } поена потеза. Преостало { $dice_count } коцкица.

# Fresh dice
tossup-you-get-fresh = Нема коцкица! Добијате { $count } нових коцкица.
tossup-player-gets-fresh = { $player } добија { $count } нових коцкица.

# Bust
tossup-you-bust = Пропаст! Губите { $points } поена за овај потез.
tossup-player-busts = { $player } пропада и губи { $points } поена!

# Bank
tossup-you-bank = Чувате { $points } поена. Укупан резултат: { $total }.
tossup-player-banks = { $player } чува { $points } поена. Укупан резултат: { $total }.

# Winner
tossup-winner = { $player } побеђује са { $score } поена!
tossup-tie-tiebreaker = Изједначено између { $players }! Одлучујућа рунда!

# Options
tossup-set-rules-variant = Варијанта правила: { $variant }
tossup-select-rules-variant = Одаберите варијанту правила:
tossup-option-changed-rules = Варијанта правила промењена на { $variant }

tossup-set-starting-dice = Почетне коцкице: { $count }
tossup-enter-starting-dice = Унесите број почетних коцкица:
tossup-option-changed-dice = Почетне коцкице промењене на { $count }

# Rules variants
tossup-rules-standard = Стандардно
tossup-rules-playpalace = PlayPalace

# Rules explanations
tossup-rules-standard-desc = 3 зелене, 2 жуте, 1 црвена по коцкици. Пропаст ако нема зелених и барем једна црвена.
tossup-rules-playpalace-desc = Равномерна расподела. Пропаст ако су све коцкице црвене.

# Disabled reasons
tossup-need-points = Требате поене за чување.

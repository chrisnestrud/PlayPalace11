# Pig game messages
# Note: Common messages like round-start, turn-start, target-score are in games.ftl

# Game info
game-name-pig = Прасе
pig-category = Игре са коцкицама

# Actions
pig-roll = Баци коцку
pig-bank = Сачувај { $points } поена

# Game events (Pig-specific)
pig-rolls = { $player } баца коцку...
pig-roll-result = { $roll }, укупно { $total }
pig-bust = О не, јединица! { $player } губи { $points } поена.
pig-bank-action = { $player } одлучује да сачува { $points }, укупно { $total }
pig-winner = Имамо победника, и то је { $player }!

# Pig-specific options
pig-set-min-bank = Минимално чување: { $points }
pig-set-dice-sides = Стране коцке: { $sides }
pig-enter-min-bank = Унесите минималне поене за чување:
pig-enter-dice-sides = Унесите број страна коцке:
pig-option-changed-min-bank = Минимални поени за чување промењени на { $points }
pig-option-changed-dice = Коцка сада има { $sides } страна

# Disabled reasons
pig-need-more-points = Требате више поена за чување.

# Validation errors
pig-error-min-bank-too-high = Минимални поени за чување морају бити мањи од циљног резултата.

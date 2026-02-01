# Farkle game messages

# Game info
game-name-farkle = Farkle

# Actions - Roll and Bank
farkle-roll = Баците { $count } { $count ->
    [one] коцку
   *[other] коцкица
}
farkle-bank = Спремите { $points } поена

# Scoring combination actions (matching v10 exactly)
farkle-take-single-one = Једна 1 за { $points } поена
farkle-take-single-five = Једна 5 за { $points } поена
farkle-take-three-kind = Три { $number } за { $points } поена
farkle-take-four-kind = Четири { $number } за { $points } поена
farkle-take-five-kind = Пет { $number } за { $points } поена
farkle-take-six-kind = Шест { $number } за { $points } поена
farkle-take-small-straight = Мали низ за { $points } поена
farkle-take-large-straight = Велики низ за { $points } поена
farkle-take-three-pairs = Три пара за { $points } поена
farkle-take-double-triplets = Двоструки тројци за { $points } поена
farkle-take-full-house = Пуна кућа за { $points } поена

# Game events (matching v10 exactly)
farkle-rolls = { $player } баца { $count } { $count ->
    [one] коцку
   *[other] коцкица
}...
farkle-you-roll = Бацате { $count } { $count ->
    [one] коцку
   *[other] коцкица
}...
farkle-roll-result = { $dice }
farkle-farkle = FARKLE! { $player } губи { $points } поена
farkle-you-farkle = FARKLE! Губите { $points } поена
farkle-takes-combo = { $player } узима { $combo } за { $points } поена
farkle-you-take-combo = Узимате { $combo } за { $points } поена
farkle-hot-dice = Вруће коцкице!
farkle-banks = { $player } спрема { $points } поена за укупно { $total }
farkle-you-bank = Спремате { $points } поена за укупно { $total }
farkle-winner = { $player } побеђује са { $score } поена!
farkle-you-win = Побеђујете са { $score } поена!
farkle-winners-tie = Имамо нерешено! Победници: { $players }

# Check turn score action
farkle-turn-score = { $player } има { $points } поена овог потеза.
farkle-no-turn = Тренутно нико није на потезу.

# Farkle-specific options
farkle-set-target-score = Циљни резултат: { $score }
farkle-enter-target-score = Унесите циљни резултат (500-5000):
farkle-option-changed-target = Циљни резултат постављен на { $score }.

# Disabled action reasons
farkle-must-take-combo = Морате прво узети комбинацију за бодовање.
farkle-cannot-bank = Тренутно не можете спремити.

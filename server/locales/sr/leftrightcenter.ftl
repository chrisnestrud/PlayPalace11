# Messages for Left Right Center (Serbian)

# Game name
game-name-leftrightcenter = Лево Десно Центар

# Actions
lrc-roll = Баци { $count } { $count ->
    [one] коцкицу
   *[other] коцкица
}

# Dice faces
lrc-face-left = Лево
lrc-face-right = Десно
lrc-face-center = Центар
lrc-face-dot = Тачка

# Game events
lrc-roll-results = { $player } је бацио { $results }.
lrc-pass-left = { $player } преда { $count } { $count ->
    [one] жетон
   *[other] жетона
} играчу { $target }.
lrc-pass-right = { $player } преда { $count } { $count ->
    [one] жетон
   *[other] жетона
} играчу { $target }.
lrc-pass-center = { $player } ставља { $count } { $count ->
    [one] жетон
   *[other] жетона
} у центар.
lrc-no-chips = { $player } нема жетона за бацање.
lrc-center-pot = { $count } { $count ->
    [one] жетон
   *[other] жетона
} у центру.
lrc-player-chips = { $player } сада има { $count } { $count ->
    [one] жетон
   *[other] жетона
}.
lrc-winner = { $player } побеђује са { $count } { $count ->
    [one] жетоном
   *[other] жетона
}!

# Options
lrc-set-starting-chips = Почетни жетони: { $count }
lrc-enter-starting-chips = Унесите почетне жетоне:
lrc-option-changed-starting-chips = Почетни жетони постављени на { $count }.

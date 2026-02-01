# Messages for Left Right Center (English)

# Game name
game-name-leftrightcenter = Left Right Center

# Actions
lrc-roll = Tirar { $count } { $count ->
    [one] dado
   *[other] dados
}

# Dice faces
lrc-face-left = Izquierda
lrc-face-right = Derecha
lrc-face-center = Centro
lrc-face-dot = Punto

# Game events
lrc-roll-results = { $player } saca { $results }.
lrc-pass-left = { $player } pasa { $count } { $count ->
    [one] ficha
   *[other] fichas
} a { $target }.
lrc-pass-right = { $player } pasa { $count } { $count ->
    [one] ficha
   *[other] fichas
} a { $target }.
lrc-pass-center = { $player } pone { $count } { $count ->
    [one] ficha
   *[other] fichas
} en el centro.
lrc-no-chips = { $player } no tiene fichas para tirar.
lrc-center-pot = { $count } { $count ->
    [one] ficha
   *[other] fichas
} en el centro.
lrc-player-chips = { $player } ahora tiene { $count } { $count ->
    [one] ficha
   *[other] fichas
}.
lrc-winner = ¡{ $player } gana con { $count } { $count ->
    [one] ficha
   *[other] fichas
}!

# Options
lrc-set-starting-chips = Fichas iniciales: { $count }
lrc-enter-starting-chips = Ingresa las fichas iniciales:
lrc-option-changed-starting-chips = Fichas iniciales establecidas en { $count }.

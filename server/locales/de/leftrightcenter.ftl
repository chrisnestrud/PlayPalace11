# Nachrichten für Left Right Center (Deutsch)

# Spielname
game-name-leftrightcenter = Left Right Center

# Aktionen
lrc-roll = { $count } { $count ->
    [one] Würfel
   *[other] Würfel
} würfeln

# Würfelseiten
lrc-face-left = Links
lrc-face-right = Rechts
lrc-face-center = Mitte
lrc-face-dot = Punkt

# Spielereignisse
lrc-roll-results = { $player } würfelt { $results }.
lrc-pass-left = { $player } gibt { $count } { $count ->
    [one] Chip
   *[other] Chips
} an { $target } weiter.
lrc-pass-right = { $player } gibt { $count } { $count ->
    [one] Chip
   *[other] Chips
} an { $target } weiter.
lrc-pass-center = { $player } legt { $count } { $count ->
    [one] Chip
   *[other] Chips
} in die Mitte.
lrc-no-chips = { $player } hat keine Chips zum Würfeln.
lrc-center-pot = { $count } { $count ->
    [one] Chip
   *[other] Chips
} in der Mitte.
lrc-player-chips = { $player } hat jetzt { $count } { $count ->
    [one] Chip
   *[other] Chips
}.
lrc-winner = { $player } gewinnt mit { $count } { $count ->
    [one] Chip
   *[other] Chips
}!

# Optionen
lrc-set-starting-chips = Startchips: { $count }
lrc-enter-starting-chips = Startchips eingeben:
lrc-option-changed-starting-chips = Startchips auf { $count } gesetzt.

# Five Card Draw

game-name-fivecarddraw = Five Card Draw

draw-set-starting-chips = Startchips: { $count }
draw-enter-starting-chips = Startchips eingeben
draw-option-changed-starting-chips = Startchips auf { $count } gesetzt.

draw-set-ante = Ante: { $count }
draw-enter-ante = Ante-Betrag eingeben
draw-option-changed-ante = Ante auf { $count } gesetzt.

draw-set-turn-timer = Zugzeitmesser: { $mode }
draw-select-turn-timer = Zugzeitmesser auswählen
draw-option-changed-turn-timer = Zugzeitmesser auf { $mode } gesetzt.

draw-set-raise-mode = Erhöhungsmodus: { $mode }
draw-select-raise-mode = Erhöhungsmodus auswählen
draw-option-changed-raise-mode = Erhöhungsmodus auf { $mode } gesetzt.

draw-set-max-raises = Max. Erhöhungen: { $count }
draw-enter-max-raises = Max. Erhöhungen eingeben (0 für unbegrenzt)
draw-option-changed-max-raises = Max. Erhöhungen auf { $count } gesetzt.

draw-antes-posted = Antes gesetzt: { $amount }.
draw-betting-round-1 = Setzrunde.
draw-betting-round-2 = Setzrunde.
draw-begin-draw = Ziehphase.
draw-not-draw-phase = Es ist nicht Zeit zum Ziehen.
draw-not-betting = Sie können während der Ziehphase nicht setzen.

draw-toggle-discard = Ablegen für Karte { $index } umschalten
draw-card-keep = { $card }, behalten
draw-card-discard = { $card }, wird abgelegt
draw-card-kept = { $card } behalten.
draw-card-discarded = { $card } ablegen.
draw-draw-cards = Karten ziehen
draw-draw-cards-count = { $count } { $count ->
    [one] Karte
   *[other] Karten
} ziehen
draw-dealt-cards = Sie erhalten { $cards }.
draw-you-drew-cards = Sie ziehen { $cards }.
draw-you-draw = Sie ziehen { $count } { $count ->
    [one] Karte
   *[other] Karten
}.
draw-player-draws = { $player } zieht { $count } { $count ->
    [one] Karte
   *[other] Karten
}.
draw-you-stand-pat = Sie bleiben stehen.
draw-player-stands-pat = { $player } bleibt stehen.
draw-you-discard-limit = Sie dürfen bis zu { $count } Karten ablegen.
draw-player-discard-limit = { $player } darf bis zu { $count } Karten ablegen.

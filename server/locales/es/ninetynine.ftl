# Ninety Nine - English Localization
# Messages match v10 exactly

# Game info
ninetynine-name = Ninety Nine
ninetynine-description = Un juego de cartas donde los jugadores intentan evitar llevar el total por encima de 99. ¡El último jugador en pie gana!

# Round
ninetynine-round = Ronda { $round }.

# Turn
ninetynine-player-turn = Turno de { $player }.

# Playing cards - match v10 exactly
ninetynine-you-play = Juegas { $card }. El conteo ahora es { $count }.
ninetynine-player-plays = { $player } juega { $card }. El conteo ahora es { $count }.

# Direction reverse
ninetynine-direction-reverses = ¡La dirección de juego se invierte!

# Skip
ninetynine-player-skipped = { $player } es saltado.

# Token loss - match v10 exactly
ninetynine-you-lose-tokens = Pierdes { $amount } { $amount ->
    [one] ficha
    *[other] fichas
}.
ninetynine-player-loses-tokens = { $player } pierde { $amount } { $amount ->
    [one] ficha
    *[other] fichas
}.

# Elimination
ninetynine-player-eliminated = ¡{ $player } ha sido eliminado!

# Game end
ninetynine-player-wins = ¡{ $player } gana el juego!

# Dealing
ninetynine-you-deal = Repartes las cartas.
ninetynine-player-deals = { $player } reparte las cartas.

# Drawing cards
ninetynine-you-draw = Robas { $card }.
ninetynine-player-draws = { $player } roba una carta.

# No valid cards
ninetynine-no-valid-cards = ¡{ $player } no tiene cartas que no pasen de 99!

# Status - for C key
ninetynine-current-count = El conteo es { $count }.

# Hand check - for H key
ninetynine-hand-cards = Tus cartas: { $cards }.
ninetynine-hand-empty = No tienes cartas.

# Ace choice
ninetynine-ace-choice = ¿Jugar As como +1 o +11?
ninetynine-ace-add-eleven = Agregar 11
ninetynine-ace-add-one = Agregar 1

# Ten choice
ninetynine-ten-choice = ¿Jugar 10 como +10 o -10?
ninetynine-ten-add = Agregar 10
ninetynine-ten-subtract = Restar 10

# Manual draw
ninetynine-draw-card = Robar carta
ninetynine-draw-prompt = Presiona Espacio o D para robar una carta.

# Options
ninetynine-set-tokens = Fichas iniciales: { $tokens }
ninetynine-enter-tokens = Ingresa el número de fichas iniciales:
ninetynine-option-changed-tokens = Fichas iniciales establecidas en { $tokens }.
ninetynine-set-rules = Variante de reglas: { $rules }
ninetynine-select-rules = Selecciona la variante de reglas
ninetynine-option-changed-rules = Variante de reglas establecida en { $rules }.
ninetynine-set-hand-size = Tamaño de mano: { $size }
ninetynine-enter-hand-size = Ingresa el tamaño de mano:
ninetynine-option-changed-hand-size = Tamaño de mano establecido en { $size }.
ninetynine-set-autodraw = Robo automático: { $enabled }
ninetynine-option-changed-autodraw = Robo automático establecido en { $enabled }.

# Rules variant announcements (shown at game start)
ninetynine-rules-quentin = Reglas de Quentin C.
ninetynine-rules-rsgames = Reglas de RS Games.

# Rules variant choices (for menu display)
ninetynine-rules-variant-quentin_c = Quentin C
ninetynine-rules-variant-rs_games = RS Games

# Disabled action reasons
ninetynine-choose-first = Necesitas hacer una elección primero.
ninetynine-draw-first = Necesitas robar una carta primero.

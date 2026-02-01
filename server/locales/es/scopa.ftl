# Scopa game messages
# Note: Common messages like round-start, turn-start, target-score, team-mode are in games.ftl

# Game name
game-name-scopa = Scopa

# Game events
scopa-initial-table = Cartas de mesa: { $cards }
scopa-no-initial-table = No hay cartas en la mesa para comenzar.
scopa-you-collect = Recoges { $cards } con { $card }
scopa-player-collects = { $player } recoge { $cards } con { $card }
scopa-you-put-down = Pones { $card }.
scopa-player-puts-down = { $player } pone { $card }.
scopa-scopa-suffix =  - ¡SCOPA!
scopa-clear-table-suffix = , limpiando la mesa.
scopa-remaining-cards = { $player } obtiene las cartas restantes de la mesa.
scopa-scoring-round = Puntuando ronda...
scopa-most-cards = { $player } anota 1 punto por más cartas ({ $count } cartas).
scopa-most-cards-tie = Más cartas es un empate - no se otorga punto.
scopa-most-diamonds = { $player } anota 1 punto por más diamantes ({ $count } diamantes).
scopa-most-diamonds-tie = Más diamantes es un empate - no se otorga punto.
scopa-seven-diamonds = { $player } anota 1 punto por el 7 de diamantes.
scopa-seven-diamonds-multi = { $player } anota 1 punto por más 7 de diamantes ({ $count } × 7 de diamantes).
scopa-seven-diamonds-tie = 7 de diamantes es un empate - no se otorga punto.
scopa-most-sevens = { $player } anota 1 punto por más sietes ({ $count } sietes).
scopa-most-sevens-tie = Más sietes es un empate - no se otorga punto.
scopa-round-scores = Puntuaciones de ronda:
scopa-round-score-line = { $player }: +{ $round_score } (total: { $total_score })
scopa-table-empty = No hay cartas en la mesa.
scopa-no-such-card = No hay carta en esa posición.
scopa-captured-count = Has capturado { $count } cartas

# View actions
scopa-view-table = Ver mesa
scopa-view-captured = Ver capturadas

# Scopa-specific options
scopa-enter-target-score = Ingresa la puntuación objetivo (1-121)
scopa-set-cards-per-deal = Cartas por reparto: { $cards }
scopa-enter-cards-per-deal = Ingresa las cartas por reparto (1-10)
scopa-set-decks = Número de mazos: { $decks }
scopa-enter-decks = Ingresa el número de mazos (1-6)
scopa-toggle-escoba = Escoba (suma a 15): { $enabled }
scopa-toggle-hints = Mostrar pistas de captura: { $enabled }
scopa-set-mechanic = Mecánica de scopa: { $mechanic }
scopa-select-mechanic = Selecciona la mecánica de scopa
scopa-toggle-instant-win = Victoria instantánea en scopa: { $enabled }
scopa-toggle-team-scoring = Agrupar cartas de equipo para puntuación: { $enabled }
scopa-toggle-inverse = Modo inverso (alcanzar objetivo = eliminación): { $enabled }

# Option change announcements
scopa-option-changed-cards = Cartas por reparto establecidas en { $cards }.
scopa-option-changed-decks = Número de mazos establecido en { $decks }.
scopa-option-changed-escoba = Escoba { $enabled }.
scopa-option-changed-hints = Pistas de captura { $enabled }.
scopa-option-changed-mechanic = Mecánica de scopa establecida en { $mechanic }.
scopa-option-changed-instant = Victoria instantánea en scopa { $enabled }.
scopa-option-changed-team-scoring = Puntuación de cartas de equipo { $enabled }.
scopa-option-changed-inverse = Modo inverso { $enabled }.

# Scopa mechanic choices
scopa-mechanic-normal = Normal
scopa-mechanic-no_scopas = Sin Scopas
scopa-mechanic-only_scopas = Solo Scopas

# Disabled action reasons
scopa-timer-not-active = El temporizador de ronda no está activo.

# Validation errors
scopa-error-not-enough-cards = No hay suficientes cartas en { $decks } { $decks ->
    [one] mazo
    *[other] mazos
} para { $players } { $players ->
    [one] jugador
    *[other] jugadores
} con { $cards_per_deal } cartas cada uno. (Se necesitan { $cards_per_deal } × { $players } = { $cards_needed } cartas, pero solo hay { $total_cards }.)

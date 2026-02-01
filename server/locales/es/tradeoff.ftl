# Tradeoff game messages

# Game info
game-name-tradeoff = Tradeoff

# Round and iteration flow
tradeoff-round-start = Ronda { $round }.
tradeoff-iteration = Mano { $iteration } de 3.

# Phase 1: Trading
tradeoff-you-rolled = Sacaste: { $dice }.
tradeoff-toggle-trade = { $value } ({ $status })
tradeoff-trade-status-trading = intercambiando
tradeoff-trade-status-keeping = manteniendo
tradeoff-confirm-trades = Confirmar intercambios ({ $count } dados)
tradeoff-keeping = Manteniendo { $value }.
tradeoff-trading = Intercambiando { $value }.
tradeoff-player-traded = { $player } intercambió: { $dice }.
tradeoff-player-traded-none = { $player } mantuvo todos los dados.

# Phase 2: Taking from pool
tradeoff-your-turn-take = Tu turno para tomar un dado del grupo.
tradeoff-take-die = Tomar un { $value } ({ $remaining } restantes)
tradeoff-you-take = Tomas un { $value }.
tradeoff-player-takes = { $player } toma un { $value }.

# Phase 3: Scoring
tradeoff-player-scored = { $player } ({ $points } pts): { $sets }.
tradeoff-no-sets = { $player }: sin sets.

# Set descriptions (concise)
tradeoff-set-triple = trío de { $value }s
tradeoff-set-group = grupo de { $value }s
tradeoff-set-mini-straight = mini escalera { $low }-{ $high }
tradeoff-set-double-triple = doble trío ({ $v1 }s y { $v2 }s)
tradeoff-set-straight = escalera { $low }-{ $high }
tradeoff-set-double-group = doble grupo ({ $v1 }s y { $v2 }s)
tradeoff-set-all-groups = todos los grupos
tradeoff-set-all-triplets = todos los tríos

# Round end
tradeoff-round-scores = Puntuaciones de ronda { $round }:
tradeoff-score-line = { $player }: +{ $round_points } (total: { $total })
tradeoff-leader = { $player } lidera con { $score }.

# Game end
tradeoff-winner = ¡{ $player } gana con { $score } puntos!
tradeoff-winners-tie = ¡Es un empate! ¡{ $players } empataron con { $score } puntos!

# Status checks
tradeoff-view-hand = Ver tu mano
tradeoff-view-pool = Ver el grupo
tradeoff-view-players = Ver jugadores
tradeoff-hand-display = Tu mano ({ $count } dados): { $dice }
tradeoff-pool-display = Grupo ({ $count } dados): { $dice }
tradeoff-player-info = { $player }: { $hand }. Intercambió: { $traded }.
tradeoff-player-info-no-trade = { $player }: { $hand }. No intercambió nada.

# Error messages
tradeoff-not-trading-phase = No está en la fase de intercambio.
tradeoff-not-taking-phase = No está en la fase de tomar.
tradeoff-already-confirmed = Ya confirmado.
tradeoff-no-die = No hay dado para alternar.
tradeoff-no-more-takes = No hay más tomas disponibles.
tradeoff-not-in-pool = Ese dado no está en el grupo.

# Options
tradeoff-set-target = Puntuación objetivo: { $score }
tradeoff-enter-target = Ingresa la puntuación objetivo:
tradeoff-option-changed-target = Puntuación objetivo establecida en { $score }.

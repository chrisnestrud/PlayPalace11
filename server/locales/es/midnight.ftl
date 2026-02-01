# 1-4-24 (Midnight) game messages
# Note: Common messages like round-start, turn-start, target-score are in games.ftl

# Game info
game-name-midnight = 1-4-24
midnight-category = Juegos de Dados

# Actions
midnight-roll = Tirar los dados
midnight-keep-die = Mantener { $value }
midnight-bank = Guardar

# Game events
midnight-turn-start = Turno de { $player }.
midnight-you-rolled = Sacaste: { $dice }.
midnight-player-rolled = { $player } sacó: { $dice }.

# Keeping dice
midnight-you-keep = Mantienes { $die }.
midnight-player-keeps = { $player } mantiene { $die }.
midnight-you-unkeep = Dejas de mantener { $die }.
midnight-player-unkeeps = { $player } deja de mantener { $die }.

# Turn status
midnight-you-have-kept = Dados mantenidos: { $kept }. Tiradas restantes: { $remaining }.
midnight-player-has-kept = { $player } ha mantenido: { $kept }. { $remaining } dados restantes.

# Scoring
midnight-you-scored = Anotaste { $score } puntos.
midnight-scored = { $player } anotó { $score } puntos.
midnight-you-disqualified = No tienes 1 y 4. ¡Descalificado!
midnight-player-disqualified = { $player } no tiene 1 y 4. ¡Descalificado!

# Round results
midnight-round-winner = ¡{ $player } gana la ronda!
midnight-round-tie = Empate de ronda entre { $players }.
midnight-all-disqualified = ¡Todos los jugadores descalificados! Sin ganador esta ronda.

# Game winner
midnight-game-winner = ¡{ $player } gana el juego con { $wins } victorias de ronda!
midnight-game-tie = ¡Es un empate! { $players } ganaron { $wins } rondas cada uno.

# Options
midnight-set-rounds = Rondas a jugar: { $rounds }
midnight-enter-rounds = Ingresa el número de rondas a jugar:
midnight-option-changed-rounds = Rondas a jugar cambiadas a { $rounds }

# Disabled reasons
midnight-need-to-roll = Necesitas tirar los dados primero.
midnight-no-dice-to-keep = No hay dados disponibles para mantener.
midnight-must-keep-one = Debes mantener al menos un dado por tirada.
midnight-must-roll-first = Debes tirar los dados primero.
midnight-keep-all-first = Debes mantener todos los dados antes de guardar.

# Toss Up game messages
# Note: Common messages like round-start, turn-start, target-score are in games.ftl

# Game info
game-name-tossup = Toss Up
tossup-category = Juegos de Dados

# Actions
tossup-roll-first = Tirar { $count } dados
tossup-roll-remaining = Tirar { $count } dados restantes
tossup-bank = Guardar { $points } puntos

# Game events
tossup-turn-start = Turno de { $player }. Puntuación: { $score }
tossup-you-roll = Sacaste: { $results }.
tossup-player-rolls = { $player } sacó: { $results }.

# Turn status
tossup-you-have-points = Puntos del turno: { $turn_points }. Dados restantes: { $dice_count }.
tossup-player-has-points = { $player } tiene { $turn_points } puntos de turno. { $dice_count } dados restantes.

# Fresh dice
tossup-you-get-fresh = ¡No quedan dados! Obteniendo { $count } dados frescos.
tossup-player-gets-fresh = { $player } obtiene { $count } dados frescos.

# Bust
tossup-you-bust = ¡Busto! Pierdes { $points } puntos para este turno.
tossup-player-busts = ¡{ $player } hace busto y pierde { $points } puntos!

# Bank
tossup-you-bank = Guardas { $points } puntos. Puntuación total: { $total }.
tossup-player-banks = { $player } guarda { $points } puntos. Puntuación total: { $total }.

# Winner
tossup-winner = ¡{ $player } gana con { $score } puntos!
tossup-tie-tiebreaker = ¡Es un empate entre { $players }! ¡Ronda de desempate!

# Options
tossup-set-rules-variant = Variante de reglas: { $variant }
tossup-select-rules-variant = Selecciona la variante de reglas:
tossup-option-changed-rules = Variante de reglas cambiada a { $variant }

tossup-set-starting-dice = Dados iniciales: { $count }
tossup-enter-starting-dice = Ingresa el número de dados iniciales:
tossup-option-changed-dice = Dados iniciales cambiados a { $count }

# Rules variants
tossup-rules-standard = Estándar
tossup-rules-playpalace = PlayPalace

# Rules explanations
tossup-rules-standard-desc = 3 verdes, 2 amarillos, 1 rojo por dado. Busto si no hay verdes y al menos un rojo.
tossup-rules-playpalace-desc = Distribución equitativa. Busto si todos los dados son rojos.

# Disabled reasons
tossup-need-points = Necesitas puntos para guardar.

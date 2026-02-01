# Pig game messages
# Note: Common messages like round-start, turn-start, target-score are in games.ftl

# Game info
game-name-pig = Pig
pig-category = Juegos de Dados

# Actions
pig-roll = Tirar el dado
pig-bank = Guardar { $points } puntos

# Game events (Pig-specific)
pig-rolls = { $player } tira el dado...
pig-roll-result = Un { $roll }, para un total de { $total }
pig-bust = ¡Oh no, un 1! { $player } pierde { $points } puntos.
pig-bank-action = { $player } decide guardar { $points }, para un total de { $total }
pig-winner = ¡Tenemos un ganador, y es { $player }!

# Pig-specific options
pig-set-min-bank = Mínimo para guardar: { $points }
pig-set-dice-sides = Lados del dado: { $sides }
pig-enter-min-bank = Ingresa los puntos mínimos para guardar:
pig-enter-dice-sides = Ingresa el número de lados del dado:
pig-option-changed-min-bank = Puntos mínimos para guardar cambiados a { $points }
pig-option-changed-dice = El dado ahora tiene { $sides } lados

# Disabled reasons
pig-need-more-points = Necesitas más puntos para guardar.

# Validation errors
pig-error-min-bank-too-high = Los puntos mínimos para guardar deben ser menores que la puntuación objetivo.

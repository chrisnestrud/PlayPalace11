# Chaos Bear game messages

# Game name
game-name-chaosbear = Chaos Bear

# Actions
chaosbear-roll-dice = Tirar dados
chaosbear-draw-card = Robar una carta
chaosbear-check-status = Verificar estado

# Game intro (3 separate messages like v10)
chaosbear-intro-1 = ¡Chaos Bear ha comenzado! Todos los jugadores comienzan 30 casillas adelante del oso.
chaosbear-intro-2 = Tira dados para avanzar, y roba cartas en múltiplos de 5 para obtener efectos especiales.
chaosbear-intro-3 = ¡No dejes que el oso te atrape!

# Turn announcement
chaosbear-turn = Turno de { $player }; casilla { $position }.

# Rolling
chaosbear-roll = { $player } sacó { $roll }.
chaosbear-position = { $player } está ahora en la casilla { $position }.

# Drawing cards
chaosbear-draws-card = { $player } roba una carta.
chaosbear-card-impulsion = ¡Impulso! ¡{ $player } avanza 3 casillas a la casilla { $position }!
chaosbear-card-super-impulsion = ¡Súper impulso! ¡{ $player } avanza 5 casillas a la casilla { $position }!
chaosbear-card-tiredness = ¡Cansancio! Energía del oso menos 1. Ahora tiene { $energy } de energía.
chaosbear-card-hunger = ¡Hambre! Energía del oso más 1. Ahora tiene { $energy } de energía.
chaosbear-card-backward = ¡Empujón hacia atrás! { $player } retrocede a la casilla { $position }.
chaosbear-card-random-gift = ¡Regalo aleatorio!
chaosbear-gift-back = { $player } retrocedió a la casilla { $position }.
chaosbear-gift-forward = ¡{ $player } avanzó a la casilla { $position }!

# Bear turn
chaosbear-bear-roll = El oso sacó { $roll } + su energía de { $energy } = { $total }.
chaosbear-bear-energy-up = ¡El oso sacó un 3 y ganó 1 de energía!
chaosbear-bear-position = ¡El oso está ahora en la casilla { $position }!
chaosbear-player-caught = ¡El oso atrapó a { $player }! ¡{ $player } ha sido derrotado!
chaosbear-bear-feast = ¡El oso pierde 3 de energía después de darse un festín con su carne!

# Status check
chaosbear-status-player-alive = { $player }: casilla { $position }.
chaosbear-status-player-caught = { $player }: atrapado en la casilla { $position }.
chaosbear-status-bear = El oso está en la casilla { $position } con { $energy } de energía.

# End game
chaosbear-winner = ¡{ $player } sobrevivió y gana! ¡Alcanzó la casilla { $position }!
chaosbear-tie = ¡Es un empate en la casilla { $position }!

# Disabled action reasons
chaosbear-you-are-caught = Has sido atrapado por el oso.
chaosbear-not-on-multiple = Solo puedes robar cartas en múltiplos de 5.

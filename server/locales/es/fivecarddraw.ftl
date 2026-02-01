# Five Card Draw

game-name-fivecarddraw = Five Card Draw

draw-set-starting-chips = Fichas iniciales: { $count }
draw-enter-starting-chips = Ingresa las fichas iniciales
draw-option-changed-starting-chips = Fichas iniciales establecidas en { $count }.

draw-set-ante = Apuesta inicial: { $count }
draw-enter-ante = Ingresa el monto de apuesta inicial
draw-option-changed-ante = Apuesta inicial establecida en { $count }.

draw-set-turn-timer = Temporizador de turno: { $mode }
draw-select-turn-timer = Selecciona el temporizador de turno
draw-option-changed-turn-timer = Temporizador de turno establecido en { $mode }.

draw-set-raise-mode = Modo de apuesta: { $mode }
draw-select-raise-mode = Selecciona el modo de apuesta
draw-option-changed-raise-mode = Modo de apuesta establecido en { $mode }.

draw-set-max-raises = Máximo de apuestas: { $count }
draw-enter-max-raises = Ingresa el máximo de apuestas (0 para ilimitado)
draw-option-changed-max-raises = Máximo de apuestas establecido en { $count }.

draw-antes-posted = Apuestas iniciales puestas: { $amount }.
draw-betting-round-1 = Ronda de apuestas.
draw-betting-round-2 = Ronda de apuestas.
draw-begin-draw = Fase de robo.
draw-not-draw-phase = No es momento de robar.
draw-not-betting = No puedes apostar durante la fase de robo.

draw-toggle-discard = Alternar descarte para carta { $index }
draw-card-keep = { $card }, mantenida
draw-card-discard = { $card }, será descartada
draw-card-kept = Mantener { $card }.
draw-card-discarded = Descartar { $card }.
draw-draw-cards = Robar cartas
draw-draw-cards-count = Robar { $count } { $count ->
    [one] carta
   *[other] cartas
}
draw-dealt-cards = Se te reparten { $cards }.
draw-you-drew-cards = Robas { $cards }.
draw-you-draw = Robas { $count } { $count ->
    [one] carta
   *[other] cartas
}.
draw-player-draws = { $player } roba { $count } { $count ->
    [one] carta
   *[other] cartas
}.
draw-you-stand-pat = Te plantas.
draw-player-stands-pat = { $player } se planta.
draw-you-discard-limit = Puedes descartar hasta { $count } cartas.
draw-player-discard-limit = { $player } puede descartar hasta { $count } cartas.

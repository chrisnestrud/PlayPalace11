# Five Card Draw

game-name-fivecarddraw = Five Card Draw

draw-set-starting-chips = Jetons de départ : { $count }
draw-enter-starting-chips = Entrez les jetons de départ
draw-option-changed-starting-chips = Jetons de départ définis sur { $count }.

draw-set-ante = Ante : { $count }
draw-enter-ante = Entrez le montant de l'ante
draw-option-changed-ante = Ante définie sur { $count }.

draw-set-turn-timer = Minuterie de tour : { $mode }
draw-select-turn-timer = Sélectionnez la minuterie de tour
draw-option-changed-turn-timer = Minuterie de tour définie sur { $mode }.

draw-set-raise-mode = Mode de relance : { $mode }
draw-select-raise-mode = Sélectionnez le mode de relance
draw-option-changed-raise-mode = Mode de relance défini sur { $mode }.

draw-set-max-raises = Relances max : { $count }
draw-enter-max-raises = Entrez les relances max (0 pour illimité)
draw-option-changed-max-raises = Relances max définies sur { $count }.

draw-antes-posted = Antes payées : { $amount }.
draw-betting-round-1 = Tour de mise.
draw-betting-round-2 = Tour de mise.
draw-begin-draw = Phase de pioche.
draw-not-draw-phase = Ce n'est pas le moment de piocher.
draw-not-betting = Vous ne pouvez pas miser pendant la phase de pioche.

draw-toggle-discard = Basculer la défausse pour la carte { $index }
draw-card-keep = { $card }, gardée
draw-card-discard = { $card }, sera défaussée
draw-card-kept = Garde { $card }.
draw-card-discarded = Défausse { $card }.
draw-draw-cards = Piocher des cartes
draw-draw-cards-count = Piocher { $count } { $count ->
    [0] carte
    [1] carte
   *[other] cartes
}
draw-dealt-cards = Vous recevez { $cards }.
draw-you-drew-cards = Vous piochez { $cards }.
draw-you-draw = Vous piochez { $count } { $count ->
    [0] carte
    [1] carte
   *[other] cartes
}.
draw-player-draws = { $player } pioche { $count } { $count ->
    [0] carte
    [1] carte
   *[other] cartes
}.
draw-you-stand-pat = Vous restez pat.
draw-player-stands-pat = { $player } reste pat.
draw-you-discard-limit = Vous pouvez défausser jusqu'à { $count } cartes.
draw-player-discard-limit = { $player } peut défausser jusqu'à { $count } cartes.

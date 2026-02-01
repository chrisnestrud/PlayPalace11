# Messages du jeu Chaos Bear

# Nom du jeu
game-name-chaosbear = Chaos Bear

# Actions
chaosbear-roll-dice = Lancer les dés
chaosbear-draw-card = Piocher une carte
chaosbear-check-status = Vérifier le statut

# Intro du jeu (3 messages séparés comme dans la v10)
chaosbear-intro-1 = Chaos Bear a commencé ! Tous les joueurs commencent 30 cases devant l'ours.
chaosbear-intro-2 = Lancez les dés pour avancer, et piochez des cartes sur les multiples de 5 pour obtenir des effets spéciaux.
chaosbear-intro-3 = Ne laissez pas l'ours vous attraper !

# Annonce de tour
chaosbear-turn = Tour de { $player } ; case { $position }.

# Lancer
chaosbear-roll = { $player } a lancé { $roll }.
chaosbear-position = { $player } est maintenant à la case { $position }.

# Piocher des cartes
chaosbear-draws-card = { $player } pioche une carte.
chaosbear-card-impulsion = Impulsion ! { $player } avance de 3 cases à la case { $position } !
chaosbear-card-super-impulsion = Super impulsion ! { $player } avance de 5 cases à la case { $position } !
chaosbear-card-tiredness = Fatigue ! Énergie de l'ours moins 1. Il a maintenant { $energy } énergie.
chaosbear-card-hunger = Faim ! Énergie de l'ours plus 1. Il a maintenant { $energy } énergie.
chaosbear-card-backward = Poussée en arrière ! { $player } recule à la case { $position }.
chaosbear-card-random-gift = Cadeau aléatoire !
chaosbear-gift-back = { $player } est retourné à la case { $position }.
chaosbear-gift-forward = { $player } est avancé à la case { $position } !

# Tour de l'ours
chaosbear-bear-roll = L'ours a lancé { $roll } + ses { $energy } énergie = { $total }.
chaosbear-bear-energy-up = L'ours a lancé un 3 et a gagné 1 énergie !
chaosbear-bear-position = L'ours est maintenant à la case { $position } !
chaosbear-player-caught = L'ours a attrapé { $player } ! { $player } a été vaincu !
chaosbear-bear-feast = L'ours perd 3 énergies après s'être régalé de leur chair !

# Vérification de statut
chaosbear-status-player-alive = { $player } : case { $position }.
chaosbear-status-player-caught = { $player } : attrapé à la case { $position }.
chaosbear-status-bear = L'ours est à la case { $position } avec { $energy } énergie.

# Fin de jeu
chaosbear-winner = { $player } a survécu et gagne ! Il a atteint la case { $position } !
chaosbear-tie = Égalité à la case { $position } !

# Raisons d'action désactivée
chaosbear-you-are-caught = Vous avez été attrapé par l'ours.
chaosbear-not-on-multiple = Vous ne pouvez piocher des cartes que sur les multiples de 5.

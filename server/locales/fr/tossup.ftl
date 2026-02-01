# Messages du jeu Toss Up

# Informations sur le jeu
game-name-tossup = Toss Up
tossup-category = Jeux de dés

# Actions
tossup-roll-first = Lancer { $count } dés
tossup-roll-remaining = Lancer { $count } dés restants
tossup-bank = Banquer { $points } points

# Événements de jeu
tossup-turn-start = Tour de { $player }. Score : { $score }
tossup-you-roll = Vous avez lancé : { $results }.
tossup-player-rolls = { $player } a lancé : { $results }.

# Statut du tour
tossup-you-have-points = Points du tour : { $turn_points }. Dés restants : { $dice_count }.
tossup-player-has-points = { $player } a { $turn_points } points de tour. { $dice_count } dés restants.

# Dés frais
tossup-you-get-fresh = Plus de dés ! Obtention de { $count } dés frais.
tossup-player-gets-fresh = { $player } obtient { $count } dés frais.

# Bust
tossup-you-bust = Bust ! Vous perdez { $points } points pour ce tour.
tossup-player-busts = { $player } fait bust et perd { $points } points !

# Banque
tossup-you-bank = Vous banquez { $points } points. Score total : { $total }.
tossup-player-banks = { $player } banque { $points } points. Score total : { $total }.

# Gagnant
tossup-winner = { $player } gagne avec { $score } points !
tossup-tie-tiebreaker = Égalité entre { $players } ! Manche de départage !

# Options
tossup-set-rules-variant = Variante de règles : { $variant }
tossup-select-rules-variant = Sélectionnez la variante de règles :
tossup-option-changed-rules = Variante de règles changée à { $variant }

tossup-set-starting-dice = Dés de départ : { $count }
tossup-enter-starting-dice = Entrez le nombre de dés de départ :
tossup-option-changed-dice = Dés de départ changés à { $count }

# Variantes de règles
tossup-rules-standard = Standard
tossup-rules-playpalace = PlayPalace

# Explications des règles
tossup-rules-standard-desc = 3 verts, 2 jaunes, 1 rouge par dé. Bust si pas de verts et au moins un rouge.
tossup-rules-playpalace-desc = Distribution égale. Bust si tous les dés sont rouges.

# Raisons désactivées
tossup-need-points = Vous avez besoin de points pour banquer.

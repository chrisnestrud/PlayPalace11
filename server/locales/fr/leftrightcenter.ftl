# Messages pour Left Right Center (Français)

# Nom du jeu
game-name-leftrightcenter = Left Right Center

# Actions
lrc-roll = Lancer { $count } { $count ->
    [0] dé
    [1] dé
   *[other] dés
}

# Faces des dés
lrc-face-left = Gauche
lrc-face-right = Droite
lrc-face-center = Centre
lrc-face-dot = Point

# Événements de jeu
lrc-roll-results = { $player } lance { $results }.
lrc-pass-left = { $player } passe { $count } { $count ->
    [0] jeton
    [1] jeton
   *[other] jetons
} à { $target }.
lrc-pass-right = { $player } passe { $count } { $count ->
    [0] jeton
    [1] jeton
   *[other] jetons
} à { $target }.
lrc-pass-center = { $player } met { $count } { $count ->
    [0] jeton
    [1] jeton
   *[other] jetons
} au centre.
lrc-no-chips = { $player } n'a pas de jetons à lancer.
lrc-center-pot = { $count } { $count ->
    [0] jeton
    [1] jeton
   *[other] jetons
} au centre.
lrc-player-chips = { $player } a maintenant { $count } { $count ->
    [0] jeton
    [1] jeton
   *[other] jetons
}.
lrc-winner = { $player } gagne avec { $count } { $count ->
    [0] jeton
    [1] jeton
   *[other] jetons
} !

# Options
lrc-set-starting-chips = Jetons de départ : { $count }
lrc-enter-starting-chips = Entrez les jetons de départ :
lrc-option-changed-starting-chips = Jetons de départ définis sur { $count }.

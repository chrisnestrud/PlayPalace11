# Ninety Nine - Localisation française
# Les messages correspondent exactement à la v10

# Informations sur le jeu
ninetynine-name = Quatre-vingt-dix-neuf
ninetynine-description = Un jeu de cartes où les joueurs essaient d'éviter de pousser le total au-dessus de 99. Le dernier joueur debout gagne !

# Manche
ninetynine-round = Manche { $round }.

# Tour
ninetynine-player-turn = Tour de { $player }.

# Jouer des cartes - correspondant exactement à v10
ninetynine-you-play = Vous jouez { $card }. Le compte est maintenant { $count }.
ninetynine-player-plays = { $player } joue { $card }. Le compte est maintenant { $count }.

# Inversion de direction
ninetynine-direction-reverses = La direction du jeu s'inverse !

# Passer
ninetynine-player-skipped = { $player } est passé.

# Perte de jetons - correspondant exactement à v10
ninetynine-you-lose-tokens = Vous perdez { $amount } { $amount ->
    [0] jeton
    [1] jeton
   *[other] jetons
}.
ninetynine-player-loses-tokens = { $player } perd { $amount } { $amount ->
    [0] jeton
    [1] jeton
   *[other] jetons
}.

# Élimination
ninetynine-player-eliminated = { $player } a été éliminé !

# Fin de jeu
ninetynine-player-wins = { $player } gagne le jeu !

# Distribution
ninetynine-you-deal = Vous distribuez les cartes.
ninetynine-player-deals = { $player } distribue les cartes.

# Piocher des cartes
ninetynine-you-draw = Vous piochez { $card }.
ninetynine-player-draws = { $player } pioche une carte.

# Pas de cartes valides
ninetynine-no-valid-cards = { $player } n'a pas de cartes qui ne dépasseraient pas 99 !

# Statut - pour la touche C
ninetynine-current-count = Le compte est { $count }.

# Vérification de main - pour la touche H
ninetynine-hand-cards = Vos cartes : { $cards }.
ninetynine-hand-empty = Vous n'avez pas de cartes.

# Choix d'As
ninetynine-ace-choice = Jouer l'As comme +1 ou +11 ?
ninetynine-ace-add-eleven = Ajouter 11
ninetynine-ace-add-one = Ajouter 1

# Choix de Dix
ninetynine-ten-choice = Jouer le 10 comme +10 ou -10 ?
ninetynine-ten-add = Ajouter 10
ninetynine-ten-subtract = Soustraire 10

# Pioche manuelle
ninetynine-draw-card = Piocher une carte
ninetynine-draw-prompt = Appuyez sur Espace ou D pour piocher une carte.

# Options
ninetynine-set-tokens = Jetons de départ : { $tokens }
ninetynine-enter-tokens = Entrez le nombre de jetons de départ :
ninetynine-option-changed-tokens = Jetons de départ définis sur { $tokens }.
ninetynine-set-rules = Variante de règles : { $rules }
ninetynine-select-rules = Sélectionnez la variante de règles
ninetynine-option-changed-rules = Variante de règles définie sur { $rules }.
ninetynine-set-hand-size = Taille de main : { $size }
ninetynine-enter-hand-size = Entrez la taille de main :
ninetynine-option-changed-hand-size = Taille de main définie sur { $size }.
ninetynine-set-autodraw = Pioche automatique : { $enabled }
ninetynine-option-changed-autodraw = Pioche automatique définie sur { $enabled }.

# Annonces de variante de règles (affichées au démarrage du jeu)
ninetynine-rules-quentin = Règles Quentin C.
ninetynine-rules-rsgames = Règles RS Games.

# Choix de variante de règles (pour affichage du menu)
ninetynine-rules-variant-quentin_c = Quentin C
ninetynine-rules-variant-rs_games = RS Games

# Raisons d'action désactivée
ninetynine-choose-first = Vous devez d'abord faire un choix.
ninetynine-draw-first = Vous devez d'abord piocher une carte.

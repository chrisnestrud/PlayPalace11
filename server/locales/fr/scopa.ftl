# Messages du jeu Scopa

# Nom du jeu
game-name-scopa = Scopa

# Événements de jeu
scopa-initial-table = Cartes de table : { $cards }
scopa-no-initial-table = Aucune carte sur la table pour commencer.
scopa-you-collect = Vous collectez { $cards } avec { $card }
scopa-player-collects = { $player } collecte { $cards } avec { $card }
scopa-you-put-down = Vous posez { $card }.
scopa-player-puts-down = { $player } pose { $card }.
scopa-scopa-suffix =  - SCOPA !
scopa-clear-table-suffix = , vidant la table.
scopa-remaining-cards = { $player } obtient les cartes de table restantes.
scopa-scoring-round = Calcul des scores...
scopa-most-cards = { $player } marque 1 point pour le plus de cartes ({ $count } cartes).
scopa-most-cards-tie = Le plus de cartes est une égalité - aucun point attribué.
scopa-most-diamonds = { $player } marque 1 point pour le plus de carreaux ({ $count } carreaux).
scopa-most-diamonds-tie = Le plus de carreaux est une égalité - aucun point attribué.
scopa-seven-diamonds = { $player } marque 1 point pour le 7 de carreau.
scopa-seven-diamonds-multi = { $player } marque 1 point pour le plus de 7 de carreau ({ $count } × 7 de carreau).
scopa-seven-diamonds-tie = Le 7 de carreau est une égalité - aucun point attribué.
scopa-most-sevens = { $player } marque 1 point pour le plus de sept ({ $count } sept).
scopa-most-sevens-tie = Le plus de sept est une égalité - aucun point attribué.
scopa-round-scores = Scores de manche :
scopa-round-score-line = { $player } : +{ $round_score } (total : { $total_score })
scopa-table-empty = Il n'y a aucune carte sur la table.
scopa-no-such-card = Aucune carte à cette position.
scopa-captured-count = Vous avez capturé { $count } cartes

# Actions de vue
scopa-view-table = Voir la table
scopa-view-captured = Voir les capturées

# Options spécifiques à Scopa
scopa-enter-target-score = Entrez le score cible (1-121)
scopa-set-cards-per-deal = Cartes par distribution : { $cards }
scopa-enter-cards-per-deal = Entrez les cartes par distribution (1-10)
scopa-set-decks = Nombre de paquets : { $decks }
scopa-enter-decks = Entrez le nombre de paquets (1-6)
scopa-toggle-escoba = Escoba (somme à 15) : { $enabled }
scopa-toggle-hints = Afficher les indices de capture : { $enabled }
scopa-set-mechanic = Mécanique scopa : { $mechanic }
scopa-select-mechanic = Sélectionnez la mécanique scopa
scopa-toggle-instant-win = Victoire instantanée sur scopa : { $enabled }
scopa-toggle-team-scoring = Mettre en commun les cartes d'équipe pour le score : { $enabled }
scopa-toggle-inverse = Mode inversé (atteindre la cible = élimination) : { $enabled }

# Annonces de changement d'options
scopa-option-changed-cards = Cartes par distribution définies sur { $cards }.
scopa-option-changed-decks = Nombre de paquets défini sur { $decks }.
scopa-option-changed-escoba = Escoba { $enabled }.
scopa-option-changed-hints = Indices de capture { $enabled }.
scopa-option-changed-mechanic = Mécanique scopa définie sur { $mechanic }.
scopa-option-changed-instant = Victoire instantanée sur scopa { $enabled }.
scopa-option-changed-team-scoring = Score des cartes d'équipe { $enabled }.
scopa-option-changed-inverse = Mode inversé { $enabled }.

# Choix de mécanique scopa
scopa-mechanic-normal = Normal
scopa-mechanic-no_scopas = Pas de Scopas
scopa-mechanic-only_scopas = Scopas uniquement

# Raisons d'action désactivée
scopa-timer-not-active = La minuterie de manche n'est pas active.

# Erreurs de validation
scopa-error-not-enough-cards = Pas assez de cartes dans { $decks } { $decks ->
    [0] paquet
    [1] paquet
   *[other] paquets
} pour { $players } { $players ->
    [0] joueur
    [1] joueur
   *[other] joueurs
} avec { $cards_per_deal } cartes chacun. (Besoin de { $cards_per_deal } × { $players } = { $cards_needed } cartes, mais n'en avons que { $total_cards }.)

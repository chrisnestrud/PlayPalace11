# Messages du jeu Tradeoff

# Informations sur le jeu
game-name-tradeoff = Tradeoff

# Flux de manche et d'itération
tradeoff-round-start = Manche { $round }.
tradeoff-iteration = Main { $iteration } sur 3.

# Phase 1 : Échange
tradeoff-you-rolled = Vous avez lancé : { $dice }.
tradeoff-toggle-trade = { $value } ({ $status })
tradeoff-trade-status-trading = échange
tradeoff-trade-status-keeping = garde
tradeoff-confirm-trades = Confirmer les échanges ({ $count } dés)
tradeoff-keeping = Garde { $value }.
tradeoff-trading = Échange { $value }.
tradeoff-player-traded = { $player } a échangé : { $dice }.
tradeoff-player-traded-none = { $player } a gardé tous les dés.

# Phase 2 : Prendre dans la réserve
tradeoff-your-turn-take = Votre tour de prendre un dé de la réserve.
tradeoff-take-die = Prendre un { $value } ({ $remaining } restant)
tradeoff-you-take = Vous prenez un { $value }.
tradeoff-player-takes = { $player } prend un { $value }.

# Phase 3 : Score
tradeoff-player-scored = { $player } ({ $points } pts) : { $sets }.
tradeoff-no-sets = { $player } : aucun ensemble.

# Descriptions d'ensembles (concis)
tradeoff-set-triple = triple de { $value }
tradeoff-set-group = groupe de { $value }
tradeoff-set-mini-straight = mini suite { $low }-{ $high }
tradeoff-set-double-triple = double triple ({ $v1 } et { $v2 })
tradeoff-set-straight = suite { $low }-{ $high }
tradeoff-set-double-group = double groupe ({ $v1 } et { $v2 })
tradeoff-set-all-groups = tous les groupes
tradeoff-set-all-triplets = tous les triplets

# Fin de manche
tradeoff-round-scores = Scores de la manche { $round } :
tradeoff-score-line = { $player } : +{ $round_points } (total : { $total })
tradeoff-leader = { $player } mène avec { $score }.

# Fin de jeu
tradeoff-winner = { $player } gagne avec { $score } points !
tradeoff-winners-tie = Égalité ! { $players } à égalité avec { $score } points !

# Vérifications de statut
tradeoff-view-hand = Voir votre main
tradeoff-view-pool = Voir la réserve
tradeoff-view-players = Voir les joueurs
tradeoff-hand-display = Votre main ({ $count } dés) : { $dice }
tradeoff-pool-display = Réserve ({ $count } dés) : { $dice }
tradeoff-player-info = { $player } : { $hand }. Échangé : { $traded }.
tradeoff-player-info-no-trade = { $player } : { $hand }. Rien échangé.

# Messages d'erreur
tradeoff-not-trading-phase = Pas dans la phase d'échange.
tradeoff-not-taking-phase = Pas dans la phase de prise.
tradeoff-already-confirmed = Déjà confirmé.
tradeoff-no-die = Aucun dé à basculer.
tradeoff-no-more-takes = Plus de prises disponibles.
tradeoff-not-in-pool = Ce dé n'est pas dans la réserve.

# Options
tradeoff-set-target = Score cible : { $score }
tradeoff-enter-target = Entrez le score cible :
tradeoff-option-changed-target = Score cible défini sur { $score }.

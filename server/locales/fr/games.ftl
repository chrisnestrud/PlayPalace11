# Messages de jeu partagés pour PlayPalace
# Ces messages sont communs à plusieurs jeux

# Noms de jeux
game-name-ninetynine = Quatre-vingt-dix-neuf

# Flux de manche et de tour
game-round-start = Manche { $round }.
game-round-end = Manche { $round } terminée.
game-turn-start = Tour de { $player }.
game-your-turn = Votre tour.
game-no-turn = Aucun tour en ce moment.

# Affichage des scores
game-scores-header = Scores actuels :
game-score-line = { $player } : { $score } points
game-final-scores-header = Scores finaux :

# Victoire/défaite
game-winner = { $player } gagne !
game-winner-score = { $player } gagne avec { $score } points !
game-tiebreaker = Égalité ! Manche de départage !
game-tiebreaker-players = Égalité entre { $players } ! Manche de départage !
game-eliminated = { $player } a été éliminé avec { $score } points.

# Options communes
game-set-target-score = Score cible : { $score }
game-enter-target-score = Entrez le score cible :
game-option-changed-target = Score cible défini sur { $score }.

game-set-team-mode = Mode équipe : { $mode }
game-select-team-mode = Sélectionnez le mode équipe
game-option-changed-team = Mode équipe défini sur { $mode }.
game-team-mode-individual = Individuel
game-team-mode-x-teams-of-y = { $num_teams } équipes de { $team_size }

# Valeurs d'options booléennes
option-on = activé
option-off = désactivé

# Boîte de statut
status-box-closed = Informations de statut fermées.

# Fin de jeu
game-leave = Quitter le jeu

# Minuterie de manche
round-timer-paused = { $player } a mis le jeu en pause (appuyez sur p pour démarrer la prochaine manche).
round-timer-resumed = Minuterie de manche reprise.
round-timer-countdown = Prochaine manche dans { $seconds }...

# Jeux de dés - garder/relancer les dés
dice-keeping = Garde { $value }.
dice-rerolling = Relance { $value }.
dice-locked = Ce dé est verrouillé et ne peut pas être changé.

# Distribution (jeux de cartes)
game-deal-counter = Distribution { $current }/{ $total }.
game-you-deal = Vous distribuez les cartes.
game-player-deals = { $player } distribue les cartes.

# Noms de cartes
card-name = { $rank } de { $suit }
no-cards = Aucune carte

# Noms de couleurs
suit-diamonds = carreau
suit-clubs = trèfle
suit-hearts = cœur
suit-spades = pique

# Noms de rangs
rank-ace = as
rank-ace-plural = as
rank-two = 2
rank-two-plural = 2
rank-three = 3
rank-three-plural = 3
rank-four = 4
rank-four-plural = 4
rank-five = 5
rank-five-plural = 5
rank-six = 6
rank-six-plural = 6
rank-seven = 7
rank-seven-plural = 7
rank-eight = 8
rank-eight-plural = 8
rank-nine = 9
rank-nine-plural = 9
rank-ten = 10
rank-ten-plural = 10
rank-jack = valet
rank-jack-plural = valets
rank-queen = dame
rank-queen-plural = dames
rank-king = roi
rank-king-plural = rois

# Descriptions de mains de poker
poker-high-card-with = { $high } haute, avec { $rest }
poker-high-card = { $high } haute
poker-pair-with = Paire de { $pair }, avec { $rest }
poker-pair = Paire de { $pair }
poker-two-pair-with = Double paire, { $high } et { $low }, avec { $kicker }
poker-two-pair = Double paire, { $high } et { $low }
poker-trips-with = Brelan, { $trips }, avec { $rest }
poker-trips = Brelan, { $trips }
poker-straight-high = Suite à { $high }
poker-flush-high-with = Couleur à { $high }, avec { $rest }
poker-full-house = Full, { $trips } sur { $pair }
poker-quads-with = Carré, { $quads }, avec { $kicker }
poker-quads = Carré, { $quads }
poker-straight-flush-high = Quinte flush à { $high }
poker-unknown-hand = Main inconnue

# Erreurs de validation (communes à tous les jeux)
game-error-invalid-team-mode = Le mode équipe sélectionné n'est pas valide pour le nombre actuel de joueurs.

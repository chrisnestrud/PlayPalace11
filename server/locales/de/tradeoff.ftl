# Tradeoff-Spielnachrichten

# Spielinformationen
game-name-tradeoff = Tradeoff

# Runden- und Iterationsablauf
tradeoff-round-start = Runde { $round }.
tradeoff-iteration = Blatt { $iteration } von 3.

# Phase 1: Handeln
tradeoff-you-rolled = Sie würfelten: { $dice }.
tradeoff-toggle-trade = { $value } ({ $status })
tradeoff-trade-status-trading = tauschen
tradeoff-trade-status-keeping = behalten
tradeoff-confirm-trades = Tausch bestätigen ({ $count } Würfel)
tradeoff-keeping = { $value } behalten.
tradeoff-trading = { $value } tauschen.
tradeoff-player-traded = { $player } tauschte: { $dice }.
tradeoff-player-traded-none = { $player } behielt alle Würfel.

# Phase 2: Aus dem Pool nehmen
tradeoff-your-turn-take = Sie sind am Zug, einen Würfel aus dem Pool zu nehmen.
tradeoff-take-die = Eine { $value } nehmen ({ $remaining } übrig)
tradeoff-you-take = Sie nehmen eine { $value }.
tradeoff-player-takes = { $player } nimmt eine { $value }.

# Phase 3: Punktevergabe
tradeoff-player-scored = { $player } ({ $points } Pkt.): { $sets }.
tradeoff-no-sets = { $player }: keine Sets.

# Set-Beschreibungen (prägnant)
tradeoff-set-triple = Drilling von { $value }en
tradeoff-set-group = Gruppe von { $value }en
tradeoff-set-mini-straight = Mini-Straße { $low }-{ $high }
tradeoff-set-double-triple = Doppelter Drilling ({ $v1 }en und { $v2 }en)
tradeoff-set-straight = Straße { $low }-{ $high }
tradeoff-set-double-group = Doppelte Gruppe ({ $v1 }en und { $v2 }en)
tradeoff-set-all-groups = Alle Gruppen
tradeoff-set-all-triplets = Alle Drillinge

# Rundenende
tradeoff-round-scores = Runde { $round } Punktzahlen:
tradeoff-score-line = { $player }: +{ $round_points } (gesamt: { $total })
tradeoff-leader = { $player } führt mit { $score }.

# Spielende
tradeoff-winner = { $player } gewinnt mit { $score } Punkten!
tradeoff-winners-tie = Es ist ein Unentschieden! { $players } gleichauf mit { $score } Punkten!

# Statusprüfungen
tradeoff-view-hand = Ihre Hand ansehen
tradeoff-view-pool = Den Pool ansehen
tradeoff-view-players = Spieler ansehen
tradeoff-hand-display = Ihre Hand ({ $count } Würfel): { $dice }
tradeoff-pool-display = Pool ({ $count } Würfel): { $dice }
tradeoff-player-info = { $player }: { $hand }. Getauscht: { $traded }.
tradeoff-player-info-no-trade = { $player }: { $hand }. Nichts getauscht.

# Fehlermeldungen
tradeoff-not-trading-phase = Nicht in der Handelsphase.
tradeoff-not-taking-phase = Nicht in der Nehmphase.
tradeoff-already-confirmed = Bereits bestätigt.
tradeoff-no-die = Kein Würfel zum Umschalten.
tradeoff-no-more-takes = Keine weiteren Nahmen verfügbar.
tradeoff-not-in-pool = Dieser Würfel ist nicht im Pool.

# Optionen
tradeoff-set-target = Zielpunktzahl: { $score }
tradeoff-enter-target = Zielpunktzahl eingeben:
tradeoff-option-changed-target = Zielpunktzahl auf { $score } gesetzt.

# Scopa-Spielnachrichten
# Hinweis: Gemeinsame Nachrichten wie round-start, turn-start, target-score, team-mode sind in games.ftl

# Spielname
game-name-scopa = Scopa

# Spielereignisse
scopa-initial-table = Tischkarten: { $cards }
scopa-no-initial-table = Keine Karten auf dem Tisch zum Start.
scopa-you-collect = Sie sammeln { $cards } mit { $card }
scopa-player-collects = { $player } sammelt { $cards } mit { $card }
scopa-you-put-down = Sie legen { $card } ab.
scopa-player-puts-down = { $player } legt { $card } ab.
scopa-scopa-suffix =  - SCOPA!
scopa-clear-table-suffix = , räumt den Tisch ab.
scopa-remaining-cards = { $player } erhält die verbleibenden Tischkarten.
scopa-scoring-round = Bewertungsrunde...
scopa-most-cards = { $player } erzielt 1 Punkt für die meisten Karten ({ $count } Karten).
scopa-most-cards-tie = Meiste Karten ist ein Unentschieden - kein Punkt vergeben.
scopa-most-diamonds = { $player } erzielt 1 Punkt für die meisten Karos ({ $count } Karos).
scopa-most-diamonds-tie = Meiste Karos ist ein Unentschieden - kein Punkt vergeben.
scopa-seven-diamonds = { $player } erzielt 1 Punkt für die Karo 7.
scopa-seven-diamonds-multi = { $player } erzielt 1 Punkt für die meisten Karo 7 ({ $count } × Karo 7).
scopa-seven-diamonds-tie = Karo 7 ist ein Unentschieden - kein Punkt vergeben.
scopa-most-sevens = { $player } erzielt 1 Punkt für die meisten Siebenen ({ $count } Siebenen).
scopa-most-sevens-tie = Meiste Siebenen ist ein Unentschieden - kein Punkt vergeben.
scopa-round-scores = Rundenpunktzahlen:
scopa-round-score-line = { $player }: +{ $round_score } (gesamt: { $total_score })
scopa-table-empty = Es gibt keine Karten auf dem Tisch.
scopa-no-such-card = Keine Karte an dieser Position.
scopa-captured-count = Sie haben { $count } Karten gesammelt

# Ansichtsaktionen
scopa-view-table = Tisch ansehen
scopa-view-captured = Gesammelte ansehen

# Scopa-spezifische Optionen
scopa-enter-target-score = Zielpunktzahl eingeben (1-121)
scopa-set-cards-per-deal = Karten pro Ausgabe: { $cards }
scopa-enter-cards-per-deal = Karten pro Ausgabe eingeben (1-10)
scopa-set-decks = Anzahl der Decks: { $decks }
scopa-enter-decks = Anzahl der Decks eingeben (1-6)
scopa-toggle-escoba = Escoba (Summe auf 15): { $enabled }
scopa-toggle-hints = Sammelhinweise anzeigen: { $enabled }
scopa-set-mechanic = Scopa-Mechanik: { $mechanic }
scopa-select-mechanic = Scopa-Mechanik auswählen
scopa-toggle-instant-win = Sofortiger Sieg bei Scopa: { $enabled }
scopa-toggle-team-scoring = Team-Karten für Bewertung zusammenlegen: { $enabled }
scopa-toggle-inverse = Inversemodus (Ziel erreichen = Eliminierung): { $enabled }

# Optionsänderungsankündigungen
scopa-option-changed-cards = Karten pro Ausgabe auf { $cards } gesetzt.
scopa-option-changed-decks = Anzahl der Decks auf { $decks } gesetzt.
scopa-option-changed-escoba = Escoba { $enabled }.
scopa-option-changed-hints = Sammelhinweise { $enabled }.
scopa-option-changed-mechanic = Scopa-Mechanik auf { $mechanic } gesetzt.
scopa-option-changed-instant = Sofortiger Sieg bei Scopa { $enabled }.
scopa-option-changed-team-scoring = Team-Kartenbewertung { $enabled }.
scopa-option-changed-inverse = Inversemodus { $enabled }.

# Scopa-Mechanik-Auswahlmöglichkeiten
scopa-mechanic-normal = Normal
scopa-mechanic-no_scopas = Keine Scopas
scopa-mechanic-only_scopas = Nur Scopas

# Gründe für deaktivierte Aktionen
scopa-timer-not-active = Der Rundenzeitmesser ist nicht aktiv.

# Validierungsfehler
scopa-error-not-enough-cards = Nicht genug Karten in { $decks } { $decks ->
    [one] Deck
   *[other] Decks
} für { $players } { $players ->
    [one] Spieler
   *[other] Spieler
} mit { $cards_per_deal } Karten jeweils. (Benötige { $cards_per_deal } × { $players } = { $cards_needed } Karten, habe aber nur { $total_cards }.)

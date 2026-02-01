# 1-4-24 (Midnight)-Spielnachrichten
# Hinweis: Gemeinsame Nachrichten wie round-start, turn-start, target-score sind in games.ftl

# Spielinformationen
game-name-midnight = 1-4-24
midnight-category = Würfelspiele

# Aktionen
midnight-roll = Die Würfel werfen
midnight-keep-die = { $value } behalten
midnight-bank = Sichern

# Spielereignisse
midnight-turn-start = { $player } ist am Zug.
midnight-you-rolled = Sie würfelten: { $dice }.
midnight-player-rolled = { $player } würfelte: { $dice }.

# Würfel behalten
midnight-you-keep = Sie behalten { $die }.
midnight-player-keeps = { $player } behält { $die }.
midnight-you-unkeep = Sie geben { $die } frei.
midnight-player-unkeeps = { $player } gibt { $die } frei.

# Zugstatus
midnight-you-have-kept = Behaltene Würfel: { $kept }. Verbleibende Würfe: { $remaining }.
midnight-player-has-kept = { $player } hat behalten: { $kept }. { $remaining } Würfel verbleiben.

# Punktevergabe
midnight-you-scored = Sie erzielten { $score } Punkte.
midnight-scored = { $player } erzielte { $score } Punkte.
midnight-you-disqualified = Sie haben nicht sowohl 1 als auch 4. Disqualifiziert!
midnight-player-disqualified = { $player } hat nicht sowohl 1 als auch 4. Disqualifiziert!

# Rundenergebnisse
midnight-round-winner = { $player } gewinnt die Runde!
midnight-round-tie = Runde unentschieden zwischen { $players }.
midnight-all-disqualified = Alle Spieler disqualifiziert! Kein Gewinner diese Runde.

# Spielgewinner
midnight-game-winner = { $player } gewinnt das Spiel mit { $wins } Rundensiegen!
midnight-game-tie = Es ist ein Unentschieden! { $players } gewannen jeweils { $wins } Runden.

# Optionen
midnight-set-rounds = Zu spielende Runden: { $rounds }
midnight-enter-rounds = Anzahl zu spielender Runden eingeben:
midnight-option-changed-rounds = Zu spielende Runden auf { $rounds } geändert

# Deaktivierte Gründe
midnight-need-to-roll = Sie müssen zuerst würfeln.
midnight-no-dice-to-keep = Keine verfügbaren Würfel zum Behalten.
midnight-must-keep-one = Sie müssen mindestens einen Würfel pro Wurf behalten.
midnight-must-roll-first = Sie müssen zuerst würfeln.
midnight-keep-all-first = Sie müssen alle Würfel behalten, bevor Sie sichern.

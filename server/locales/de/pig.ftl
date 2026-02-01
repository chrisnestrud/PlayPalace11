# Pig-Spielnachrichten
# Hinweis: Gemeinsame Nachrichten wie round-start, turn-start, target-score sind in games.ftl

# Spielinformationen
game-name-pig = Pig
pig-category = Würfelspiele

# Aktionen
pig-roll = Würfel werfen
pig-bank = { $points } Punkte sichern

# Spielereignisse (Pig-spezifisch)
pig-rolls = { $player } würfelt...
pig-roll-result = Eine { $roll }, insgesamt { $total }
pig-bust = Oh nein, eine 1! { $player } verliert { $points } Punkte.
pig-bank-action = { $player } entscheidet sich, { $points } zu sichern, insgesamt { $total }
pig-winner = Wir haben einen Gewinner, und es ist { $player }!

# Pig-spezifische Optionen
pig-set-min-bank = Mindestsicherung: { $points }
pig-set-dice-sides = Würfelseiten: { $sides }
pig-enter-min-bank = Geben Sie die Mindestpunktzahl zum Sichern ein:
pig-enter-dice-sides = Geben Sie die Anzahl der Würfelseiten ein:
pig-option-changed-min-bank = Mindestsicherung auf { $points } geändert
pig-option-changed-dice = Würfel hat jetzt { $sides } Seiten

# Deaktivierte Gründe
pig-need-more-points = Sie brauchen mehr Punkte zum Sichern.

# Validierungsfehler
pig-error-min-bank-too-high = Mindestsicherung muss unter der Zielpunktzahl liegen.

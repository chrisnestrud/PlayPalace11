# Chaos Bear-Spielnachrichten

# Spielname
game-name-chaosbear = Chaos Bear

# Aktionen
chaosbear-roll-dice = Würfel werfen
chaosbear-draw-card = Eine Karte ziehen
chaosbear-check-status = Status prüfen

# Spieleinführung (3 separate Nachrichten wie v10)
chaosbear-intro-1 = Chaos Bear hat begonnen! Alle Spieler starten 30 Felder vor dem Bären.
chaosbear-intro-2 = Würfeln Sie, um vorwärts zu ziehen, und ziehen Sie Karten auf Vielfachen von 5, um spezielle Effekte zu erhalten.
chaosbear-intro-3 = Lassen Sie sich nicht vom Bären erwischen!

# Zugankündigung
chaosbear-turn = { $player } ist am Zug; Feld { $position }.

# Würfeln
chaosbear-roll = { $player } würfelte { $roll }.
chaosbear-position = { $player } ist jetzt auf Feld { $position }.

# Karten ziehen
chaosbear-draws-card = { $player } zieht eine Karte.
chaosbear-card-impulsion = Impuls! { $player } bewegt sich 3 Felder vorwärts auf Feld { $position }!
chaosbear-card-super-impulsion = Superimpuls! { $player } bewegt sich 5 Felder vorwärts auf Feld { $position }!
chaosbear-card-tiredness = Müdigkeit! Bärenenergie minus 1. Es hat jetzt { $energy } Energie.
chaosbear-card-hunger = Hunger! Bärenenergie plus 1. Es hat jetzt { $energy } Energie.
chaosbear-card-backward = Rückwärts-Stoß! { $player } bewegt sich zurück auf Feld { $position }.
chaosbear-card-random-gift = Zufallsgeschenk!
chaosbear-gift-back = { $player } ging zurück auf Feld { $position }.
chaosbear-gift-forward = { $player } ging vorwärts auf Feld { $position }!

# Bärenzug
chaosbear-bear-roll = Der Bär würfelte { $roll } + seine { $energy } Energie = { $total }.
chaosbear-bear-energy-up = Der Bär würfelte eine 3 und erhielt 1 Energie!
chaosbear-bear-position = Der Bär ist jetzt auf Feld { $position }!
chaosbear-player-caught = Der Bär erwischte { $player }! { $player } wurde besiegt!
chaosbear-bear-feast = Der Bär verliert 3 Energie, nachdem er sich an ihrem Fleisch ergötzt hat!

# Statusprüfung
chaosbear-status-player-alive = { $player }: Feld { $position }.
chaosbear-status-player-caught = { $player }: erwischt auf Feld { $position }.
chaosbear-status-bear = Der Bär ist auf Feld { $position } mit { $energy } Energie.

# Spielende
chaosbear-winner = { $player } hat überlebt und gewinnt! Er erreichte Feld { $position }!
chaosbear-tie = Es ist ein Unentschieden auf Feld { $position }!

# Gründe für deaktivierte Aktionen
chaosbear-you-are-caught = Sie wurden vom Bären erwischt.
chaosbear-not-on-multiple = Sie können nur auf Vielfachen von 5 Karten ziehen.

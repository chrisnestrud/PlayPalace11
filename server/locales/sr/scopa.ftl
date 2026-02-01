# Scopa game messages
# Note: Common messages like round-start, turn-start, target-score, team-mode are in games.ftl

# Game name
game-name-scopa = Скопа

# Game events
scopa-initial-table = Карте на столу: { $cards }
scopa-no-initial-table = Нема карата на столу за почетак.
scopa-you-collect = Скупљаш { $cards } са { $card }
scopa-player-collects = { $player } скупља { $cards } са { $card }
scopa-you-put-down = Стављаш { $card }.
scopa-player-puts-down = { $player } ставља { $card }.
scopa-scopa-suffix =  - СКОПА!
scopa-clear-table-suffix = , чистећи сто.
scopa-remaining-cards = { $player } добија преостале карте са стола.
scopa-scoring-round = Бодовање рунде...
scopa-most-cards = { $player } добија 1 поен за највише карата ({ $count } карата).
scopa-most-cards-tie = Највише карата је нерешено - поен се не додељује.
scopa-most-diamonds = { $player } добија 1 поен за највише каро ({ $count } каро).
scopa-most-diamonds-tie = Највише каро је нерешено - поен се не додељује.
scopa-seven-diamonds = { $player } добија 1 поен за седмицу каро.
scopa-seven-diamonds-multi = { $player } добија 1 поен за највише седмица каро ({ $count } × седмица каро).
scopa-seven-diamonds-tie = Седмица каро је нерешено - поен се не додељује.
scopa-most-sevens = { $player } добија 1 поен за највише седмица ({ $count } седмица).
scopa-most-sevens-tie = Највише седмица је нерешено - поен се не додељује.
scopa-round-scores = Резултати рунде:
scopa-round-score-line = { $player }: +{ $round_score } (укупно: { $total_score })
scopa-table-empty = Нема карата на столу.
scopa-no-such-card = Нема карте на тој позицији.
scopa-captured-count = Ухватио си { $count } карата

# View actions
scopa-view-table = Погледај сто
scopa-view-captured = Погледај ухваћене

# Scopa-specific options
scopa-enter-target-score = Унеси циљни резултат (1-121)
scopa-set-cards-per-deal = Карте по дељењу: { $cards }
scopa-enter-cards-per-deal = Унеси карте по дељењу (1-10)
scopa-set-decks = Број шпилова: { $decks }
scopa-enter-decks = Унеси број шпилова (1-6)
scopa-toggle-escoba = Ескоба (збир до 15): { $enabled }
scopa-toggle-hints = Прикажи савете за хватање: { $enabled }
scopa-set-mechanic = Скопа механика: { $mechanic }
scopa-select-mechanic = Изабери скопа механику
scopa-toggle-instant-win = Тренутна победа на скопа: { $enabled }
scopa-toggle-team-scoring = Здружи тимске карте за бодовање: { $enabled }
scopa-toggle-inverse = Инверзни режим (достизање циља = елиминација): { $enabled }

# Option change announcements
scopa-option-changed-cards = Карте по дељењу постављене на { $cards }.
scopa-option-changed-decks = Број шпилова постављен на { $decks }.
scopa-option-changed-escoba = Ескоба { $enabled }.
scopa-option-changed-hints = Савети за хватање { $enabled }.
scopa-option-changed-mechanic = Скопа механика постављена на { $mechanic }.
scopa-option-changed-instant = Тренутна победа на скопа { $enabled }.
scopa-option-changed-team-scoring = Бодовање тимских карата { $enabled }.
scopa-option-changed-inverse = Инверзни режим { $enabled }.

# Scopa mechanic choices
scopa-mechanic-normal = Нормално
scopa-mechanic-no_scopas = Без Скопа
scopa-mechanic-only_scopas = Само Скопе

# Disabled action reasons
scopa-timer-not-active = Мерач времена рунде није активан.

# Validation errors
scopa-error-not-enough-cards = Нема довољно карата у { $decks } { $decks ->
    [one] шпилу
    *[other] шпилова
} за { $players } { $players ->
    [one] играча
    *[other] играча
} са { $cards_per_deal } карата сваки. (Потребно { $cards_per_deal } × { $players } = { $cards_needed } карата, али има само { $total_cards }.)

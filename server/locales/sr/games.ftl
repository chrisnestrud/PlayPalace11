# Shared game messages for PlayPalace
# These messages are common across multiple games

# Game names
game-name-ninetynine = Деведесет девет

# Round and turn flow
game-round-start = Рунда { $round }.
game-round-end = Рунда { $round } завршена.
game-turn-start = { $player } је на потезу.
game-your-turn = Ви сте на потезу.
game-no-turn = Тренутно нико није на потезу.

# Score display
game-scores-header = Тренутни резултати:
game-score-line = { $player }: { $score } поена
game-final-scores-header = Коначни резултати:

# Win/loss
game-winner = { $player } побеђује!
game-winner-score = { $player } побеђује са { $score } поена!
game-tiebreaker = Нерешено! Одлучујућа рунда!
game-tiebreaker-players = Нерешено између { $players }! Одлучујућа рунда!
game-eliminated = { $player } је елиминисан/а са { $score } поена.

# Common options
game-set-target-score = Циљни резултат: { $score }
game-enter-target-score = Унесите циљни резултат:
game-option-changed-target = Циљни резултат постављен на { $score }.

game-set-team-mode = Тимски режим: { $mode }
game-select-team-mode = Изаберите тимски режим
game-option-changed-team = Тимски режим постављен на { $mode }.
game-team-mode-individual = Индивидуално
game-team-mode-x-teams-of-y = { $num_teams } тимова од { $team_size }

# Boolean option values
option-on = укључено
option-off = искључено

# Status box
status-box-closed = Информације о статусу затворене.

# Game end
game-leave = Напусти игру

# Round timer
round-timer-paused = { $player } је паузирао/ла игру (притисните п за почетак следеће рунде).
round-timer-resumed = Одбројавање рунде настављено.
round-timer-countdown = Следећа рунда за { $seconds }...

# Dice games - keeping/releasing dice
dice-keeping = Задржавам { $value }.
dice-rerolling = Поново бацам { $value }.
dice-locked = Та коцка је закључана и не може се променити.

# Dealing (card games)
game-deal-counter = Дељење { $current }/{ $total }.
game-you-deal = Ви делите карте.
game-player-deals = { $player } дели карте.

# Card names
card-name = { $rank } { $suit }
no-cards = Нема карата

# Suit names
suit-diamonds = каро
suit-clubs = треф
suit-hearts = херц
suit-spades = пик

# Rank names
rank-ace = кец
rank-ace-plural = кецеви
rank-two = 2
rank-two-plural = двојке
rank-three = 3
rank-three-plural = тројке
rank-four = 4
rank-four-plural = четворке
rank-five = 5
rank-five-plural = петице
rank-six = 6
rank-six-plural = шестице
rank-seven = 7
rank-seven-plural = седмице
rank-eight = 8
rank-eight-plural = осмице
rank-nine = 9
rank-nine-plural = деветке
rank-ten = 10
rank-ten-plural = десетке
rank-jack = дечко
rank-jack-plural = дечки
rank-queen = дама
rank-queen-plural = даме
rank-king = краљ
rank-king-plural = краљеви

# Poker hand descriptions
poker-high-card-with = { $high } високо, са { $rest }
poker-high-card = { $high } високо
poker-pair-with = Пар { $pair }, са { $rest }
poker-pair = Пар { $pair }
poker-two-pair-with = Два пара, { $high } и { $low }, са { $kicker }
poker-two-pair = Два пара, { $high } и { $low }
poker-trips-with = Три исте, { $trips }, са { $rest }
poker-trips = Три исте, { $trips }
poker-straight-high = { $high } високо кента
poker-flush-high-with = { $high } високо флеш, са { $rest }
poker-full-house = Фул хаус, { $trips } преко { $pair }
poker-quads-with = Четири исте, { $quads }, са { $kicker }
poker-quads = Четири исте, { $quads }
poker-straight-flush-high = { $high } високо кента флеш
poker-unknown-hand = Непозната рука

# Validation errors (common across games)
game-error-invalid-team-mode = Изабрани тимски режим није важећи за тренутни број играча.

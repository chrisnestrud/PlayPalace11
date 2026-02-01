# Tradeoff game messages

# Game info
game-name-tradeoff = Размена

# Round and iteration flow
tradeoff-round-start = Рунда { $round }.
tradeoff-iteration = Рука { $iteration } од 3.

# Phase 1: Trading
tradeoff-you-rolled = Бацили сте: { $dice }.
tradeoff-toggle-trade = { $value } ({ $status })
tradeoff-trade-status-trading = размена
tradeoff-trade-status-keeping = задржавање
tradeoff-confirm-trades = Потврдите размене ({ $count } коцки)
tradeoff-keeping = Задржавање { $value }.
tradeoff-trading = Размена { $value }.
tradeoff-player-traded = { $player } је разменио: { $dice }.
tradeoff-player-traded-none = { $player } је задржао све коцке.

# Phase 2: Taking from pool
tradeoff-your-turn-take = Ваш ред да узмете коцку из фонда.
tradeoff-take-die = Узмите { $value } (преостало { $remaining })
tradeoff-you-take = Узимате { $value }.
tradeoff-player-takes = { $player } узима { $value }.

# Phase 3: Scoring
tradeoff-player-scored = { $player } ({ $points } пое.): { $sets }.
tradeoff-no-sets = { $player }: нема сетова.

# Set descriptions (concise)
tradeoff-set-triple = тројка { $value }
tradeoff-set-group = група { $value }
tradeoff-set-mini-straight = мини низ { $low }-{ $high }
tradeoff-set-double-triple = двострука тројка ({ $v1 } и { $v2 })
tradeoff-set-straight = низ { $low }-{ $high }
tradeoff-set-double-group = двострука група ({ $v1 } и { $v2 })
tradeoff-set-all-groups = све групе
tradeoff-set-all-triplets = све тројке

# Round end
tradeoff-round-scores = Резултати рунде { $round }:
tradeoff-score-line = { $player }: +{ $round_points } (укупно: { $total })
tradeoff-leader = { $player } води са { $score }.

# Game end
tradeoff-winner = { $player } побеђује са { $score } поена!
tradeoff-winners-tie = Нерешено! { $players } нерешено са { $score } поена!

# Status checks
tradeoff-view-hand = Погледајте своју руку
tradeoff-view-pool = Погледајте фонд
tradeoff-view-players = Погледајте играче
tradeoff-hand-display = Ваша рука ({ $count } коцки): { $dice }
tradeoff-pool-display = Фонд ({ $count } коцки): { $dice }
tradeoff-player-info = { $player }: { $hand }. Разменио: { $traded }.
tradeoff-player-info-no-trade = { $player }: { $hand }. Није разменио ништа.

# Error messages
tradeoff-not-trading-phase = Није фаза размене.
tradeoff-not-taking-phase = Није фаза узимања.
tradeoff-already-confirmed = Већ потврђено.
tradeoff-no-die = Нема коцке за промену.
tradeoff-no-more-takes = Нема више доступних узимања.
tradeoff-not-in-pool = Та коцка није у фонду.

# Options
tradeoff-set-target = Циљни резултат: { $score }
tradeoff-enter-target = Унесите циљни резултат:
tradeoff-option-changed-target = Циљни резултат постављен на { $score }.

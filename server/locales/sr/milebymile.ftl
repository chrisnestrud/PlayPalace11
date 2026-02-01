# Mile by Mile game messages
# Note: Common messages like round-start, turn-start, team-mode are in games.ftl

# Game name
game-name-milebymile = Миља по Миља

# Game options
milebymile-set-distance = Удаљеност трке: { $miles } миља
milebymile-enter-distance = Унесите удаљеност трке (300-3000)
milebymile-set-winning-score = Победнички резултат: { $score } поена
milebymile-enter-winning-score = Унесите победнички резултат (1000-10000)
milebymile-toggle-perfect-crossing = Захтевај тачан завршетак: { $enabled }
milebymile-toggle-stacking = Дозволи гомилање напада: { $enabled }
milebymile-toggle-reshuffle = Промешај одбачене карте: { $enabled }
milebymile-toggle-karma = Правило карме: { $enabled }
milebymile-set-rig = Намештање шпила: { $rig }
milebymile-select-rig = Изаберите опцију намештања шпила

# Option change announcements
milebymile-option-changed-distance = Удаљеност трке постављена на { $miles } миља.
milebymile-option-changed-winning = Победнички резултат постављен на { $score } поена.
milebymile-option-changed-crossing = Захтевај тачан завршетак { $enabled }.
milebymile-option-changed-stacking = Дозволи гомилање напада { $enabled }.
milebymile-option-changed-reshuffle = Промешај одбачене карте { $enabled }.
milebymile-option-changed-karma = Правило карме { $enabled }.
milebymile-option-changed-rig = Намештање шпила постављено на { $rig }.

# Status
milebymile-status = { $name }: { $points } поена, { $miles } миља, Проблеми: { $problems }, Сигурности: { $safeties }

# Card actions
milebymile-no-matching-safety = Немате одговарајућу сигурносну карту!
milebymile-cant-play = Не можете одиграти { $card } јер { $reason }.
milebymile-no-card-selected = Није изабрана карта за одбацивање.
milebymile-no-valid-targets = Нема важећих мета за ову опасност!
milebymile-you-drew = Извукли сте: { $card }
milebymile-discards = { $player } одбацује карту.
milebymile-select-target = Изаберите мету

# Distance plays
milebymile-plays-distance-individual = { $player } игра { $distance } миља и сада је на { $total } миља.
milebymile-plays-distance-team = { $player } игра { $distance } миља; њихов тим је сада на { $total } миља.

# Journey complete
milebymile-journey-complete-perfect-individual = { $player } је завршио путовање са савршеним прелазом!
milebymile-journey-complete-perfect-team = Тим { $team } је завршио путовање са савршеним прелазом!
milebymile-journey-complete-individual = { $player } је завршио путовање!
milebymile-journey-complete-team = Тим { $team } је завршио путовање!

# Hazard plays
milebymile-plays-hazard-individual = { $player } игра { $card } на { $target }.
milebymile-plays-hazard-team = { $player } игра { $card } на Тим { $team }.

# Remedy/Safety plays
milebymile-plays-card = { $player } игра { $card }.
milebymile-plays-dirty-trick = { $player } игра { $card } као Прљави Трик!

# Deck
milebymile-deck-reshuffled = Одбачене карте промешане назад у шпил.

# Race
milebymile-new-race = Почиње нова трка!
milebymile-race-complete = Трка завршена! Израчунавање резултата...
milebymile-earned-points = { $name } је зарадио { $score } поена у овој трци: { $breakdown }.
milebymile-total-scores = Укупни резултати:
milebymile-team-score = { $name }: { $score } поена

# Scoring breakdown
milebymile-from-distance = { $miles } од пређене удаљености
milebymile-from-trip = { $points } од завршетка путовања
milebymile-from-perfect = { $points } од савршеног прелаза
milebymile-from-safe = { $points } од сигурног путовања
milebymile-from-shutout = { $points } од потпуног затварања
milebymile-from-safeties = { $points } од { $count } { $safeties ->
    [one] сигурности
    *[other] сигурности
}
milebymile-from-all-safeties = { $points } од све 4 сигурности
milebymile-from-dirty-tricks = { $points } од { $count } { $tricks ->
    [one] прљавог трика
    *[other] прљавих трикова
}

# Game end
milebymile-wins-individual = { $player } побеђује у игри!
milebymile-wins-team = Тим { $team } побеђује у игри! ({ $members })
milebymile-final-score = Коначан резултат: { $score } поена

# Karma messages - clash (both lose karma)
milebymile-karma-clash-you-target = Ви и ваша мета сте обоје осуђени! Напад је неутрализован.
milebymile-karma-clash-you-attacker = Ви и { $attacker } сте обоје осуђени! Напад је неутрализован.
milebymile-karma-clash-others = { $attacker } и { $target } су обоје осуђени! Напад је неутрализован.
milebymile-karma-clash-your-team = Ваш тим и ваша мета су обоје осуђени! Напад је неутрализован.
milebymile-karma-clash-target-team = Ви и Тим { $team } сте обоје осуђени! Напад је неутрализован.
milebymile-karma-clash-other-teams = Тим { $attacker } и Тим { $target } су обоје осуђени! Напад је неутрализован.

# Karma messages - attacker shunned
milebymile-karma-shunned-you = Осуђени сте због своје агресије! Ваша карма је изгубљена.
milebymile-karma-shunned-other = { $player } је осуђен због своје агресије!
milebymile-karma-shunned-your-team = Ваш тим је осуђен због своје агресије! Карма вашег тима је изгубљена.
milebymile-karma-shunned-other-team = Тим { $team } је осуђен због своје агресије!

# False Virtue
milebymile-false-virtue-you = Играте Лажну Врлину и враћате своју карму!
milebymile-false-virtue-other = { $player } игра Лажну Врлину и враћа своју карму!
milebymile-false-virtue-your-team = Ваш тим игра Лажну Врлину и враћа своју карму!
milebymile-false-virtue-other-team = Тим { $team } игра Лажну Врлину и враћа своју карму!

# Problems/Safeties (for status display)
milebymile-none = ништа

# Unplayable card reasons
milebymile-reason-not-on-team = нисте у тиму
milebymile-reason-stopped = стали сте
milebymile-reason-has-problem = имате проблем који спречава вожњу
milebymile-reason-speed-limit = ограничење брзине је активно
milebymile-reason-exceeds-distance = прекорачило би { $miles } миља
milebymile-reason-no-targets = нема важећих мета
milebymile-reason-no-speed-limit = нисте под ограничењем брзине
milebymile-reason-has-right-of-way = Предност Пролаза омогућава вожњу без зелених светала
milebymile-reason-already-moving = већ се крећете
milebymile-reason-must-fix-first = прво морате поправити { $problem }
milebymile-reason-has-gas = ваш аутомобил има бензин
milebymile-reason-tires-fine = ваше гуме су у реду
milebymile-reason-no-accident = ваш аутомобил није имао несрећу
milebymile-reason-has-safety = већ имате ту сигурност
milebymile-reason-has-karma = још увек имате своју карму
milebymile-reason-generic = не може се одиграти сада

# Card names
milebymile-card-out-of-gas = Остало без Бензина
milebymile-card-flat-tire = Празна Гума
milebymile-card-accident = Несрећа
milebymile-card-speed-limit = Ограничење Брзине
milebymile-card-stop = Стоп
milebymile-card-gasoline = Бензин
milebymile-card-spare-tire = Резервна Гума
milebymile-card-repairs = Поправке
milebymile-card-end-of-limit = Крај Ограничења
milebymile-card-green-light = Зелено Светло
milebymile-card-extra-tank = Додатни Резервоар
milebymile-card-puncture-proof = Отпорно на Пробијање
milebymile-card-driving-ace = Ас Вожње
milebymile-card-right-of-way = Предност Пролаза
milebymile-card-false-virtue = Лажна Врлина
milebymile-card-miles = { $miles } миља

# Disabled action reasons
milebymile-no-dirty-trick-window = Нема активног прозора за прљави трик.
milebymile-not-your-dirty-trick = То није прозор за прљави трик вашег тима.
milebymile-between-races = Причекајте почетак следеће трке.

# Validation errors
milebymile-error-karma-needs-three-teams = Правило карме захтева најмање 3 различита аутомобила/тима.

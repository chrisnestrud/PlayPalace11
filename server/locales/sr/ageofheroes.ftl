# Age of Heroes game messages
# A civilization-building card game for 2-6 players

# Game name
game-name-ageofheroes = Доба хероја

# Tribes
ageofheroes-tribe-egyptians = Египћани
ageofheroes-tribe-romans = Римљани
ageofheroes-tribe-greeks = Грци
ageofheroes-tribe-babylonians = Вавилонци
ageofheroes-tribe-celts = Келти
ageofheroes-tribe-chinese = Кинези

# Special Resources (for monuments)
ageofheroes-special-limestone = Кречњак
ageofheroes-special-concrete = Бетон
ageofheroes-special-marble = Мермер
ageofheroes-special-bricks = Опека
ageofheroes-special-sandstone = Пешчар
ageofheroes-special-granite = Гранит

# Standard Resources
ageofheroes-resource-iron = Гвожђе
ageofheroes-resource-wood = Дрво
ageofheroes-resource-grain = Жито
ageofheroes-resource-stone = Камен
ageofheroes-resource-gold = Злато

# Events
ageofheroes-event-population-growth = Раст становништва
ageofheroes-event-earthquake = Земљотрес
ageofheroes-event-eruption = Ерупција
ageofheroes-event-hunger = Глад
ageofheroes-event-barbarians = Варвари
ageofheroes-event-olympics = Олимпијске игре
ageofheroes-event-hero = Херој
ageofheroes-event-fortune = Срећа

# Buildings
ageofheroes-building-army = Војска
ageofheroes-building-fortress = Тврђава
ageofheroes-building-general = Генерал
ageofheroes-building-road = Пут
ageofheroes-building-city = Град

# Actions
ageofheroes-action-tax-collection = Наплата пореза
ageofheroes-action-construction = Градња
ageofheroes-action-war = Рат
ageofheroes-action-do-nothing = Не ради ништа
ageofheroes-play = Играј

# War goals
ageofheroes-war-conquest = Освајање
ageofheroes-war-plunder = Пљачка
ageofheroes-war-destruction = Уништење

# Game options
ageofheroes-set-victory-cities = Градови за победу: { $cities }
ageofheroes-enter-victory-cities = Унесите број градова за победу (3-7)
ageofheroes-set-victory-monument = Завршетак споменика: { $progress }%
ageofheroes-toggle-neighbor-roads = Путеви само до суседа: { $enabled }
ageofheroes-set-max-hand = Максимална величина руке: { $cards } карата

# Option change announcements
ageofheroes-option-changed-victory-cities = За победу је потребно { $cities } градова.
ageofheroes-option-changed-victory-monument = Праг завршетка споменика постављен на { $progress }%.
ageofheroes-option-changed-neighbor-roads = Путеви само до суседа { $enabled }.
ageofheroes-option-changed-max-hand = Максимална величина руке постављена на { $cards } карата.

# Setup phase
ageofheroes-setup-start = Ви сте вођа племена { $tribe }. Ваш посебан ресурс за споменик је { $special }. Бацајте коцке да одредите редослед потеза.
ageofheroes-setup-viewer = Играчи бацају коцке да одреде редослед потеза.
ageofheroes-roll-dice = Бацајте коцке
ageofheroes-war-roll-dice = Бацајте коцке
ageofheroes-dice-result = Бацили сте { $total } ({ $die1 } + { $die2 }).
ageofheroes-dice-result-other = { $player } је бацио { $total }.
ageofheroes-dice-tie = Више играча је бацило { $total }. Бацајемо поново...
ageofheroes-first-player = { $player } је бацио највише са { $total } и иде први.
ageofheroes-first-player-you = Са { $total } поена, ви идете први.

# Preparation phase
ageofheroes-prepare-start = Играчи морају одиграти карте догађаја и одбацити катастрофе.
ageofheroes-prepare-your-turn = Имате { $count } { $count ->
    [one] карту
    [few] карте
    *[other] карата
} за играње или одбацивање.
ageofheroes-prepare-done = Фаза припреме завршена.

# Events played/discarded
ageofheroes-population-growth = { $player } игра Раст становништва и гради нови град.
ageofheroes-population-growth-you = Ви играте Раст становништва и градите нови град.
ageofheroes-discard-card = { $player } одбацује { $card }.
ageofheroes-discard-card-you = Ви одбацујете { $card }.
ageofheroes-earthquake = Земљотрес погађа племе { $player }; њихове војске иду на опоравак.
ageofheroes-earthquake-you = Земљотрес погађа ваше племе; ваше војске иду на опоравак.
ageofheroes-eruption = Ерупција уништава један од градова { $player }.
ageofheroes-eruption-you = Ерупција уништава један од ваших градова.

# Disaster effects
ageofheroes-hunger-strikes = Глад удара.
ageofheroes-lose-card-hunger = Губите { $card }.
ageofheroes-barbarians-pillage = Варвари нападају ресурсе { $player }.
ageofheroes-barbarians-attack = Варвари нападају ресурсе { $player }.
ageofheroes-barbarians-attack-you = Варвари нападају ваше ресурсе.
ageofheroes-lose-card-barbarians = Губите { $card }.
ageofheroes-block-with-card = { $player } блокира катастрофу користећи { $card }.
ageofheroes-block-with-card-you = Ви блокирате катастрофу користећи { $card }.

# Targeted disaster cards (Earthquake/Eruption)
ageofheroes-select-disaster-target = Изаберите мету за { $card }.
ageofheroes-no-targets = Нема доступних мета.
ageofheroes-earthquake-strikes-you = { $attacker } игра Земљотрес против вас. Ваше војске су онеспособљене.
ageofheroes-earthquake-strikes = { $attacker } игра Земљотрес против { $player }.
ageofheroes-armies-disabled = { $count } { $count ->
    [one] војска је онеспособљена
    [few] војске су онеспособљене
    *[other] војски је онеспособљено
} на један потез.
ageofheroes-eruption-strikes-you = { $attacker } игра Ерупцију против вас. Један од ваших градова је уништен.
ageofheroes-eruption-strikes = { $attacker } игра Ерупцију против { $player }.
ageofheroes-city-destroyed = Град је уништен ерупцијом.

# Fair phase
ageofheroes-fair-start = Освиће на тргу.
ageofheroes-fair-draw-base = Вучете { $count } { $count ->
    [one] карту
    [few] карте
    *[other] карата
}.
ageofheroes-fair-draw-roads = Вучете { $count } { $count ->
    [one] додатну карту
    [few] додатне карте
    *[other] додатних карата
} захваљујући вашој путној мрежи.
ageofheroes-fair-draw-other = { $player } вуче { $count } { $count ->
    [one] карту
    [few] карте
    *[other] карата
}.

# Trading/Auction
ageofheroes-auction-start = Аукција почиње.
ageofheroes-offer-trade = Понудите размену
ageofheroes-offer-made = { $player } нуди { $card } за { $wanted }.
ageofheroes-offer-made-you = Ви нудите { $card } за { $wanted }.
ageofheroes-trade-accepted = { $player } прихвата понуду { $other } и мења { $give } за { $receive }.
ageofheroes-trade-accepted-you = Ви прихватате понуду { $other } и добијате { $receive }.
ageofheroes-trade-cancelled = { $player } повлачи своју понуду за { $card }.
ageofheroes-trade-cancelled-you = Ви повлачите своју понуду за { $card }.
ageofheroes-stop-trading = Престаните трговати
ageofheroes-select-request = Нудите { $card }. Шта желите узамену?
ageofheroes-cancel = Откажи
ageofheroes-left-auction = { $player } одлази.
ageofheroes-left-auction-you = Ви одлазите са трга.
ageofheroes-any-card = Било која карта
ageofheroes-cannot-trade-own-special = Не можете трговати својим посебним ресурсом за споменик.
ageofheroes-resource-not-in-game = Овај посебан ресурс се не користи у овој игри.

# Main play phase
ageofheroes-play-start = Фаза игре.
ageofheroes-day = Дан { $day }
ageofheroes-draw-card = { $player } вуче карту из шпила.
ageofheroes-draw-card-you = Ви вучете { $card } из шпила.
ageofheroes-your-action = Шта желите да урадите?

# Tax Collection
ageofheroes-tax-collection = { $player } бира Наплату пореза: { $cities } { $cities ->
    [one] град
    [few] града
    *[other] градова
} прикупља { $cards } { $cards ->
    [one] карту
    [few] карте
    *[other] карата
}.
ageofheroes-tax-collection-you = Ви бирате Наплату пореза: { $cities } { $cities ->
    [one] град
    [few] града
    *[other] градова
} прикупља { $cards } { $cards ->
    [one] карту
    [few] карте
    *[other] карата
}.
ageofheroes-tax-no-city = Наплата пореза: Немате преживелих градова. Одбаците карту да бисте повукли нову.
ageofheroes-tax-no-city-done = { $player } бира Наплату пореза али нема градова, па мења карту.
ageofheroes-tax-no-city-done-you = Наплата пореза: Заменили сте { $card } за нову карту.

# Construction
ageofheroes-construction-menu = Шта желите да градите?
ageofheroes-construction-done = { $player } је изградио { $article } { $building }.
ageofheroes-construction-done-you = Ви сте изградили { $article } { $building }.
ageofheroes-construction-stop = Престаните градити
ageofheroes-construction-stopped = Одлучили сте да престанете градити.
ageofheroes-road-select-neighbor = Изаберите ком суседу желите да градите пут.
ageofheroes-direction-left = Лево од вас
ageofheroes-direction-right = Десно од вас
ageofheroes-road-request-sent = Захтев за пут послат. Чека се одобрење суседа.
ageofheroes-road-request-received = { $requester } тражи дозволу за изградњу пута до вашег племена.
ageofheroes-road-request-denied-you = Ви сте одбили захтев за пут.
ageofheroes-road-request-denied = { $denier } је одбио ваш захтев за пут.
ageofheroes-road-built = { $tribe1 } и { $tribe2 } су сада повезани путем.
ageofheroes-road-no-target = Нема суседних племена за изградњу пута.
ageofheroes-approve = Одобри
ageofheroes-deny = Одбиј
ageofheroes-supply-exhausted = Нема више { $building } за изградњу.

# Do Nothing
ageofheroes-do-nothing = { $player } прескаче.
ageofheroes-do-nothing-you = Ви прескачете...

# War
ageofheroes-war-declare = { $attacker } објављује рат { $defender }. Циљ: { $goal }.
ageofheroes-war-prepare = Изаберите своје војске за { $action }.
ageofheroes-war-no-army = Немате војске или карте хероја.
ageofheroes-war-no-targets = Нема валидних мета за рат.
ageofheroes-war-no-valid-goal = Нема валидних циљева рата против ове мете.
ageofheroes-war-select-target = Изаберите ког играча ћете напасти.
ageofheroes-war-select-goal = Изаберите свој циљ рата.
ageofheroes-war-prepare-attack = Изаберите своје нападачке снаге.
ageofheroes-war-prepare-defense = { $attacker } вас напада; Изаберите своје одбрамбене снаге.
ageofheroes-war-select-armies = Изаберите војске: { $count }
ageofheroes-war-select-generals = Изаберите генерале: { $count }
ageofheroes-war-select-heroes = Изаберите хероје: { $count }
ageofheroes-war-attack = Нападните...
ageofheroes-war-defend = Бранитесе...
ageofheroes-war-prepared = Ваше снаге: { $armies } { $armies ->
    [one] војска
    [few] војске
    *[other] војски
}{ $generals ->
    [0] {""}
    [one] {" и 1 генерал"}
    [few] {" и { $generals } генерала"}
    *[other] {" и { $generals } генерала"}
}{ $heroes ->
    [0] {""}
    [one] {" и 1 херој"}
    [few] {" и { $heroes } хероја"}
    *[other] {" и { $heroes } хероја"}
}.
ageofheroes-war-roll-you = Ви бацате { $roll }.
ageofheroes-war-roll-other = { $player } баца { $roll }.
ageofheroes-war-bonuses-you = { $general ->
    [0] {
        { $fortress ->
            [0] {""}
            [one] {"+1 од тврђаве = { $total } укупно"}
            [few] {"+{ $fortress } од тврђава = { $total } укупно"}
            *[other] {"+{ $fortress } од тврђава = { $total } укупно"}
        }
    }
    *[other] {
        { $fortress ->
            [0] {"+{ $general } од генерала = { $total } укупно"}
            [one] {"+{ $general } од генерала, +1 од тврђаве = { $total } укупно"}
            [few] {"+{ $general } од генерала, +{ $fortress } од тврђава = { $total } укупно"}
            *[other] {"+{ $general } од генерала, +{ $fortress } од тврђава = { $total } укупно"}
        }
    }
}
ageofheroes-war-bonuses-other = { $general ->
    [0] {
        { $fortress ->
            [0] {""}
            [one] {"{ $player }: +1 од тврђаве = { $total } укупно"}
            [few] {"{ $player }: +{ $fortress } од тврђава = { $total } укупно"}
            *[other] {"{ $player }: +{ $fortress } од тврђава = { $total } укупно"}
        }
    }
    *[other] {
        { $fortress ->
            [0] {"{ $player }: +{ $general } од генерала = { $total } укупно"}
            [one] {"{ $player }: +{ $general } од генерала, +1 од тврђаве = { $total } укупно"}
            [few] {"{ $player }: +{ $general } од генерала, +{ $fortress } од тврђава = { $total } укупно"}
            *[other] {"{ $player }: +{ $general } од генерала, +{ $fortress } од тврђава = { $total } укупно"}
        }
    }
}

# Battle
ageofheroes-battle-start = Битка почиње. { $attacker } има { $att_armies } { $att_armies ->
    [one] војску
    [few] војске
    *[other] војски
} против { $defender } са { $def_armies } { $def_armies ->
    [one] војском
    [few] војске
    *[other] војски
}.
ageofheroes-dice-roll-detailed = { $name } баца { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } од генерала" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 од тврђаве" }
    [few] { " + { $fortress } од тврђава" }
    *[other] { " + { $fortress } од тврђава" }
} = { $total }.
ageofheroes-dice-roll-detailed-you = Ви бацате { $dice }{ $general ->
    [0] {""}
    *[other] { " + { $general } од генерала" }
}{ $fortress ->
    [0] {""}
    [one] { " + 1 од тврђаве" }
    [few] { " + { $fortress } од тврђава" }
    *[other] { " + { $fortress } од тврђава" }
} = { $total }.
ageofheroes-round-attacker-wins = { $attacker } побеђује у рунди ({ $att_total } против { $def_total }). { $defender } губи војску.
ageofheroes-round-defender-wins = { $defender } се успешно брани ({ $def_total } против { $att_total }). { $attacker } губи војску.
ageofheroes-round-draw = Обе стране имају { $total }. Нема изгубљених војски.
ageofheroes-battle-victory-attacker = { $attacker } побеђује { $defender }.
ageofheroes-battle-victory-defender = { $defender } се успешно брани против { $attacker }.
ageofheroes-battle-mutual-defeat = И { $attacker } и { $defender } губе све војске.
ageofheroes-general-bonus = +{ $count } од { $count ->
    [one] генерала
    [few] генерала
    *[other] генерала
}
ageofheroes-fortress-bonus = +{ $count } од одбране тврђаве
ageofheroes-battle-winner = { $winner } побеђује у бици.
ageofheroes-battle-draw = Битка се завршава нерешено...
ageofheroes-battle-continue = Наставите битку.
ageofheroes-battle-end = Битка је завршена.

# War outcomes
ageofheroes-conquest-success = { $attacker } osvaja { $count } { $count ->
    [one] град
    [few] града
    *[other] градова
} од { $defender }.
ageofheroes-plunder-success = { $attacker } пљачка { $count } { $count ->
    [one] карту
    [few] карте
    *[other] карата
} од { $defender }.
ageofheroes-destruction-success = { $attacker } уништава { $count } { $count ->
    [one] ресурс
    [few] ресурса
    *[other] ресурса
} споменика { $defender }.
ageofheroes-army-losses = { $player } губи { $count } { $count ->
    [one] војску
    [few] војске
    *[other] војски
}.
ageofheroes-army-losses-you = Ви губите { $count } { $count ->
    [one] војску
    [few] војске
    *[other] војски
}.

# Army return
ageofheroes-army-return-road = Ваше трупе се одмах враћају путем.
ageofheroes-army-return-delayed = { $count } { $count ->
    [one] јединица се враћа
    [few] јединице се враћају
    *[other] јединица се враћа
} на крају вашег следећег потеза.
ageofheroes-army-returned = Трупе { $player } су се вратиле из рата.
ageofheroes-army-returned-you = Ваше трупе су се вратиле из рата.
ageofheroes-army-recover = Војске { $player } се опорављају од земљотреса.
ageofheroes-army-recover-you = Ваше војске се опорављају од земљотреса.

# Olympics
ageofheroes-olympics-cancel = { $player } игра Олимпијске игре. Рат отказан.
ageofheroes-olympics-prompt = { $attacker } је објавио рат. Имате Олимпијске игре - желите ли их искористити за отказивање?
ageofheroes-yes = Да
ageofheroes-no = Не

# Monument progress
ageofheroes-monument-progress = Споменик { $player } је { $count }/5 завршен.
ageofheroes-monument-progress-you = Ваш споменик је { $count }/5 завршен.

# Hand management
ageofheroes-discard-excess = Имате више од { $max } карата. Одбаците { $count } { $count ->
    [one] карту
    [few] карте
    *[other] карата
}.
ageofheroes-discard-excess-other = { $player } мора одбацити вишак карата.
ageofheroes-discard-more = Одбаците још { $count } { $count ->
    [one] карту
    [few] карте
    *[other] карата
}.

# Victory
ageofheroes-victory-cities = { $player } је изградио 5 градова! Царство пет градова.
ageofheroes-victory-cities-you = Ви сте изградили 5 градова! Царство пет градова.
ageofheroes-victory-monument = { $player } је завршио свој споменик! Носиоци велике културе.
ageofheroes-victory-monument-you = Ви сте завршили свој споменик! Носиоци велике културе.
ageofheroes-victory-last-standing = { $player } је последње преживело племе! Најупорнији.
ageofheroes-victory-last-standing-you = Ви сте последње преживело племе! Најупорнији.
ageofheroes-game-over = Игра завршена.

# Elimination
ageofheroes-eliminated = { $player } је елиминисан.
ageofheroes-eliminated-you = Ви сте елиминисани.

# Hand
ageofheroes-hand-empty = Немате карата.
ageofheroes-hand-contents = Ваша рука ({ $count } { $count ->
    [one] карта
    [few] карте
    *[other] карата
}): { $cards }

# Status
ageofheroes-status = { $player } ({ $tribe }): { $cities } { $cities ->
    [one] град
    [few] града
    *[other] градова
}, { $armies } { $armies ->
    [one] војска
    [few] војске
    *[other] војски
}, { $monument }/5 споменик
ageofheroes-status-detailed-header = { $player } ({ $tribe })
ageofheroes-status-cities = Градови: { $count }
ageofheroes-status-armies = Војске: { $count }
ageofheroes-status-generals = Генерали: { $count }
ageofheroes-status-fortresses = Тврђаве: { $count }
ageofheroes-status-monument = Споменик: { $count }/5
ageofheroes-status-roads = Путеви: { $left }{ $right }
ageofheroes-status-road-left = лево
ageofheroes-status-road-right = десно
ageofheroes-status-none = ништа
ageofheroes-status-earthquake-armies = Војске на опоравку: { $count }
ageofheroes-status-returning-armies = Војске које се враћају: { $count }
ageofheroes-status-returning-generals = Генерали који се враћају: { $count }

# Deck info
ageofheroes-deck-empty = Нема више { $card } карата у шпилу.
ageofheroes-deck-count = Преостало карата: { $count }
ageofheroes-deck-reshuffled = Гомила одбачених карата је промешана у шпил.

# Give up
ageofheroes-give-up-confirm = Да ли сте сигурни да желите да одустанете?
ageofheroes-gave-up = { $player } је одустао!
ageofheroes-gave-up-you = Ви сте одустали!

# Hero card
ageofheroes-hero-use = Користити као војску или генерала?
ageofheroes-hero-army = Војска
ageofheroes-hero-general = Генерал

# Fortune card
ageofheroes-fortune-reroll = { $player } користи Срећу за поново бацање.
ageofheroes-fortune-prompt = Изгубили сте бацање. Искористити Срећу за поново бацање?

# Disabled action reasons
ageofheroes-not-your-turn = Није ваш потез.
ageofheroes-game-not-started = Игра још није почела.
ageofheroes-wrong-phase = Ова акција није доступна у тренутној фази.
ageofheroes-no-resources = Немате потребне ресурсе.

# Building costs (for display)
ageofheroes-cost-army = 2 жита, гвожђе
ageofheroes-cost-fortress = Гвожђе, дрво, камен
ageofheroes-cost-general = Гвожђе, злато
ageofheroes-cost-road = 2 камена
ageofheroes-cost-city = 2 дрво, камен

# Pirates of the Lost Seas game messages
# Note: Common messages like round-start, turn-start are in games.ftl

# Game name
game-name-pirates = Пирати Изгубљених Мора

# Game start and setup
pirates-welcome = Добродошли у Пирате Изгубљених Мора! Пловите морима, сакупљајте драгуље и борите се са другим пиратима!
pirates-oceans = Ваше путовање ће вас водити кроз: { $oceans }
pirates-gems-placed = { $total } драгуља је расуто по морима. Пронађите их све!
pirates-golden-moon = Златни Месец излази! Сви добици XP су утростручени ово коло!

# Turn announcements
pirates-turn = Потез играча { $player }. Позиција { $position }

# Movement actions
pirates-move-left = Пловити лево
pirates-move-right = Пловити десно
pirates-move-2-left = Пловити 2 поља лево
pirates-move-2-right = Пловити 2 поља десно
pirates-move-3-left = Пловити 3 поља лево
pirates-move-3-right = Пловити 3 поља десно

# Movement messages
pirates-move-you = Пловите { $direction } на позицију { $position }.
pirates-move-you-tiles = Пловите { $tiles } поља { $direction } на позицију { $position }.
pirates-move = { $player } плови { $direction } на позицију { $position }.
pirates-map-edge = Не можете пловити даље. Налазите се на позицији { $position }.

# Position and status
pirates-check-status = Провери стање
pirates-check-position = Провери позицију
pirates-check-moon = Провери светлост месеца
pirates-your-position = Ваша позиција: { $position } у { $ocean }
pirates-moon-brightness = Златни Месец сија { $brightness }%. ({ $collected } од { $total } драгуља је сакупљено).
pirates-no-golden-moon = Златни Месец не може се видети на небу сада.

# Gem collection
pirates-gem-found-you = Пронашли сте { $gem }! Вреди { $value } поена.
pirates-gem-found = { $player } је пронашао { $gem }! Вреди { $value } поена.
pirates-all-gems-collected = Сви драгуљи су сакупљени!

# Winner
pirates-winner = { $player } побеђује са { $score } поена!

# Skills menu
pirates-use-skill = Користи способност
pirates-select-skill = Изаберите способност за коришћење

# Combat - Attack initiation
pirates-cannonball = Испали топовску куглу
pirates-no-targets = Нема циљева у домету { $range } поља.
pirates-attack-you-fire = Испаљујете топовску куглу на { $target }!
pirates-attack-incoming = { $attacker } испаљује топовску куглу на вас!
pirates-attack-fired = { $attacker } испаљује топовску куглу на { $defender }!

# Combat - Rolls
pirates-attack-roll = Бацање за напад: { $roll }
pirates-attack-bonus = Бонус напада: +{ $bonus }
pirates-defense-roll = Бацање за одбрану: { $roll }
pirates-defense-roll-others = { $player } баца { $roll } за одбрану.
pirates-defense-bonus = Бонус одбране: +{ $bonus }

# Combat - Hit results
pirates-attack-hit-you = Директан погодак! Погодили сте { $target }!
pirates-attack-hit-them = Погодио вас је { $attacker }!
pirates-attack-hit = { $attacker } погађа { $defender }!

# Combat - Miss results
pirates-attack-miss-you = Ваша топовска кугла је промашила { $target }.
pirates-attack-miss-them = Топовска кугла вас је промашила!
pirates-attack-miss = Топовска кугла играча { $attacker } промашује { $defender }.

# Combat - Push
pirates-push-you = Гурате { $target } { $direction } на позицију { $position }!
pirates-push-them = { $attacker } вас гура { $direction } на позицију { $position }!
pirates-push = { $attacker } гура { $defender } { $direction } са { $old_pos } на { $new_pos }.

# Combat - Gem stealing
pirates-steal-attempt = { $attacker } покушава да украде драгуљ!
pirates-steal-rolls = Бацање за крађу: { $steal } против одбране: { $defend }
pirates-steal-success-you = Украли сте { $gem } од { $target }!
pirates-steal-success-them = { $attacker } вам је украо { $gem }!
pirates-steal-success = { $attacker } краде { $gem } од { $defender }!
pirates-steal-failed = Покушај крађе није успео!

# XP and Leveling
pirates-xp-gained = +{ $xp } XP
pirates-level-up = { $player } је достигао ниво { $level }!
pirates-level-up-you = Достигли сте ниво { $level }!
pirates-level-up-multiple = { $player } је стекао { $levels } нивоа! Сада ниво { $level }!
pirates-level-up-multiple-you = Стекли сте { $levels } нивоа! Сада ниво { $level }!
pirates-skills-unlocked = { $player } је откључао нове способности: { $skills }.
pirates-skills-unlocked-you = Откључали сте нове способности: { $skills }.

# Skill activation
pirates-skill-activated = { $player } активира { $skill }!
pirates-buff-expired = Бонус { $skill } играча { $player } је истекао.

# Sword Fighter skill
pirates-sword-fighter-activated = Борац са Мачем активиран! +4 бонус напада за { $turns } потеза.

# Push skill (defense buff)
pirates-push-activated = Гурање активирано! +3 бонус одбране за { $turns } потеза.

# Skilled Captain skill
pirates-skilled-captain-activated = Вешт Капетан активиран! +2 напад и +2 одбрана за { $turns } потеза.

# Double Devastation skill
pirates-double-devastation-activated = Двострука Девастација активирана! Домет напада повећан на 10 поља за { $turns } потеза.

# Battleship skill
pirates-battleship-activated = Бојни брод активиран! Можете испалити два хица овај потез!
pirates-battleship-no-targets = Нема циљева за хиц { $shot }.
pirates-battleship-shot = Испаљивање хица { $shot }...

# Portal skill
pirates-portal-no-ships = Нема других бродова у видном пољу за портал.
pirates-portal-fizzle = Портал играча { $player } нестаје без циља.
pirates-portal-success = { $player } се телепортује у { $ocean } на позицију { $position }!

# Gem Seeker skill
pirates-gem-seeker-reveal = Мора шапућу о { $gem } на позицији { $position }. ({ $uses } коришћења преостало)

# Level requirements
pirates-requires-level-15 = Захтева ниво 15
pirates-requires-level-150 = Захтева ниво 150

# XP Multiplier options
pirates-set-combat-xp-multiplier = множилац xp за борбу: { $combat_multiplier }
pirates-enter-combat-xp-multiplier = искуство за борбу
pirates-set-find-gem-xp-multiplier = множилац xp за проналажење драгуља: { $find_gem_multiplier }
pirates-enter-find-gem-xp-multiplier = искуство за проналажење драгуља

# Gem stealing options
pirates-set-gem-stealing = Крађа драгуља: { $mode }
pirates-select-gem-stealing = Изаберите режим крађе драгуља
pirates-option-changed-stealing = Крађа драгуља постављена на { $mode }.

# Gem stealing mode choices
pirates-stealing-with-bonus = Са бонусом бацања
pirates-stealing-no-bonus = Без бонуса бацања
pirates-stealing-disabled = Онемогућено

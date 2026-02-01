# Yahtzee game messages

# Game info
game-name-yahtzee = Yahtzee

# Actions - Rolling
yahtzee-roll = Поново бацајте ({ $count } преостало)
yahtzee-roll-all = Бацајте коцке

# Upper section scoring categories
yahtzee-score-ones = Јединице за { $points } поена
yahtzee-score-twos = Двојке за { $points } поена
yahtzee-score-threes = Тројке за { $points } поена
yahtzee-score-fours = Четворке за { $points } поена
yahtzee-score-fives = Петице за { $points } поена
yahtzee-score-sixes = Шестице за { $points } поена

# Lower section scoring categories
yahtzee-score-three-kind = Три једнака за { $points } поена
yahtzee-score-four-kind = Четири једнака за { $points } поена
yahtzee-score-full-house = Пуна кућа за { $points } поена
yahtzee-score-small-straight = Мали низ за { $points } поена
yahtzee-score-large-straight = Велики низ за { $points } поена
yahtzee-score-yahtzee = Yahtzee за { $points } поена
yahtzee-score-chance = Шанса за { $points } поена

# Game events
yahtzee-you-rolled = Бацили сте: { $dice }. Преостала бацања: { $remaining }
yahtzee-player-rolled = { $player } је бацио: { $dice }. Преостала бацања: { $remaining }

# Scoring announcements
yahtzee-you-scored = Освојили сте { $points } поена у { $category }.
yahtzee-player-scored = { $player } је освојио { $points } у { $category }.

# Yahtzee bonus
yahtzee-you-bonus = Yahtzee бонус! +100 поена
yahtzee-player-bonus = { $player } је добио Yahtzee бонус! +100 поена

# Upper section bonus
yahtzee-you-upper-bonus = Бонус горње секције! +35 поена ({ $total } у горњој секцији)
yahtzee-player-upper-bonus = { $player } је зарадио бонус горње секције! +35 поена
yahtzee-you-upper-bonus-missed = Промашили сте бонус горње секције ({ $total } у горњој секцији, потребно 63).
yahtzee-player-upper-bonus-missed = { $player } је промашио бонус горње секције.

# Scoring mode
yahtzee-choose-category = Изаберите категорију за бодовање.
yahtzee-continuing = Наставак потеза.

# Status checks
yahtzee-check-scoresheet = Проверите картицу резултата
yahtzee-view-dice = Проверите руку
yahtzee-your-dice = Ваше коцке: { $dice }.
yahtzee-your-dice-kept = Ваше коцке: { $dice }. Задржане: { $kept }
yahtzee-not-rolled = Још нисте бацили.

# Scoresheet display
yahtzee-scoresheet-header = === Картица резултата играча { $player } ===
yahtzee-scoresheet-upper = Горња секција:
yahtzee-scoresheet-lower = Доња секција:
yahtzee-scoresheet-category-filled = { $category }: { $points }
yahtzee-scoresheet-category-open = { $category }: -
yahtzee-scoresheet-upper-total-bonus = Укупно горње: { $total } (БОНУС: +35)
yahtzee-scoresheet-upper-total-needed = Укупно горње: { $total } (још { $needed } за бонус)
yahtzee-scoresheet-yahtzee-bonus = Yahtzee бонуси: { $count } x 100 = { $total }
yahtzee-scoresheet-grand-total = УКУПАН РЕЗУЛТАТ: { $total }

# Category names (for announcements)
yahtzee-category-ones = Јединице
yahtzee-category-twos = Двојке
yahtzee-category-threes = Тројке
yahtzee-category-fours = Четворке
yahtzee-category-fives = Петице
yahtzee-category-sixes = Шестице
yahtzee-category-three-kind = Три једнака
yahtzee-category-four-kind = Четири једнака
yahtzee-category-full-house = Пуна кућа
yahtzee-category-small-straight = Мали низ
yahtzee-category-large-straight = Велики низ
yahtzee-category-yahtzee = Yahtzee
yahtzee-category-chance = Шанса

# Game end
yahtzee-winner = { $player } побеђује са { $score } поена!
yahtzee-winners-tie = Нерешено! { $players } су сви освојили { $score } поена!

# Options
yahtzee-set-rounds = Број игара: { $rounds }
yahtzee-enter-rounds = Унесите број игара (1-10):
yahtzee-option-changed-rounds = Број игара постављен на { $rounds }.

# Disabled action reasons
yahtzee-no-rolls-left = Немате више бацања.
yahtzee-roll-first = Морате прво бацити.
yahtzee-category-filled = Та категорија је већ попуњена.

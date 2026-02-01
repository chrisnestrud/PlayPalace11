# Ninety Nine - English Localization
# Messages match v10 exactly

# Game info
ninetynine-name = Деведесет Девет
ninetynine-description = Картaшка игра где играчи покушавају да избегну да укупни збир пређе 99. Последњи играч преживели побеђује!

# Round
ninetynine-round = Рунда { $round }.

# Turn
ninetynine-player-turn = Ред играча { $player }.

# Playing cards - match v10 exactly
ninetynine-you-play = Играте { $card }. Збир је сада { $count }.
ninetynine-player-plays = { $player } игра { $card }. Збир је сада { $count }.

# Direction reverse
ninetynine-direction-reverses = Смер игре се окреће!

# Skip
ninetynine-player-skipped = { $player } је прескочен.

# Token loss - match v10 exactly
ninetynine-you-lose-tokens = Губите { $amount } { $amount ->
    [one] жетон
   *[other] жетона
}.
ninetynine-player-loses-tokens = { $player } губи { $amount } { $amount ->
    [one] жетон
   *[other] жетона
}.

# Elimination
ninetynine-player-eliminated = { $player } је елиминисан!

# Game end
ninetynine-player-wins = { $player } побеђује игру!

# Dealing
ninetynine-you-deal = Ви делите карте.
ninetynine-player-deals = { $player } дели карте.

# Drawing cards
ninetynine-you-draw = Извлачите { $card }.
ninetynine-player-draws = { $player } извлачи карту.

# No valid cards
ninetynine-no-valid-cards = { $player } нема карата које неће прећи 99!

# Status - for C key
ninetynine-current-count = Збир је { $count }.

# Hand check - for H key
ninetynine-hand-cards = Ваше карте: { $cards }.
ninetynine-hand-empty = Немате карата.

# Ace choice
ninetynine-ace-choice = Играјте кеца као +1 или +11?
ninetynine-ace-add-eleven = Додај 11
ninetynine-ace-add-one = Додај 1

# Ten choice
ninetynine-ten-choice = Играјте 10 као +10 или -10?
ninetynine-ten-add = Додај 10
ninetynine-ten-subtract = Одузми 10

# Manual draw
ninetynine-draw-card = Извуци карту
ninetynine-draw-prompt = Притисните размак или D за извлачење карте.

# Options
ninetynine-set-tokens = Почетни жетони: { $tokens }
ninetynine-enter-tokens = Унесите број почетних жетона:
ninetynine-option-changed-tokens = Почетни жетони постављени на { $tokens }.
ninetynine-set-rules = Варијанта правила: { $rules }
ninetynine-select-rules = Изаберите варијанту правила
ninetynine-option-changed-rules = Варијанта правила постављена на { $rules }.
ninetynine-set-hand-size = Величина руке: { $size }
ninetynine-enter-hand-size = Унесите величину руке:
ninetynine-option-changed-hand-size = Величина руке постављена на { $size }.
ninetynine-set-autodraw = Аутоматско извлачење: { $enabled }
ninetynine-option-changed-autodraw = Аутоматско извлачење постављено на { $enabled }.

# Rules variant announcements (shown at game start)
ninetynine-rules-quentin = Quentin C правила.
ninetynine-rules-rsgames = RS Games правила.

# Rules variant choices (for menu display)
ninetynine-rules-variant-quentin_c = Quentin C
ninetynine-rules-variant-rs_games = RS Games

# Disabled action reasons
ninetynine-choose-first = Морате прво направити избор.
ninetynine-draw-first = Морате прво извући карту.

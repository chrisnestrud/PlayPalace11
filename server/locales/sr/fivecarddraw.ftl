# Five Card Draw

game-name-fivecarddraw = Покер са Пет Карата

draw-set-starting-chips = Почетни жетони: { $count }
draw-enter-starting-chips = Унесите почетне жетоне
draw-option-changed-starting-chips = Почетни жетони постављени на { $count }.

draw-set-ante = Улазни улог: { $count }
draw-enter-ante = Унесите износ улазног улога
draw-option-changed-ante = Улазни улог постављен на { $count }.

draw-set-turn-timer = Мерач времена: { $mode }
draw-select-turn-timer = Изаберите мерач времена
draw-option-changed-turn-timer = Мерач времена постављен на { $mode }.

draw-set-raise-mode = Режим подизања: { $mode }
draw-select-raise-mode = Изаберите режим подизања
draw-option-changed-raise-mode = Режим подизања постављен на { $mode }.

draw-set-max-raises = Максимално подизања: { $count }
draw-enter-max-raises = Унесите максимално подизања (0 за неограничено)
draw-option-changed-max-raises = Максимално подизања постављено на { $count }.

draw-antes-posted = Улазни улози постављени: { $amount }.
draw-betting-round-1 = Рунда клађења.
draw-betting-round-2 = Рунда клађења.
draw-begin-draw = Фаза извлачења.
draw-not-draw-phase = Није време за извлачење.
draw-not-betting = Не можете се кладити током фазе извлачења.

draw-toggle-discard = Промените одбацивање за карту { $index }
draw-card-keep = { $card }, задржано
draw-card-discard = { $card }, биће одбачено
draw-card-kept = Задржите { $card }.
draw-card-discarded = Одбаците { $card }.
draw-draw-cards = Извуците карте
draw-draw-cards-count = Извуците { $count } { $count ->
    [one] карту
   *[other] карата
}
draw-dealt-cards = Добијате { $cards }.
draw-you-drew-cards = Извлачите { $cards }.
draw-you-draw = Извлачите { $count } { $count ->
    [one] карту
   *[other] карата
}.
draw-player-draws = { $player } извлачи { $count } { $count ->
    [one] карту
   *[other] карата
}.
draw-you-stand-pat = Стојите.
draw-player-stands-pat = { $player } стоји.
draw-you-discard-limit = Можете одбацити до { $count } карата.
draw-player-discard-limit = { $player } може одбацити до { $count } карата.

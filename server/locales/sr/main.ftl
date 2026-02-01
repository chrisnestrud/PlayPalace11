# Main UI messages for PlayPalace

# Game categories
category-card-games = Игре са картама
category-dice-games = Игре са коцкама
category-rb-play-center = РБ Плаy центар
category-poker = Покер
category-uncategorized = Без категорије

# Menu titles
main-menu-title = Главни мени
play-menu-title = Играј
categories-menu-title = Категорије игара
tables-menu-title = Доступни столови

# Menu items
play = Играј
view-active-tables = Погледај активне столове
options = Подешавања
logout = Одјава
back = Назад
go-back = Иди назад
context-menu = Контекстуални мени.
no-actions-available = Нема доступних радњи.
create-table = Направи нови сто
join-as-player = Придружи се као играч
join-as-spectator = Придружи се као посматрач
leave-table = Напусти сто
start-game = Почни игру
add-bot = Додај бота
remove-bot = Уклони бота
actions-menu = Мени радњи
save-table = Сачувај сто
whose-turn = Чији је ред
whos-at-table = Ко је за столом
check-scores = Провери резултате
check-scores-detailed = Детаљни резултати

# Turn messages
game-player-skipped = { $player } је прескочен.

# Table messages
table-created = { $host } је направио нови { $game } сто.
table-joined = { $player } се придружио столу.
table-left = { $player } је напустио сто.
new-host = { $player } је сада домаћин.
waiting-for-players = Чекамо играче. {$min} мин, { $max } макс.
game-starting = Игра почиње!
table-listing = Сто од { $host } ({ $count } корисника)
table-listing-one = Сто од { $host } ({ $count } корисник)
table-listing-with = Сто од { $host } ({ $count } корисника) са { $members }
table-listing-game = { $game }: сто од { $host } ({ $count } корисника)
table-listing-game-one = { $game }: сто од { $host } ({ $count } корисник)
table-listing-game-with = { $game }: сто од { $host } ({ $count } корисника) са { $members }
table-not-exists = Сто више не постоји.
table-full = Сто је пун.
player-replaced-by-bot = { $player } је отишао и замењен је ботом.
player-took-over = { $player } је преузео од бота.
spectator-joined = Придружио си се столу од { $host } као посматрач.

# Spectator mode
spectate = Посматрај
now-playing = { $player } сада игра.
now-spectating = { $player } сада посматра.
spectator-left = { $player } је престао да посматра.

# General
welcome = Добродошли у PlayPalace!
goodbye = Довиђења!

# User presence announcements
user-online = { $player } је дошао на мрежу.
user-offline = { $player } је отишао ван мреже.
user-is-admin = { $player } је администратор PlayPalace-а.
user-is-server-owner = { $player } је власник сервера PlayPalace-а.
online-users-none = Нема корисника на мрежи.
online-users-one = 1 корисник: { $users }
online-users-many = { $count } корисника: { $users }
online-user-not-in-game = Није у игри
online-user-waiting-approval = Чека одобрење

# Options
language = Језик
language-option = Језик: { $language }
language-changed = Језик постављен на { $language }.

# Boolean option states
option-on = Укључено
option-off = Искључено

# Sound options
turn-sound-option = Звук потеза: { $status }

# Dice options
clear-kept-option = Обриши задржане коцке при бацању: { $status }
dice-keeping-style-option = Стил задржавања коцкица: { $style }
dice-keeping-style-changed = Стил задржавања коцкица постављен на { $style }.
dice-keeping-style-indexes = Индекси коцкица
dice-keeping-style-values = Вредности коцкица

# Bot names
cancel = Откажи
no-bot-names-available = Нема доступних имена ботова.
select-bot-name = Изабери име за бота
enter-bot-name = Унеси име бота
no-options-available = Нема доступних опција.
no-scores-available = Нема доступних резултата.

# Duration estimation
estimate-duration = Процени трајање
estimate-computing = Рачунам процењено трајање игре...
estimate-result = Просек бота: { $bot_time } (± { $std_dev }). { $outlier_info }Процењено људско време: { $human_time }.
estimate-error = Није могуће проценити трајање.
estimate-already-running = Процена трајања је већ у току.

# Save/Restore
saved-tables = Сачувани столови
no-saved-tables = Немате сачуваних столова.
no-active-tables = Нема активних столова.
restore-table = Врати
delete-saved-table = Обриши
saved-table-deleted = Сачувани сто обрисан.
missing-players = Не може се вратити: ови играчи нису доступни: { $players }
table-restored = Сто враћен! Сви играчи су пребачени.
table-saved-destroying = Сто сачуван! Враћање на главни мени.
game-type-not-found = Тип игре више не постоји.

# Action disabled reasons
action-not-your-turn = Није твој ред.
action-not-playing = Игра још није почела.
action-spectator = Посматрачи не могу то да ураде.
action-not-host = Само домаћин може то да уради.
action-game-in-progress = Не може се урадити док игра траје.
action-need-more-players = Потребно је више играча за почетак.
action-table-full = Сто је пун.
action-no-bots = Нема ботова за уклањање.
action-bots-cannot = Ботови не могу то да ураде.
action-no-scores = Још нема доступних резултата.

# Dice actions
dice-not-rolled = Још ниси бацио коцке.
dice-locked = Ова коцка је закључана.
dice-no-dice = Нема доступних коцкица.

# Game actions
game-turn-start = Ред играча { $player }.
game-no-turn = Тренутно нико није на реду.
table-no-players = Нема играча.
table-players-one = { $count } играч: { $players }.
table-players-many = { $count } играча: { $players }.
table-spectators = Посматрачи: { $spectators }.
game-leave = Напусти
game-over = Крај игре
game-final-scores = Коначни резултати
game-points = { $count } { $count ->
    [one] поен
   *[other] поена
}
status-box-closed = Затворено.
play = Играј

# Leaderboards
leaderboards = Листе
leaderboards-menu-title = Листе
leaderboards-select-game = Изабери игру за преглед листе
leaderboard-no-data = Још нема података на листи за ову игру.

# Leaderboard types
leaderboard-type-wins = Водећи по победама
leaderboard-type-rating = Оцена вештине
leaderboard-type-total-score = Укупан резултат
leaderboard-type-high-score = Највиши резултат
leaderboard-type-games-played = Одигране игре
leaderboard-type-avg-points-per-turn = Просечни поени по потезу
leaderboard-type-best-single-turn = Најбољи појединачни потез
leaderboard-type-score-per-round = Резултат по рунди

# Leaderboard headers
leaderboard-wins-header = { $game } - Водећи по победама
leaderboard-total-score-header = { $game } - Укупан резултат
leaderboard-high-score-header = { $game } - Највиши резултат
leaderboard-games-played-header = { $game } - Одигране игре
leaderboard-rating-header = { $game } - Оцене вештине
leaderboard-avg-points-header = { $game } - Просечни поени по потезу
leaderboard-best-turn-header = { $game } - Најбољи појединачни потез
leaderboard-score-per-round-header = { $game } - Резултат по рунди

# Leaderboard entries
leaderboard-wins-entry = { $rank }: { $player }, { $wins } { $wins ->
    [one] победа
   *[other] победа
} { $losses } { $losses ->
    [one] пораз
   *[other] пораза
}, { $percentage }% победа
leaderboard-score-entry = { $rank }. { $player }: { $value }
leaderboard-avg-entry = { $rank }. { $player }: { $value } просечно
leaderboard-games-entry = { $rank }. { $player }: { $value } игара

# Player stats
leaderboard-player-stats = Твоје статистике: { $wins } победа, { $losses } пораза ({ $percentage }% победа)
leaderboard-no-player-stats = Још ниси играо ову игру.

# Skill rating leaderboard
leaderboard-no-ratings = Још нема података о оценама за ову игру.
leaderboard-rating-entry = { $rank }. { $player }: { $rating } оцена ({ $mu } ± { $sigma })
leaderboard-player-rating = Твоја оцена: { $rating } ({ $mu } ± { $sigma })
leaderboard-no-player-rating = Још немаш оцену за ову игру.

# My Stats menu
my-stats = Моје статистике
my-stats-select-game = Изабери игру за преглед својих статистика
my-stats-no-data = Још ниси играо ову игру.
my-stats-no-games = Још ниси играо ниједну игру.
my-stats-header = { $game } - Твоје статистике
my-stats-wins = Победе: { $value }
my-stats-losses = Порази: { $value }
my-stats-winrate = Проценат победа: { $value }%
my-stats-games-played = Одигране игре: { $value }
my-stats-total-score = Укупан резултат: { $value }
my-stats-high-score = Највиши резултат: { $value }
my-stats-rating = Оцена вештине: { $value } ({ $mu } ± { $sigma })
my-stats-no-rating = Још нема оцене вештине
my-stats-avg-per-turn = Просечни поени по потезу: { $value }
my-stats-best-turn = Најбољи појединачни потез: { $value }

# Prediction system
predict-outcomes = Предвиди исходе
predict-header = Предвиђени исходи (према оцени вештине)
predict-entry = { $rank }. { $player } (оцена: { $rating })
predict-entry-2p = { $rank }. { $player } (оцена: { $rating }, { $probability }% шанса за победу)
predict-unavailable = Предвиђања оцена нису доступна.
predict-need-players = Потребна су најмање 2 људска играча за предвиђања.
action-need-more-humans = Потребно је више људских играча.
confirm-leave-game = Да ли си сигуран да желиш да напустиш сто?
confirm-yes = Да
confirm-no = Не

# Administration
administration = Администрација
admin-menu-title = Администрација

# Account approval
account-approval = Одобрење налога
account-approval-menu-title = Одобрење налога
no-pending-accounts = Нема налога на чекању.
approve-account = Одобри
decline-account = Одбиј
account-approved = Налог играча { $player } је одобрен.
account-declined = Налог играча { $player } је одбијен и обрисан.

# Waiting for approval (shown to unapproved users)
waiting-for-approval = Твој налог чека одобрење администратора.
account-approved-welcome = Твој налог је одобрен! Добродошао у PlayPalace!
account-declined-goodbye = Твој захтев за налог је одбијен.
    Разлог:
account-banned = Твој налог је блокиран и није доступан.

# Login errors
incorrect-username = Корисничко име које си унео не постоји.
incorrect-password = Лозинка коју си унео је нетачна.
already-logged-in = Овај налог је већ пријављен.

# Decline reason
decline-reason-prompt = Унеси разлог за одбијање (или притисни Escape за отказивање):
account-action-empty-reason = Разлог није наведен.

# Admin notifications for account requests
account-request = захтев за налог
account-action = предузета радња за налог

# Admin promotion/demotion
promote-admin = Унапреди администратора
demote-admin = Разреши администратора
promote-admin-menu-title = Унапреди администратора
demote-admin-menu-title = Разреши администратора
no-users-to-promote = Нема корисника доступних за унапређење.
no-admins-to-demote = Нема администратора доступних за разрешење.
confirm-promote = Да ли си сигуран да желиш да унапредиш { $player } у администратора?
confirm-demote = Да ли си сигуран да желиш да разрешиш { $player } са позиције администратора?
broadcast-to-all = Објави свим корисницима
broadcast-to-admins = Објави само администраторима
broadcast-to-nobody = Тихо (без објаве)
promote-announcement = { $player } је унапређен у администратора!
promote-announcement-you = Унапређен си у администратора!
demote-announcement = { $player } је разрешен са позиције администратора.
demote-announcement-you = Разрешен си са позиције администратора.
not-admin-anymore = Више ниси администратор и не можеш извршити ову радњу.
not-server-owner = Само власник сервера може извршити ову радњу.

# Server ownership transfer
transfer-ownership = Пренеси власништво
transfer-ownership-menu-title = Пренеси власништво
no-admins-for-transfer = Нема администратора доступних за пренос власништва.
confirm-transfer-ownership = Да ли си сигуран да желиш да пренесеш власништво сервера на { $player }? Бићеш разрешен на администратора.
transfer-ownership-announcement = { $player } је сада власник сервера Play Palace!
transfer-ownership-announcement-you = Сада си власник сервера Play Palace!

# User banning
ban-user = Блокирај корисника
unban-user = Одблокирај корисника
no-users-to-ban = Нема корисника доступних за блокирање.
no-users-to-unban = Нема блокираних корисника за одблокирање.
confirm-ban = Да ли си сигуран да желиш да блокираш { $player }?
confirm-unban = Да ли си сигуран да желиш да одблокираш { $player }?
ban-reason-prompt = Унеси разлог за блокирање (необавезно):
unban-reason-prompt = Унеси разлог за одблокирање (необавезно):
user-banned = { $player } је блокиран.
user-unbanned = { $player } је одблокиран.
you-have-been-banned = Блокиран си са овог сервера.
    Разлог:
you-have-been-unbanned = Одблокиран си са овог сервера.
    Разлог:
ban-no-reason = Разлог није наведен.

# Virtual bots (server owner only)
virtual-bots = Виртуелни ботови
virtual-bots-fill = Попуни сервер
virtual-bots-clear = Обриши све ботове
virtual-bots-status = Статус
virtual-bots-clear-confirm = Да ли си сигуран да желиш да обришеш све виртуелне ботове? Ово ће такође уништити све столове на којима се налазе.
virtual-bots-not-available = Виртуелни ботови нису доступни.
virtual-bots-filled = Додато { $added } виртуелних ботова. { $online } је сада на мрежи.
virtual-bots-already-filled = Сви виртуелни ботови из конфигурације су већ активни.
virtual-bots-cleared = Обрисано { $bots } виртуелних ботова и уништено { $tables } { $tables ->
    [one] сто
   *[other] столова
}.
virtual-bot-table-closed = Сто затворен од стране администратора.
virtual-bots-none-to-clear = Нема виртуелних ботова за брисање.
virtual-bots-status-report = Виртуелни ботови: { $total } укупно, { $online } на мрежи, { $offline } ван мреже, { $in_game } у игри.
virtual-bots-guided-overview = Вођени столови
virtual-bots-groups-overview = Групе ботова
virtual-bots-profiles-overview = Профили
virtual-bots-guided-header = Вођени столови: { $count } правило/правила. Алокација: { $allocation }, резервно: { $fallback }, подразумевани профил: { $default_profile }.
virtual-bots-guided-empty = Нису конфигурисани вођени столови.
virtual-bots-guided-status-active = активан
virtual-bots-guided-status-inactive = неактиван
virtual-bots-guided-table-linked = повезан са столом { $table_id } (домаћин { $host }, играчи { $players }, људи { $humans })
virtual-bots-guided-table-stale = сто { $table_id } недостаје на серверу
virtual-bots-guided-table-unassigned = тренутно није праћен ниједан сто
virtual-bots-guided-next-change = следећа промена за { $ticks } корака
virtual-bots-guided-no-schedule = нема распореда
virtual-bots-guided-warning = ⚠ недовољно попуњено
virtual-bots-guided-line = { $table }: игра { $game }, приоритет { $priority }, ботови { $assigned } (мин { $min_bots }, макс { $max_bots }), чека { $waiting }, недоступно { $unavailable }, статус { $status }, профил { $profile }, групе { $groups }. { $table_state }. { $next_change } { $warning_text }
virtual-bots-groups-header = Групе ботова: { $count } ознака/ознака, { $bots } конфигурисаних ботова.
virtual-bots-groups-empty = Нису дефинисане групе ботова.
virtual-bots-groups-line = { $group }: профил { $profile }, ботови { $total } (на мрежи { $online }, чека { $waiting }, у игри { $in_game }, ван мреже { $offline }), правила { $rules }.
virtual-bots-groups-no-rules = нема
virtual-bots-no-profile = подразумевано
virtual-bots-profile-inherit-default = наслеђује подразумевани профил
virtual-bots-profiles-header = Профили: { $count } дефинисано (подразумевано: { $default_profile }).
virtual-bots-profiles-empty = Нису дефинисани профили.
virtual-bots-profiles-line = { $profile } ({ $bot_count } ботова) надјачава: { $overrides }.
virtual-bots-profiles-no-overrides = наслеђује основну конфигурацију

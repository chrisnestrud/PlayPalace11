# スコパ

# ゲーム名
game-name-scopa = スコパ

# ゲームイベント
scopa-initial-table = テーブルカード: { $cards }
scopa-no-initial-table = 開始時にテーブルにカードはありません。
scopa-you-collect = あなたは{ $card }で{ $cards }を集めました
scopa-player-collects = { $player }は{ $card }で{ $cards }を集めました
scopa-you-put-down = あなたは{ $card }を置きました。
scopa-player-puts-down = { $player }は{ $card }を置きました。
scopa-scopa-suffix =  - スコパ!
scopa-clear-table-suffix = 、テーブルをクリアしました。
scopa-remaining-cards = { $player }が残りのテーブルカードを獲得しました。
scopa-scoring-round = スコアリングラウンド...
scopa-most-cards = { $player }が最多カード({ $count }枚)で1点を獲得しました。
scopa-most-cards-tie = 最多カードは引き分け - 点数は授与されません。
scopa-most-diamonds = { $player }が最多ダイヤ({ $count }枚)で1点を獲得しました。
scopa-most-diamonds-tie = 最多ダイヤは引き分け - 点数は授与されません。
scopa-seven-diamonds = { $player }がダイヤの7で1点を獲得しました。
scopa-seven-diamonds-multi = { $player }が最多ダイヤの7({ $count }枚×ダイヤの7)で1点を獲得しました。
scopa-seven-diamonds-tie = ダイヤの7は引き分け - 点数は授与されません。
scopa-most-sevens = { $player }が最多7({ $count }枚)で1点を獲得しました。
scopa-most-sevens-tie = 最多7は引き分け - 点数は授与されません。
scopa-round-scores = ラウンドスコア:
scopa-round-score-line = { $player }: +{ $round_score }(合計: { $total_score })
scopa-table-empty = テーブルにカードはありません。
scopa-no-such-card = その位置にカードはありません。
scopa-captured-count = あなたは{ $count }枚のカードを獲得しました

# 表示アクション
scopa-view-table = テーブルを表示
scopa-view-captured = 獲得したカードを表示

# スコパ特有のオプション
scopa-enter-target-score = 目標スコアを入力(1-121)
scopa-set-cards-per-deal = 配布枚数: { $cards }
scopa-enter-cards-per-deal = 配布枚数を入力(1-10)
scopa-set-decks = デッキ数: { $decks }
scopa-enter-decks = デッキ数を入力(1-6)
scopa-toggle-escoba = エスコバ(合計15): { $enabled }
scopa-toggle-hints = キャプチャヒントを表示: { $enabled }
scopa-set-mechanic = スコパメカニクス: { $mechanic }
scopa-select-mechanic = スコパメカニクスを選択
scopa-toggle-instant-win = スコパで即座に勝利: { $enabled }
scopa-toggle-team-scoring = チームカードをプールしてスコアリング: { $enabled }
scopa-toggle-inverse = 反転モード(目標到達=敗退): { $enabled }

# オプション変更通知
scopa-option-changed-cards = 配布枚数が{ $cards }に設定されました。
scopa-option-changed-decks = デッキ数が{ $decks }に設定されました。
scopa-option-changed-escoba = エスコバが{ $enabled }になりました。
scopa-option-changed-hints = キャプチャヒントが{ $enabled }になりました。
scopa-option-changed-mechanic = スコパメカニクスが{ $mechanic }に設定されました。
scopa-option-changed-instant = スコパでの即座勝利が{ $enabled }になりました。
scopa-option-changed-team-scoring = チームカードスコアリングが{ $enabled }になりました。
scopa-option-changed-inverse = 反転モードが{ $enabled }になりました。

# スコパメカニクス選択肢
scopa-mechanic-normal = ノーマル
scopa-mechanic-no_scopas = スコパなし
scopa-mechanic-only_scopas = スコパのみ

# アクション無効理由
scopa-timer-not-active = ラウンドタイマーはアクティブではありません。

# 検証エラー
scopa-error-not-enough-cards = { $decks }個のデッキには{ $players }人のプレイヤーが各{ $cards_per_deal }枚持つには十分なカードがありません。({ $cards_per_deal } × { $players } = { $cards_needed }枚必要ですが、{ $total_cards }枚しかありません。)

# トレードオフ

# ゲーム情報
game-name-tradeoff = トレードオフ

# ラウンドとイテレーションの流れ
tradeoff-round-start = ラウンド{ $round }。
tradeoff-iteration = ハンド{ $iteration }/3。

# フェーズ1: トレード
tradeoff-you-rolled = あなたは{ $dice }をロールしました。
tradeoff-toggle-trade = { $value }({ $status })
tradeoff-trade-status-trading = トレード中
tradeoff-trade-status-keeping = 保持中
tradeoff-confirm-trades = トレードを確定({ $count }個のサイコロ)
tradeoff-keeping = { $value }を保持します。
tradeoff-trading = { $value }をトレードします。
tradeoff-player-traded = { $player }がトレードしました: { $dice }。
tradeoff-player-traded-none = { $player }はすべてのサイコロを保持しました。

# フェーズ2: プールから取る
tradeoff-your-turn-take = プールからサイコロを取るあなたのターンです。
tradeoff-take-die = { $value }を取る(残り{ $remaining }個)
tradeoff-you-take = あなたは{ $value }を取りました。
tradeoff-player-takes = { $player }は{ $value }を取りました。

# フェーズ3: スコアリング
tradeoff-player-scored = { $player }({ $points }点): { $sets }。
tradeoff-no-sets = { $player }: セットなし。

# セットの説明
tradeoff-set-triple = { $value }のトリプル
tradeoff-set-group = { $value }のグループ
tradeoff-set-mini-straight = ミニストレート{ $low }-{ $high }
tradeoff-set-double-triple = ダブルトリプル({ $v1 }と{ $v2 })
tradeoff-set-straight = ストレート{ $low }-{ $high }
tradeoff-set-double-group = ダブルグループ({ $v1 }と{ $v2 })
tradeoff-set-all-groups = すべてのグループ
tradeoff-set-all-triplets = すべてのトリプレット

# ラウンド終了
tradeoff-round-scores = ラウンド{ $round }のスコア:
tradeoff-score-line = { $player }: +{ $round_points }(合計: { $total })
tradeoff-leader = { $player }が{ $score }点でリードしています。

# ゲーム終了
tradeoff-winner = { $player }が{ $score }点で勝利!
tradeoff-winners-tie = 引き分けです!{ $players }が{ $score }点で並びました!

# ステータスチェック
tradeoff-view-hand = ハンドを表示
tradeoff-view-pool = プールを表示
tradeoff-view-players = プレイヤーを表示
tradeoff-hand-display = あなたのハンド({ $count }個のサイコロ): { $dice }
tradeoff-pool-display = プール({ $count }個のサイコロ): { $dice }
tradeoff-player-info = { $player }: { $hand }。トレード: { $traded }。
tradeoff-player-info-no-trade = { $player }: { $hand }。何もトレードしませんでした。

# エラーメッセージ
tradeoff-not-trading-phase = トレードフェーズではありません。
tradeoff-not-taking-phase = テイクフェーズではありません。
tradeoff-already-confirmed = 既に確定しています。
tradeoff-no-die = 切り替えるサイコロがありません。
tradeoff-no-more-takes = これ以上取ることはできません。
tradeoff-not-in-pool = そのサイコロはプールにありません。

# オプション
tradeoff-set-target = 目標スコア: { $score }
tradeoff-enter-target = 目標スコアを入力:
tradeoff-option-changed-target = 目標スコアが{ $score }に設定されました。

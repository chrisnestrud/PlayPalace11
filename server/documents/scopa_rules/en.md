# Rules Of Scopa
PlayPalace team, 2026.

## TL;DR
Scopa is a classic Italian card game whose origins stretch back to at least the 18th century. The name means "broom" in Italian, referring to the act of sweeping all the cards off the table. It is one of the most popular card games in Italy and has many regional variants played across the Mediterranean.

The goal is to capture cards from the table by playing cards from your hand that match table cards by rank, or whose value equals the sum of multiple table cards. At the end of each round, points are awarded for having the most cards, the most diamonds, the 7 of diamonds, and the most sevens. Clearing the entire table in a single capture earns you a coveted "scopa" point. The first player (or team) to reach a target score wins.

## Gameplay
Scopa is traditionally played with an Italian deck of 40 cards, but in PlayPalace we use a standard deck with the picture cards removed.

The game is divided into rounds. At the start of each round, a dealer is selected (the dealer rotates each round), the deck is shuffled, and cards are dealt. Play begins with the player to the dealer's left and proceeds in turn order.

### On Your Turn
On your turn, you must play exactly one card from your hand. One of two things happens:

If the card you play matches the rank of a card on the table, you capture that table card (along with the card you played) and add both to your captured pile. If no single card matches by rank, but multiple table cards add up to the rank of your played card, you capture that entire set instead. If a rank match exists, it takes priority over sum combinations. When multiple capture options are available, the game automatically selects the one that captures the most cards.

If your card does not match any table card by rank, and no combination of table cards sums to its value, the card is simply placed on the table alongside the others.

When all players run out of cards, a new deal occurs from the remaining deck. This continues until the deck is exhausted, at which point the round ends. Any cards remaining on the table after the final play are awarded to whichever player made the last capture during that round.

### Example
It is round 1 and you are dealt a 7, a 3, and a 10. The table has a 4, a 3, and a 6 on it.

You play your 7. It sums up to the 4 and 3 on the table, so you capture both cards. The table now has just the 6.

Your opponent then puts a four on the table. The  6 you left is still there. You play your 10. The 4 and 6 on the table sum to 10, so you capture both of them. The table is now empty, which means you have scored a scopa! That is an extra point for you.

On your next turn, you clearly must play your 3, since it's your last card that deal.

### Scoring
At the end of each round, points are awarded in the following categories. In each category, if there is a tie, no one receives the point.

* **Most cards:** The player (or team) who captured the most cards earns 1 point.
* **Most diamonds:** The player (or team) who captured the most diamonds earns 1 point.
* **7 of diamonds:** The player (or team) who captured the 7 of diamonds earns 1 point.
* **Most sevens:** The player (or team) who captured the most 7s earns 1 point.
Also: each time you clear the entire table with a capture during the round, you earn 1 point immediately (these are tallied as you play, not at the end).

The default target score is 11, though the host can set it anywhere from 1 to 121. The first player or team to reach the target score wins the game. If multiple players reach the target in the same round, the highest score wins.

### Game Variants
The host can configure several options that change how the game plays:

* **Escoba mode:** Instead of matching by rank, captures are made by finding combinations of table cards that, together with the played card, sum to 15. This is the Spanish variant of Scopa.
* **Scopa mechanic:** Can be set to "normal" (scopas are scored as usual), "no scopas" (clearing the table does not award a bonus point), or "only scopas" (only scopa points count; the four standard scoring categories are skipped entirely).
* **Instant win scopas:** When enabled, a player wins immediately upon reaching the target score from scopa points, rather than waiting for the round to end.
* **Inverse Scopa:** A reverse mode where reaching the target score eliminates you instead. The last player standing wins. If everyone is eliminated in the same round, the player with the lowest score wins.
* **Cards per deal:** The number of cards dealt to each player per deal (default 3, range 1-10).
* **Number of decks:** Multiple decks can be combined for larger groups (1-6 decks).
* **Team mode:** Players can be organized into teams, with various configurations available depending on the number of players.
* **Team card scoring:** When playing in teams, team members' captured cards are pooled together for scoring purposes (enabled by default).
* **Show capture hints:** When enabled, each card in your hand displays a hint showing what it would capture if played.

## Keyboard Shortcuts
Shortcuts specific to the game of Scopa:
* C: View all table cards.
* D: View your captured card count.
* 1-9: View a specific table card by position (1st through 9th).
* 0: View the 10th table card.
* T: Check whose turn it is.
* S: Check current scores.
* Shift+S: View detailed scores.
* P: Pause or skip the round timer (host only).

## Game Theory / Tips
* Pay attention to which sevens and diamonds have been captured. These are worth a disproportionate amount of the round's scoring categories, so capturing them is almost always worthwhile.
* The 7 of diamonds is the single most valuable card in the game. It contributes to three of the four scoring categories (most diamonds, 7 of diamonds, most sevens). Prioritize capturing it whenever possible.
* When you have no capture available, prefer playing cards that are hard for your opponent to use. This depends on the variation, but generally it means playing high cards in normal Scopa (9+) and cards of a value less than 5 in Escoba.
* To elaborate, in Escoba, cards with a value of 4 or lower are safe to play onto an empty table, since no single card in the deck can combine with a table card that low to reach 15. This prevents your opponent from getting both a capture and a scopa on their next turn.

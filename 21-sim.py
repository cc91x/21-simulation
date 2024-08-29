from bankroll import Bankroll
from count import Count
from shoe import Shoe
from gameplayConfig import GameplayConfig as cfg
from gameplayEngine import GameplayEngine
from handAnalyzer import HandAnalyzer


if __name__ == '__main__':
    shoe = Shoe(cfg.DECKS_IN_SHOE, cfg.CUT_CARD_RANGE)
    shoe.shuffle()
    bankroll = Bankroll(0)
    count = Count(cfg.DECKS_IN_SHOE, cfg.STARTING_COUNT)
    hand_analyzer = HandAnalyzer()
    game = GameplayEngine(bankroll, count, shoe, hand_analyzer)

    game.play_blackjack()

    hand_analyzer.display_info()

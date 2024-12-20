from bankroll import Bankroll
from count import Count
from gameplay_config import GameplayConfig as cfg
from gameplay_engine import GameplayEngine
from hand_analyzer import HandAnalyzer
from shoe import Shoe
from util_functions import print_game_configuration


if __name__ == '__main__':
    shoe = Shoe(cfg.DECKS_IN_SHOE, cfg.CUT_CARD_RANGE)
    bankroll = Bankroll(0)
    count = Count(cfg.DECKS_IN_SHOE, cfg.STARTING_COUNT)
    hand_analyzer = HandAnalyzer()
    game = GameplayEngine(bankroll, count, shoe, hand_analyzer)

    print_game_configuration()
    shoe.shuffle()
    game.play_blackjack()
    hand_analyzer.display_info()
    hand_analyzer.save_simulation_results()

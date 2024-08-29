from bankroll import Bankroll
from card import Card
from constants import HandResult
from count import Count
from shoe import Shoe
from dealerHand import DealerHand
from customLogging import global_logger as logger
from gameplayConfig import GameplayConfig as cfg
from gameplayEngine import GameplayEngine
from playerHand import PlayerHand

deck = Shoe(cfg.DECKS_IN_SHOE, cfg.CUT_CARD_RANGE)
count = Count(cfg.DECKS_IN_SHOE, 0)

bankroll = Bankroll(0)
cards = [Card('HEARTS', '8'), Card('HEARTS', '3'), Card('HEARTS', 'A')]
player_hands = [PlayerHand(bankroll, 10, cards)]

dealer_cards = [Card('HEARTS', '5'), Card('HEARTS', '10'), Card('HEARTS', '4')]
dealer_hand = DealerHand(dealer_cards)

game = GameplayEngine(logger, count, deck)
res = game.determine_hand_results(player_hands, dealer_hand)

print(res)




""" This file is used mainly for debugging specific hands and scenarios  """

from bankroll import Bankroll
from card import Card
from constants import CardRank, Suit
from count import Count
from shoe import Shoe
from dealer_hand import DealerHand
from custom_logging import global_logger as logger
from hand_analyzer import HandAnalyzer
from gameplay_config import GameplayConfig as cfg
from gameplay_engine import GameplayEngine
from player_hand import PlayerHand

# Remember to set the logging level to CARD or DECISION in the config file
shoe = Shoe(cfg.DECKS_IN_SHOE, cfg.CUT_CARD_RANGE)
count = Count(cfg.DECKS_IN_SHOE, 0)
bankroll = Bankroll(0)
hand_analyzer = HandAnalyzer()
game = GameplayEngine(bankroll, count, shoe, hand_analyzer)
shoe.shuffle()

# Input specific hand cards here
player_card_1 = Card(Suit.SPADE, CardRank.ACE)
player_card_2 = Card(Suit.HEART, CardRank.ACE)
dealer_face_up_card = Card(Suit.SPADE, CardRank.FOUR)
dealer_face_down_card = Card(Suit.SPADE, CardRank.TEN)
next_cards_to_deal = [
    dealer_face_down_card, dealer_face_up_card, Card(Suit.SPADE, CardRank.SEVEN), 
    Card(Suit.SPADE, CardRank.SIX), Card(Suit.SPADE, CardRank.NINE), Card(Suit.SPADE, CardRank.JACK), Card(Suit.SPADE, CardRank.JACK)
]

for card in next_cards_to_deal[::-1]:
    shoe.add_to_front_of_deck(card)

player_cards = [player_card_1, player_card_2]
player_hands = [PlayerHand(bankroll, 1, player_cards)]
dealer_hand = DealerHand([])
dealer_hand.deal_card_face_down(shoe)
dealer_hand.deal_card_face_up(shoe, count, logger)
game.play_hand(player_hands, dealer_hand)

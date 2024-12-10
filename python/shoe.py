""" A class representing the a deck of cards as it is dealt """

from random import randint, shuffle

from card import Card
from constants import CardRank, Suit


class Shoe():

    def __init__(self, num_decks, cut_card_range=[75,75]):
        self._cut_card_range = cut_card_range
        self._cut_card_point = self._calculate_cut_card_point()
        self._dealt = []
        self._in_shoe = []
        self._num_decks = num_decks
        self._num_shuffles = 0
        for _ in range(num_decks):
            self._add_new_deck(self._in_shoe)

    @property
    def dealt(self):
        return self._dealt

    @property
    def num_decks(self):
        return self._num_decks 

    @property
    def num_cards(self):
        return self.num_decks * 52
    
    @property
    def num_shuffles(self):
        return self._num_shuffles
    
    # only used for testing
    def add_to_front_of_deck(self, card):
        self._in_shoe.append(card)

    def deal_card(self):
        if len(self._in_shoe) == 0:
            raise Exception('Out of cards')
        else:
            card = self._in_shoe.pop()
            self.dealt.append(card)
            return card

    def should_reshuffle(self):
        return (len(self._dealt) / self.num_cards) > self._cut_card_point    

    def shuffle(self):
        """Moves all of the dealt cards back to the shoe and shuffles"""
        self._in_shoe.extend(self._dealt)
        self._dealt = []
        shuffle(self._in_shoe)
        self._num_shuffles += 1 
        self.cut_card_point = self._calculate_cut_card_point()
    
    def _add_new_deck(self, shoe):
        for suit in Suit:
            for card in CardRank:
                shoe.append(Card(suit, card))

    def _calculate_cut_card_point(self):
        lo, hi = self._cut_card_range
        return randint(lo, hi) / 100.0


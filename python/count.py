""" A class which handles the counting of cards """

from math import ceil, floor

from gameplay_config import GameplayConfig as cfg
from util_functions import load_1d_decision_matrix

DECK_LENGTH = 52


class Count():
    
    def __init__(self, num_decks, starting_count):
        self._cards_dealt = []
        self._count_matrix = load_1d_decision_matrix(cfg.COUNT_DIRECTORY + 'COUNT_CARD_VALUES.csv')
        self._num_decks = num_decks
        self._running_count = starting_count
        self._starting_count = starting_count

    @property 
    def count(self):
        if cfg.CONVERT_TO_TRUE_COUNT:
            decks_remaining = self._num_decks - (int(round(len(self._cards_dealt) / DECK_LENGTH, 0)))
            true_count_raw = self._running_count / (decks_remaining if decks_remaining != 0 else 1)
            val = floor(true_count_raw) if self._running_count > 0 else ceil(true_count_raw)
            return val
        else:
            return self._running_count

    @property
    def num_decks(self):
        return self._num_decks

    def count_card(self, card):
        self._cards_dealt.append(card)
        self._running_count += self._count_matrix.get(card.numeric_value)

    def reset(self):
        self._cards_dealt = []
        self._running_count = self._starting_count

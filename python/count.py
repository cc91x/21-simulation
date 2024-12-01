""" A class which handles the counting of cards """

from math import ceil, floor

from gameplay_config import GameplayConfig as cfg
from util_functions import load_1d_decision_matrix


class Count():
    
    def __init__(self, num_decks, starting_count):
        self._cards_dealt = []
        self._count_matrix = load_1d_decision_matrix(cfg.COUNT_DIRECTORY + 'COUNT_CARD_VALUES.csv')
        self._num_decks = num_decks
        self._running_count = starting_count

    @property 
    def count(self):
        if cfg.CONVERT_TO_TRUE_COUNT:
            true_count_raw = self._running_count / self.num_decks
            return floor(true_count_raw) if self._running_count > 0 else ceil(true_count_raw)
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
        self._running_count = 0

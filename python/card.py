""" A class representing a card """
 

class Card():

    def __init__(self, suit, card_rank):
        self._numeric_value = card_rank.value
        self._rank = card_rank.rank
        self._suit = suit

    @property
    def numeric_value(self):
        return self._numeric_value

    @property
    def suit(self):
        return self._suit  
    
    def get_card_string(self):
        return f'[{self._rank}{self.suit.value}]'
    
    def is_ace(self):
        return self._rank == 'A'

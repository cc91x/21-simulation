""" A class representing the player's hand """

from hand import Hand


class PlayerHand(Hand):
    def __init__(self, bankroll, bet_value, starter_cards, is_split=False):
        super().__init__(starter_cards, 'Player')
        self._bankroll = bankroll
        self._bet_value = bet_value
        self._number_hits_allowed = 10 
        self._has_insurance = False
        self._is_split = is_split
        self._is_surrendered = False
        bankroll.subtract(bet_value)

    @property
    def bankroll(self):
        return self._bankroll

    @property
    def bet_value(self):
        return self._bet_value
    
    @property
    def is_allowed_to_hit(self):
        return (not self._is_surrendered) and (self._number_hits_allowed > 0)

    @property
    def has_insurance(self):
        return self._has_insurance
    
    @property 
    def is_split(self):
        return self._is_split 
    
    @property 
    def is_surrendered(self):
        return self._is_surrendered 

    def limit_to_one_hit(self):
        if self._number_hits_allowed > 0:
            self._number_hits_allowed = 1

    def count_hit(self):
        self._number_hits_allowed -= 1

    def double_down(self):
        self._bankroll.subtract(self._bet_value)
        self._bet_value *= 2
   
    def get_initial_deal(self):
        return self._cards[:2]

    def is_blackjack(self):
        return (not self.is_split) and (self.get_optimal_score() == 21) and (len(self.cards) == 2)

    def split_hand(self):
        self._bankroll.add(self._bet_value)
        hand1 = PlayerHand(self._bankroll, self._bet_value, [self._cards[0]], is_split=True)
        hand2 = PlayerHand(self._bankroll, self._bet_value, [self._cards[1]], is_split=True)
        return [hand1, hand2]                   

    def surrender(self):
        self._is_surrendered = True

    def take_insurance(self):
        self._insurance = True
        self._bankroll.subtract(self._bet_value / 2)

""" A class representing the player's hand """


from hand import Hand
from vingtFunctions import calculate_win_amount


class PlayerHand(Hand):
    def __init__(self, bankroll, bet_value, starter_cards):
        super().__init__(starter_cards, 'Player')
        self._bankroll = bankroll
        self._bet_value = bet_value 
        self._insurance = False
        bankroll.subtract(bet_value)

    @property
    def bankroll(self):
        return self._bankroll

    @property
    def bet_value(self):
        return self._bet_value

    @property
    def insurance(self):
        return self._insurance
    
    
    def double_down(self):
        self._bankroll.subtract(self._bet_value)
        self._bet_value *= 2
   
    def get_initial_deal(self):
        return self._cards[:2]

    def get_win_amount(self, result, does_dealer_have_blackjack):
        win_amount = calculate_win_amount(result, self._bet_value)
        if does_dealer_have_blackjack and self._insurance:
            win_amount += self._bet_value

        return win_amount

    def split_hand(self):
        hand1 = PlayerHand(self._bankroll, self._bet_value, [self._cards[0]])
        hand2 = PlayerHand(self._bankroll, self._bet_value, [self._cards[1]])
        return [hand1, hand2]                   

    def surrender(self):
        self._bankroll.add(self._bet_value / 2)

    def take_insurance(self):
        self._insurance = True
        self._bankroll.subtract(self._bet_value / 2)

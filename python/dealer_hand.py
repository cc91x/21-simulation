""" A class representing the dealer's hand """

from hand import Hand


class DealerHand(Hand):

    def __init__(self, starter_cards):
        super().__init__(starter_cards, 'Dealer')
        self._face_down_card = None
        # self._face_down_card = None if starter_cards == [] else starter_cards[0]

    def deal_card_face_down(self, card):
        self._cards.append(card)
        self._face_down_card = card 

    def get_dealer_score(self):
        """Returns optimal dealer score. Note this is different than 
           get_optimal_score, as the ace is valued at 1 for soft 16's
           and below"""
        baseTotal = self.get_non_aces_hand_total()
        
        if self._get_aces_count() == 0:
            return baseTotal
        
        if baseTotal >= 6 and baseTotal <= 10:
            return baseTotal + 11
        else:
            return baseTotal + 1 
        
    def get_face_up_card(self):
        for card in self._cards:
            if self._face_down_card != card:
                return card 

    def reveal_face_down_card(self, count):
        if not self._face_down_card:
            raise Exception('There is no dealer face down card')
        else:
            count.count_card(self._face_down_card)

""" A parent class for PlayerHand and DealerHand classes"""


class Hand():
    def __init__(self, cards, hand_type='PLAYER'):
        self._cards = cards
        self._hand_type = hand_type

    @property
    def cards(self):
        return self._cards

    def _get_aces_count(self):
        return len(list(filter(lambda x: x.is_ace(), self._cards)))
    
    def contains_ace(self):
        return self._get_aces_count() != 0

    def deal_card_face_up(self, card, running_count, logger):
      logger.decision(f'Dealt card to {self._hand_type}: {card.get_card_string()}')
      self.cards.append(card)
      running_count.count_card(card)

    def get_hand_string(self):
        return f'{self._hand_type} [{"".join(card.get_card_string() for card in self.cards)}]'
    
    def get_non_aces_hand_total(self):
        """ Returns the sum of the hand excluding one ace. If there are 
            no aces present, returns the score of the hand. If there are
            1...n aces, values n-1 aces each at 1.
        """
        base_total, seen_ace = 0, False 
        for card in self.cards: 
            if card.is_ace() and not seen_ace:
                seen_ace = True
            else: 
                base_total += 1 if card.is_ace() else card.numeric_value
        return base_total

    def get_optimal_score(self):
        """Returns the score if there are no aces in hand. If there is
           an ace, returns the highest possible score 21 or under. """
        base_total = self.get_non_aces_hand_total()
    
        if self._get_aces_count() == 0:
            return base_total
        
        return base_total + 11 if base_total <= 10 else base_total + 1

    def is_blackjack(self):
        return self.get_optimal_score() == 21 and len(self.cards) == 2

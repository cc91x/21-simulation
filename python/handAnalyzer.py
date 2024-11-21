""" A class for processing the results throughout the simulation """

from constants import STRATEGY_NAME
from customLogging import global_logger as logger
from hand import Hand

COUNT = 'Count'
HANDS_PLAYED = '# Hands'
PNL = 'PNL'
DASH = '-'
FIRST_COL_OFFSET = 4


class HandAnalyzer():

    def __init__(self):
        self._hands_by_cards = {}
        self._hands_by_cards_aces = {}
        self._hands_by_count = {}
        self._hands_played = 0

    @property
    def hands_played(self):
        return self._hands_played
     
    def _display_card_based_logging(self, matrix, col_prefix_func):
        max_pnl_str, max_hand_str = len(PNL), len(HANDS_PLAYED)
        for _, d in matrix.items():
            for hand, pnl in d.values():
                max_pnl_str = max(max_pnl_str, len(str(pnl)))
                max_hand_str = max(max_hand_str, len(str(hand)))

        col_width = max_pnl_str + max_hand_str + 3
        
        header_1_str = ' ' * FIRST_COL_OFFSET
        header_2_str = ' ' * FIRST_COL_OFFSET
        dash_str = '-' * (FIRST_COL_OFFSET + 1) 
        for i in range(2, 12):
            header_1_str += f' |{str(i).center(col_width - 1)}'
            header_2_str += f' | {HANDS_PLAYED.rjust(max_hand_str)} {PNL.rjust(max_pnl_str)}'
            dash_str += f'|{DASH * (col_width)}'
        
        logger.summary(header_1_str)
        logger.summary(header_2_str)
        logger.summary(dash_str)
    
        for pair_val in self._min_range(matrix.keys()):
            results_by_dealer_card = matrix.get(pair_val, {})
            row_str = col_prefix_func(pair_val)
            for dealer_card in range(2, 12):
                hands_played, pnl = results_by_dealer_card.get(dealer_card, (0, 0))
                row_str += f' | {str(hands_played).rjust(max_hand_str)} {str(pnl).rjust(max_pnl_str)}'
            logger.summary(row_str)

    def _display_count_based_logging(self):
        max_count_len = max(len(COUNT), max(len(str(ct)) for ct in self._hands_by_count.keys()))
        max_hands_len = max(len(HANDS_PLAYED), max(len(str(h)) for h, _ in self._hands_by_count.values()))
        max_pnl_len = max(len(PNL), max(len(str(p)) for _, p in self._hands_by_count.values()))
        
        logger.summary('')
        logger.summary('HAND STATISTICS BY COUNT')
        
        logger.summary(f'{COUNT.rjust(max_count_len)} | {HANDS_PLAYED.rjust(max_hands_len)} | {PNL.rjust(max_pnl_len)}')
        logger.summary(f'{DASH * max_count_len}-|-{DASH * max_hands_len}-|-{DASH * max_pnl_len}')
        
        for count in self._min_range(self._hands_by_count.keys()):
            hands_played, pnl = self._hands_by_count.get(count, (0, 0))
            logger.summary(f'{str(count).rjust(max_count_len)} | {str(hands_played).rjust(max_hands_len)} | {str(pnl).rjust(max_pnl_len)}')

    def _display_summary_statistics(self):
        logger.summary('')
        ending_pnl = sum(bal for _, bal in self._hands_by_count.values())
        logger.summary(f'Simulation Complete. Played {self._hands_played} hands. Ending Pnl is {ending_pnl}.')
        logger.summary(f'Used strategy: {STRATEGY_NAME}')
        
    def _format_aces_pair(self, val):
        return f'A,{val}:' 

    def _format_pair(self, val):
        return f'{str(val).rjust(3)}:'
    
    def _min_range(self, lst):
        return range(min(lst), max(lst) + 1)
    
    def _update_count_based_log(self, count, handPnl):
        hands_played, balance = self._hands_by_count.get(count.count, (0, 0))
        self._hands_by_count[count.count] = (hands_played + 1, balance + handPnl)
    
    def _update_cards_based_log(self, d, hand, dealerUpCard, handPnl):
        score = hand.get_non_aces_hand_total()
        if not score in d:
                d[score] = {}

        hands_played, balance = d.get(score).get(dealerUpCard.numeric_value, (0, 0)) 
        d[score][dealerUpCard.numeric_value] = (hands_played + 1, balance + handPnl) 


    def analyze_hand(self, playerHand, dealerUpCard, handPnl, count):
        self._update_count_based_log(count, handPnl)

        playerDealtCards = Hand(playerHand.get_initial_deal())
        if playerDealtCards.contains_ace():
            self._update_cards_based_log(self._hands_by_cards_aces, playerDealtCards, dealerUpCard, handPnl)
        else: 
            self._update_cards_based_log(self._hands_by_cards, playerDealtCards, dealerUpCard, handPnl)

        self._hands_played += 1

    def display_info(self): 
        logger.summary('END OF GAME ANALYSIS \n')

        if len(self._hands_by_cards_aces) > 0: 
            logger.summary('')
            logger.summary('HAND STATISTICS BY ACE, CARD vs DEALER UP CARD')
            self._display_card_based_logging(self._hands_by_cards_aces, self._format_aces_pair)

        if len(self._hands_by_cards) > 0:
            logger.summary('')
            logger.summary('HAND STATISTICS BY PAIR TOTAL vs DEALER UP CARD')
            self._display_card_based_logging(self._hands_by_cards, self._format_pair)

        self._display_count_based_logging()
        self._display_summary_statistics()  

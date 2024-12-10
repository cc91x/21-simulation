""" A class for processing the results throughout the simulation """

from datetime import datetime

from custom_logging import global_logger as logger
from gameplay_config import GameplayConfig as cfg
from hand import Hand

COUNT = 'Count'
HANDS_PLAYED = 'Hands'
PNL = 'PNL'
EDGE_PCT = 'Edge %'
DASH = '-'
FIRST_COL_OFFSET = 4
FIRST_COL_OFFSET_ACES = 5
MAX_EDGE_LEN = 6 # ex. -12.34


class HandAnalyzer():

    def __init__(self):
        self._hands_by_cards = {}
        self._hands_by_cards_aces = {}
        self._hands_by_count = {}
        self._hands_played = 0
        self._start_time = datetime.now()

    @property
    def hands_played(self):
        return self._hands_played
    
    def _aggregate_stats_from_range(self, count_range):
        hands, pnl, wager = 0, 0, 0
        for count in count_range:
            h, p, w = self._hands_by_count.pop(count, (0, 0, 0))
            hands += h
            pnl += p 
            wager += w
        return (hands, pnl, wager)
    
    def _calculate_player_edge(self, hands_played, total_pnl, total_stake):
        if hands_played == 0:
            return 0.0
        else:
            edge = total_pnl / total_stake
            return round(edge * 100, 2) 
     
    def _display_card_based_logging(self, matrix, column_prefix_func, header_column_offset):
        max_pnl_str, max_hand_str = len(PNL), len(HANDS_PLAYED)
        for _, d in matrix.items():
            for hand, pnl in d.values():
                max_pnl_str = max(max_pnl_str, len(str(pnl)))
                max_hand_str = max(max_hand_str, len(str(hand)))

        col_width = max_pnl_str + max_hand_str  + 3
        
        header_1_str = ' ' * header_column_offset
        header_2_str = ' ' * header_column_offset
        dash_str = '-' * (header_column_offset + 1) 
        for i in range(2, 12):
            header_1_str += f' |{str(i).center(col_width - 1)}'
            header_2_str += f' | {HANDS_PLAYED.rjust(max_hand_str)} {PNL.rjust(max_pnl_str)}'
            dash_str += f'|{DASH * (col_width)}'
        
        logger.summary(header_1_str)
        logger.summary(header_2_str)
        logger.summary(dash_str)
    
        for pair_val in self._min_range(matrix.keys()):
            results_by_dealer_card = matrix.get(pair_val, {})
            row_str = column_prefix_func(pair_val)
            for dealer_card in range(2, 12):
                hands_played, pnl = results_by_dealer_card.get(dealer_card, (0, 0))
                row_str += f' | {str(hands_played).rjust(max_hand_str)} {str(pnl).rjust(max_pnl_str)}'
            logger.summary(row_str)

    def _display_count_based_logging(self):
        max_count_len = max(len(COUNT), max(len(str(ct)) for ct in self._hands_by_count.keys()))
        max_hands_len = max(len(HANDS_PLAYED), max(len(str(h)) for h, _, _ in self._hands_by_count.values()))
        max_pnl_len = max(len(PNL), max(len(str(p)) for _, p, _ in self._hands_by_count.values()))
        
        logger.summary('')
        logger.summary('HAND STATISTICS BY COUNT')
        
        logger.summary(f'{COUNT.rjust(max_count_len)} | {HANDS_PLAYED.rjust(max_hands_len)} | ' +
                       f'{PNL.center(max_pnl_len)} | {EDGE_PCT.rjust(MAX_EDGE_LEN + 1)}')
        logger.summary(f'{DASH * max_count_len}-|-{DASH * max_hands_len}-|-{DASH * max_pnl_len}-|' + 
                       f'-{DASH * (MAX_EDGE_LEN + 1)}-')
        
        self._condense_counts_indices()
        for count in self._min_range(self._hands_by_count.keys()):
            hands_played, total_pnl, total_stake = self._hands_by_count.get(count, (0, 0, 0))
            edge = self._calculate_player_edge(hands_played, total_pnl, total_stake)
            logger.summary(f'{str(count).rjust(max_count_len)} | {str(hands_played).rjust(max_hands_len)} |' + 
                            f' {str(total_pnl).rjust(max_pnl_len)} | {str(edge).rjust(MAX_EDGE_LEN)}%')

    def _display_summary_statistics(self):
        logger.summary('')
        total_pnl = self._get_total_pnl()
        player_edge_pct = self._calculate_player_edge(self._hands_played, total_pnl, self._get_total_stake())
        symbol = '+' if total_pnl >= 0 else ''

        logger.summary(f'Simulation Complete. Played {self._hands_played} hands. Final Pnl is {symbol}{total_pnl} units')
        logger.summary(f'Player edge in this simulation: {player_edge_pct}%')
        logger.summary(f'Used strategy: {cfg.STRATEGY_NAME}')
        
    def _get_total_pnl(self):
        return sum(bal for _, bal, _ in self._hands_by_count.values())
    
    def _get_total_stake(self):
        return sum(stake for _, _, stake in self._hands_by_count.values())

    def _format_aces_pair(self, val):
        return f'A,{val}:'.rjust(5) 

    def _format_pair(self, val):
        return f'{str(val).rjust(3)}:'
    
    def _min_range(self, lst):
        return range(min(lst), max(lst) + 1)
    
    def _condense_counts_indices(self):
        std_min, std_max = min(self._hands_by_count.keys()), max(self._hands_by_count.keys())
        config_min, config_max = cfg.RECORDING_RANGE
        
        hands, pnl, wager = self._aggregate_stats_from_range(range(std_min, config_min))
        min_hands, min_pnl, min_wager = self._hands_by_count.get(config_min, (0, 0, 0))
        self._hands_by_count[config_min] = (hands + min_hands, pnl + min_pnl, wager + min_wager)

        hands, pnl, wager = self._aggregate_stats_from_range(range(config_max + 1, std_max + 1))
        max_hands, max_pnl, max_wager = self._hands_by_count.get(config_max, (0, 0, 0))
        self._hands_by_count[config_max] = (hands + max_hands, pnl + max_pnl, wager + max_wager) 

    def _update_count_based_log(self, pre_hand_count, hand_pnl, bet_units):
        hands_played, current_pnl, stake = self._hands_by_count.get(pre_hand_count, (0, 0, 0))
        self._hands_by_count[pre_hand_count] = (hands_played + 1, current_pnl + hand_pnl, stake + bet_units)
    
    def _update_cards_based_log(self, d, hand, dealer_up_card, hand_pnl):
        score = hand.get_non_aces_hand_total()
        if not score in d:
                d[score] = {}

        hands_played, balance = d.get(score).get(dealer_up_card.numeric_value, (0, 0)) 
        d[score][dealer_up_card.numeric_value] = (hands_played + 1, balance + hand_pnl) 


    def analyze_hand(self, player_hand, dealer_up_card, hand_pnl, pre_hand_count, bet_units):
        self._update_count_based_log(pre_hand_count, hand_pnl, bet_units)
        player_dealt_cards = Hand(player_hand.get_initial_deal())
        
        if player_dealt_cards.contains_ace():
            self._update_cards_based_log(self._hands_by_cards_aces, player_dealt_cards, dealer_up_card, hand_pnl)
        else: 
            self._update_cards_based_log(self._hands_by_cards, player_dealt_cards, dealer_up_card, hand_pnl)

        self._hands_played += 1

    def display_info(self): 
        logger.summary('END OF GAME ANALYSIS \n')

        if len(self._hands_by_cards_aces) > 0: 
            logger.summary('')
            logger.summary('HAND STATISTICS BY ACE, CARD vs DEALER UP CARD')
            self._display_card_based_logging(self._hands_by_cards_aces, self._format_aces_pair, FIRST_COL_OFFSET_ACES)

        if len(self._hands_by_cards) > 0:
            logger.summary('')
            logger.summary('HAND STATISTICS BY PAIR TOTAL vs DEALER UP CARD')
            self._display_card_based_logging(self._hands_by_cards, self._format_pair, FIRST_COL_OFFSET)

        self._display_count_based_logging()
        self._display_summary_statistics()  

    def save_simulation_results(self):
        endtime = datetime.now()
        duration = endtime - self._start_time
        rows = [
            f'Finished running simulation at {endtime.strftime("%Y-%m-%d %H:%M:%S")}',
            f'Simulation duration: {int(duration.total_seconds() // 60)}m{int(duration.total_seconds() % 60)}s{int(duration.microseconds // 1000)}ms',
            f'Hands Played: {self._hands_played}',
            f'Player edge: {self._calculate_player_edge(self._hands_played, self._get_total_pnl(), self._get_total_stake())}%',
            f'Strategy: {cfg.STRATEGY_NAME}',
            '-- Game Rules -- ',
            f'DECKS_IN_SHOE={cfg.DECKS_IN_SHOE}',
            f'CUT_CARD_RANGE={cfg.CUT_CARD_RANGE}',
            f'BLACKJACK_PAYOUT={cfg.BLACKJACK_PAYOUT}',
            f'DEALER_HIT_SOFT_17={cfg.DEALER_HIT_SOFT_17}',
            f'SPLIT_MAX_TIMES={cfg.SPLIT_MAX_TIMES}',
            f'SURRENDER_ALLOWED={cfg.SURRENDER_ALLOWED}',
            f'CONVERT_TO_TRUE_COUNT={cfg.CONVERT_TO_TRUE_COUNT}',
            f'STARTING_COUNT={cfg.STARTING_COUNT}'
        ]

        with open("../results/simulation_results.txt", "a") as f:
            for row in rows:
                f.write(row)
                f.write('\n')
            f.write('\n\n')

""" Class performing all game related player decisions, as configured in csv's"""

from custom_logging import global_logger as logger
from gameplay_config import GameplayConfig as cfg
from util_functions import adjust_to_range, do_matrix_lookup_3d, load_1d_decision_matrix, load_3d_decision_matrix


class DecisionEngine():

    def __init__(self, count):
        self._count = count
        self._bet_sizing_mapping = load_1d_decision_matrix(cfg.COUNT_DIRECTORY + 'BET_SIZING_MAPPING.csv')
        self._hard_should_hit_matrix = load_3d_decision_matrix(cfg.COUNT_DIRECTORY + 'HARD_SHOULD_HIT_MATRIX.csv')
        self._hard_should_double_matrix = load_3d_decision_matrix(cfg.COUNT_DIRECTORY + 'HARD_SHOULD_DOUBLE_MATRIX.csv')
        self._should_split_matrix = load_3d_decision_matrix(cfg.COUNT_DIRECTORY + 'SHOULD_SPLIT_MATRIX.csv')
        self._should_surrender_matrix = load_3d_decision_matrix(cfg.COUNT_DIRECTORY + 'SHOULD_SURRENDER_MATRIX.csv')
        self._should_take_insurance_matrix = load_1d_decision_matrix(cfg.COUNT_DIRECTORY + 'SHOULD_TAKE_INSURANCE_MATRIX.csv')
        self._soft_should_hit_matrix = load_3d_decision_matrix(cfg.COUNT_DIRECTORY + 'SOFT_SHOULD_HIT_MATRIX.csv')
        self._soft_should_double_matrix = load_3d_decision_matrix(cfg.COUNT_DIRECTORY + 'SOFT_SHOULD_DOUBLE_MATRIX.csv')


    def determine_bet_size(self, count):
        return self._bet_sizing_mapping.get(adjust_to_range(count, self._bet_sizing_mapping.keys()))
    
    def should_dealer_hit(self, dealer_hand):
        dealer_score = dealer_hand.get_dealer_score()
        if dealer_hand.contains_ace() and dealer_score == 17:
            return cfg.DEALER_HIT_SOFT_17
            
        return dealer_score < 17
    
    def should_double_down_func(self, player_hand, dealer_up_card, pre_hand_count):
        non_ace_total = player_hand.get_non_aces_hand_total()

        if player_hand.contains_ace() and non_ace_total < 10:
            decision = do_matrix_lookup_3d(self._soft_should_double_matrix, pre_hand_count, non_ace_total, dealer_up_card.numeric_value)
        else:
            decision = do_matrix_lookup_3d(self._hard_should_double_matrix, pre_hand_count, player_hand.get_optimal_score(), dealer_up_card.numeric_value)

        logger.decision(f'Double down hand decision function is {decision} for {player_hand.get_hand_string()} and dealer up card: {dealer_up_card.get_card_string()}')
        return decision
    
    def should_player_hit(self, player_hand, dealer_up_card, pre_hand_count):
        non_ace_total = player_hand.get_non_aces_hand_total()

        if player_hand.contains_ace() and non_ace_total < 10:
            decision = do_matrix_lookup_3d(self._soft_should_hit_matrix, pre_hand_count, non_ace_total, dealer_up_card.numeric_value)
        else:
            decision = do_matrix_lookup_3d(self._hard_should_hit_matrix, pre_hand_count, player_hand.get_optimal_score(), dealer_up_card.numeric_value)

        logger.card(f'Player hit decision is {decision} with {player_hand.get_hand_string()} and dealer up card {dealer_up_card.get_card_string()}')
        return decision
    
    def should_split_func(self, player_hand, dealer_up_card, pre_hand_count):
        card1, card2 = player_hand.cards
        decision = (card1.numeric_value == card2.numeric_value) and do_matrix_lookup_3d(self._should_split_matrix, pre_hand_count, card1.numeric_value, dealer_up_card.numeric_value)
        logger.decision(f'''Split hand decision is {decision} with two {card1.get_card_string()} and dealer up card {dealer_up_card.get_card_string()}''')
        return decision
        
    def should_surrender_func(self, player_hand, dealer_up_card, pre_hand_count): 
        decision = do_matrix_lookup_3d(self._should_surrender_matrix, pre_hand_count, player_hand.get_optimal_score(), dealer_up_card.numeric_value)
        logger.decision(f'Player surrender decision is {decision} with {player_hand.get_hand_string()} and dealer up card {dealer_up_card.get_card_string()}')
        return decision
    
    def should_take_insurance_func(self, dealer_up_card, pre_hand_count):
        decision = dealer_up_card.is_ace() and bool(self._should_take_insurance_matrix.get(adjust_to_range(pre_hand_count, self._should_take_insurance_matrix.keys()), 0))
        logger.decision(f'Insurance decision is {decision} taken with dealer up card: {dealer_up_card.get_card_string()} and count: {pre_hand_count}')
        return decision

""" Miscellaneous helper functions """

from bisect import bisect_left
from csv import reader

from constants import HandResult
from custom_logging import global_logger as logger
from gameplay_config import GameplayConfig as cfg


def adjust_to_range(num, val_range):
    """ Used to map a count to a decision count. Often times decisions are defined every few changes in count, e.g. -2,0,2,4... 
    We then only define decision charts for counts when they change. There would be a chart for counts -2, 0, 2, 4, but no chart for -1, 1, 3.
    We would then map each value to the closest defined count towards 0. So 1 maps to 0, 3 to 2, -3 to -2, -1 to 0 etc. 
    """
    sorted_range = sorted(val_range)
    idx = 0 
    pos = bisect_left(sorted_range, num)

    if pos == len(sorted_range): # num > max(range)
        idx = len(sorted_range) - 1
    elif sorted_range[pos] == num: # num is in range
        idx = pos
    elif num >= 0: # num is positive and between two counts. Choose one closer to 0 if possible 
        idx = pos - 1 if pos != 0 else 0
    else: # num is negative and between two counts. One to the right closer to 0 
        idx = pos

    return sorted_range[idx]
    
def get_payout_from_bet(result, bet_value):
        if result == HandResult.WIN:
            return bet_value * 2
        elif result == HandResult.BLACKJACK_WIN:
            return bet_value + (bet_value * cfg.BLACKJACK_PAYOUT)
        elif result == HandResult.PUSH:
            return bet_value
        elif result == HandResult.SURRENDER:
             return bet_value * 0.5 
        else:
             return 0
      
def get_win_amount(result, hand, does_dealer_have_blackjack):
        win_amount = get_payout_from_bet(result, hand.bet_value)
        if does_dealer_have_blackjack and hand.has_insurance:
            win_amount += hand._bet_value

        return win_amount
        
def do_matrix_lookup_3d(matrix, count, row, col):
    top_layer = matrix.get(adjust_to_range(count, matrix.keys()), {})
    return top_layer.get(adjust_to_range(row, top_layer.keys()), {}).get(col, False)
        
def load_1d_decision_matrix(path): 
    matrix = {}
    with open(path, mode='r') as file:
        csv_reader = reader(file)
        next(csv_reader)
        for card, count_val in csv_reader:
            matrix[int(card)] = int(count_val) 
        
    return matrix

def load_3d_decision_matrix(path):
    matrix = {}
    with open(path, mode='r') as file:
        csv_reader = reader(file)
        count, d = 0, {}
        columns = []
        
        for row in csv_reader:
            if row[0] == 'count':
                matrix[count] = d
                count = int(row[1])
            elif row[0] == '_':
                columns = row
            else:
                player_card = int(row[0])
                d[player_card] = {}
                for i in range(1, len(row)):
                    if row[i] == '1':
                        d[player_card][int(columns[i])] = True

        matrix[count] = d
    
    return matrix

def print_game_configuration():
    logger.summary(f'Starting simulation using strateg: {cfg.STRATEGY_NAME}')
    logger.summary(f'Game has {cfg.DECKS_IN_SHOE} decks and cut card point is in range: {cfg.CUT_CARD_RANGE}')
    logger.summary(f'Will play the minimum of {cfg.SHUFFLES_TO_PLAY} shuffles and {cfg.HANDS_TO_PLAY} hands \n')

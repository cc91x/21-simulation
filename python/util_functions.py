""" Miscellaneous helper functions """

from csv import reader

from constants import HandResult
from custom_logging import global_logger as logger
from gameplay_config import GameplayConfig as cfg


def adjust_to_range(num, val_range):
    mn, mx = min(val_range), max(val_range)
    if num < mn:
        return mn
    elif num > mx:
        return mx
    else:
        return num
    
def calculate_win_amount(result, bet_value):
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


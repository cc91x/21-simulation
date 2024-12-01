""" A static class used to house game specific config properties """

from configparser import ConfigParser

from constants import LogLevel

config = ConfigParser()
raw_config_file_path = '../config/blackjackConfig.ini'
config.read(raw_config_file_path)


class GameplayConfig():
    
    def _read_num_range(num_range):
        s1, s2 = num_range.strip('[]').split(',')
        return [int(s1), int(s2)]
    
    LOG_LEVEL = LogLevel[config.get('SETUP', 'LOG_LEVEL')]
    CONSOLE_LOGGING = config.getboolean('SETUP', 'CONSOLE_LOGGING')
    STRATEGY_NAME = config.get('SETUP', 'COUNTING_STRATEGY_DIRECTORY')
    COUNT_DIRECTORY = f'../strategies/{STRATEGY_NAME}/'
    HANDS_TO_PLAY = config.getint('SETUP', 'HANDS_TO_PLAY')
    SHUFFLES_TO_PLAY =  config.getint('SETUP', 'SHUFFLES_TO_PLAY')

    CUT_CARD_RANGE = _read_num_range(config.get('RULES', 'CUT_CARD_RANGE'))
    DECKS_IN_SHOE = config.getint('RULES', 'DECKS_IN_SHOE')
    BLACKJACK_PAYOUT = config.getfloat('RULES', 'BLACKJACK_PAYOUT')
    DEALER_HIT_SOFT_17 = config.getboolean('RULES', 'DEALER_HIT_SOFT_17')  
    SPLIT_MAX_TIMES = config.getint('RULES', 'SPLIT_MAX_TIMES') 
    DOUBLE_AFTER_SPLIT = config.getboolean('RULES', 'DOUBLE_AFTER_SPLIT')  
    SURRENDER_ALLOWED = config.getboolean('RULES', 'SURRENDER_ALLOWED')

    CONVERT_TO_TRUE_COUNT = config.getboolean('COUNTING_STRATEGY', 'CONVERT_TO_TRUE_COUNT')
    STARTING_COUNT = config.getint('COUNTING_STRATEGY', 'STARTING_COUNT')

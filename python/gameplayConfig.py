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
    
    COUNT_DIRECTORY = '../strategies/' + config.get('SETUP', 'COUNTING_STRATEGY_DIRECTORY') + '/'
    LOG_LEVEL = LogLevel[config.get('SETUP', 'LOG_LEVEL')]
    CONSOLE_LOGGING = config.getboolean('SETUP', 'CONSOLE_LOGGING')
        
    HANDS_TO_PLAY = config.getint('SIMULATION', 'HANDS_TO_PLAY')
    SHUFFLES_TO_PLAY =  config.getint('SIMULATION', 'SHUFFLES_TO_PLAY')
    
    BALANCED_COUNT = config.getboolean('COUNTING_STRATEGY', 'BALANCED_COUNT')
    STARTING_COUNT = config.getint('COUNTING_STRATEGY', 'STARTING_COUNT')

    CUT_CARD_RANGE = _read_num_range(config.get('RULES', 'CUT_CARD_RANGE'))
    DECKS_IN_SHOE = config.getint('RULES', 'DECKS_IN_SHOE')
    BLACKJACK_PAYOUT = config.getfloat('RULES', 'BLACKJACK_PAYOUT')
    DEALER_HIT_SOFT_17 = config.getboolean('RULES', 'DEALER_HIT_SOFT_17')  
    SPLIT_MAX_TIMES = config.getint('RULES', 'SPLIT_MAX_TIMES') 
    DOUBLE_AFTER_SPLIT = config.getboolean('RULES', 'DOUBLE_AFTER_SPLIT')  

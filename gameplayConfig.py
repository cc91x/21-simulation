""" A static class used to house game specific config properties """

from configparser import ConfigParser

from constants import LogLevel, BASE_DIRECTORY

config = ConfigParser()
raw_config_file_path = BASE_DIRECTORY + '/config/blackjackConfig.ini'
config.read(raw_config_file_path)


class GameplayConfig():
    
    def _read_num_range(num_range):
        s1, s2 = num_range.strip('[]').split(',')
        return [int(s1), int(s2)]

    LOG_LEVEL = LogLevel[config.get('GAMEPLAY', 'LOG_LEVEL')]
    CONSOLE_LOGGING = config.getboolean('GAMEPLAY', 'CONSOLE_LOGGING')
    
    BALANCED_COUNT = config.getboolean('GAMEPLAY', 'BALANCED_COUNT')
    STARTING_COUNT = config.getint('GAMEPLAY', 'STARTING_COUNT')
    
    HANDS_TO_PLAY = config.getint('GAMEPLAY', 'HANDS_TO_PLAY')
    SHUFFLES_TO_PLAY =  config.getint('GAMEPLAY', 'SHUFFLES_TO_PLAY')
    
    CUT_CARD_RANGE = _read_num_range(config.get('GAMEPLAY', 'CUT_CARD_RANGE'))
    DECKS_IN_SHOE = config.getint('GAMEPLAY', 'DECKS_IN_SHOE')
    BLACKJACK_PAYOUT = config.getfloat('GAMEPLAY', 'BLACKJACK_PAYOUT')
    DEALER_HIT_SOFT_17 = config.getboolean('GAMEPLAY', 'DEALER_HIT_SOFT_17')  
    SPLIT_MAX_TIMES = config.getint('GAMEPLAY', 'SPLIT_MAX_TIMES') 
    DOUBLE_AFTER_SPLIT = config.getboolean('GAMEPLAY', 'DOUBLE_AFTER_SPLIT')  

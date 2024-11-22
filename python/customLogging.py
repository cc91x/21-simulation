""" A class for project specific logging """

from logging import addLevelName, StreamHandler, Logger, getLogger, Formatter 
from logging.handlers import RotatingFileHandler

from constants import LogLevel
from gameplayConfig import GameplayConfig as cfg


def card_logging_level(self, message, *args, **kwargs):
    if self.isEnabledFor(LogLevel.CARD.value):
        self._log(LogLevel.CARD.value, message, args, **kwargs)

def decision_logging_level(self, message, *args, **kwargs):
    if self.isEnabledFor(LogLevel.DECISION.value):
        self._log(LogLevel.DECISION.value, message, args, **kwargs)

def summary_logging_level(self, message, *args, **kwargs):
    if self.isEnabledFor(LogLevel.SUMMARY.value):
        self._log(LogLevel.SUMMARY.value, message, args, **kwargs)

def setupLogging(log_level, include_console_logging): 
    addLevelName(LogLevel.CARD.value, 'CARD')
    addLevelName(LogLevel.DECISION.value, 'DECISION')
    addLevelName(LogLevel.SUMMARY.value, 'SUMMARY')
    Logger.card = card_logging_level
    Logger.decision = decision_logging_level
    Logger.summary = summary_logging_level

    logger = getLogger(__name__)
    logger.setLevel(log_level)
    formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

    log_file_path = '../logs/blackjack.log'    
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=1)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)    

    if include_console_logging:
        console_handler = StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

global_logger = setupLogging(cfg.LOG_LEVEL.value, cfg.CONSOLE_LOGGING)

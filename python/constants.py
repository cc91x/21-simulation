""" Custom enums and constant variables """

from enum import Enum


class CardRank(Enum):
    
    def __init__(self, rank, value):
        self._rank = rank
        self._value = value
    
    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        return self._value 
    
    ACE = ('A', 11)
    TWO = ('2', 2)
    THREE = ('3', 3)
    FOUR = ('4', 4)
    FIVE = ('5', 5)
    SIX = ('6', 6)
    SEVEN = ('7', 7)
    EIGHT = ('8', 8)
    NINE = ('9', 9)
    TEN = ('10', 10)
    JACK = ('J', 10)
    QUEEN = ('Q', 10)
    KING = ('K', 10)


class HandResult(Enum):
    WIN = 1
    BLACKJACK_WIN = 2
    PUSH = 3
    LOSE = 4
    SURRENDER = 5


class LogLevel(Enum):
    DECISION = 21
    CARD = 22
    SUMMARY = 23


class Suit(Enum):
    CLUB =  '\u2663' 
    DIAMOND = '\u2666' 
    HEART = '\u2665'
    SPADE = '\u2660'

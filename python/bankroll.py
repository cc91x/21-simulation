""" A class for the player's bankroll """

class Bankroll():
    
    def __init__(self, starting_balance):
        self._balance = starting_balance 

    @property
    def balance(self):
        return self._balance
    
    def add(self, value):
        self._balance += value
    
    def subtract(self, value):
        self._balance -= value 

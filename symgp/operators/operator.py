from typing import Callable
from .oprules import OpRules as _OPRS    

class Operator:
    """
    A class to represent an operator in the symbolic regression model.\n
    Basically a wrapper around a function with some metadata to handle compatibility checks and other stuff.
    """
    function:Callable
    name:str
    rules:_OPRS

    def __init__(self, name:str, function:Callable, rules:_OPRS):
        self.name = name
        self.function = function
        self.rules = rules
    def __call__(self, *args):
        return self.function(*args)
    def __eq__(self, other):
        return self.name == other.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __hash__(self):
        return hash(self.name)
    def __ne__(self, other):
        return not self.__eq__(other)

__all__ = ["Operator"]
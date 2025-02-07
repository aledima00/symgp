from ..individual import IndividualTree
from typing import Callable as _CLB

class RecOp:
    def __init__(self, name:str, func:_CLB[[IndividualTree,IndividualTree],IndividualTree]):
        self.name = name
        self.f = func
    def __call__(self, *args):
        return self.f(*args)
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    
class MutOp:
    def __init__(self, name:str, func:_CLB[[IndividualTree],IndividualTree]):
        self.name = name
        self.f = func
    def __call__(self, *args):
        return self.f(*args)
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    
__all__ = ["RecOp","MutOp"]
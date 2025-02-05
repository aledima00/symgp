from typing import Callable as _Callable
from .oprules import OpRules as _OPRS   
from ..format import Formatted
from colorama import Fore, Back, Style 
import inspect
import re

class Operator:
    """
    A class to represent an operator in the symbolic regression model.\n
    Basically a wrapper around a function with some metadata to handle compatibility checks and other stuff.
    """
    function:_Callable
    name:str
    rules:_OPRS

    def __init__(self, name:str, function:_Callable, rules:_OPRS):
        self.name = name
        self.function = function
        self.rules = rules
    def __call__(self, *args):
        return self.function(*args)
    def __eq__(self, other):
        return self.name == other.name
    def fstr(self)->Formatted:
        fstr = Formatted()
        fstr.fore(Fore.YELLOW).append(self.name)
        return fstr
    def getInfo(self)->str:
        fstr = Formatted()
        fstr.style(Style.DIM).fore(Fore.YELLOW).append(f"Operator('{self.name}'){{").ret().indent()
        fstr.fore(Fore.GREEN).append(f"Function:\t").fore(Fore.CYAN).append(f"`{self.function.__name__}`, defined in: {inspect.getsourcefile(self.function)}, @ line {inspect.getsourcelines(self.function)[1]}").ret()
        fstr.fore(Fore.GREEN).append(f"Rules:\t\t")
        fstr.concatenate(self.rules.fstr()).ret()
        fstr.unindent().fore(Fore.YELLOW).append("}")
        return str(fstr)
    def __repr__(self):
        return re.sub(r"\s+","", self.getInfo())
    def __hash__(self):
        return hash(self.name)
    def __ne__(self, other):
        return not self.__eq__(other)

__all__ = ["Operator"]
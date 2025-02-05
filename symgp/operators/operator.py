from typing import Callable as _Callable
from .oprules import OpRules as _OPRS   
from consoleformat import Formatted
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
    def fstr(self,fstr:Formatted=Formatted())->Formatted:
        fstr.append(self.name,fore=Fore.YELLOW)
        return fstr
    def getInfo(self,fstr:Formatted=Formatted())->str:
        src_str = inspect.getsourcefile(self.function)
        src_words = src_str.split("\\")
        if len(src_words)>3:
            src_str = "...."
            for i in range(len(src_words)-3,len(src_words)):
                src_str += "\\"+src_words[i]
        fstr.style(Style.NORMAL).fore(Fore.YELLOW).append(f"Operator('{self.name}'):")
        fstr.ret().indent().fore(Fore.GREEN)
        fstr.append(f"Function: ").fore(Fore.CYAN).append(f"`{self.function.__name__}`, defined in: {src_str}, @ line {inspect.getsourcelines(self.function)[1]}").ret().dropFore()
        fstr.append(f"Rules:").ret().indent()
        self.rules.fstr(fstr)
        fstr.ret().unindent().dropFore().dropFore()
        return str(fstr)
    def __repr__(self):
        return re.sub(r"\s+","", self.getInfo())
    def __hash__(self):
        return hash(self.name)
    def __ne__(self, other):
        return not self.__eq__(other)

__all__ = ["Operator"]
from typing import Callable as _Callable
from consoleformat import Formatted
from colorama import Fore 
import inspect

class Operator:
    """
    A class to represent an operator in the symbolic regression model.\n
    Basically a wrapper around a function with some metadata to handle compatibility checks and other stuff.
    """
    function:_Callable
    name:str
    arity:int

    def __init__(self, name:str, arity:int, func:_Callable):
        self.name = name
        self.function = func
        self.arity = arity
    def __call__(self, *args):
        assert len(args) == self.arity, f"Operator '{self.name}' expects {self.arity} arguments, got {len(args)}"
        return self.function(*args)
    def fstr(self,fstr:Formatted=Formatted())->Formatted:
        fstr.append(self.name,fore=Fore.YELLOW)
        return fstr
    def getInfo(self)->str:
        fstr = Formatted()
        src_str = inspect.getsourcefile(self.function)
        src_words = src_str.split("\\")
        if len(src_words)>3:
            src_str = "...."
            for i in range(len(src_words)-3,len(src_words)):
                src_str += "\\"+src_words[i]
        fstr.fore(Fore.YELLOW).append(f"Operator('{self.name}'):")
        fstr.ret().indent().fore(Fore.GREEN)
        fstr.append(f"Function: ").append(f"`{self.function.__name__}`, defined in: {src_str}, @ line {inspect.getsourcelines(self.function)[1]}",fore=Fore.CYAN).ret()
        fstr.append(f"Arity: ").append(f"{self.arity}",fore=Fore.CYAN)
        fstr.dropFore().dropFore()
        return str(fstr)

__all__ = ["Operator"]
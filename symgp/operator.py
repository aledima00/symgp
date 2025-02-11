from typing import Callable as _Callable
from consoleformat import Formatted
from colorama import Fore 
import inspect
import numpy as np
from typing import Tuple as _TUP, List as _LST

class Operator:
    function:_Callable
    name:str
    arity:int

    def __init__(self, name:str, arity:int, func:_Callable,expr:str=None,*,simplify_func:_Callable[[_LST],_TUP['Operator',_LST]]|None=None):
        self.name = name
        self.function = func
        self.arity = arity
        if expr is not None:
            self.expr = expr
        else:
            self.expr = f"np.{name}("
            for i in range(self.arity):
                self.expr += f"#{i+1}" + ("" if i==self.arity-1 else ",")
            self.expr += ")"

        self.simplifiable = simplify_func is not None
        self.simplify_func = simplify_func

    # define the simplified function that acts on tuples like (operator,[args])
    def simplified(self,in_lst:_LST)->_TUP['Operator',_LST]:
        return self.simplify_func(*in_lst) if self.simplifiable else None

    def __call__(self, *args):
        if len(args) != self.arity:
            raise ValueError(f"Operator '{self.name}' expects {self.arity} arguments, got {len(args)}")
        with np.errstate(invalid='ignore', divide='ignore', over='ignore'):
            return self.function(*args)
        
    def solved_expr(self,args:list)->str:
        assert len(args) == self.arity, f"Operator '{self.name}' expects {self.arity} arguments, got {len(args)}"
        ret = self.expr
        for i in range(self.arity):
            ret = ret.replace(f"#{i+1}",args[i])
        return ret

    def fstr(self,fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
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
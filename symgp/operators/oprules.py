from typing import List as _List
from colorama import Fore
from consoleformat import Formatted
from .datatypes import DataType as _DTYP

class OpRules:
    """
    A class to represent the constraints and the rules for an operator in the symbolic regression model.
    """

    arity:int
    input_types: _List[_DTYP] # fixed specifications for inputs
    output_type: _DTYP # fixed specifications for output
    

    def __init__(self, arity:int, input_types:_List[_DTYP]=None, output_type:_DTYP=None):
        self.arity = arity
        self.input_types = input_types if input_types is not None else [_DTYP() for _ in range(arity)]
        self.output_type = output_type if output_type is not None else _DTYP()
    
    def fstr(self,fstr:Formatted=Formatted())->Formatted:

        fstr.append(f"ARITY: ").fore(Fore.CYAN).append(f"{self.arity}").ret()
        fstr.dropFore().append("INPUT_TYPES:")
        
        ## start of input specs
        fstr.fore(Fore.CYAN).append("[").ret().indent()
        
        
        for i in range(self.arity):
            self.input_types[i].fstr(fstr)
            if i != self.arity-1:
                fstr.append(",")
            fstr.ret()
        fstr.unindent().append("]").dropFore().ret()
        ## end of input specks
        
        fstr.append(f"OUTPUT_TYPE:\t\t")
        self.output_type.fstr(fstr).ret()
        fstr.unindent().ret()
        return fstr
    def __str__(self):
        return str(self.fstr())
    def __repr__(self):
        return str(self)

__all__ = ["OpRules"]
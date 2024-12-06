from typing import List
from .specifications import TypeSpec, types, dtypes
from typing import Callable, List, Tuple

class OpRules:
    """
    A class to represent the constraints and the rules for an operator in the symbolic regression model.
    """
    arity:int
    output_frule:Callable[[List[TypeSpec], List[Tuple]], TypeSpec] # output type rule function
    input_types:List[TypeSpec] # fixed input type specs
    output_type:TypeSpec # fixed output type spec
    input_fcheck:Callable[[List[TypeSpec], List[Tuple]], bool] # input type check function

    def __init__(self, arity:int, output_frule:Callable[[List[TypeSpec], List[Tuple]], TypeSpec], input_types:List[TypeSpec]=None, output_types:TypeSpec=None, input_fcheck:Callable[[List[TypeSpec], List[Tuple]], bool]=None):
        self.arity = arity
        self.output_frule = output_frule
        self.input_types = input_types if input_types is not None else [TypeSpec() for _ in range(arity)]
        self.output_types = output_types if output_types is not None else TypeSpec()
        self.input_fcheck = input_fcheck if input_fcheck is not None else lambda *x: True
        

class Operator:
    """
    A class to represent an operator in the symbolic regression model.\n
    Basically a wrapper around a function with some metadata to handle compatibility checks and other stuff.
    """
    function:callable
    name:str
    rules:OpRules

    def __init__(self, name:str, function:callable, rules:OpRules):
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

__all__ = ["OpRules", "Operator"]
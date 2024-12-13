from typing import Callable, List
from .specifications import Specs
from enum import Enum

class OpRules:
    """
    A class to represent the constraints and the rules for an operator in the symbolic regression model.
    """
    

    arity:int
    inputs_specs: List[Specs]
    output_specs: Specs
    input_con
    output_rules:List # output type rule function
    input_types:List[TypeSpec] # fixed input type specs
    output_type:TypeSpec # fixed output type spec
    input_fcheck:List[Callable[[List[TypeSpec]], bool]] # input type check function

    def __init__(self, arity:int, output_frule:Callable[[List[TypeSpec]], TypeSpec], input_types:List[TypeSpec]=None, output_type:TypeSpec=None, input_fcheck:Callable[[List[TypeSpec]], bool]=None):
        self.arity = arity
        self.output_frule = output_frule
        self.input_types = input_types if input_types is not None else [TypeSpec() for _ in range(arity)]
        self.output_type = output_type if output_type is not None else TypeSpec()
        self.input_fcheck = input_fcheck if input_fcheck is not None else lambda *x: True

__all__ = ["OpRules"]
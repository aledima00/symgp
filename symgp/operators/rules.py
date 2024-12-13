from .specifications import Specs as _SP
from typing import List
from enum import Enum

class OUTPUT_FRULES(Enum):
    """
    Enum to represent the possible output type rules for an operator.
    Basically a function that obtain th output spces from the input specs.
    """
    INHERIT_SHAPE = 1
    TRANSPOSE_SHAPE = 2
    MATMUL_SHAPE = 3

    def eval(self, spec_list:List[_SP]):
        if self == OUTPUT_FRULES.INHERIT_SHAPE:
            return spec_list[0]
        elif self == OUTPUT_FRULES.TRANSPOSE_SHAPE:
            ret = spec_list[0].copy()
            ret.shape = ret.shape[::-1]
            return ret
        elif self == OUTPUT_FRULES.MATMUL_SHAPE:
            s1 = spec_list[0].shape
            s2 = spec_list[1].shape
            ret = spec_list[0].copy()
            ret.shape = (s1[0], s2[1])
            return ret
        else:
            raise ValueError("Invalid output rule")
        

class INPUT_BINARY_FCHECKS(Enum):
    """
    Enum to represent the possible input type checks for first 2 inputs of an operator.
    Basically bool checks on input specs.
    It is used for binary operators, but if there are also some scalar inputs, they should be at the end of the list.
    """
    SAME_TYPE = 1
    SAME_DTYPE = 2
    SAME_SHAPE = 3
    TRANSPOSED_SHAPE = 4

    def eval(self, spec_list:List[_SP]):
        if self == INPUT_BINARY_FCHECKS.SAME_TYPE:
            return spec_list[0].type == spec_list[1].type
        elif self == INPUT_BINARY_FCHECKS.SAME_DTYPE:
            return spec_list[0].dtype == spec_list[1].dtype
        elif self == INPUT_BINARY_FCHECKS.SAME_SHAPE:
            return spec_list[0].shape == spec_list[1].shape
        elif self == INPUT_BINARY_FCHECKS.TRANSPOSED_SHAPE:
            return spec_list[0].shape == spec_list[1].shape[::-1]
        else:
            raise ValueError("Invalid input binary fcheck")

__all__ = ["OUTPUT_FRULES", "INPUT_BINARY_FCHECKS"]
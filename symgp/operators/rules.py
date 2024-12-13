from .specifications import Specs as _SP
from typing import List as _List
from enum import Enum as _Enum
from .specifications import ShapeTypes as _ST, DataTypes as _DT

class OUTPUT_COMPUTE_RULES(_Enum):
    """
    Enum to represent the possible output type rules for an operator.
    Basically a function that obtain th output spces from the input specs.
    """
    INHERIT_SHAPE_TYPE = 1 # output has same type as input [NPARRAY or SCALAR]
    INHERIT_DATA_TYPE = 2 # output has same dtype as input [INT, FLOAT, BOOL, STR]
    INHERIT_SHAPE = 3 # output has same shape as input
    TRANSPOSE_SHAPE = 4 # output has the shape of the input transposed
    MATMUL_SHAPE = 5 # output has the shape of the matrix multiplication of the inputs
        

class INPUT_BINARY_CHECKS(_Enum):
    """
    Enum to represent the possible input type checks for first 2 inputs of an operator.
    Basically bool checks on input specs.
    It is used for binary operators, but if there are also some scalar inputs, they should be at the end of the list.
    """
    SAME_SHAPE_TYPE = 1
    SAME_DATA_TYPE = 2
    SAME_SHAPE = 3
    TRANSPOSED_SHAPE = 4

__all__ = ["OUTPUT_COMPUTE_RULES", "INPUT_BINARY_CHECKS"]
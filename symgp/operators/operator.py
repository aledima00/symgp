import numpy as _np
from typing import Callable, List, Tuple

class Types:
    SCALAR = "scalar"
    NPARRAY = "nparray"

    @classmethod
    def all(cls):
        return [cls.SCALAR, cls.NPARRAY]

class DTypes:
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STR = "str"

    @classmethod
    def all(cls):
        return [cls.INT, cls.FLOAT, cls.BOOL, cls.STR]

types = Types.all()
dtypes = DTypes.all()

class Spec:
    """
    A class to represent the type of an operator's input or output.
    """
    type:str
    dtype:str
    shape:Tuple[int]
    def __init__(self, type_spec: str, dtype_spec:str,shape_spec:Tuple[int]=None):
        assert type_spec in types, f"Invalid type {type_spec}. Must be one of {types}"
        assert dtype_spec in dtypes, f"Invalid dtype {dtype_spec}. Must be one of {dtypes}"
        if type_spec == Types.NPARRAY:
            assert shape_spec is not None, "Shape must be provided for nparray type"
        else:
            assert shape_spec is None, "Shape must not be provided for scalar type"
        self.type = type_spec
        self.dtype = dtype_spec
        self.shape = shape_spec

    def __repr__(self):
        return f"Spec(type:{self.type}, dtype:{self.dtype}, shape:{self.shape})"

class Operator:
    """
    A class to represent an operator in the symbolic regression model.\n
    Basically a wrapper around a function with some metadata.
    """
    function:callable
    arity:int
    name:str
    output_spec:Spec
    input_specs:List[Spec]

    def __init__(self, name:str, function:callable, arity:int, output_type:Spec, input_types:List[Spec]):
        self.name = name
        self.function = function
        self.arity = arity
        self.output_type = output_type
        self.input_types = input_types
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

__all__ = ["Operator", "Spec", "types", "dtypes", "Types", "DTypes"]
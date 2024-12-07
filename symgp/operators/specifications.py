from typing import Tuple

class Types:
    SCALAR = "scalar"
    NPARRAY = "nparray"
    UNSPECIFIED_TYPE = "unspecified_type"

    @classmethod
    def all(cls):
        return [cls.SCALAR, cls.NPARRAY]

class DTypes:
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STR = "str"
    UNSPECIFIED_DTYPE = "unspecified_dtype"

    @classmethod
    def all(cls):
        return [cls.INT, cls.FLOAT, cls.BOOL, cls.STR]

types = Types.all()
dtypes = DTypes.all()

class TypeSpec:
    # add shape specification, that should be None if no fixed shape is required
    """
    A class to represent the type of an operator's input or output in case is fixed (otherwise `None` can be used).
    It can tell:
    - if the type is scalar or nparray
    - if the dtype is int, float, bool, or str
    """
    type:str
    dtype:str
    shape:Tuple
    def __init__(self, type_spec: str, dtype_spec:str, shape:Tuple=None):
        assert type_spec in types, f"Invalid type '{type_spec}'. Must be one of {types}"
        assert dtype_spec in dtypes, f"Invalid dtype '{dtype_spec}'. Must be one of {dtypes}"
        self.type = type_spec
        self.dtype = dtype_spec
        self.shape = None
    def __repr__(self):
        return f"TypeSpec(type:{self.type}, dtype:{self.dtype}, shape:{self.shape or 'UNSPECIFIED'})"
    def copy(self):
        return TypeSpec(self.type, self.dtype, self.shape)
        
__all__ = ["TypeSpec", "types", "dtypes", "Types", "DTypes"]
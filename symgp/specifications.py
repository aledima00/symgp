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

class TypeSpec:
    """
    A class to represent the type of an operator's input or output in case is fixed (otherwise `None` can be used).
    It can tell:
    - if the type is scalar or nparray
    - if the dtype is int, float, bool, or str
    """
    type:str
    dtype:str
    def __init__(self, type_spec: str=None, dtype_spec:str=None):
        assert type_spec in types or type_spec is None, f"Invalid type {type_spec}. Must be one of {types}"
        assert dtype_spec in dtypes or dtype_spec is None, f"Invalid dtype {dtype_spec}. Must be one of {dtypes}"
        self.type = type_spec
        self.dtype = dtype_spec
    def __repr__(self):
        return f"TypeSpec(type:{self.type}, dtype:{self.dtype})"
        
__all__ = ["TypeSpec", "types", "dtypes", "Types", "DTypes"]
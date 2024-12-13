from typing import Tuple as _Tuple
from enum import Enum as _Enum

class ShapeTypes(_Enum):
    SCALAR = "scalar"
    NPARRAY = "nparray"
    UNSPECIFIED_TYPE = "unspecified_type"

class DataTypes(_Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STR = "str"
    UNSPECIFIED_DTYPE = "unspecified_dtype"


class Specs:
    # add shape specification, that should be None if no fixed shape is required
    """
    A class to represent the type of an operator's input or output in case is fixed (otherwise `None` can be used).
    It can tell:
    - if the type is scalar or nparray
    - if the dtype is int, float, bool, or str
    """
    def __init__(self, shape_type:ShapeTypes, data_type:DataTypes, shape:_Tuple):
        assert shape_type in ShapeTypes, f"Invalid shape type: {shape_type}"
        assert data_type in DataTypes, f"Invalid data type: {data_type}"
        assert shape_type != ShapeTypes.NPARRAY or shape is not None, "NPArray type requires a shape (Tuple)"

        self.shape_type = shape_type
        self.data_type = data_type
        self.shape = shape
    def __repr__(self):
        return f"Specifications(shape_type:{self.shape_type}, dtype:{self.data_type}, shape:{self.shape or 'UNSPECIFIED'})"
    def copy(self):
        return Specs(self.shape_type, self.data_type, self.shape)
        
__all__ = ["Specs", "ShapeTypes", "DataTypes"]
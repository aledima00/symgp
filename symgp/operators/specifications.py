from typing import Tuple as _Tuple
from enum import Enum as _Enum
from colorama import Fore, Back, Style
from ..format import Formatted

class ShapeTypes(_Enum):
    SCALAR = "scalar"
    NPARRAY = "nparray"
    UNSPECIFIED_SHAPE_TYPE = "unspecified_type"

class DataTypes(_Enum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STR = "str"
    UNSPECIFIED_DATA_TYPE = "unspecified_dtype"


class Specs:
    # add shape specification, that should be None if no fixed shape is required
    """
    A class to represent the type of an operator's input or output in case is fixed (otherwise `None` can be used).
    It can tell:
    - if the type is scalar or nparray
    - if the dtype is int, float, bool, or str
    """
    def __init__(self, shape_type:ShapeTypes=ShapeTypes.UNSPECIFIED_SHAPE_TYPE, data_type:DataTypes=DataTypes.UNSPECIFIED_DATA_TYPE, shape:_Tuple=None):
        
        assert shape_type in ShapeTypes, f"Invalid shape type: {shape_type}"
        assert data_type in DataTypes, f"Invalid data type: {data_type}"
        assert shape_type != ShapeTypes.NPARRAY or shape is not None, "NPArray type requires a shape (Tuple)"

        self.shape_type = shape_type
        self.data_type = data_type
        self.shape = shape

    def fstr(self)->Formatted:
        fstr = Formatted()
        fstr.style(Style.DIM).fore(Fore.WHITE).append("Specs(").ret().indent()
        fstr.fore(Fore.GREEN).append(f"ShapeType:").fore(Fore.CYAN).append(f"\t'{self.shape_type.name}'").ret()
        fstr.fore(Fore.GREEN).append(f"DataType:").fore(Fore.CYAN).append(f"\t'{self.data_type.name}'").ret()
        fstr.fore(Fore.GREEN).append(f"Shape:").fore(Fore.CYAN).append(f"\t\t'{self.shape or "UNSPECIFIED_SHAPE"}'").ret().unindent().fore(Fore.WHITE).append(")")
        return fstr
    def __str__(self):
        return str(self.fstr())
    def __repr__(self):
        return str(self)
    def copy(self):
        return Specs(self.shape_type, self.data_type, self.shape)
        
__all__ = ["Specs", "ShapeTypes", "DataTypes"]
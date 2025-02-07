import numpy as np
from colorama import Fore
from consoleformat import Formatted as _FMT
from dataclasses import dataclass
from typing import ClassVar


_dtnames_map ={
    "NUM":np.number,
    "COMPLEX":np.complexfloating,
    "FLOAT":np.floating,
    "INT":np.integer,
    "SINT":np.signedinteger,
    "UINT":np.unsignedinteger,
    "BOOL":np.bool,
    "CHAR":np.character,
    "STR":np.str_,
    "ANY":np.object_
}

class DataType:
    def __init__(self, data_type_str:str="ANY"):
        assert data_type_str in _dtnames_map, f"Invalid data type: {data_type_str}"
        self.__dtname = data_type_str
        self.__dt = _dtnames_map[data_type_str]
    def accepts(self, otherDT:"DataType")->bool:
        return np.issubdtype(otherDT.__dt, self.__dt)
    def subtypes(self)->list:
        return [dt for dt in _dtnames_map if np.issubdtype(dt, self.__dt)]
    def fstr(self, fstr:_FMT=_FMT())->_FMT:
        fstr.fore(Fore.CYAN).append(self.__dtname).dropFore()
        return fstr
    def numpy_type(self):
        return self.__dt
    def __str__(self):
        return self.__dtname
    def __repr__(self):
        return self.__dtname
    
@dataclass(frozen=True)
class DataTypes:
    NUM: ClassVar[DataType] = DataType("NUM")
    COMPLEX: ClassVar[DataType] = DataType("COMPLEX")
    FLOAT: ClassVar[DataType] = DataType("FLOAT")
    INT: ClassVar[DataType] = DataType("INT")
    SINT: ClassVar[DataType] = DataType("SINT")
    UINT: ClassVar[DataType] = DataType("UINT")
    BOOL: ClassVar[DataType] = DataType("BOOL")
    CHAR: ClassVar[DataType] = DataType("CHAR")
    STR: ClassVar[DataType] = DataType("STR")
    ANY: ClassVar[DataType] = DataType("ANY")
    
__all__ = ["DataType","DataTypes"]
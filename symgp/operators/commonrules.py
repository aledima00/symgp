from .oprules import OpRules
from .specifications import TypeSpec as TS
from typing import List

class ARITIES:
    UNARY = 1
    BINARY = 2
    TERNARY = 3

class OUTPUT_FRULES:
    def INHERIT_SHAPE(ITS_list:List[TS]):
        return ITS_list[0]
    def TRANSPOSE_SHAPE(ITS_list:List[TS]):
        ret = ITS_list[0].copy()
        ret.shape = ret.shape[::-1]
    def MATMUL_SHAPE(ITS_list:List[TS]):
        s1 = ITS_list[0].shape
        s2 = ITS_list[1].shape
        ret = ITS_list[0].copy()
        ret.shape = (s1[0], s2[1])

class INPUT_FCHECKS:
    def SAME_SHAPE(ITS_list:List[TS]):
        return ITS_list[0].shape == ITS_list[1].shape
    def TRANSPOSED_SHAPE(ITS_list:List[TS]):
        return ITS_list[0].shape == ITS_list[1].shape[::-1]
    def SAME_SHAPE_SAME_DTYPE(ITS_list:List[TS]):
        return ITS_list[0].shape == ITS_list[1].shape and ITS_list[0].dtype == ITS_list[1].dtype
    def TRANSPOSED_SHAPE_SAME_DTYPE(ITS_list:List[TS]):
        return ITS_list[0].shape == ITS_list[1].shape[::-1] and ITS_list[0].dtype == ITS_list[1].dtype
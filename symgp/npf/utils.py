from . import functions as _fs
from .. import Operator as _op


def get_all():
    return [getattr(_fs, func) for func in dir(_fs) if isinstance(getattr(_fs, func), _op)]

def get_unary():
    all_funcs = get_all()
    return [func for func in all_funcs if func.arity == 1]

def get_nary():
    all_funcs = get_all()
    return [func for func in all_funcs if func.arity > 1]

def get_binary():
    all_funcs = get_all()
    return [func for func in all_funcs if func.arity == 2]

def get_by_arity(n):
    all_funcs = get_all()
    return [func for func in all_funcs if func.arity == n]

def is_unary(op:_op):
    return op.arity == 1
def is_nary(op:_op):
    return op.arity > 1
def is_binary(op:_op):
    return op.arity == 2
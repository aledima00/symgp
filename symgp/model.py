from .operator import Operator as _op
from .individual import Leaf

class Model:
    max_depth:int
    operators:list[_op]
    inputLeaves:list[Leaf]
    def __init__(self,max_depth:int,operators:list[_op],inputLeaves:list[Leaf]):
        self.max_depth = max_depth
        self.operators = operators
        self.inputs = inputLeaves

__all__ = ["Model"]
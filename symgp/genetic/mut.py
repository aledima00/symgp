from ..individual import IndividualTree,Node,Leaf
import numpy as np
from .. import npf
from typing import List as _LST

class PointMut:
    def __init__(self,*,rng:np.random.Generator,Fset:_LST[Node]):
        self.name="Point Mutation Operator"
        self.rng = rng
        self.Fset = Fset
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        nodes = ret.subnodes(keep_leaves=False,keep_root=True)
        if len(nodes) != 0:
            p = self.rng.choice(nodes)
            ops = [op for op in self.Fset if op.arity == p.operator.arity]
            p.operator = self.rng.choice(ops)
        ret.update_input_leaves()
        return ret

class PermMut:
    def __init__(self,*,random:bool=False,rng:np.random.Generator=None):
        assert not (random and rng is None), "rng must be provided for random=True"
        self.name="Permutation Mutation Operator"
        self.rng = rng
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        nodes = ret.subnodes(keep_leaves=False,keep_root=True)
        nary_nodes = [n for n in nodes if n.operator.arity > 1]
        if len(nary_nodes) != 0:
            p = self.rng.choice(nary_nodes)
            p.children = self.rng.permutation(p.children)
        ret.update_input_leaves()
        return ret

class HoistMut:
    def __init__(self,*,rng:np.random.Generator):
        self.name="Hoist Mutation Operator"
        self.rng = rng
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        nodes = ret.subnodes(keep_leaves=False,keep_root=False)
        if len(nodes) != 0:
            p = self.rng.choice(nodes)
            ret.root = p
        ret.update_input_leaves()
        return ret

class MixedMut:
    def __init__(self,*,rng:np.random.Generator,Fset:_LST[Node]):
        self.name="Mixed Mutation Operator"
        self.rng = rng
        self.Fset = Fset
        self.mutops = [PointMut(rng=rng,Fset=Fset),PermMut(rng=rng),HoistMut(rng=rng)]
    def __call__(self,it:IndividualTree):
        return self.rng.choice(self.mutops)(it)
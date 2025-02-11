from ..individual import IndividualTree,Node,Leaf,VarLeaf
import numpy as np
from .. import npf
from typing import List as _LST, Callable as _CLB

class SubTreeMut:
    def __init__(self,*,rng:np.random.Generator,grow_func:_CLB):
        self.name="Subtree Mutation Operator"
        self.rng = rng
        self.grow_func = grow_func
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        new_tree = self.grow_func()
        nodes = ret.subnodes(keep_leaves=False,keep_root=False)
        if len(nodes) != 0:
            p = self.rng.choice(nodes)
            # replace random child of p with new_tree
            idx = self.rng.integers(0,len(p.children))
            p.children[idx] = new_tree.root
        ret.update()
        return ret

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
        ret.update()
        return ret

class PermMut:
    def __init__(self,*,random:bool=False,rng:np.random.Generator=None):
        assert not (random and rng is None), "rng must be provided for random=True"
        self.name="Permutation Mutation Operator"
        self.rng = rng
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        nodes = ret.subnodes(keep_leaves=False,keep_root=True)
        if len(nodes) != 0:
            nary_nodes = [n for n in nodes if n.operator.arity > 1]
            if len(nary_nodes) != 0:
                p = self.rng.choice(nary_nodes)
                p.children = self.rng.permutation(p.children)
            ret.update()
        return ret

class HoistMut:
    def __init__(self,*,rng:np.random.Generator):
        self.name="Hoist Mutation Operator"
        self.rng = rng
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        nodes = ret.subnodes(keep_leaves=True,keep_root=False)
        if len(nodes) != 0:
            p = self.rng.choice(nodes)
            ret.root = p
        ret.update()
        return ret
    
    
class CollapseMut:
    def __init__(self,*,rng:np.random.Generator,input_leaves_names:_LST[str],lgen_func:_CLB):
        self.name="Collapse Mutation Operator"
        self.rng = rng
        self.input_leaves_names = input_leaves_names
        self.lgen_func = lgen_func
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        lf = self.lgen_func()
        nodes = ret.subnodes(keep_leaves=False,keep_root=True)
        if len(nodes) != 0:
            p = self.rng.choice(nodes)
            # replace random child of p with lf
            idx = self.rng.integers(0,len(p.children))
            p.children[idx] = lf
        ret.update()
        return ret

class MixedMut:
    def __init__(self,*,rng:np.random.Generator,Fset:_LST[Node],input_leaves_names:_LST[str],grow_func:_CLB,lgen_func:_CLB,probabs:_LST=None):
        self.name="Mixed Mutation Operator"
        self.rng = rng
        self.Fset = Fset
        self.mutops =[
                PointMut(rng=rng,Fset=Fset),
                PermMut(rng=rng),
                HoistMut(rng=rng),
                CollapseMut(rng=rng,input_leaves_names=input_leaves_names,lgen_func=lgen_func),
                SubTreeMut(rng=rng,grow_func=grow_func)
            ]
        if probabs is None:
            self.probabs = [0.2,0.2,0.2,0.2,0.2]
        else:
            self.probabs = probabs
            # normalize probabs
            self.probabs = [p/sum(self.probabs) for p in self.probabs]
    def __call__(self,it:IndividualTree):
        return self.rng.choice(self.mutops,p=self.probabs)(it)
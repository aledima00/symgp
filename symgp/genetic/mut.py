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
        ret.update_input_leaves()
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
    
class ConstMut:
    def __init__(self,*,rng:np.random.Generator):
        self.name="Constant Mutation Operator"
        self.rng = rng
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        leaves = ret.subnodes(keep_leaves=True,keep_root=True)
        leaves = [l for l in leaves if (isinstance(l,Leaf) and not isinstance(l,VarLeaf))]
        if len(leaves) != 0:
            p = self.rng.choice(leaves)
            p.value = self.rng.random()
        ret.update_input_leaves()
        return ret
    
class CollapseMut:
    def __init__(self,*,rng:np.random.Generator,input_leaves_names:_LST[str],c_prop:float=0.3):
        self.name="Collapse Mutation Operator"
        self.rng = rng
        self.input_leaves_names = input_leaves_names
        self.c_prop = c_prop
    def __call__(self,it:IndividualTree):
        ret = it.deepCopy()
        if self.rng.random() < self.c_prop:
            lf = Leaf(self.rng.random())
        else:
            lf = VarLeaf(self.rng.choice(self.input_leaves_names))
        nodes = ret.subnodes(keep_leaves=False,keep_root=True)
        if len(nodes) != 0:
            p = self.rng.choice(nodes)
            # replace random child of p with lf
            idx = self.rng.integers(0,len(p.children))
            p.children[idx] = lf
        ret.update_input_leaves()
        return ret

class MixedMut:
    def __init__(self,*,rng:np.random.Generator,Fset:_LST[Node],input_leaves_names:_LST[str],c_prop:float=0.3,grow_func:_CLB):
        self.name="Mixed Mutation Operator"
        self.rng = rng
        self.Fset = Fset
        self.mutops =[
            PointMut(rng=rng,Fset=Fset),
            PermMut(rng=rng),HoistMut(rng=rng),
            ConstMut(rng=rng),
            CollapseMut(rng=rng,input_leaves_names=input_leaves_names,c_prop=c_prop),
            SubTreeMut(rng=rng,grow_func=grow_func)
        ]
    def __call__(self,it:IndividualTree):
        return self.rng.choice(self.mutops)(it)
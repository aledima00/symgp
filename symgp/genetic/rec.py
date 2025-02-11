from ..individual import IndividualTree
import numpy as np


class SubEx:
    def __init__(self,rng:np.random.Generator):
        self.name="Subtree Exchange Operator"
        self.rng = rng
    def __call__(self,it1:IndividualTree,it2:IndividualTree):
        ret1 = it1.deepCopy()
        ret2 = it2.deepCopy()
        nodes1 = ret1.subnodes(keep_leaves=False,keep_root=True)
        nodes2 = ret2.subnodes(keep_leaves=False,keep_root=True)
        if len(nodes1) != 0 and len(nodes2) != 0:
            p1 = self.rng.choice(nodes1)
            p2 = self.rng.choice(nodes2)
            if len(p1.children) !=0 and len(p2.children) != 0:
                idx1 = self.rng.integers(0,len(p1.children))
                idx2 = self.rng.integers(0,len(p2.children))
                p1.children[idx1],p2.children[idx2] = p2.children[idx2],p1.children[idx1]
        ret1.update()
        ret2.update()
        return ret1,ret2

__all__ = ["SubEx"]
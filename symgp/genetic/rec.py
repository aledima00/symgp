from ..individual import IndividualTree
import numpy as np


class SubEx:
    """
    Exchanges a subtree from it1 with a subtree from it2.
    Args:
        it1 (IndividualTree): The first individual tree.
        it2 (IndividualTree): The second individual tree.
    Returns:
        IndividualTree: A new individual tree.
    """
    def __init__(self,rng:np.random.Generator):
        self.name="Subtree Exchange Operator"
        self.rng = rng
    def __call__(self,it1:IndividualTree,it2:IndividualTree):
        nodes1 = it1.subnodes(keep_leaves=False)
        nodes2 = it2.subnodes(keep_leaves=False)
        p1 = self.rng.choice(nodes1)
        p2 = self.rng.choice(nodes2)
        idx1 = self.rng.integers(0,len(p1.children))
        idx2 = self.rng.integers(0,len(p2.children))
        p1.children[idx1],p2.children[idx2] = p2.children[idx2],p1.children[idx1]

__all__ = ["SubEx"]
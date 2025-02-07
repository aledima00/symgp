from .genop import RecOp
from ..individual import IndividualTree
import numpy as np


def _subtree_exchange(it1:IndividualTree,it2:IndividualTree,rng:np.random.Generator):
    """
    Exchanges a subtree from it1 with a subtree from it2.
    Args:
        it1 (IndividualTree): The first individual tree.
        it2 (IndividualTree): The second individual tree.
    Returns:
        IndividualTree: A new individual tree.
    """
    nodes1 = it1.subnodes()
    nodes2 = it2.subnodes()
    p1 = rng.choice(nodes1)
    p2 = rng.choice(nodes2)
    ch1 = rng.choice(p1.children)
    ch2 = rng.choice(p2.children)
    p1.children.remove(ch1)
    p2.children.remove(ch2)
    p1.children.append(ch2)
    p2.children.append(ch1)


SubEx = RecOp("SubtreeExchange",_subtree_exchange)

__all__ = ["SubEx"]
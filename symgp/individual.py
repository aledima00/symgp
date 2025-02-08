from . import Operator
from typing import List
from consoleformat import Formatted
from colorama import Fore
from typing import Dict as _DCT

class Node:
    operator:Operator # operator used in the node
    input_children:List['Node'] # list of children used as inputs for the operator

    def __init__(self, operator:Operator, children:List['Node']):
        self.children = children
        self.operator = operator
    def evaluate(self):
        return self.operator(*[child.evaluate() for child in self.children])
    def fstr(self,fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        fstr.append(f"(")
        self.operator.fstr(fstr)
        for child in self.children:
            fstr.append(", ")
            child.fstr(fstr)
        fstr.append(")")
        return fstr
    def tree_fstr(self,depth=0, ended_levels=dict(),fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        if depth not in ended_levels:
            ended_levels[depth] = False
        if depth>0:
            for i in range(1,depth):
                fstr.append("     " if ended_levels[i] else "  │  ")
            fstr.append("  └──" if ended_levels[depth] else "  ├──")
        fstr.append(f"'{self.operator.name}'",fore=Fore.YELLOW)
        fstr.ret()
        for i,child in enumerate(self.children):
            is_last = i == len(self.children)-1
            if is_last:
                ended_levels[depth+1] = True
            else:
                for k in ended_levels.keys():
                    if k>depth:
                        ended_levels[k] = False
            child.tree_fstr(depth+1, ended_levels,fstr=fstr)
        return fstr
    
    def subnodes(self,keep_leaves:bool=True):
        sn = [child for child in self.children if (keep_leaves or not isinstance(child,Leaf))]
        for child in self.children:
            if keep_leaves or not isinstance(child,Leaf):
                sn += child.subnodes(keep_leaves)
        return sn
    
    def depth(self):
        return 1 + max([child.depth() for child in self.children])
    
    def deepCopy(self):
        return Node(self.operator,[child.deepCopy() for child in self.children])
    
    def __str__(self):
        return str(self.fstr())
    def __repr__(self):
        return str(self)

class Leaf(Node):
    def __init__(self, value):
        # no operator nor children for a leaf
        self.operator = None
        self.children = []
        self.value = value
    def evaluate(self):
        return self.value
    def fstr(self,fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        fstr.append(f"{self.value:.03f}",fore=Fore.GREEN)
        return fstr
    def tree_fstr(self,depth=0,ended_levels=dict(),fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        if depth not in ended_levels:
            ended_levels[depth] = False
        for i in range(1,depth):
            fstr.append("     " if ended_levels[i] else "  │  ")
        fstr.append("  └──" if ended_levels[depth] else "  ├──")
        self.fstr(fstr)
        fstr.ret()
        return fstr
    def subnodes(self):
        return []
    def depth(self):
        return 1
    def deepCopy(self):
        return Leaf(self.value)
    def __str__(self):
        return str(self.fstr())
    
class VarLeaf(Leaf):
    def __init__(self, name:str):
        self.name = name
        self.assigned = False
        super().__init__(None) # no value
    def evaluate(self):
        if not self.assigned:
            raise ValueError("Leaf value is not set")
        tempv = self.value
        self.assigned = False
        self.value = None
        return tempv
    def assign(self,value):
        self.value = value
        self.assigned = True
    def fstr(self,fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        fstr.append(f"{self.name}",fore=Fore.CYAN)
        return fstr
    def deepCopy(self):
        return VarLeaf(self.name)
    def __str__(self):
        return str(self.fstr())


class IndividualTree:
    inputLeaves:_DCT[str,VarLeaf]
    root:Node
    numInputs:int
    
    def __init__(self, root:Node, inputLeaves:List[VarLeaf]=[]):
        self.root = root
        self.numInputs = len(inputLeaves)
        self.inputLeaves = dict((il.name,il) for il in inputLeaves)

    def evaluate(self,kv_inputs:_DCT[str,object]):
        if len(kv_inputs) != self.numInputs:
            raise ValueError("Input length does not match")
        for k,v in kv_inputs.items():
            self.inputLeaves[k].assign(v)
        return self.root.evaluate()
    def tree_fstr(self)->Formatted:
        return self.root.tree_fstr()
    def fstr(self)->Formatted:
        return self.root.fstr()
    
    def subnodes(self,keep_leaves:bool=True,keep_root:bool=False):
        sn = self.root.subnodes(keep_leaves)
        if keep_root:
            sn = [self.root] + sn
        return sn
    def depth(self):
        return self.root.depth()
    def deepCopy(self):
        return IndividualTree(self.root.deepCopy(),inputLeaves=[il.deepCopy() for il in self.inputLeaves])
    
__all__ = ["Node", "Leaf", "IndividualTree","VarLeaf"]
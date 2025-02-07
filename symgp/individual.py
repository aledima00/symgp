from . import Operator
from typing import List
from consoleformat import Formatted
from colorama import Fore

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
    
    def subnodes(self):
        sn = [child for child in self.children]
        for child in self.children:
            sn += child.subnodes()
        return sn
    
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
        fstr.append(str(self.value),fore=Fore.GREEN)
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
    def __str__(self):
        return str(self.fstr())


class IndividualTree:
    inputLeaves:List[Node]
    root:Node
    numInputs:int
    
    def __init__(self, root:Node, inputLeaves:List[VarLeaf]=[]):
        self.root = root
        self.numInputs = len(inputLeaves)
        self.inputLeaves:List[VarLeaf] = inputLeaves

    def evaluate(self,inputValues):
        if len(inputValues) != self.numInputs:
            raise ValueError("Input length does not match")
        for i in range(self.numInputs):
            self.inputLeaves[i].assign(inputValues[i])
        return self.root.evaluate()
    def tree_fstr(self)->Formatted:
        return self.root.tree_fstr()
    def fstr(self)->Formatted:
        return self.root.fstr()
    
    def subnodes(self):
        return self.root.subnodes()
    
__all__ = ["Node", "Leaf", "IndividualTree","VarLeaf"]
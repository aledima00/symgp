from .operators import Operator
from typing import List
from .format import Formatted
from colorama import Fore

class Node:
    operator:Operator # operator used in the node
    input_children:List['Node'] # list of children used as inputs for the operator
    value:any # only used for Leaf Nodes

    def __init__(self, operator:Operator, children:List['Node']):
        self.children = children
        self.operator = operator
        self.value = None
    def evaluate(self):
        return self.operator(*[child.evaluate() for child in self.children])
    def fstr(self,fstr:Formatted=Formatted())->Formatted:
        fstr.append(f"(")
        self.operator.fstr(fstr)
        for child in self.children:
            fstr.append(", ")
            child.fstr(fstr)
        fstr.append(")")
        return fstr
    def tree_fstr(self,depth=0, ended_levels=dict(),fstr:Formatted=Formatted())->Formatted:
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
            child.tree_fstr(depth+1, ended_levels,fstr=fstr)
        return fstr
    def __str__(self):
        str(self.fstr())
    def __repr__(self):
        return str(self)

class Leaf(Node):
    def __init__(self, value=None):
        self.operator = None
        self.children = []
        self.value = value
    def evaluate(self):
        if self.value is None:
            raise ValueError("Leaf value is not set")
        return self.value
    def fstr(self,fstr:Formatted=Formatted()):
        fstr.append(str(self.value),fore=Fore.GREEN)
        return fstr
    def tree_fstr(self,depth=0,ended_levels=dict(),fstr:Formatted=Formatted())->Formatted:
        if depth not in ended_levels:
            ended_levels[depth] = False
        for i in range(1,depth):
            fstr.append("     " if ended_levels[i] else "  │  ")
        fstr.append("  └──" if ended_levels[depth] else "  ├──")
        self.fstr(fstr)
        fstr.ret()
        return fstr
    def __str__(self):
        return f"Leaf({self.value})"
    def __repr__(self):
        return str(self)


class IndividualTree:
    inputLeaves:list["Node"]
    root:Node
    numInputs:int
    
    def __init__(self, root:Node, inputLeaves:list["Node"]=[]):
        self.root = root
        self.numInputs = len(inputLeaves)
        self.inputLeaves = inputLeaves

    def evaluate(self,inputValues):
        if len(inputValues) != self.numInputs:
            raise ValueError("Input length does not match")
        for i in range(self.numInputs):
            self.inputLeaves[i].value = inputValues[i]
        return self.root.evaluate()
    
__all__ = ["Node", "Leaf", "IndividualTree"]
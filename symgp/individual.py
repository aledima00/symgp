from .operators import Operator
from typing import List

class Node:
    operator:Operator # operator used in the node
    input_children:List['Node'] # list of children used as inputs for the operator
    value:any # only used for Leaf Nodes

    def __init__(self, operator:Operator, input_children:List['Node']):
        self.input_children = input_children
        self.operator = operator
        self.value = None
    def evaluate(self):
        return self.operator(*[child.evaluate() for child in self.children])
    def __str__(self):
        return f"({self.operator}, {', '.join([str(child) for child in self.children])})"
    def __repr__(self):
        return f"({self.operator}, {', '.join([str(child) for child in self.children])})"

class Leaf(Node):
    def __init__(self, value=None):
        self.operator = None
        self.children = []
        self.value = value
    def evaluate(self):
        if self.value is None:
            raise ValueError("Leaf value is not set")
        return self.value
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)


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
    
    def __str__(self):
        return str(self.root)
    def __repr__(self):
        return str(self.root)
    
__all__ = ["Node", "Leaf", "IndividualTree"]
class Node:
    def __init__(self, function=None, children=[]):
        self.function = function
        self.children = children
        self.value = None
    def evaluate(self):
        return self.function(*[child.evaluate() for child in self.children])
    def appendChild(self, child:"Node"):
        self.children.append(child)
    def __str__(self):
        return "("+self.function.__name__ +", " +", ".join([str(child) for child in self.children]) + ")"


class Leaf(Node):
    def __init__(self, value=None):
        self.function = None
        self.children = []
        self.value = value
    def evaluate(self):
        if self.value is None:
            raise ValueError("Leaf value is not set")
        return self.value
    def __str__(self):
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
    
__all__ = ["Node", "Leaf", "IndividualTree"]
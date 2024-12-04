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
    

if __name__ == "__main__":

    # Define functions
    def add(x, y):
        return x + y

    def sub(x, y):
        return x - y

    def mul(x, y):
        return x * y

    # Create nodes
    leaf1 = Leaf()
    leaf2 = Leaf()
    leaf3 = Leaf(5)
    add_node = Node(add, [leaf1, leaf2])
    root = Node(mul, [add_node, leaf3])

    # Create individual tree
    tree = IndividualTree(root, [leaf1, leaf2])

    # Evaluate the tree
    result = tree.evaluate([3,4])
    print(f"Result of the tree evaluation: {result}")
    print(f"LISP of Tree structure: {tree}")
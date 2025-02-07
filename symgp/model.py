from . import Operator as _op
from .individual import Leaf, VarLeaf, IndividualTree, Node
import numpy as np
from typing import List as _LST
from . import npf

_secret_recipe = 12345

class Model:
    max_depth:int
    population_size:int

    Fset:_LST[_op] # Fset is the set of functions that can be used in the model
    Tset:_LST[_op] # Tset is the set of terminal nodes, which are the input leaves and constants

    # Tset is the set of terminal nodes, which are the input leaves and constantss
    inputLeaves:_LST[VarLeaf] # actual inputs
    c_prop:float # random constants proportion

    rng:np.random.Generator
    
    def __init__(self,max_depth:int,population_size:int,Fset:list[_op],inputLeaves:list[VarLeaf],*,c_prop:float=0.3,rand_seed:int=_secret_recipe):
        """
        Initializes the model with the given parameters.
        Args:
            max_depth (int): The maximum depth of the model.
            Fset (list[_op]): A list of function set operations.
            inputLeaves (list[VarLeaf]): A list of input leaves (variables).
            c_prop (float, optional): The proportion of constants to input leaves. Defaults to 0.4.
        """
        
        self.max_depth = max_depth
        self.population_size = population_size
        self.Fset = Fset
        self.inputLeaves = inputLeaves
        self.c_prop = c_prop
        self.rng = np.random.Generator(np.random.PCG64([rand_seed]))

    def __grow(self,curr_depth=0)->IndividualTree:
        """
        Grows a new individual tree.
        Returns:
            IndividualTree: A new individual tree.
        """
        if curr_depth == self.max_depth:
            # reached the maximum depth: choose a constant or a leaf
            if self.rng.random() < self.c_prop:
                return Leaf(self.rng.random())
            else:
                return self.rng.choice(self.inputLeaves)
        op = self.rng.choice(self.Fset)
        children = []
        for i in range(op.arity):
            children.append(self.__grow(curr_depth+1))
        curr_node = Node(operator=op,children=children)
        if curr_depth == 0:
            return IndividualTree(curr_node,inputLeaves=self.inputLeaves)
        else:
            return curr_node
        
    def sample(self):
        """
        Samples a new individual tree from the model.
        Returns:
            IndividualTree: A new individual tree.
        """
        return self.__grow()

class BaseModel(Model):
    def __init__(self,max_depth:int,population_size:int,inputLeaves:list[VarLeaf],*,c_prop:float=0.3,rand_seed:int=_secret_recipe):
        super().__init__(max_depth=max_depth,population_size=population_size,Fset=npf.get_all(),inputLeaves=inputLeaves,c_prop=c_prop,rand_seed=rand_seed)

__all__ = ["Model","BaseModel"]
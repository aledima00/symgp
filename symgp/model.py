from . import Operator as _op
from .individual import Leaf, VarLeaf, IndividualTree, Node
import numpy as np
from typing import List as _LST
from . import npf
from .genetic import MixedMut,SubEx
from tqdm.auto import tqdm

_secret_recipe = 12345

class Model:
    max_depth:int
    population_size:int

    # Fset is the set of functions that can be used to grow the trees
    unaryFset:_LST[_op] # unary functions
    naryFset:_LST[_op] # n-ary functions

    # Tset is the set of terminal nodes, which are the input leaves and constants
    input_leaves_names:_LST[str] # actual inputs
    c_prop:float # proportion of constants to input leaves in the terminal set
    unary_prop:float # proportion of drawing unary functions to drawing n-ary functions when growing a tree

    rng:np.random.Generator

    __population:_LST[IndividualTree]

    # genetic operators
    MutOp:MixedMut
    RecOp:SubEx

    
    def __init__(self,max_depth:int,population_size:int,Fset:list[_op],input_leaves_names:list[str],*,c_prop:float=0.3,rand_seed:int=_secret_recipe,unary_prop:float=0.5):
        """
        Initializes the model with the given parameters.
        Args:
            max_depth (int): The maximum depth of the model.
            Fset (list[_op]): A list of function set operations.
            input_leaves_names (list[str]): A list of name of input leaves (variables).
            c_prop (float, optional): The proportion of constants to input leaves. Defaults to 0.4.
            rand_seed (int, optional): The random seed. Defaults to 12345.
            unary_prop (float, optional): The proportion of drawing unary functions to drawing n-ary functions when growing a tree. Defaults to 0.5.
        """
        
        self.max_depth = max_depth
        self.population_size = population_size
        self.unaryFset = [op for op in Fset if npf.is_unary(op)]
        self.naryFset = [op for op in Fset if npf.is_nary(op)]
        self.input_leaves_names = input_leaves_names
        self.c_prop = c_prop
        self.unary_prop = unary_prop        
        self.rng = np.random.Generator(np.random.PCG64([rand_seed]))
        self.__population = []
        self.MutOp = MixedMut(rng=self.rng,Fset=self.unaryFset+self.naryFset,input_leaves_names=input_leaves_names,c_prop=c_prop,grow_func=self.__grow)
        self.RecOp = SubEx(rng=self.rng)

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
                return VarLeaf(self.rng.choice(self.input_leaves_names))
        if self.rng.random() < self.unary_prop:
            op = self.rng.choice(self.unaryFset)
        else:
            op = self.rng.choice(self.naryFset)
        children = []
        for i in range(op.arity):
            children.append(self.__grow(curr_depth+1))
        curr_node = Node(operator=op,children=children)
        if curr_depth == 0:
            return IndividualTree(curr_node)
        else:
            return curr_node
        
    def populate(self):
        """
        Populates the model with a new generation of individual trees.
        Returns:
            list[IndividualTree]: A list of new individual trees.
        """
        self.__population= [self.__grow() for _ in range(self.population_size)]
    
    def kill(self):
        """
        Kills the current population of the model.
        """
        self.__population = []

    def population(self):
        """
        Returns the current population of the model.
        Returns:
            list[IndividualTree]: The current population of the model.
        """
        return self.__population
    
    def sample(self):
        """
        Samples a new individual tree from the model.
        Returns:
            IndividualTree: A new individual tree.
        """
        return self.__grow()
    def Fset(self):
        return self.unaryFset+self.naryFset
    
    def evolve(self,X:np.ndarray,Y:np.ndarray,*,generations:int,elitism_rate:float=0.02,mutation_rate:float=0.1,pool_size:int=2):
        """
        Evolves the model for a given number of generations.
        Args:
            X (np.ndarray): The input data.
            Y (np.ndarray): The output data.
            generations (int): The number of generations to evolve the model.
        """
        for g in tqdm(range(generations), position=0, desc="Evolving", leave=True):
            progress = g/generations
            #LAMBDA_PARSIMONY = 10*(1-progress)
            # sort the population by fitness
            self.__population.sort(key=lambda x: x.fitness(X,Y,self.input_leaves_names,lam=progress),reverse=True)
            
            # determine proportion of elites and offspring
            SZ_ELITES = int(elitism_rate*self.population_size)
            SZ_OFFSPRING = self.population_size - SZ_ELITES
            
            # elitism: keep the top individuals
            elites = self.__population[:SZ_ELITES]
            self.__population = self.__population[SZ_ELITES:]

            # prepare tournament selection
            def _tournament_selection():
                pool = self.rng.choice(self.__population,size=pool_size,replace=False)
                return max(pool,key=lambda x: x.fitness(X,Y,self.input_leaves_names,lam=progress))
            
            # actual generatio of offspring
            offspring = []
            for _ in tqdm(range(SZ_OFFSPRING),desc=f"Generating offspring({g}/{generations})",position=1, leave=False):
                if self.rng.random() < mutation_rate:
                    p = _tournament_selection()
                    offspring.append(self.MutOp(p))
                else:
                    p1 = _tournament_selection()
                    p2 = _tournament_selection()
                    rp1,rp2 = self.RecOp(p1,p2)
                    offspring.append(rp1)
                    offspring.append(rp2)

            # generational approach + elitism
            self.__population = elites + offspring
        
        # sort the population by fitness in last generation in order to get the best individual as the first element
        self.__population.sort(key=lambda x: x.mse(X,Y,self.input_leaves_names))
    def __getitem__(self,idx):
        return self.__population[idx]
    def __iter__(self):
        return iter(self.__population)

class BaseModel(Model):
    def __init__(self,max_depth:int,population_size:int,input_leaves_names:list[str],*,c_prop:float=0.3,rand_seed:int=_secret_recipe):
        super().__init__(max_depth=max_depth,population_size=population_size,Fset=npf.get_all(),input_leaves_names=input_leaves_names,c_prop=c_prop,rand_seed=rand_seed)

__all__ = ["Model","BaseModel"]
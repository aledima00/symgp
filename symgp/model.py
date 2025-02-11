from . import Operator as _op
from .individual import Leaf, VarLeaf, IndividualTree, Node, SpecialLeaf
import numpy as np
from typing import List as _LST, Literal as _LIT, Dict as _DCT
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

    rng:np.random.Generator

    # genetic operators
    MutOp:MixedMut
    RecOp:SubEx

    
    def __init__(self,max_depth:int,population_size:int,Fset:list[_op],input_leaves_names:list[str],*,rand_seed:int=_secret_recipe,fitness_grouping_perc=None,generation_params:_DCT|None=None):
        
        self.max_depth = max_depth
        self.population_size = population_size
        self.unaryFset = [op for op in Fset if npf.is_unary(op)]
        self.naryFset = [op for op in Fset if npf.is_nary(op)]
        self.input_leaves_names = input_leaves_names
        self.rng = np.random.Generator(np.random.PCG64([rand_seed]))
        self.__population = []
        self.MutOp = MixedMut(rng=self.rng,Fset=self.unaryFset+self.naryFset,input_leaves_names=input_leaves_names,grow_func=self.__grow,lgen_func=self.__leaf_gen,probabs=[30,15,7.5,7.5,30])
        self.RecOp = SubEx(rng=self.rng)
        self.fittest_grp_size = None if fitness_grouping_perc is None else int(fitness_grouping_perc*population_size)
        self.split_in_fitness_groups = fitness_grouping_perc is not None

        
        if generation_params is None:
            # default generation parameters
            self._int_constants = True
            self._randc_mean = 0
            self._randc_std = 5
            self._ctv_prop = 0.3
            self._stv_prop = 0.1
            self._unary_to_others_prop = 0.5
        else:
            allowed_generation_params ={
                "int_constants":bool,
                "randc_mean":float|int,
                "randc_std":float|int,
                "ctv_prop":float|int,
                "stv_prop":float|int,
                "unary_to_others_prop":float|int
            }
            for k,v in generation_params.items():
                if k in allowed_generation_params:
                    if isinstance(v,allowed_generation_params[k]):
                        setattr(self,f"_{k}",v)
                    else:
                        raise ValueError(f"Invalid type for constant generation parameter: {k} should be {allowed_generation_params[k]} but is {type(v)}")
                else:
                    raise ValueError(f"Invalid constant generation parameter: {k}")

    def __grow(self,curr_depth=0)->IndividualTree:
        """
        Grows a new individual tree.
        Returns:
            IndividualTree: A new individual tree.
        """
        if curr_depth == self.max_depth:
            # reached the maximum depth: generate a leaf
            return self.__leaf_gen()
        if self.rng.random() < self._unary_to_others_prop:
            op = self.rng.choice(self.unaryFset)
        else:
            op = self.rng.choice(self.naryFset)
        children = []
        for i in range(op.arity):
            children.append(self.__grow(curr_depth+1))
        curr_node = Node(operator=op,children=children)
        if curr_depth == 0:
            return IndividualTree(curr_node, simplify=True)
        else:
            return curr_node
        
    def __leaf_gen(self)->Leaf|SpecialLeaf|VarLeaf:
        if self.rng.random() < self._ctv_prop:
            if self.rng.random() < self._stv_prop:
                strval = self.rng.choice(["pi","e"])
                return SpecialLeaf(strval)
            else:
                cval = self.rng.normal(self._randc_mean,self._randc_std)
                if self._int_constants:
                    cval = np.round(cval)
                return Leaf(cval)
        else:
            return VarLeaf(self.rng.choice(self.input_leaves_names))

        
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
    
    def evolve(self,X:np.ndarray,Y:np.ndarray,*,generations:int,elitism_rate:float|tuple=0.02,mutation_rate:float|tuple=0.1,pool_size:int=2,parsimony_weight:float|tuple=0,parsimony_format:_LIT["linear","bilinear"]="linear"):
        
        # check if there are dynamic parameters
        dynamic_mutation = isinstance(mutation_rate,tuple)
        dynamic_elitism = isinstance(elitism_rate,tuple)
        dynamic_parsimony = isinstance(parsimony_weight,tuple)

        for g in tqdm(range(generations), position=0, desc="Evolving", leave=True):
            progress = g/generations

            # adjust mutation and elitism rates
            mrate = mutation_rate if not dynamic_mutation else mutation_rate[0] + (mutation_rate[1]-mutation_rate[0])*progress
            eltrate = elitism_rate if not dynamic_elitism else elitism_rate[0] + (elitism_rate[1]-elitism_rate[0])*progress
            parsweight = parsimony_weight if not dynamic_parsimony else parsimony_weight[0] + (parsimony_weight[1]-parsimony_weight[0])*progress

            # sort the population by fitness
            self.__population.sort(key=lambda x: x.fitness(X,Y,self.input_leaves_names,parsimony_weight=parsweight,parsimony_format=parsimony_format),reverse=True)
            
            # determine proportion of elites and offspring
            SZ_ELITES = int(eltrate*self.population_size)
            SZ_OFFSPRING = self.population_size - SZ_ELITES
            
            # elitism: keep the top individuals
            elites = self.__population[:SZ_ELITES]
            self.__population = self.__population[SZ_ELITES:]

            # prepare tournament selection
            def _tournament_selection():
                # check if the model must be split in 2 fitness groups
                if self.split_in_fitness_groups:
                    fittest_group = self.__population[:self.fittest_grp_size]
                    rest = self.__population[self.fittest_grp_size:]
                    draw_grp = fittest_group if self.rng.random() < 0.8 else rest
                else:
                    draw_grp = self.__population
                pool = self.rng.choice(draw_grp,size=pool_size,replace=False)
                return max(pool,key=lambda x: x.fitness(X,Y,self.input_leaves_names,parsimony_weight=parsweight,parsimony_format=parsimony_format))
            
            # actual generatio of offspring
            offspring = []
            for _ in tqdm(range(SZ_OFFSPRING),desc=f"Generating offspring({g}/{generations})",position=1, leave=False):
                if self.rng.random() < mrate:
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
    def __init__(self,max_depth:int,population_size:int,input_leaves_names:list[str],*,rand_seed:int=_secret_recipe,fitness_grouping_perc=None,generation_params:_DCT|None=None):
        super().__init__(max_depth=max_depth,population_size=population_size,Fset=npf.get_all(),input_leaves_names=input_leaves_names,rand_seed=rand_seed,fitness_grouping_perc=fitness_grouping_perc,generation_params=generation_params)

__all__ = ["Model","BaseModel"]
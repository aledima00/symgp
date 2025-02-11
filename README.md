# symgp
Python Symbolic regression with Genetic Programming.

## Overview

`symgp` is a Python library for symbolic regression using genetic programming. It allows users to evolve mathematical expressions to fit given data. The library leverages the power of genetic algorithms to automatically discover mathematical models that best describe the provided data.

## Installation

### Using pip

You can install `symgp` using pip from the GitHub repository:

```sh
pip install git+https://github.com/aledima00/symgp.git
```

### Using Poetry

You can install `symgp` using Poetry from the GitHub repository:

```sh
poetry add git+https://github.com/aledima00/symgp.git
```

### From Source

To install `symgp` from source, clone the repository and install it using Poetry (`poetry` is required):

```sh
git clone https://github.com/aledima00/symgp.git
cd symgp
poetry install
```

## Usage

### Basic Example

Here is a basic example of how to use `symgp` to perform symbolic regression:

```python
import numpy as np
from symgp import BaseModel

# Load your data
X = np.random.rand(1, 100)  # Example input data
Y = np.sin(X)  # Example output data

# Define the input variable names
LEAVES_NAMES = [f"x[{i}]" for i in range(X.shape[0])]

# some generation params
generation_params = {
    "int_constants":True, # use int as random constants
    "randc_mean":0, # mean of random constants
    "randc_std":5, # stddev of random constants
    "ctv_prop":0.3, # ratio of constants to input variables
    "stv_prop":0.1, # ratio of special constants (pi,e,...) to normal ones
    "unary_to_others_prop":0.5 # ratio of unary operators to normal ones
}

# Initialize the model
model = BaseModel(
    max_depth=8,
    population_size=1000,
    input_leaves_names=LEAVES_NAMES,
    rand_seed=1234567890,
    generation_params=generation_params
)

# Populate the initial population
model.populate()

# Evolve the population
model.evolve(X,Y, 
    generations=10,
    mutation_rate=0.1,
    elitism_rate=0.02,
    pool_size=2,
    parsimonyweight=0.1,
    parsimony_format='bilinear'
)

# Get the best individual
best_individual = model.population()[0]

# Print the best individual and its fitness
print("Best individual:", best_individual.fstr())
print("Fitness:", best_individual.fitness(X, Y, LEAVES_NAMES))
```

## Library Components

### Core Classes

#### **Operator**

The `Operator` class represents a mathematical operator used in the symbolic expressions.

- **Attributes:**
  - `name`: The name of the operator.
  - `arity`: The number of arguments the operator takes.
  - `function`: The function implementing the operator.
  - `expr`: The string representation of the operator.
  - `simplify_func`: A function to simplify expressions involving this operator.

- **Methods:**
  - `__init__(self, name: str, arity: int, func: Callable, expr: str = None, *, simplify_func: Callable[[List], Tuple['Operator', List]] = None)`: Initializes the operator.
    - `name`: The name of the operator.
    - `arity`: The number of arguments the operator takes.
    - `func`: The function implementing the operator.
    - `expr`: The string representation of the operator.
    - `simplify_func`: A function to simplify expressions involving this operator.
  - `__call__(self, *args)`: Applies the operator to the given arguments.
    - `args`: The arguments to apply the operator to.
  - `simplified(self, in_lst: List) -> Tuple['Operator', List]`: Simplifies the operator with the given arguments.
    - `in_lst`: The list of arguments to simplify.
  - `solved_expr(self, args: list) -> str`: Returns the string representation of the operator with the given arguments.
    - `args`: The arguments to include in the string representation.
  - `fstr(self, fstr: Formatted = None) -> Formatted`: Returns a formatted string representation of the operator.
    - `fstr`: The formatted string to append to.
  - `getInfo(self) -> str`: Returns detailed information about the operator.

#### **Node**

The `Node` class represents a node in the symbolic expression tree.

- **Attributes:**
  - `operator`: The operator used in the node.
  - `children`: The list of child nodes.

- **Methods:**
  - `__init__(self, operator: Operator, children: List['Node'])`: Initializes the node.
    - `operator`: The operator used in the node.
    - `children`: The list of child nodes.
  - `simplify(self) -> "Node"`: Simplifies the node.
  - `evaluate(self)`: Evaluates the node.
  - `fstr(self, fstr: Formatted = None) -> Formatted`: Returns a formatted string representation of the node.
    - `fstr`: The formatted string to append to.
  - `tree_fstr(self, depth: int = 0, ended_levels: dict = dict(), fstr: Formatted = None) -> Formatted`: Returns a tree-formatted string representation of the node.
    - `depth`: The current depth of the tree.
    - `ended_levels`: The levels that have ended.
    - `fstr`: The formatted string to append to.
  - `subnodes(self, keep_leaves: bool = True) -> List['Node']`: Returns the subnodes of the node.
    - `keep_leaves`: Whether to keep the leaves in the subnodes.
  - `expr(self, names: Dict[str, str] = None) -> str`: Returns the string representation of the node.
    - `names`: The names to use in the string representation.
  - `depth(self) -> int`: Returns the depth of the node.
  - `deepCopy(self) -> "Node"`: Returns a deep copy of the node.

#### **Leaf**

The `Leaf` class represents a leaf node in the symbolic expression tree.

- **Attributes:**
  - `value`: The value of the leaf.

- **Methods:**
  - `__init__(self, value)`: Initializes the leaf.
    - `value`: The value of the leaf.
  - `evaluate(self)`: Evaluates the leaf.
  - `fstr(self, fstr: Formatted = None) -> Formatted`: Returns a formatted string representation of the leaf.
    - `fstr`: The formatted string to append to.
  - `tree_fstr(self, depth: int = 0, ended_levels: dict = dict(), fstr: Formatted = None) -> Formatted`: Returns a tree-formatted string representation of the leaf.
    - `depth`: The current depth of the tree.
    - `ended_levels`: The levels that have ended.
    - `fstr`: The formatted string to append to.
  - `depth(self) -> int`: Returns the depth of the leaf.
  - `expr(self, names: Dict[str, str] = None) -> str`: Returns the string representation of the leaf.
    - `names`: The names to use in the string representation.
  - `deepCopy(self) -> "Leaf"`: Returns a deep copy of the leaf.

#### **VarLeaf**

The `VarLeaf` class represents a variable leaf node in the symbolic expression tree.

- **Attributes:**
  - `name`: The name of the variable.
  - `assigned`: Whether the variable has been assigned a value.
  - `value`: The value of the variable.

- **Methods:**
  - `__init__(self, name: str)`: Initializes the variable leaf.
    - `name`: The name of the variable.
  - `evaluate(self)`: Evaluates the variable leaf.
  - `assign(self, value)`: Assigns a value to the variable leaf.
    - `value`: The value to assign to the variable leaf.
  - `unassign(self)`: Unassigns the value of the variable leaf.
  - `fstr(self, fstr: Formatted = None) -> Formatted`: Returns a formatted string representation of the variable leaf.
    - `fstr`: The formatted string to append to.
  - `expr(self, names: Dict[str, str] = None) -> str`: Returns the string representation of the variable leaf.
    - `names`: The names to use in the string representation.
  - `deepCopy(self) -> "VarLeaf"`: Returns a deep copy of the variable leaf.

#### **SpecialLeaf**

The `SpecialLeaf` class represents a special constant leaf node (e.g., π, e) in the symbolic expression tree.

- **Attributes:**
  - `name`: The name of the special constant.
  - `value`: The value of the special constant.

- **Methods:**
  - `__init__(self, name: Literal["pi", "e"])`: Initializes the special leaf.
    - `name`: The name of the special constant.
  - `fstr(self, fstr: Formatted = None) -> Formatted`: Returns a formatted string representation of the special leaf.
    - `fstr`: The formatted string to append to.

#### **IndividualTree**

The `IndividualTree` class represents an individual symbolic expression tree.

- **Attributes:**
  - `root`: The root node of the tree.
  - `inputLeaves`: The dictionary of input leaves.
  - `numInputs`: The number of input leaves.

- **Methods:**
  - `__init__(self, root: Node, *, simplify: bool = False)`: Initializes the individual tree.
    - `root`: The root node of the tree.
    - `simplify`: Whether to simplify the tree.
  - `update(self)`: Updates the tree.
  - `evaluate_sample(self, kv_inputs: Dict[str, object])`: Evaluates the tree with the given input values.
    - `kv_inputs`: The input values to evaluate the tree with.
  - `tree_fstr(self) -> Formatted`: Returns a tree-formatted string representation of the tree.
  - `fstr(self) -> Formatted`: Returns a formatted string representation of the tree.
  - `evaluate(self, inputs: np.ndarray, order: List[str]) -> np.ndarray`: Evaluates the tree with the given input array.
    - `inputs`: The input array to evaluate the tree with.
    - `order`: The order of the input variables.
  - `mse(self, inputs: np.ndarray, outputs: np.ndarray, order: List[str])`: Computes the mean squared error of the tree.
    - `inputs`: The input array.
    - `outputs`: The output array.
    - `order`: The order of the input variables.
  - `fitness(self, inputs: np.ndarray, outputs: np.ndarray, order: List[str], *, parsimony_weight: float = 0, parsimony_format: Literal["linear", "bilinear"] = "linear")`: Computes the fitness of the tree.
    - `inputs`: The input array.
    - `outputs`: The output array.
    - `order`: The order of the input variables.
    - `parsimony_weight`: The weight of the parsimony penalty.
    - `parsimony_format`: The format of the parsimony penalty.
  - `subnodes(self, keep_leaves: bool = True, keep_root: bool = False) -> List[Node]`: Returns the subnodes of the tree.
    - `keep_leaves`: Whether to keep the leaves in the subnodes.
    - `keep_root`: Whether to keep the root in the subnodes.
  - `getExpr(self, names: Dict[str, str] = None) -> str`: Returns the string representation of the tree.
    - `names`: The names to use in the string representation.
  - `depth(self) -> int`: Returns the depth of the tree.
  - `deepCopy(self) -> "IndividualTree"`: Returns a deep copy of the tree.

### Genetic Operators

#### **SubEx**

The `SubEx` class represents the subtree exchange operator used in genetic programming.

- **Attributes:**
  - `name`: The name of the operator.
  - `rng`: The random number generator.

- **Methods:**
  - `__init__(self, rng: np.random.Generator)`: Initializes the subtree exchange operator.
    - `rng`: The random number generator.
  - `__call__(self, it1: IndividualTree, it2: IndividualTree) -> Tuple[IndividualTree, IndividualTree]`: Applies the subtree exchange operator to two individuals.
    - `it1`: The first individual.
    - `it2`: The second individual.

#### **PointMut**

The `PointMut` class represents the point mutation operator used in genetic programming.

- **Attributes:**
  - `name`: The name of the operator.
  - `rng`: The random number generator.
  - `Fset`: The set of functions that can be used in the mutation.

- **Methods:**
  - `__init__(self, rng: np.random.Generator, Fset: List[Node])`: Initializes the point mutation operator.
    - `rng`: The random number generator.
    - `Fset`: The set of functions that can be used in the mutation.
  - `__call__(self, it: IndividualTree) -> IndividualTree`: Applies the point mutation operator to an individual.
    - `it`: The individual to apply the mutation to.

#### **PermMut**

The `PermMut` class represents the permutation mutation operator used in genetic programming.

- **Attributes:**
  - `name`: The name of the operator.
  - `rng`: The random number generator.

- **Methods:**
  - `__init__(self, rng: np.random.Generator)`: Initializes the permutation mutation operator.
    - `rng`: The random number generator.
  - `__call__(self, it: IndividualTree) -> IndividualTree`: Applies the permutation mutation operator to an individual.
    - `it`: The individual to apply the mutation to.

#### **HoistMut**

The `HoistMut` class represents the hoist mutation operator used in genetic programming.

- **Attributes:**
  - `name`: The name of the operator.
  - `rng`: The random number generator.

- **Methods:**
  - `__init__(self, rng: np.random.Generator)`: Initializes the hoist mutation operator.
    - `rng`: The random number generator.
  - `__call__(self, it: IndividualTree) -> IndividualTree`: Applies the hoist mutation operator to an individual.
    - `it`: The individual to apply the mutation to.

#### **CollapseMut**

The `CollapseMut` class represents the collapse mutation operator used in genetic programming.

- **Attributes:**
  - `name`: The name of the operator.
  - `rng`: The random number generator.
  - `input_leaves_names`: The list of input leaves names.
  - `lgen_func`: The function to generate leaf nodes.

- **Methods:**
  - `__init__(self, rng: np.random.Generator, input_leaves_names: List[str], lgen_func: Callable)`: Initializes the collapse mutation operator.
    - `rng`: The random number generator.
    - `input_leaves_names`: The list of input leaves names.
    - `lgen_func`: The function to generate leaf nodes.
  - `__call__(self, it: IndividualTree) -> IndividualTree`: Applies the collapse mutation operator to an individual.
    - `it`: The individual to apply the mutation to.

#### **MixedMut**

The `MixedMut` class represents a mixed mutation operator that combines multiple mutation operators.

- **Attributes:**
  - `name`: The name of the operator.
  - `rng`: The random number generator.
  - `Fset`: The set of functions that can be used in the mutation.
  - `mutops`: The list of mutation operators.

- **Methods:**
  - `__init__(self, rng: np.random.Generator, Fset: List[Node], input_leaves_names: List[str], grow_func: Callable, lgen_func: Callable)`: Initializes the mixed mutation operator.
    - `rng`: The random number generator.
    - `Fset`: The set of functions that can be used in the mutation.
    - `input_leaves_names`: The list of input leaves names.
    - `grow_func`: The function to grow new trees.
    - `lgen_func`: The function to generate leaf nodes.
  - `__call__(self, it: IndividualTree) -> IndividualTree`: Applies a randomly chosen mutation operator to an individual.
    - `it`: The individual to apply the mutation to.

### Models

#### **Model**

The `Model` class represents the genetic programming model.

- **Attributes:**
  - `max_depth`: The maximum depth of the trees.
  - `population_size`: The size of the population.
  - `unaryFset`: The set of unary functions.
  - `naryFset`: The set of n-ary functions.
  - `input_leaves_names`: The list of input leaves names.
  - `rng`: The random number generator.
  - `MutOp`: The mutation operator.
  - `RecOp`: The recombination operator.
  - `fittest_grp_size`: The size of the fittest group.
  - `split_in_fitness_groups`: Whether to split the population into fitness groups.

- **Methods:**
  - `__init__(self, max_depth: int, population_size: int, Fset: list[Operator], input_leaves_names: list[str], *, rand_seed: int = _secret_recipe, fitness_grouping_perc: float = None, generation_params: Dict = None)`: Initializes the model.
    - `max_depth`: The maximum depth of the trees.
    - `population_size`: The size of the population.
    - `Fset`: The set of functions that can be used in the trees.
    - `input_leaves_names`: The list of input leaves names.
    - `rand_seed`: The random seed.
    - `fitness_grouping_perc`: The percentage of the population to group by fitness.
    - `generation_params`: The parameters for generating the trees.
  - `__grow(self, curr_depth: int = 0) -> IndividualTree`: Grows a new individual tree.
    - `curr_depth`: The current depth of the tree.
  - `__leaf_gen(self) -> Leaf | SpecialLeaf | VarLeaf`: Generates a new leaf node.
  - `populate(self)`: Populates the model with a new generation of individual trees.
  - `kill(self)`: Kills the current population of the model.

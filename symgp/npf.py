## this section is dedicated to implementations of the most common numpy functions
import numpy as np
from .operators import Operator, OpRules, DataTypes

# Define the operators
add = Operator(
    "add",
    lambda a,b: np.add(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM,DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

sub = Operator(
    "sub",
    lambda a,b: np.subtract(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM,DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

mul = Operator(
    "mul",
    lambda a,b: np.multiply(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM,DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

div = Operator(
    "div",
    lambda a,b: np.divide(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM,DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

pow = Operator(
    "pow",
    lambda a,b: np.power(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM,DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

log = Operator(
    "log",
    lambda x, b: np.log(x) / np.log(b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

sin = Operator(
    "sin",
    lambda x: np.sin(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

cos = Operator(
    "cos",
    lambda x: np.cos(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

tan = Operator(
    "tan",
    lambda x: np.tan(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

arcsin = Operator(
    "arcsin",
    lambda x: np.arcsin(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

arccos = Operator(
    "arccos",
    lambda x: np.arccos(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

arctan = Operator(
    "arctan",
    lambda x: np.arctan(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

sinh = Operator(
    "sinh",
    lambda x: np.sinh(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

cosh = Operator(
    "cosh",
    lambda x: np.cosh(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

tanh = Operator(
    "tanh",
    lambda x: np.tanh(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

arcsinh = Operator(
    "arcsinh",
    lambda x: np.arcsinh(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

arccosh = Operator(
    "arccosh",
    lambda x: np.arccosh(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

arctanh = Operator(
    "arctanh",
    lambda x: np.arctanh(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

abs = Operator(
    "abs",
    lambda x: np.abs(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

sign = Operator(
    "sign",
    lambda x: np.sign(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

floor = Operator(
    "floor",
    lambda x: np.floor(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

ceil = Operator(
    "ceil",
    lambda x: np.ceil(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

round = Operator(
    "round",
    lambda x: np.round(x),
    OpRules(
        arity=1,
        input_types=[DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

maximum = Operator(
    "maximum",
    lambda a,b: np.maximum(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

minimum = Operator(
    "minimum",
    lambda a,b: np.minimum(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.NUM
    )
)

equal = Operator(
    "equal",
    lambda a,b: np.equal(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.BOOL
    )
)

not_equal = Operator(
    "not_equal",
    lambda a,b: np.not_equal(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.BOOL
    )
)

less = Operator(
    "less",
    lambda a,b: np.less(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.BOOL
    )
)

less_equal = Operator(
    "less_equal",
    lambda a,b: np.less_equal(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.BOOL
    )
)

greater = Operator(
    "greater",
    lambda a,b: np.greater(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.BOOL
    )
)

greater_equal = Operator(
    "greater_equal",
    lambda a,b: np.greater_equal(a,b),
    OpRules(
        arity=2,
        input_types=[DataTypes.NUM, DataTypes.NUM],
        output_type=DataTypes.BOOL
    )
)


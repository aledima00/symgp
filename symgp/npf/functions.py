## this section is dedicated to implementations of the most common numpy functions
import numpy as np
from .. import Operator

# Define the operators
add = Operator(
    "add",
    arity=2,
    func=lambda a, b: np.add(a, b),
    simplify_func=lambda a, b: (mul,[a,2]) if a == b else None
)

sub = Operator(
    "sub",
    arity=2,
    func=lambda a, b: np.subtract(a, b),
    expr="np.subtract(#1,#2)",
    simplify_func=lambda a, b: (0,[]) if a == b else None
)

mul = Operator(
    "mul",
    arity=2,
    func=lambda a, b: np.multiply(a, b),
    expr="np.multiply(#1,#2)",
    simplify_func=lambda a, b: (pow,[a,2]) if a == b else None
)

div = Operator(
    "div",
    arity=2,
    func=lambda a, b: np.divide(a, b),
    expr="np.divide(#1,#2)",
    simplify_func=lambda a, b: (1,[]) if a == b else None
)

negation = Operator(
    "negation",
    arity=1,
    func=lambda x: -x,
    expr="-#1"
)

inverse = Operator(
    "inverse",
    arity=1,
    func=lambda x: 1 / x,
    expr="1/#1"
)

pow = Operator(
    "pow",
    arity=2,
    func=lambda a, b: np.power(a, b),
    expr="np.power(#1,#2)"
)

square = Operator(
    "square",
    arity=1,
    func=lambda x: np.square(x),
)

exp = Operator(
    "exp",
    arity=1,
    func=lambda x: np.exp(x)
)

sqrt = Operator(
    "sqrt",
    arity=1,
    func=lambda x: np.sqrt(x)
)

cbrt = Operator(
    "cbrt",
    arity=1,
    func=lambda x: np.cbrt(x)
)

log10 = Operator(
    "log10",
    arity=1,
    func=lambda x: np.log10(x)
)

ln = Operator(
    "ln",
    arity=1,
    func=lambda x: np.log(x),
    expr="np.log(#1)"
)

log = Operator(
    "log",
    arity=2,
    func=lambda x, b: np.log(x) / np.log(b),
    expr="np.log(#1)/np.log(#2)",
    simplify_func=lambda a,b: (1,[]) if a == b else None
)

heavyside = Operator(
    "heavyside",
    arity=1,
    func=lambda x: np.heaviside(x, 0)
)

sin = Operator(
    "sin",
    arity=1,
    func=lambda x: np.sin(x)
)

cos = Operator(
    "cos",
    arity=1,
    func=lambda x: np.cos(x)
)

tan = Operator(
    "tan",
    arity=1,
    func=lambda x: np.tan(x)
)

arcsin = Operator(
    "arcsin",
    arity=1,
    func=lambda x: np.arcsin(x)
)

arccos = Operator(
    "arccos",
    arity=1,
    func=lambda x: np.arccos(x)
)

arctan = Operator(
    "arctan",
    arity=1,
    func=lambda x: np.arctan(x)
)

sinh = Operator(
    "sinh",
    arity=1,
    func=lambda x: np.sinh(x)
)

cosh = Operator(
    "cosh",
    arity=1,
    func=lambda x: np.cosh(x)
)

tanh = Operator(
    "tanh",
    arity=1,
    func=lambda x: np.tanh(x)
)

arcsinh = Operator(
    "arcsinh",
    arity=1,
    func=lambda x: np.arcsinh(x)
)

arccosh = Operator(
    "arccosh",
    arity=1,
    func=lambda x: np.arccosh(x)
)

arctanh = Operator(
    "arctanh",
    arity=1,
    func=lambda x: np.arctanh(x)
)

abs = Operator(
    "abs",
    arity=1,
    func=lambda x: np.abs(x)
)

sign = Operator(
    "sign",
    arity=1,
    func=lambda x: np.sign(x)
)

floor = Operator(
    "floor",
    arity=1,
    func=lambda x: np.floor(x)
)

ceil = Operator(
    "ceil",
    arity=1,
    func=lambda x: np.ceil(x)
)

round = Operator(
    "round",
    arity=1,
    func=lambda x: np.round(x)
)

maximum = Operator(
    "maximum",
    arity=2,
    func=lambda a, b: np.maximum(a, b),
    simplify_func=lambda a, b: (a,[]) if a == b else None
)

minimum = Operator(
    "minimum",
    arity=2,
    func=lambda a, b: np.minimum(a, b),
    simplify_func=lambda a, b: (a,[]) if a == b else None
)
## this section is dedicated to implementations of the most common numpy functions
import numpy as np
from .. import Operator

# Define the operators
add = Operator(
    "add",
    arity=2,
    func=lambda a, b: np.add(a, b)
)

sub = Operator(
    "sub",
    arity=2,
    func=lambda a, b: np.subtract(a, b),
    expr="np.subtract(#1,#2)"
)

mul = Operator(
    "mul",
    arity=2,
    func=lambda a, b: np.multiply(a, b),
    expr="np.multiply(#1,#2)"
)

div = Operator(
    "div",
    arity=2,
    func=lambda a, b: np.divide(a, b),
    expr="np.divide(#1,#2)"
)

pow = Operator(
    "pow",
    arity=2,
    func=lambda a, b: np.power(a, b),
    expr="np.power(#1,#2)"
)

log = Operator(
    "log",
    arity=2,
    func=lambda x, b: np.log(x) / np.log(b),
    expr="np.log(#1)/np.log(#2)"
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
    func=lambda a, b: np.maximum(a, b)
)

minimum = Operator(
    "minimum",
    arity=2,
    func=lambda a, b: np.minimum(a, b)
)
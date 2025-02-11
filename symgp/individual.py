from . import Operator
from typing import List
from consoleformat import Formatted
from colorama import Fore
from typing import Dict as _DCT, List as _LS, Literal as _LIT
import numpy as np

class Node:
    operator:Operator # operator used in the node
    input_children:List['Node'] # list of children used as inputs for the operator

    def __init__(self, operator:Operator, children:List['Node']):
        self.children = children
        self.operator = operator
    def simplify(self)->"Node":
        if not isinstance(self,Leaf):
            for i,child in enumerate(self.children):
                if isinstance(child,Node) and not isinstance(child,Leaf):
                    self.children[i] = child.simplify()
            simplified = self.operator.simplified(self.children)
            if simplified is not None:
                op, chs = simplified
                if isinstance(op,Operator):
                    self.operator = op
                    self.children = chs
                else:
                    return Leaf(op)
        return self
    def evaluate(self):
        return self.operator(*[child.evaluate() for child in self.children])
    def fstr(self,fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        fstr.append(f"(")
        self.operator.fstr(fstr)
        for child in self.children:
            fstr.append(", ")
            child.fstr(fstr)
        fstr.append(")")
        return fstr
    def tree_fstr(self,depth=0, ended_levels=dict(),fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        if depth not in ended_levels:
            ended_levels[depth] = False
        if depth>0:
            for i in range(1,depth):
                fstr.append("     " if ended_levels[i] else "  │  ")
            fstr.append("  └──" if ended_levels[depth] else "  ├──")
        fstr.append(f"'{self.operator.name}'",fore=Fore.YELLOW)
        fstr.ret()
        for i,child in enumerate(self.children):
            is_last = i == len(self.children)-1
            if is_last:
                ended_levels[depth+1] = True
            else:
                for k in ended_levels.keys():
                    if k>depth:
                        ended_levels[k] = False
            child.tree_fstr(depth+1, ended_levels,fstr=fstr)
        return fstr
    
    def subnodes(self,keep_leaves:bool=True):
        sn = [child for child in self.children if (keep_leaves or not isinstance(child,Leaf))]
        for child in self.children:
            if not isinstance(child,Leaf):
                sn += child.subnodes(keep_leaves)
        return sn
    
    def expr(self,names:_DCT[str,str]|None=None):
        return self.operator.solved_expr([child.expr(names=names) for child in self.children])
    
    def depth(self):
        return 1 + max([child.depth() for child in self.children])
    
    def deepCopy(self):
        return Node(self.operator,[child.deepCopy() for child in self.children])
    
    def __str__(self):
        return str(self.fstr())
    def __repr__(self):
        return str(self)

class Leaf(Node):
    def __init__(self, value):
        # no operator nor children for a leaf
        self.operator = None
        self.children = []
        self.value = value
    def evaluate(self):
        return self.value
    def fstr(self,fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        fstr.append(f"{self.value:.03f}",fore=Fore.GREEN)
        return fstr
    def tree_fstr(self,depth=0,ended_levels=dict(),fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        if depth not in ended_levels:
            ended_levels[depth] = False
        for i in range(1,depth):
            fstr.append("     " if ended_levels[i] else "  │  ")
        fstr.append("  └──" if ended_levels[depth] else "  ├──")
        self.fstr(fstr)
        fstr.ret()
        return fstr
    def depth(self):
        return 1
    def expr(self,names=None):
        return str(self.value)
    def deepCopy(self):
        return Leaf(self.value)
    def __str__(self):
        return str(self.fstr())
    
class SpecialLeaf(Leaf):
    def __init__(self, name:_LIT["pi","e"]):
        if name not in ["pi","e"]:
            raise ValueError(f"Invalid special leaf name '{name}'")
        self.name = name
        self.value = np.pi if name == "pi" else np.e
        super().__init__(self.value)
    def fstr(self,fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        fstr.append(f"{self.name}",fore=Fore.RED)
        return fstr

    
class VarLeaf(Leaf):
    def __init__(self, name:str):
        self.name = name
        self.assigned = False
        self.value = None
        super().__init__(None) # no value
    def evaluate(self):
        if not self.assigned:
            raise ValueError(f"Leaf value is not set for leaf '{self.name}', value is {self.value}, assigned is {self.assigned}")
        return self.value
    def assign(self,value):
        self.value = value
        self.assigned = True
    def unassign(self):
        self.assigned = False
        self.value = None
    def fstr(self,fstr:Formatted=None)->Formatted:
        if fstr is None:
            fstr = Formatted()
        fstr.append(f"{self.name}",fore=Fore.CYAN)
        return fstr
    def expr(self,names:_DCT[str,str]=None):
        if names is None or self.name not in names:
            return self.name
        else:
            return names[self.name]
    def deepCopy(self):
        return VarLeaf(self.name)
    def __str__(self):
        return str(self.fstr())


class IndividualTree:
    inputLeaves:_DCT[str,_LS[VarLeaf]]
    root:Node
    
    def __init__(self, root:Node,*,simplify=False):
        self.root = root
        self.numInputs=0
        self.inputLeaves = dict()
        if simplify:
            self.root = self.root.simplify()
        self.__update_input_leaves()
        

    def update(self):
        self.root = self.root.simplify()
        self.__update_input_leaves()

    def __update_input_leaves(self):
        self.inputLeaves = dict()
        if isinstance(self.root,VarLeaf):
            self.inputLeaves[self.root.name] = [self.root]
        sn = self.root.subnodes(keep_leaves=True)
        for n in sn:
            if isinstance(n,VarLeaf):
                if n.name not in self.inputLeaves:
                    self.inputLeaves[n.name] = [n]
                else:
                    self.inputLeaves[n.name].append(n)
        self.numInputs = len(self.inputLeaves)

    def evaluate_sample(self,kv_inputs:_DCT[str,object]):
        if len(kv_inputs) != self.numInputs:
            raise ValueError("Input length does not match")
        for k,v in kv_inputs.items():
            for il in self.inputLeaves[k]:
                il.assign(v)
        return self.root.evaluate()
    def tree_fstr(self)->Formatted:
        return self.root.tree_fstr()
    def fstr(self)->Formatted:
        return self.root.fstr()
    
    def evaluate(self,inputs:np.ndarray,order:_LS[str])->np.ndarray:
        assert len(inputs.shape) == 2, "Input must be 2D, shape=(num_inputs,num_samples)"
        assert inputs.shape[0] == len(order), "Input shape does not match the order"
        for i,k in enumerate(order):
            if k in self.inputLeaves:
                for il in self.inputLeaves[k]:
                    il.assign(inputs[i])
        return self.root.evaluate()
    
    def mse(self,inputs:np.ndarray,outputs:np.ndarray,order:_LS[str]):
        out = self.evaluate(inputs,order)
        diff= out-outputs
        # replace nan values from output, using 0 if also output is nan, otherwise np.inf
        diff = np.where(np.isnan(diff),np.where(np.isnan(outputs),0,np.inf),diff)
        with np.errstate(invalid='ignore', divide='ignore', over='ignore'):
            return np.mean((diff)**2)
    
    def fitness(self,inputs:np.ndarray,outputs:np.ndarray,order:_LS[str],*,parsimony_weight:float=0,parsimony_format:_LIT["linear","bilinear"]="linear"):

        if parsimony_format == "linear":
            cost = self.mse(inputs,outputs,order) + self.depth()*parsimony_weight
        elif parsimony_format == "bilinear":
            cost = self.mse(inputs,outputs,order)*self.depth()*parsimony_weight
        else:
            raise ValueError(f"Invalid parsimony format '{parsimony_format}'")
        
        return -cost
    
    def subnodes(self,keep_leaves:bool=True,keep_root:bool=False):
        sn = self.root.subnodes(keep_leaves)
        if keep_root:
            if keep_leaves or not isinstance(self.root,Leaf):
                sn = [self.root] + sn
        return sn
    
    def getExpr(self,names:_DCT[str,str]|None=None):
        return self.root.expr(names=names)
    def depth(self):
        return self.root.depth()
    def deepCopy(self):
        return IndividualTree(self.root.deepCopy())
    
__all__ = ["Node", "Leaf", "IndividualTree","VarLeaf","SpecialLeaf"]
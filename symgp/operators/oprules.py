from typing import List as _List
from .specifications import Specs as _Specs, ShapeTypes as _ST, DataTypes as _DT
from .rules import OUTPUT_COMPUTE_RULES as _OCR, INPUT_BINARY_CHECKS as _IBC
from colorama import Fore, Back, Style
from ..format import Formatted

class OpRules:
    """
    A class to represent the constraints and the rules for an operator in the symbolic regression model.
    """

    arity:int

    __inputs_specs: _List[_Specs] # fixed specifications for inputs
    output_specs: _Specs # fixed specifications for output

    output_rules:_List[_OCR] # rules to compute output specs given input specs
    input_check_rules:_List[_IBC] # rules to check input specs additional constraints

    __actual_inputs_specs:_List[_Specs] # actual input specs (when node is connected to other nodes)


    def __init__(self, arity:int, inputs_specs:_List[_Specs]=None, output_specs:_Specs=None, output_rules:_List[_OCR]=[], input_binary_checks:_List[_IBC]=[]):
        self.arity = arity

        self.__input_specs = inputs_specs if inputs_specs is not None else [_Specs() for _ in range(arity)]
        self.output_specs = output_specs if output_specs is not None else _Specs()
        
        self.output_rules = output_rules
        self.input_binary_checks = input_binary_checks

        self.__actual_inputs_specs = None

        self.__update_output_specs()

    def getInputSpecs(self)->_List[_Specs]:
        return self.__actual_inputs_specs if self.__actual_inputs_specs is not None else self.__input_specs

    def setActualInputsSpecs(self, actual_inputs_specs:_List[_Specs])->bool:
        if self.check_actual_inputs_specs(actual_inputs_specs):
            return False
        self.__actual_inputs_specs = actual_inputs_specs
        self.__update_output_specs()
        return True
        
    def check_actual_inputs_specs(self, actual_inputs_specs:_List[_Specs])->bool:
        assert len(actual_inputs_specs) == self.arity, f"Expected {self.arity} inputs, got {len(actual_inputs_specs)}"
        for i in range(self.arity):
            if not self.__input_specs[i].check_compatibility(actual_inputs_specs[i]):
                return False
        return True
    
    def clearActualInputsSpecs(self):
        self.__actual_inputs_specs = None
        self.__update_output_specs()

    def __update_output_specs(self):
        input_specs = self.getInputSpecs()
        for rule in self.output_rules:
            if rule == _OCR.INHERIT_SHAPE_TYPE:
                self.output_specs.shape_type = input_specs[0].shape_type
            elif rule == _OCR.INHERIT_DATA_TYPE:
                self.output_specs.data_type = input_specs[0].data_type
            elif rule == _OCR.INHERIT_SHAPE:
                if input_specs[0].shape_type == _ST.NPARRAY:
                    self.output_specs.shape = input_specs[0].shape
            elif rule == _OCR.TRANSPOSE_SHAPE:
                if input_specs[0].shape_type == _ST.NPARRAY:
                    self.output_specs.shape = input_specs[0].shape[::-1]
            elif rule == _OCR.MATMUL_SHAPE:
                if input_specs[0].shape_type == _ST.NPARRAY and input_specs[1].shape_type == _ST.NPARRAY:
                    self.output_specs.shape = (input_specs[0].shape[0], input_specs[1].shape[1])
            else:
                raise ValueError(f"Invalid output rule {rule}")
            
    def check_inputs_specs(self):
        input_specs = self.getInputSpecs()
        for rule in self.input_binary_checks:
            if rule == _IBC.SAME_SHAPE_TYPE:
                if input_specs[0].shape_type != input_specs[1].shape_type:
                    return False
            elif rule == _IBC.SAME_DATA_TYPE:
                if input_specs[0].data_type != input_specs[1].data_type:
                    return False
            elif rule == _IBC.SAME_SHAPE:
                if input_specs[0].shape_type == _ST.NPARRAY and input_specs[1].shape_type == _ST.NPARRAY:
                    if input_specs[0].shape != input_specs[1].shape:
                        return False
            elif rule == _IBC.TRANSPOSED_SHAPE:
                if input_specs[0].shape_type == _ST.NPARRAY and input_specs[1].shape_type == _ST.NPARRAY:
                    if input_specs[0].shape != input_specs[1].shape[::-1]:
                        return False
            else:
                raise ValueError(f"Invalid input check rule {rule}")
        return True
    
    def fstr(self):
        ibc_names = str([item.name for item in self.input_binary_checks])
        ocr_names = str([item.name for item in self.output_rules])

        fstr = Formatted()

        is_is_actual = self.__actual_inputs_specs is not None
        input_specs = self.__actual_inputs_specs if is_is_actual else self.__input_specs

        fstr.style(Style.DIM).fore(Fore.WHITE).append("OPERATOR_RULES(").ret().indent()
        fstr.fore(Fore.GREEN).append(f"ARITY:\t\t\t").fore(Fore.CYAN).append(f"{self.arity}").ret()
        fstr.fore(Fore.GREEN).append(f"INPUTS_SPECS").fore(Fore.YELLOW).append(f"[{"ACTUAL" if is_is_actual else "BASE"}]:\t").fore(Fore.CYAN).append("[").ret().indent()
        
        
        for i in range(self.arity):
            fstr.concatenate(input_specs[i].fstr())
            if i != self.arity-1:
                fstr.fore(Fore.CYAN).append(",")
            fstr.ret()
        fstr.unindent().append(f"{Fore.CYAN}]").ret()
        
        fstr.fore(Fore.GREEN).append(f"OUTPUT_SPECS:\t\t").fore(Fore.CYAN).concatenate(self.output_specs.fstr()).fore(Fore.GREEN).ret()
        fstr.append(f"OUTPUT_RULES:\t\t").fore(Fore.CYAN).append(ocr_names).fore(Fore.GREEN).ret()
        fstr.append(f"INPUT_BINARY_CHECKS:\t").fore(Fore.CYAN).append(ibc_names).fore(Fore.GREEN).ret()
        fstr.unindent().fore(Fore.WHITE).append(")").ret()
        return fstr
    def __str__(self):
        return str(self.fstr())
    def __repr__(self):
        return str(self)

__all__ = ["OpRules"]
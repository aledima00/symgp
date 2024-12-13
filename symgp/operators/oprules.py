from typing import List as _List
from .specifications import Specs as _Specs, ShapeTypes as _ST, DataTypes as _DT
from .rules import OUTPUT_COMPUTE_RULES as _OCR, INPUT_BINARY_CHECKS as _IBC
from icecream import ic

class OpRules:
    """
    A class to represent the constraints and the rules for an operator in the symbolic regression model.
    """

    arity:int

    inputs_specs: _List[_Specs] # FIXED SPECIFICATIONS FOR INPUTS
    output_specs: _Specs # FIXED SPECIFICATIONS FOR OUTPUT

    output_rules:_List[_OCR] # RULES TO COMPUTE OUTPUT SPECS GIVEN INPUT SPECS
    input_check_rules:_List[_IBC] # RULES TO CHECK INPUT SPECS ADDITIONAL CONSTRAINTS


    def __init__(self, arity:int, inputs_specs:_List[_Specs]=None, output_specs:_Specs=None, output_rules:_List[_OCR]=[], input_binary_checks:_List[_IBC]=[]):
        self.arity = arity

        self.inputs_specs = inputs_specs if inputs_specs is not None else [_Specs() for _ in range(arity)]
        self.output_specs = output_specs if output_specs is not None else _Specs()
        
        self.output_rules = output_rules
        self.input_binary_checks = input_binary_checks
        self.__update_output_specs()

    def __update_output_specs(self):
        for rule in self.output_rules:
            if rule == _OCR.INHERIT_SHAPE_TYPE:
                self.output_specs.shape_type = self.inputs_specs[0].shape_type
            elif rule == _OCR.INHERIT_DATA_TYPE:
                self.output_specs.data_type = self.inputs_specs[0].data_type
            elif rule == _OCR.INHERIT_SHAPE:
                if self.inputs_specs[0].shape_type == _ST.NPARRAY:
                    self.output_specs.shape = self.inputs_specs[0].shape
            elif rule == _OCR.TRANSPOSE_SHAPE:
                if self.inputs_specs[0].shape_type == _ST.NPARRAY:
                    self.output_specs.shape = self.inputs_specs[0].shape[::-1]
            elif rule == _OCR.MATMUL_SHAPE:
                if self.inputs_specs[0].shape_type == _ST.NPARRAY and self.inputs_specs[1].shape_type == _ST.NPARRAY:
                    self.output_specs.shape = (self.inputs_specs[0].shape[0], self.inputs_specs[1].shape[1])
            else:
                raise ValueError(f"Invalid output rule {rule}")
            
    def check_inputs_specs(self):
        for rule in self.input_binary_checks:
            if rule.value == _IBC.SAME_SHAPE_TYPE:
                if self.inputs_specs[0].shape_type != self.inputs_specs[1].shape_type:
                    return False
            elif rule.value == _IBC.SAME_DATA_TYPE:
                if self.inputs_specs[0].data_type != self.inputs_specs[1].data_type:
                    return False
            elif rule.value == _IBC.SAME_SHAPE:
                if self.inputs_specs[0].shape_type == _ST.NPARRAY and self.inputs_specs[1].shape_type == _ST.NPARRAY:
                    if self.inputs_specs[0].shape != self.inputs_specs[1].shape:
                        return False
            elif rule.value == _IBC.TRANSPOSED_SHAPE:
                if self.inputs_specs[0].shape_type == _ST.NPARRAY and self.inputs_specs[1].shape_type == _ST.NPARRAY:
                    if self.inputs_specs[0].shape != self.inputs_specs[1].shape[::-1]:
                        return False
            else:
                raise ValueError("Invalid input check rule")
        return True
            
    def modify_inputs_specs(self, specs:_List[_Specs]):
        self.inputs_specs = specs
        self.__update_output_specs()

__all__ = ["OpRules"]
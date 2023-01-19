# Copyright 2023 Unai Lería Fortea & Pablo Vizcaíno García

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...function_constructor import FunctionBuilder
    
from .generic_fitter import GenericFitter


class FunctionContainer:
    operations = {
        "+" : lambda f,g: f + g,
        "-" : lambda f,g: f - g,
        "*" : lambda f,g: f * g,
        "/" : lambda f,g: f / g,
        "//" : lambda f,g: f // g,
        "%" : lambda f,g: f % g,
        "**" : lambda f,g: f ** g
    }
    
    def __init__(self, left_fitter: GenericFitter, function_builder: FunctionBuilder):
        self.function_builder = function_builder
        self.left_fitter = left_fitter
        self.left_fitter_args_legth: int = 0
        self.right_fitter : FunctionContainer | None = None
        self.right_fitter_args_legth: int = 0
        self.operation : str
        
    def copy(self):
        return FunctionContainer(self.left_fitter, self.function_builder)
        
    def _set_right_fitter_(self, right_fitter: GenericFitter|FunctionContainer):
        if self == right_fitter:
            self.right_fitter = self.copy()
        elif isinstance(right_fitter, GenericFitter):
            self.right_fitter = FunctionContainer(right_fitter, self.function_builder)
        elif isinstance(right_fitter, FunctionContainer):
            self.right_fitter = right_fitter
            self.right_fitter.set_function_builder(self.function_builder)
        
    def __add__(self, right_fitter: GenericFitter|FunctionContainer):
        self._set_right_fitter_(right_fitter)
        self.operation = '+'
        return self
    def __sub__(self, right_fitter: GenericFitter|FunctionContainer):
        self._set_right_fitter_(right_fitter)
        self.operation = '-'
        return self
    def __mul__(self, right_fitter: GenericFitter|FunctionContainer):
        self._set_right_fitter_(right_fitter)
        self.operation = '*'
        return self
    def __truediv__(self, right_fitter: GenericFitter|FunctionContainer):
        self._set_right_fitter_(right_fitter)
        self.operation = '/'
        return self
    def __floordiv__(self, right_fitter: GenericFitter|FunctionContainer):
        self._set_right_fitter_(right_fitter)
        self.operation = '//'
        return self
    def __mod__(self, right_fitter: GenericFitter|FunctionContainer):
        self._set_right_fitter_(right_fitter)
        self.operation = '%'
        return self
    def __pow__(self, right_fitter: GenericFitter|FunctionContainer):
        self._set_right_fitter_(right_fitter)
        self.operation = '**'
        return self
        
    def function(self, x,*args):
        if self.right_fitter is not None:
            return self.operations[self.operation](
                self.left_fitter.function(x, *args[:self.left_fitter_args_legth]),
                self.right_fitter.function(x, *args[self.left_fitter_args_legth:])
            )
        else:
            return self.left_fitter.function(x, *args[:self.left_fitter_args_legth])

    def get_args(self):
        if self.right_fitter is not None:
            return (*self.left_fitter.get_args(),*self.right_fitter.get_args())
        return self.left_fitter.get_args()
    
    def get_args_length(self):
        return self.left_fitter.get_args_length() + \
            (self.right_fitter.get_args_length() if self.right_fitter is not None else 0)

    def build(self):
        return self.function_builder.build()
    
    def set_function_builder(self, function_builder: FunctionBuilder):
        self.function_builder = function_builder
        if self.right_fitter is not None:  
            self.right_fitter.set_function_builder(function_builder)
    
    def _build_(self, plot_update_function: function):
        self.left_fitter = self.left_fitter(self.function_builder.app, self.function_builder.data)
        self.left_fitter_args_legth =  self.left_fitter.get_args_length()
        
        for dp in self.left_fitter.drag_points_managers:
            self.left_fitter.drag_points_cids.append(
                dp.connect(plot_update_function)
            )
            
        if self.right_fitter is not None:
            self.right_fitter._build_(plot_update_function)
            self.right_fitter_args_legth = self.right_fitter.get_args_length()
    
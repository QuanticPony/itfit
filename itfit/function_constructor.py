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
    from . import Fitter
    from .data import DataSelection
    
from matplotlib.lines import Line2D
import numpy as np

from .fit_functions import GenericFitter
from .fit_functions.common import (GenericFitter, GenericFitterTool, FunctionContainer)


class FunctionBuilder:
    def __init__(self, app: Fitter):
        self.app = app
        self.data = self.app.data
        self.function_container: FunctionContainer
        
    def define(self, function: FunctionContainer):
        self.function_container = function
        self.function_container.set_function_builder(self)
        
    def get_args(self):
        return self.function_container.get_args()
        
    def get_args_length(self):
        return self.function_container.get_args_length()

        
    def build(self):
        self.function_container._build_(self.update)
        
        self.function = self.function_container.function
        self.args_length = self.function_container.get_args_length()
        
        if not hasattr(self, "fitter_instance"):
            self.fitter_instance = GenericFitter(app=self.app, data=self.data)
            self.fitter_instance.function_container = self
            self.fitter_instance.function = self.function_container.function
            self.fitter_instance.get_args_length = self.get_args_length
            self.fitter_instance.get_args = self.get_args
        
            self.poly = Line2D(
                self.data.get_data()[:,0],
                self.data.get_data()[:,1],
                linestyle='--',
                color='black',
                transform=None
            )
            self.patch = self.app.ax.add_patch(self.poly)
            
            self.app.blit_manager.artists.append(self)
        
        return self
        
    def update(self, *_):
        args = self.function_container.get_args()
        _x_data = self.data.get_selected()[0]
        _length = min(len(_x_data)*3, 250)
        x = np.linspace(min(_x_data), max(_x_data), _length)
        y = self.function(x, *args)
        
        xy = np.array((x,y)).T.reshape(-1,2)
        x_data, y_data = self.app.ax.transData.transform(xy).T

        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)
        
        
    def get_custom_tool(self):
        return self.CustomTool(self)
        
    class CustomTool(GenericFitterTool):
        """Toggles a custom tool Tool."""

        # default_keymap = ''
        description = 'Custom tool'
        
        def __init__(self, function_builder: FunctionBuilder):
            self.function_builder = function_builder
            
        def __call__(self, *args, app: Fitter, data: DataSelection, **kwargs):
            super().__init__(*args, app=app, data=data, **kwargs)
            return self

        def enable(self,*args):
            """Triggered when CustomTool is enabled,
            Uses BlitManager for faster rendering of DragObjects.
            """

            super().enable()
            self.fitter = self.function_builder.build().fitter_instance

        def disable(self,*args):
            """Triggered when CustomTool is disabled.
            Removes DragObjects and disables BlitManager.
            """

            super().disable()
        
        @classmethod 
        # This seems to be needed when using python 3.10
        def __subclasses__(cls):
            return []


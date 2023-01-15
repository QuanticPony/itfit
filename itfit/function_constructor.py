from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from . import Fitter
    from .data import DataSelection
    
from matplotlib.lines import Line2D
import numpy as np

from .fit_functions import GenericFitter
from .fit_functions.generic_fitter import GenericFitterTool    

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
        
    def _set_right_fitter_(self, right_fitter: GenericFitter):
        self.right_fitter = FunctionContainer(right_fitter, self.function_builder)
        
    def __add__(self, right_fitter: GenericFitter):
        self._set_right_fitter_(right_fitter)
        self.operation = '+'
        return self.right_fitter
    def __sub__(self, right_fitter: GenericFitter):
        self._set_right_fitter_(right_fitter)
        self.operation = '-'
        return self.right_fitter
    def __mul__(self, right_fitter: GenericFitter):
        self._set_right_fitter_(right_fitter)
        self.operation = '*'
        return self.right_fitter
    def __truediv__(self, right_fitter: GenericFitter):
        self._set_right_fitter_(right_fitter)
        self.operation = '/'
        return self.right_fitter
    def __floordiv__(self, right_fitter: GenericFitter):
        self._set_right_fitter_(right_fitter)
        self.operation = '//'
        return self.right_fitter
    def __mod__(self, right_fitter: GenericFitter):
        self._set_right_fitter_(right_fitter)
        self.operation = '%'
        return self.right_fitter
    def __pow__(self, right_fitter: GenericFitter):
        self._set_right_fitter_(right_fitter)
        self.operation = '**'
        return self.right_fitter
        
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
    
    
class FunctionBuilder:
    def __init__(self, app: Fitter, data: DataSelection):
        self.app = app
        self.data = data
        self.function_container: FunctionContainer
        
        self.poly = Line2D(
            self.data.get_data()[:,0],
            self.data.get_data()[:,1],
            linestyle='--',
            color='black',
            transform=None
        )
        self.patch = self.app.ax.add_patch(self.poly)
        
        self.app.blit_manager.artists.append(self)
        
    def start(self, left_fitter: GenericFitter):
        self.function_container = FunctionContainer(left_fitter, self)
        return self.function_container
        
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
        
        # self.manager_instance = 
        
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
        default_toggled = False 
        radio_group = "fitter"
        
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

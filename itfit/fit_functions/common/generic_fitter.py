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
    from ... import Fitter

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_tools import ToolToggleBase
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
from scipy import optimize
from matplotlib.patches import Polygon

from ...data import DataSelection, DataContainer
from ...utils import DragPointCollection, FitResultContainer

class GenericFitter:
    """GenericFitter is a base implementation of a fit function.
    All fit functions must inherit GenericFitter."""
    
    name = "generic"

    @staticmethod
    def function(x: float,*args):
        """Fit function: `f(x,*args)=...`.

        Parameters:
            x (float):
                Independent variable.
            *args (list[float,...]):
                0, 1 or multiple arguments.
        Returns:
            (float):
                `f(x, *args)`
        """
        return 0.
    
    @staticmethod
    def get_function_string():
        """Returns a string representing the function in LaTeX style
        """
        ...
    
    @staticmethod
    def gradient(x: float,*args):
        """Fit gradient: 'f(x,*args)=...'.

        Paremeters:
            x (float):
                Independent variable.
            *args (list[float,...]):
                0, 1 or multiple arguments.
        Returns:
            (float):
                'f(x,*args)'
        """
        return 0.
        
    def get_args_length(self):
        """Gets number of arguments of `function`.

        Returns:
            (int): Number of arguments of `function`.
        """
        return self.fitter_drag_collection.get_args_length()
    
    def __init__(self, app: Fitter, data: DataSelection):
        """Generic fitter constructor.

        Parameters:
            app (Fitter):
                Main application.
            data (DataSelection):
                Data to fit.
        """
        self.app = app
        self.fig = app.figure
        self.ax = app.ax
        self.data = data
        
        self.fitter_drag_collection: DragPointCollection
        
    def get_args(self):
        """Return arguments needed for `self.function`.

        Returns:
            (Tuple[float]):
                0, 1 or multiple arguments.
        """
        return self.fitter_drag_collection.get_args()

    def prop_errors(xdata,self):
        """Returns the error of the fit, given a gradient.

        Returns:
            (float):
                sigma
        """
        return np.sqrt( float( self.gradient(xdata,*self.fit[0]).T @ self.fit[1] @ self.gradient(xdata,*self.fit[0]) ))
        
    
    def on_fit(self, event):
        """Event for fit button.

        Parameters:
            event (Matplotlib event): 
                Not used
        """

        # If there is not data selected use all data
        xdata, ydata = self.data.get_selected()
        xerr, yerr = self.data.get_selected_errors()
        if np.sum(self.data.indexes_used)==0:
            xdata, ydata = self.data.xdata.copy(), self.data.ydata.copy()
        
        self.fit = optimize.curve_fit(self.function, xdata, ydata, p0=self.get_args(), full_output=True, sigma=yerr)
        fit_result = FitResultContainer(self.data.copy(), self, self.fit)
        
        # Plot fit line in background, and the confidence interval
        with self.app.blit_manager.disabled():
            self.fit_line = Line2D(xdata, fit_result.evaluate(xdata), linestyle='--', color='purple')
            
            verts_positive, verts_negative = fit_result.error_verts()
            if verts_positive and verts_negative:
                self.fit_fill = Polygon(verts_positive + list(reversed(verts_negative)),facecolor='red',edgecolor='None',alpha=0.3)
                self.ax.add_artist(self.fit_fill)
                self.ax.draw_artist(self.fit_fill)

            self.ax.add_artist(self.fit_line)
            self.ax.draw_artist(self.fit_line)
            
       
       # Redraw plot to show line     
        self.app.blit_manager.draw()

        # Save fit in app
        self.app._add_fit(fit_result)
       
    @classmethod    
    def copy(cls):
        """Returns a copy of this object
        """
        class inner(cls):
            def __init__(self, *args):
                super().__init__(*args)
        return inner
        
    def delete(self):
        """Remove trigger. Used when tool is disabled."""
        try:
            # Remove artists in order to clean canvas
            for pm in self.drag_points_managers:
                pm.dragpoint.remove()
                self.app.blit_manager.artists.remove(pm)

            self.fitter_drag_collection.remove()
            self.app.blit_manager.artists.remove(self.fitter_drag_collection) 
        
        except AttributeError:
            pass

        
        

class GenericFitterTool(ToolToggleBase):
    """Toggles Generic Fitter Tool."""
    
    default_toggled = False 
    radio_group = "fitter"
    fitter: GenericFitter

    def __init__(self, *args, app: Fitter, data: DataSelection, **kwargs):
        """Creates a GenericFitterTool.

        Parameters:
            app (Fitter):
                Main application.
            data (DataSelection):
                Data selected.
        """
        self.app = app
        self.data = data
        super().__init__(*args, **kwargs)

    def enable(self, *args):
        """Triggered when GenericTool is enabled.
        Uses BlitManager for faster rendering of DragObjects.
        """
        self.app.blit_manager.enable()
        self.instance = self.fitter(self.app, self.data)
        
        self.button_axes =self.figure.add_axes((0.81, 0.000001, 0.1, 0.055))
        self.button = Button(self.button_axes, "Fit",color="red")
        self.button.on_clicked(self.instance.on_fit)

    def disable(self, *args):
        """Triggered when GenericTool is disabled.
        Removes DragObjects and disables BlitManager.
        """
        self.instance.delete()
        del self.instance
        
        self.app.blit_manager.disable()
        self.app.figure.canvas.draw_idle()
        del self.button
        
        self.figure.delaxes(self.button_axes)
        
        self._toggled = False # To avoid recursive disable in tool removal
        self.toolmanager.remove_tool(self.name)
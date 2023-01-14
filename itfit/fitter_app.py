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
    from . import data, utils
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    

import matplotlib.pyplot as plt

from .data import DataSelection
from .data_selectors import LassoTool
from .fit_functions import LineTool, QuadraticTool, ExponentialTool, GaussianTool, LorentzianTool
from .utils import BlitManager
from .utils.fit_container import FitResultContainer
from .plot.builder import PlotBuilder

plt.rcParams['toolbar'] = 'toolmanager'

class Fitter:
    data : data.DataSelection
    figure : Figure
    ax : Axes
    fits : dict[int, utils.FitResultContainer]
    selections : dict
    blit_manager : utils.BlitManager
    
    _last_fit : int
    def __init__(self, xdata, ydata, *args, **kargs):
        self.data = DataSelection(xdata, ydata)
        self.figure = plt.figure()
        self.ax = self.figure.gca()
        self.fits: dict[int, FitResultContainer] = {}
        self.selections = {}
        self.blit_manager = BlitManager(self)
        self._last_fit = None
        
    
    def __call__(self):
        self.data_line = self.ax.plot(self.data.xdata, self.data.ydata)
        
        self.figure.canvas.manager.toolmanager.add_tool('Lasso', LassoTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Lasso', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Line', LineTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Line', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Quadratic', QuadraticTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Quadratic', 'fitter')

        self.figure.canvas.manager.toolmanager.add_tool('Exponential', ExponentialTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Exponential', 'fitter')

        self.figure.canvas.manager.toolmanager.add_tool('Gaussian', GaussianTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Gaussian', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Lorentzian', LorentzianTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Lorentzian', 'fitter')

    def _add_fit(self, fit: FitResultContainer):
        """Adds the fit to the application

        Parameters:
            fit (FitResultContainer):
                Fit to add
        """
        self._last_fit = hash(fit)
        self.fits.update({self._last_fit: fit})
        
    def get_last_fit(self):
        """Returns the last fit

        Returns:
            (FitResultContainer): Fit result container.
        """
        return self.fits.get(self._last_fit) if (self._last_fit is not None) else None
    
    
    def get_plot_builder(self):
        """Returns a itfit.plot.PlotBuilder instance. Used to ease plot creation.
        """
        
        fit = self.get_last_fit()
        return PlotBuilder(self, fit)
    
    def default_plot_last_fit(self, xlabel: str, ylabel: str, title: str):
        """Plots last fit with default configuration:
        ```py
        .plot_data(label="Data")\
        .with_fit(label=fit.fit_manager.name.capitalize())\
        .xlabel(xlabel).ylabel(ylabel).title(title)\
            
        .spines()\
            .start_top_spine().invisible().end_top_spine()\
            .start_right_spine().invisible().end_right_spine()\
        .end_spines()\
            
        .grid().legend().tight_layout()
        ```

        Args:
            xlabel (str): x label.
            ylabel (str): y label.
            title (str): title.

        Returns:
            (itfit.plot.PlotBuilder): PlotBuilder to continue plot customization.
        """
        fit = self.get_last_fit()
        return PlotBuilder(self, fit)\
            .plot_data(label="Data")\
            .with_fit(label=fit.fit_manager.name.capitalize())\
            .xlabel(xlabel).ylabel(ylabel).title(title)\
            .spines()\
                .start_top_spine().invisible().end_top_spine()\
                .start_right_spine().invisible().end_right_spine()\
            .end_spines()\
            .grid().legend().tight_layout()

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
    from .function_constructor import FunctionBuilder
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    

import matplotlib.pyplot as plt

from .data import DataSelection
from .data_selectors import LassoTool
from . import fit_functions
from .utils import BlitManager, FitSelector
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
    
    def __init__(self, xdata, ydata, yerr=None, xerr=None, *args, **kargs):
        self.data = DataSelection(xdata, ydata, yerr=yerr, xerr=xerr)
        self.figure = plt.figure()
        self.ax = self.figure.gca()
        self.fits: dict[int, FitResultContainer] = {}
        self.selections = {}
        self.blit_manager = BlitManager(self)
        self._last_fit: int|None = None
        self._data_was_plotted = False
    
    def __call__(self):
        if not self._data_was_plotted:
            self.data_line = self.ax.plot(self.data.xdata, self.data.ydata, '.-')
            self._data_was_plotted = True
        
        self.figure.canvas.manager.toolmanager.add_tool('Lasso', LassoTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Lasso', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Line', fit_functions.linear.LineTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Line', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Quadratic', fit_functions.quadratic.QuadraticTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Quadratic', 'fitter')

        self.figure.canvas.manager.toolmanager.add_tool('Exponential', fit_functions.exponential.ExponentialTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Exponential', 'fitter')

        self.figure.canvas.manager.toolmanager.add_tool('Gaussian', fit_functions.gaussian.GaussianTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Gaussian', 'fitter')

        self.figure.canvas.manager.toolmanager.add_tool('Sine',  fit_functions.sine.SineTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Sine', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Cosine',  fit_functions.cosine.CosineTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Cosine', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Lorentzian', fit_functions.lorentzian.LorentzianTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Lorentzian', 'fitter')
        
    def add_custom_fit_function(self, function_builder: FunctionBuilder):
        if not self._data_was_plotted:
            self.data_line = self.ax.plot(self.data.xdata, self.data.ydata)
            self._data_was_plotted = True
        
        self.figure.canvas.manager.toolmanager.add_tool('Custom tool', function_builder.get_custom_tool(), app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Custom tool', 'fitter')

    def _add_fit(self, fit: FitResultContainer):
        """Adds the fit to the application

        Parameters:
            fit (FitResultContainer):
                Fit to add
        """
        self._last_fit = hash(fit)
        self.fits.update({self._last_fit: fit})

    def get_single_fit_selector(self):
        """Stars a fit selector figure where you can select one fit.

        Returns:
            (itfit.utils.FitResultContainer): Fit result container of selected fit.
        """
        selector = FitSelector(self)
        selection = selector.connect_select_one().get_selected()
        return self.fits.get(selection)

    def get_fit_selector(self):
        """Stars a fit selector figure where you can select one or more fits.

        Returns:
            (itfit.utils.FitResultContainer, list[itfit.utils.FitResultContainer]): Fit result container of selected fits, list if multiple.
        """
        selector = FitSelector(self)
        selection = selector.connect_select_multiple().get_selected()
        if isinstance(selection, list):
            return [self.fits.get(k) for k in selection]
        return self.fits.get(selection)
        
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
        .with_errors()\
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
        if fit is None:
            raise Exception("At least one fit must me made before trying to plot a fit.")
        return PlotBuilder(self, fit)\
            .plot_data(label="Data")\
            .with_errors()\
            .with_fit(label=fit.fit_manager.name.capitalize())\
            .xlabel(xlabel).ylabel(ylabel).title(title)\
            .spines()\
                .start_top_spine().invisible().end_top_spine()\
                .start_right_spine().invisible().end_right_spine()\
            .end_spines()\
            .grid().legend().tight_layout()

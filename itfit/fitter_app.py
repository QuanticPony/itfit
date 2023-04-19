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
from matplotlib.backend_tools import ToolBase
if TYPE_CHECKING:
    from . import data, utils
    from .function_constructor import FunctionBuilder
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from types import ModuleType

from .data import DataSelection
from .data_selectors import LassoTool
from . import fit_functions
from .utils import BlitManager, FitSelector
from .utils.fit_container import FitResultContainer
from .plot.builder import PlotBuilder

plt.rcParams['toolbar'] = 'toolmanager'

class Fitter:
    def __init__(self, xdata, ydata, yerr=None, xerr=None, *args, **kargs):
        self.data : data.DataSelection = DataSelection(xdata, ydata, yerr=yerr, xerr=xerr)
        self.figure : Figure = plt.figure()
        self.ax : Axes = self.figure.gca()
        self.fits: dict[int, FitResultContainer] = {}
        self.selections : dict  = {}
        self.blit_manager : BlitManager = BlitManager(self)
        self._last_fit: int|None = None
        self._data_was_plotted : bool = False
    
    def __call__(self):
        if not self._data_was_plotted:
            self.data_line = self.ax.plot(self.data.xdata, self.data.ydata, '.-')
            self._data_was_plotted = True
            
        self.figure.canvas.manager.toolmanager.add_tool('Lasso', LassoTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Lasso', 'fitter')

        self.figure.canvas.manager.toolmanager.add_tool('Fit functions', self.FitterSelectorTool, app=self)
        self.figure.canvas.manager.toolbar.add_tool('Fit functions', 'fitter')
        
        self.figure.show()
        self.figure.canvas.start_event_loop()
        
    class FitterSelectorTool(ToolBase):
        """Toggles Generic Fitter Tool."""
    
        default_toggled = False 
        radio_group = "fitter"

        def __init__(self, *args, app: Fitter, **kwargs):
            """Creates a FitterSelectorTool.

            Parameters:
                app (Fitter):
                    Main application.
            """
            self.app = app
            super().__init__(*args, **kwargs)
            
            self.name_to_fitter_tool: dict[str, fit_functions.GenericFitterTool] = {}
            
            for objt_name, objt in fit_functions.__dict__.items():
                if objt_name.startswith("__") or objt_name == "common":
                    continue
                if isinstance(objt, ModuleType):
                    for name, tool in objt.__dict__.items():  
                        try:
                            if issubclass(tool, fit_functions.GenericFitterTool):
                                self.name_to_fitter_tool.update({objt_name.capitalize(): tool})
                        except Exception as e:
                            pass

        def trigger(self, *args):
            """Triggered when GenericTool is enabled.
            Uses BlitManager for faster rendering of DragObjects.
            """
            self.fit_selector_figure = plt.figure(figsize=((7,4)))
            rect1 = 0.1, 0.1, 0.7, 0.8 
            rect2 = 0.8, 0.1, 0.1, 0.8 
            self.ax_list = self.fit_selector_figure.add_axes(rect1, frameon=False)
            self.ax_scrollbar = self.fit_selector_figure.add_axes(rect2, frameon=False)
            
            self.ax_list.set_xticks([])
            self.ax_list.set_yticks([])
            self.ax_scrollbar.set_xticks([])
            self.ax_scrollbar.set_yticks([])
            
            class inner:
                def __init__(self, fitter_selector_tool: Fitter.FitterSelectorTool, artists, inner_name, inner_tool):
                    self.fitter_selector_tool = fitter_selector_tool
                    self.app = self.fitter_selector_tool.app
                    self.manager = self.app.figure.canvas.manager
                    self.artists = artists
                    self.data = self.app.data
                    self.inner_name = inner_name
                    self.inner_tool = inner_tool
                
                def __call__(self, event):
                    if event.artist in self.artists:
                        self.manager.toolmanager.add_tool(self.inner_name.capitalize(),
                            self.inner_tool, app=self.app, data=self.app.data)
                        self.manager.toolbar.add_tool(self.inner_name.capitalize(), "fitter_functions_group")
                        self.manager.toolbar.trigger_tool(self.inner_name.capitalize())
                        
            N = len(self.name_to_fitter_tool)
            for i, (name, tool) in enumerate(self.name_to_fitter_tool.items()):
                t1_ = self.ax_list.text(0, N-i, name, picker=True)
                t2_ = self.ax_list.text(0.3, N-i, f"${tool.fitter.get_function_string()}$", fontdict={"size":15}, picker=True)
                func = inner(self, (t1_, t2_), name, tool)
                self.fit_selector_figure.canvas.mpl_connect("pick_event", func)

                
                
            slider = Slider(self.ax_scrollbar, 'Scroll bar', 4, N, valinit=N, valstep=1, orientation='vertical')
            slider.on_changed(self.update)
            self.update(N)
            
            self.fit_selector_figure.show()
            self.fit_selector_figure.canvas.start_event_loop()
            

            
        def update(self, pos):
            self.ax_list.set_ylim(pos-4, pos+0.5)
        
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
    
    def add_filter(self, filter: function):
        """Adds a filter for data selection. The signature must be as:
        ```py
        lambda x,y : bool
        ```
        or
        ```py
        def foo(x,y) -> bool:
            return bool
        ```
        Parameters:
            filter (function): Filter function.
        """
        selection = filter(*(self.data.get_data().T))
        self.data.selection(selection)
        self.data.create_selected_poly(self.ax)
    
    
    def get_plot_builder(self):
        """Returns a itfit.plot.PlotBuilder instance. Used to ease plot creation.
        """
        
        return PlotBuilder(self)
    
    def default_plot_last_fit(self, xlabel: str="", ylabel: str="", title: str=""):
        """Plots last fit with default configuration:
        ```py
        .plot_data(label="Data")\\
        .with_errors()\\
        .with_fit(label=fit.fit_manager.name.capitalize())\\
        .xlabel(xlabel).ylabel(ylabel).title(title)\\       
        .spines()\\
            .start_top_spine().invisible().end_top_spine()\\
            .start_right_spine().invisible().end_right_spine()\\
        .end_spines()\\     
        .grid().legend().tight_layout()
        ```

        Parameters:
            xlabel (str): x label. Defaults to "".
            ylabel (str): y label. Defaults to "".
            title (str): title. Defaults to "".
            
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

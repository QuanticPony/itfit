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

"""


"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fitter_app import Fitter
    from ..utils import FitResultContainer 
    
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib import rcParams
from matplotlib import style as mpl_style
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon

from .labels import LabelBuilder
from .spines import SpineBuilder
from ..utils.fit_selector import FitSelector

class PlotBuilder:
    """PlotBuilder is a class whose intent is to uase the user in plot customization. 
    Using PlotBuilder with jupyther/notebook is strongly recomended as changes are interactive and figures are preserved.
    ![image](example1.PNG)
    """


    def __init__(self, app: Fitter, **kargs):
        """_summary_

        Parameters:
            app (itfit.Fitter): Main application.
        """
        self.fig: Figure
        self.ax: Axes
        self.fit: FitResultContainer
        self.app: Fitter = app
        self._only_selected_cache_: bool

    def plot_fit(self, fmt='--', color='black', label='', only_selected_data:bool=False, **kargs):
        """Plots the fit line into the figure.

        Parameters:
            fmt (str, optional): Fit line format. Defaults to '--'.
            color (str, optional): Color for the line. Defaults to 'black'.
            label (str, optional): Label assigned to the artists. Defaults to ''.
            only_selected_data (bool, optional): If `True` the fit is only shown for data used in optimization. Defaults to `False`.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self._start_()

        if len(self.app.fits.keys()) > 1:
            key: int = FitSelector(self.app).connect_select_one().get_selected()
            self.fit = self.app.fits.get(key)
        else:
            self.fit = self.app.get_last_fit()
        
        if only_selected_data:
            DATA = self.fit.get_fit_data_selected().T
        else:
            DATA = self.fit.get_fit_data().T
            
        self.ax.plot(*DATA, fmt, color=color, label=label, **kargs)
        return self

    def with_fit(self, fmt='--', color='black', label='', only_selected:bool = False, **kargs):
        """Same as itfit.plot.builder.PlotBuilder.plot_fit. Plots the fit line into the figure.

        Parameters:
            fmt (str, optional): Fit line format. Defaults to '--'.
            color (str, optional): Color for the line. Defaults to 'black'.
            label (str, optional): Label assigned to the artists. Defaults to ''.
            only_selected (bool, optional): Shows fit only on selected data range. Defaults to `False`.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.plot_fit(fmt=fmt, color=color, label=label, **kargs)
    
    def plot_fit_errors(self, color: str|tuple[float]|None = None, edgecolor = 'None', alpha: float = 0.3, only_selected:str|bool = 'auto', **kargs):
        """Plots error shadow on fit. Must be called after fit has been plotted.

        Parameters:
            color (str | tuple[float] | None, optional): Fill color. Defaults to None.
            edgecolor (str, optional): Color of the error shadow edges. Defaults to 'None'.
            alpha (float, optional): Alpha value. Defaults to 0.3.
            only_selected (str | bool, optional): If False error will be shown for all data range. Defaults to 'auto'.

        Raises:
            Exception: If used prior to fit plotting.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        try:
         _only_selected_ = only_selected if only_selected == 'auto' else self._only_selected_cache_
        except AttributeError:
            raise Exception("Fit must be plotted prior to fit's error shadow.")
        
        verts_positive, verts_negative = self.fit.error_verts(only_selected=_only_selected_)
        
        self.fit_fill = Polygon(verts_positive + list(reversed(verts_negative)),facecolor=color, edgecolor=edgecolor, alpha=alpha, **kargs)
        self.ax.add_artist(self.fit_fill)
        self.ax.draw_artist(self.fit_fill)
        return self

    def plot_data(self, fmt='.', color=None, label='', only_selected:bool = False, yerr:bool = True, xerr:bool = True, **kargs):
        """Plots the data fitted into the figure.

        Parameters:
            fmt (str, optional): Data line format. Defaults to '.'.
            color (str, optional): Color for the line. Defaults to None.
            label (str, optional): Label assigned to the artists. Defaults to ''.
            only_selected (bool, optional): Shows only selected data. Defaults to `False`.
            yerr (bool, optional): Shows data errors in y coordinate if given. Defaults to `True`.
            xerr (bool, optional): Shows data errors in y coordinate if given. Defaults to `True`.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self._start_()
        self._only_selected_cache_ = only_selected
        try:
            if only_selected:
                DATA = self.fit.get_data_selected().T
            else:
                DATA = self.fit.get_data().T
        except AttributeError:
            DATA = self.app.data.get_data().T
            
        self.ax.plot(*DATA, fmt, color=color, label=label, **kargs)
        return self

    def with_data(self, fmt='.', color=None, label='', only_selected:bool = False, yerr:bool = True, xerr:bool = True, **kargs):
        """Same as itfit.plot.builder.PlotBuilder.plot_data. Plots the data fitted into the figure.

        Parameters:
            fmt (str, optional): Data line format. Defaults to '.'.
            color (str, optional): Color for the line. Defaults to None.
            label (str, optional): Label assigned to the artists. Defaults to ''.
            only_selected (bool, optional): Shows only selected data. Defaults to `False`.
            yerr (bool, optional): Shows data errors in y coordinate if given. Defaults to `True`.
            xerr (bool, optional): Shows data errors in y coordinate if given. Defaults to `True`.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.plot_data(fmt=fmt, color=color, label=label, only_selected=only_selected, yerr=yerr, xerr=xerr,**kargs)
    
    def plot_data_errors(self, axis:str|bool = 'y', ecolor: str|tuple[float]|None = None, elinewidth: float|None = None, capsize: float|None = 1, errorsevery: int|tuple[int, int] = 1, **kargs):
        """Plots error bars on data. Must be called after data has been plotted.

        Parameters:
            axis (str | bool, optional): Axis in which to plot error bars. Defaults to y.
            ecolor (str | tuple[float] | None, optional): Sets the color of the error bar. Defaults to None.
            elinewidth (float | None, optional): Sets the line width of the error bar. Defaults to None.
            capsize (float | None, optional): Controls the length of the error bar cap in points. Defaults to 1.
            errorsevery (int | tuple[int, int], optional): Draws error bars on a subset of the data. e.g. every=(3,4) then error bars would be on
        x[3], x[7], x[11].... Defaults to 1.

        Raises:
            Exception: If used prior to data plotting.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        try:
            if self._only_selected_cache_:
                DATA = self.fit.get_data_selected().T
                YDATA_ERROR = self.fit.get_ydata_errors_selected()
                XDATA_ERROR = self.fit.get_xdata_errors_selected()
            else:
                DATA = self.fit.get_data().T
                YDATA_ERROR = self.fit.get_ydata_errors()
                XDATA_ERROR = self.fit.get_xdata_errors()
        except AttributeError:
            raise Exception("Data must be plotted prior to data's error bars.")

        if (axis=='x' or axis==True) and XDATA_ERROR is not None:
            self.ax.errorbar(*DATA, XDATA_ERROR, fmt='None', capsize=capsize, ecolor=ecolor, elinewidth=elinewidth, errorevery=errorsevery, **kargs)
        if (axis=='y' or axis==True) and YDATA_ERROR is not None:
            self.ax.errorbar(*DATA, YDATA_ERROR, fmt='None', capsize=capsize, ecolor=ecolor, elinewidth=elinewidth, errorevery=errorsevery, **kargs)

        return self
    
    def with_errors(self, axis:str|bool = 'y', ecolor: str|tuple[float]|None = None, elinewidth: float|None = None, capsize: float|None = 1, errorsevery: int|tuple[int, int] = 1, **kargs):
        """Same as itfit.plot.builder.PlotBuilder.plot_data_errors. Plots error bars on data. Must be called after data has been plotted.

        Parameters:
            axis (str | bool, optional): Axis in which to plot error bars. Defaults to y.
            ecolor (str | tuple[float] | None, optional): Sets the color of the error bar. Defaults to None.
            elinewidth (float | None, optional): Sets the line width of the error bar. Defaults to None.
            capsize (float | None, optional): Controls the length of the error bar cap in points. Defaults to 1.
            errorsevery (int | tuple[int, int], optional): Draws error bars on a subset of the data. e.g. every=(3,4) then error bars would be on
        x[3], x[7], x[11].... Defaults to 1.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.plot_data_errors(axis, ecolor, elinewidth, capsize, errorsevery, **kargs)
    
    def labels(self):
        """Starts labels builder. After calling it xlabel and ylabel can be accessed.

        Returns:
            (itfit.plot.labels.LabelBuilder): label builder.
        """
        return LabelBuilder(self)
    
    def title(self, title: str):
        """Shortcut to `.labels().start_title(title).end_title().end_labels()`.

        Parameters:
            title (str): Title string.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.labels().start_title(title).end_title().end_labels()

    def xlabel(self, xlabel):
        """Shortcut to `.labels().start_x_label(xlabel).end_xlabel().end_labels()`.

        Parameters:
            xlabel (str): x label string.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.labels().start_x_label(xlabel).end_xlabel().end_labels()

    def ylabel(self, ylabel):
        """Shortcut to `.labels().start_y_label(ylabel).end_ylabel().end_labels()`.

        Parameters:
            ylabel (str): y label string.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.labels().start_y_label(ylabel).end_ylabel().end_labels()


    def legend(self, *args, **kargs):
        """Toggles the legend in the plot.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.ax.legend(*args, **kargs)
        return self

    def grid(self, *args, **kwargs):
        """Toggles the grid in the plot.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.ax.grid(*args, **kwargs)
        return self

    def set_xlim(self, left: float, right: float, **kargs):
        """Sets the left and right plot limits on x axis.
        
        Parameters:
            left (float): left limit.
            right (float): right limit.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.ax.set_xlim(left=left, right=right, **kargs)
        return self

    def set_ylim(self, bottom: float, top: float, **kargs):
        """Sets the bottom and top plot limits on y axis.
        
        Parameters:
            bottom (float): bottom limit.
            top (float): top limit.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.ax.set_ylim(bottom=bottom, top=top, **kargs)
        return self

    def tight_layout(self, **kargs):
        """Adjust the padding between and around subplots.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.fig.tight_layout(**kargs)
        return self

    def set_size(self, size, unit='cm'):
        """Sets the figure size, be default in centimeters.
        
        Parameters:
            size (float): left limit.
            unit (float): right limit. Default='cm'.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        factor = 1/2.54
        if unit == 'inch':
            factor = 1
        if unit == 'px':
            factor = 1/rcParams['figure.dpi']
        self.fig.set_size_inches(size[0]*factor, size[1]*factor, forward=True)
        return self

    def spines(self):
        """Starts spines builder.

        Returns:
            (itfit.plot.spines.SpineBuilder): spine builder.
        """
        return SpineBuilder(self)
    
    def style(self, style):
        """Sets the style. Must be executed befor `start`.

        Parameters:
            style (str): Style to use.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        mpl_style.use(style)
    
        self._start_(warn=True)
        return self
    
    def _start_(self, warn=False):
        """Creates the figure and the axes.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to start building the plot.
        """
        if hasattr(self, "fig") and hasattr(self, "ax"):
            if warn:
                print("Warning: style changes will not affect an existent figure. Use `style` before ploting anything to the figure.")
            return self
        self.fig = plt.figure()
        self.ax = self.fig.gca()

    def save_fig(self, filename, transparent=False, **kargs):
        """Saves the figure with the given filename

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.fig.savefig(filename, transparent=transparent, **kargs)
        return self

    def show_inline(self):
        """Returns the figure. When used in Jupyter shows the figure in the cell output.

        Returns:
            (matplotlib.Figure): PlotBuilder's figure.
        """
        return self.fig
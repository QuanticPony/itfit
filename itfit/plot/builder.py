"""


"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..fitter_app import Fitter
    
    
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib import rcParams
from matplotlib import style as mpl_style
from matplotlib import pyplot as plt

from .labels import LabelBuilder, titleLabelBuilder, xLabelBuilder, yLabelBuilder
from .spines import SpineBuilder

class PlotBuilder:
    """PlotBuilder is a class whose intent is to uase the user in plot customization. 
    Using PlotBuilder with jupyther/notebook is strongly recomended as changes are interactive and figures are preserved.
    ![image](example1.PNG)
    """
    fig: Figure
    ax: Axes
    def __init__(self, app: Fitter, fit, **kargs):
        """_summary_

        Args:
            app (itfit.Fitter): Main application.
            figure (Figure): Figure to modify.
            axe (Axes): Axes to modify.
            fit (itfit.utils.FitResultContainer): FitResultContainer of the fit.
        """
        self.app = app
        self.fit = fit

    def plot_fit(self, fmt='--', color='black', label='', **kargs):
        """Plots the fit line into the figure.

        Args:
            fmt (str, optional): Fit line format. Defaults to '--'.
            color (str, optional): Color for the line. Defaults to 'black'.
            label (str, optional): Label assigned to the artists. Defaults to ''.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self._start_()
        self._line, = self.ax.plot(*(self.fit.get_fit_data().T), fmt, color=color, label=label, **kargs)
        return self

    def with_fit(self, fmt='--', color='black', label='', **kargs):
        """Same as itfit.plot.builder.PlotBuilder.plot_fit. Plots the fit line into the figure.

        Args:
            fmt (str, optional): Fit line format. Defaults to '--'.
            color (str, optional): Color for the line. Defaults to 'black'.
            label (str, optional): Label assigned to the artists. Defaults to ''.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.plot_fit(fmt=fmt, color=color, label=label, **kargs)

    def plot_data(self, fmt='.', color=None, label='', **kargs):
        """Plots the data fitted into the figure.

        Args:
            fmt (str, optional): Data line format. Defaults to '.'.
            color (str, optional): Color for the line. Defaults to None.
            label (str, optional): Label assigned to the artists. Defaults to ''.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self._start_()
        self._line_data, = self.ax.plot( *(self.fit.get_data().T), fmt, color=color, label=label, **kargs)
        return self

    def with_data(self, fmt='.', color=None, label='', **kargs):
        """Same as itfit.plot.builder.PlotBuilder.plot_data. Plots the data fitted into the figure.

        Args:
            fmt (str, optional): Data line format. Defaults to '.'.
            color (str, optional): Color for the line. Defaults to None.
            label (str, optional): Label assigned to the artists. Defaults to ''.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.plot_data(fmt=fmt, color=color, label=label, **kargs)
    
    def labels(self):
        """Starts labels builder.

        Returns:
            (itfit.plot.labels.LabelBuilder): label builder.
        """
        return LabelBuilder(self)
    
    def title(self, title: str):
        """Shortcut to `.labels().start_title(title).end_title().end_labels()`.

        Args:
            title (str): Title string.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.labels().start_title(title).end_title().end_labels()

    def xlabel(self, xlabel):
        """Shortcut to `.labels().start_x_label(xlabel).end_xlabel().end_labels()`.

        Args:
            xlabel (str): x label string.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        return self.labels().start_x_label(xlabel).end_xlabel().end_labels()

    def ylabel(self, ylabel):
        """Shortcut to `.labels().start_y_label(ylabel).end_ylabel().end_labels()`.

        Args:
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
        
        Args:
            left (float): left limit.
            right (float): right limit.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.ax.set_xlim(left=left, right=right, **kargs)
        return self

    def set_ylim(self, bottom: float, top: float, **kargs):
        """Sets the bottom and top plot limits on y axis.
        
        Args:
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
        
        Args:
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

        Args:
            style (str): Style to use.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        mpl_style.use(style)
        # fig, ax = plt.subplots()
        
        # fig_dict = {}
        # axes_dict = {}
        # spines_dict = {}
        # for k,v in rcParams.items():
        #     k:str; v:str
        #     if k.startswith("figure."):
        #         k = k.removeprefix("figure.")
        #         if k in ['dpi','edgecolor','facecolor','frameon']:
        #             fig_dict.update({k:v})
    
        #     elif k.startswith("axes."):
        #         k = k.removeprefix("axes.")
        #         if k.startswith("spines."):
        #             k = k.removeprefix("spines.")
        #             spines_dict.update({k:v})
        #         if k in ['facecolor', 'frameon']:
        #             axes_dict.update({k:v})
        # self.fig.update(fig_dict)
        # self.ax.update(axes_dict)
        
        # for k, bolean in spines_dict.items():
        #     self.ax.spines[k].set_visible(bolean)
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
        return self.fig
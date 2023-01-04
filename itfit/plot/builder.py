"""


"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..fitter_app import Fitter
    
    
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib import rcParams

from .labels import titleLabelBuilder, xLabelBuilder, yLabelBuilder


class PlotBuilder:
    """PlotBuilder is a class whose intent is to uase the user in plot customization. 
    Using PlotBuilder with jupyther/notebook is strongly recomended as changes are interactive and figures are preserved.
    ![image](example1.PNG)
    """
    def __init__(self, app: Fitter, figure: Figure, axe: Axes, fit, **kargs):
        """_summary_

        Args:
            app (itfit.Fitter): Main application.
            figure (Figure): Figure to modify.
            axe (Axes): Axes to modify.
            fit (itfit.utils.FitResultContainer): FitResultContainer of the fit.
        """
        self.ax = axe
        self.app = app
        self.fig = figure
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

    def title(self, title: str):
        """Starts a title builder.

        Args:
            title (str): Title string.

        Returns:
            (itfit.plot.labels.titleLabelBuilder): A titleLabelBuilder.
        """
        return titleLabelBuilder(self, title)

    def xlabel(self, xlabel):
        """Starts a x label builder.

        Args:
            xlabel (str): x label string.

        Returns:
            (itfit.plot.labels.xLabelBuilder): A xLabelBuilder.
        """
        return xLabelBuilder(self, xlabel)

    def ylabel(self, ylabel):
        """Starts a y label builder.

        Args:
            ylabel (str): y label string.

        Returns:
            (itfit.plot.labels.yLabelBuilder): A yLabelBuilder.
        """
        return yLabelBuilder(self, ylabel)

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

    def set_xlim(self, left=None, right=None, **kargs):
        """Sets the left and right plot limits on x axis.
        
        Args:
            left (float): left limit.
            right (float): right limit.

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.ax.set_xlim(left=left, right=right, **kargs)
        return self

    def set_ylim(self, bottom=None, top=None, **kargs):
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

    def save_fig(self, filename, transparent=False, **kargs):
        """Saves the figure with the given filename

        Returns:
            (itfit.plot.builder.PlotBuilder): Returns itself to continue building the plot.
        """
        self.fig.savefig(filename, transparent=transparent, **kargs)
        return self

    def show_inline(self):
        return self.fig
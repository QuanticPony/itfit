from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib import rcParams

class PlotBuilder:
    def __init__(self, app, figure: Figure, axe: Axes, fit, **kargs):
        """Plot API for easy communication between user and Figure.
        """
        self.ax = axe
        self.app = app
        self.fig = figure
        # self.ax = axe
        self.fit = fit
        
        
    def plot_fit(self, fmt='--', color='black', label='', **kargs):
        self._line, = self.ax.plot(*(self.fit.get_fit_data().T), fmt, color=color, label=label, **kargs)
        return self
        
    def with_fit(self, fmt='--', color='black', label='', **kargs):
        return self.plot_fit(fmt=fmt, color=color, label=label, **kargs)
        
    def plot_data(self, fmt='.', color=None, label='', **kargs):
        self._line_data, = self.ax.plot(*(self.fit.get_data().T), fmt, color=color, label=label, **kargs)
        return self
        
    def with_data(self, fmt='.', color=None, label='', **kargs):
        return self.plot_data(fmt=fmt, color=color, label=label, **kargs)
    
    def title(self, title):
        return self.titleLabelBuilder(self, title)
    
    def xlabel(self, xlabel):
        return self.xLabelBuilder(self, xlabel)
    
    def ylabel(self, ylabel):
        return self.yLabelBuilder(self, ylabel)
    
    def legend(self, *args, **kargs):
        self.ax.legend(*args, **kargs)
        return self
        
    def grid(self, *args, **kwargs):
        self.ax.grid(*args, **kwargs)
        return self
    
    def set_xlim(self, left=None, right=None, **kargs):
        self.ax.set_xlim(left=left, right=right, **kargs)
        return self
    
    def set_ylim(self, bottom=None, top=None, **kargs):
        self.ax.set_ylim(bottom=bottom, top=top, **kargs)
        return self
    
    def tight_layout(self, **kargs):
        self.fig.tight_layout(**kargs)
        return self
    
    def show_inline(self):
        return self.fig

    class LabelBuilder:
        def __init__(self, plot_builder, label: str):
            self._plot_builder_: PlotBuilder = plot_builder
            self._label_ = label
            self._dict_ = {}
            
        def fontsize(self, size):
            self._dict_.update({'fontsize':size})
            return self
        def fontweight(self, weight):
            self._dict_.update({'fontweight':weight})
            return self
        def color(self, color):
            self._dict_.update({'color':color})
            return self
        def verticalalignment(self, loc):
            self._dict_.update({'verticalalignment':loc})
            return self
        def horizontalalignment(self, loc):
            self._dict_.update({'horizontalalignment':loc})
            return self
        
    class xLabelBuilder(LabelBuilder):
        def __init__(self, plot_builder, label: str):
            super().__init__(plot_builder, label)
            
        def end_xlabel(self):
            self._plot_builder_.ax.set_xlabel(self._label_, self._dict_)
            return self._plot_builder_
    
    class yLabelBuilder(LabelBuilder):
        def __init__(self, plot_builder, label: str):
            super().__init__(plot_builder, label)
        
        def end_ylabel(self):
            self._plot_builder_.ax.set_ylabel(self._label_, self._dict_)
            return self._plot_builder_
        
    class titleLabelBuilder(LabelBuilder):
        def __init__(self, plot_builder, label: str):
            super().__init__(plot_builder, label)
            
        def end_title(self):
            self._plot_builder_.ax.set_title(self._label_, self._dict_)
            return self._plot_builder_
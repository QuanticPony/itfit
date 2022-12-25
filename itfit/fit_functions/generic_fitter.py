import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_tools import ToolToggleBase
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
from scipy import optimize

from ..data import DataSelection, DataContainer
from ..utils import DragPointCollection, FitResultContainer

class GenericFitter:
    """GenericFitter is a base implementation of a fit function.
    All fit functions must inherit GenericFitter."""
    
    name = "generic"

    @staticmethod
    def function(x,*args):
        """Fit function: `f(x,*args)=...`.

        Parameters:
            x (float):
                Independent variable.
            *args (list[float,...]):
                0, 1 or multiple arguments.
        Returns:
            (Float):
                `f(x, *args)`
        """
        ...
    
    def __init__(self, app, data: DataSelection):
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
        
        # TODO: this may change when dedicated ui is implemented
        self.button_axes = plt.axes([0.81, 0.000001, 0.1, 0.055])
        self.button = Button(self.button_axes, "Fit",color="red")
        self.button.on_clicked(self.on_fit)
        
    def get_args(self):
        """Return arguments needed for `self.function`.

        Returns:
            (Tuple[float]):
                0, 1 or multiple arguments.
        """
        return self.fitter_drag_collection.get_args()
    
    def on_fit(self, event):
        """Event for fit button.

        Parameters:
            event (Matplotlib event): 
                Not used
        """

        # If there is not data selected use all data
        xdata, ydata = self.data.get_selected()
        if np.sum(self.data.indexes_used)==0:
            xdata, ydata = self.data.xdata.copy(), self.data.ydata.copy()
        
        self.fit = optimize.curve_fit(self.fitter_drag_collection.function, xdata, ydata, p0=self.get_args(), full_output=True)
        fit_result = FitResultContainer(DataContainer(xdata, ydata), self, self.fit)
        
        # Plot fit line in background
        with self.app.blit_manager.disabled():
        
            self.fit_line = Line2D(xdata, self.fitter_drag_collection.function(xdata, *self.fit[0]), linestyle='--')
            self.ax.add_artist(self.fit_line)
            
            #TODO: not sure what to do with legends
            # self.fit_line.set_label(f"a={self.fit[0][0]}\nb={self.fit[0][1]}\nc={self.fit[0][2]}")
            # self.ax.legend()
            self.ax.draw_artist(self.fit_line)
       
       # Redraw plot to show line     
        self.app.blit_manager.draw()

        # Save fit in app
        self.app.fits.update({f"{self.name}-{np.random.randint(0,100)}" : fit_result})
        
    def delete(self):
        """Remove trigger. Used when tool is disabled."""
        try:
            del self.button
            self.button_axes.remove()
        
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

    def __init__(self, *args, app, data: DataSelection, **kwargs):
        """Creates a GenericFitterTool.

        Parameters:
            app (Fitter):
                Main application.
            data (DataSelection):
                Data selected.
        """
        self.app = app
        self.data = data
        self.fitter: GenericFitter
        super().__init__(*args, **kwargs)

    def enable(self, *args):
        """Triggered when GenericTool is enabled.
        Uses BlitManager for faster rendering of DragObjects.
        """
        self.app.blit_manager.enable()

    def disable(self, *args):
        """Triggered when GenericTool is disabled.
        Removes DragObjects and disables BlitManager.
        """
        self.fitter.delete()
        self.app.blit_manager.disable()
        self.app.figure.canvas.draw_idle()
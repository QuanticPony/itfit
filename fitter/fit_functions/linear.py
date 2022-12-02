from matplotlib.backend_bases import MouseButton
from matplotlib.backend_tools import ToolToggleBase
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from ..data import DataSelection
from ..utils import DragLineManager, DragPoint, DragPointManager

class Line():

    @staticmethod
    def function(x,m,n):
        """Linear function: `f(x)=mx+n`

        Parameters
        ----------
        x : Float
            Independent variable
        m : Float
            Slope
        n : Float
            f(x) at x=0

        Returns
        -------
        Float
            f(x)
        """
        return x*m+n
    
    def __init__(self, app, data: DataSelection):
        """Linear fitter following function f(x)=mx+n

        Parameters
        ----------
        app : Fitter
            _description_
        data : DataSelection
            _description_
        """
        self.app = app
        self.fig = app.figure
        self.ax = app.ax
        self.data = data
        self.parameters = np.zeros((2,2))
        
        
        ## Create DragPoints and DragLines needed
        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.2,0.3)), None), 
                            DragPoint(*self.ax.transAxes.transform((0.8,0.7)), None)]
        self.drag_points_managers = [DragPointManager(p, self.app.blit_manager) for p in self.drag_points]
        self.adjustable_segment = DragLineManager(self.drag_points, self.app.blit_manager)
        
        ## Add created DragPoints and DragLines to BlitManager
        self.app.blit_manager.artists.append(self.adjustable_segment)
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        
        
        
        # TODO: this may change when dedicated ui is implemented
        self.button_axes = plt.axes([0.81, 0.000001, 0.1, 0.055])
        self.button = Button(self.button_axes, "Fit",color="red")
        self.button.on_clicked(self.on_fit)
        
        self.fig.canvas.draw_idle()
        

    
    def get_args(self):
        """Gets linear parameters `m` and `n` from DragObjects

        Returns
        -------
        Tuple(Float, Float)
            `m` and `n`
        """
        self.parameters[:,0] = np.array(self.adjustable_segment.get_xdata())
        self.parameters[:,1] = np.array(self.adjustable_segment.get_ydata())
        p = self.parameters
        m = (p[0,1] - p[1,1])/(p[0,0] - p[1,0])
        return m, m*(-p[1,0])+p[1,1]
    
        
        
    def on_fit(self, event):
        """Event for fit button

        Parameters
        ----------
        event : Matplotlib event
            Not used
        """

        # If there is not data selected use all data
        xdata, ydata = self.data.get_selected()
        if np.sum(self.data.indexes_used)==0:
            xdata, ydata = self.data.xdata.copy(), self.data.ydata.copy()
        

        self.fit = optimize.curve_fit(self.function, xdata, ydata, p0=self.get_args(), full_output=True)

        # Plot fit line in background
        with self.app.blit_manager.disabled():
        
            self.fit_line = Line2D(xdata, self.function(xdata, *self.fit[0]), linestyle='--')
            self.ax.add_artist(self.fit_line)
            self.fit_line.set_label(f"m={self.fit[0][0]}\nn={self.fit[0][1]}")
            self.ax.legend()
            self.ax.draw_artist(self.fit_line)
       
       # Redraw plot to show line     
        self.app.blit_manager.draw()

        # Save fit in app
        self.app.fits.update({f"linear-{np.random.randint(0,100)}" : (self.fit, self.data.get_selected(), self.fit_line)})
        
        

        
    def delete(self):
        """Line remove trigger. Used when tool is disabled"""
        
        #TODO: add a zoom plot?? 
        try:
            del self.button
            self.button_axes.remove()
        

            # Remove artists in order to clean canvas
            for pm in self.drag_points_managers:
                pm.dragpoint.remove()
                self.app.blit_manager.artists.remove(pm)

            self.adjustable_segment.remove()
            self.app.blit_manager.artists.remove(self.adjustable_segment) 
        
        except AttributeError:
            pass
    


class LineTool(ToolToggleBase):
    """Toggles Line Tool."""
    
    # default_keymap = ''
    description = 'Line me please'
    default_toggled = False
    radio_group = "fitter"

    def __init__(self, *args, app, data: DataSelection, **kwargs):
        self.app = app
        self.data = data
        super().__init__(*args, **kwargs)

    def enable(self, *args):
        """Triggered when LineTool is enabled.
        Uses BlitManager for faster rendering of DragObjects.
        """
        self.app.blit_manager.enable()
        self.line = Line(self.app, self.data)

    def disable(self, *args):
        """Triggered when LineTool is disabled.
        Removes DragObjects and disables BlitManager.
        """
        self.line.delete()
        self.app.blit_manager.disable()
        self.app.figure.canvas.draw_idle()

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
    def __init__(self, app, data: DataSelection):
        self.app = app
        self.fig = app.figure
        self.ax = app.ax
        self.data = data

        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.2,0.3)), None), 
                            DragPoint(*self.ax.transAxes.transform((0.8,0.7)), None)]
        self.drag_points_managers = [DragPointManager(p, self.app.blit_manager) for p in self.drag_points]
        self.adjustable_segment = DragLineManager(self.drag_points, self.app.blit_manager)
        
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        self.app.blit_manager.artists.append(self.adjustable_segment)
        
        
        # TODO: mejorar
        self.button_axes = plt.axes([0.81, 0.000001, 0.1, 0.055])
        self.button = Button(self.button_axes, "Fit",color="red")
        
        self.button.on_clicked(self.on_fit)
        
        self.fig.canvas.draw_idle()
        
        self.p = np.zeros((2,2))

    
    def get_args(self):
        self.p[:,0] = np.array(self.adjustable_segment.get_xdata())
        self.p[:,1] = np.array(self.adjustable_segment.get_ydata())
        p = self.p
        m = (p[0,1] - p[1,1])/(p[0,0] - p[1,0])
        return m, m*(-p[1,0])+p[1,1]
    
    @staticmethod
    def function(x,m,n):
        return x*m+n
        
    def __call__(self, x):
        p = self.p
        div = (p[0,0] - p[1,0])
        m = (p[0,1] - p[1,1]) / div if div!=0 else 0
        if self.clics==0:
            m=0
        
        return m*(x-p[1,0])+p[1,1]
        
    def on_fit(self, event):
        # m, n = self.get_args()
        xdata, ydata = self.data.get_selected()
        if np.sum(self.data.indexes_used)==0:
            xdata, ydata = self.data.xdata.copy(), self.data.ydata.copy()
        self.fit = optimize.curve_fit(self.function, xdata, ydata, p0=self.get_args(), full_output=True)


        # This part is for ploting the fit line in the background
        self.app.blit_manager.disable()
        
        self.fit_line = Line2D(xdata, self.function(xdata, *self.fit[0]), linestyle='--')
        self.ax.add_artist(self.fit_line)
        self.fit_line.set_label(f"m={self.fit[0][0]}\nn={self.fit[0][1]}")
        self.ax.legend()
        self.ax.draw_artist(self.fit_line)
        
        self.app.blit_manager.enable()


        self.app.fits.update({f"linear-{np.random.randint(0,100)}" : (self.fit, self.data.get_selected(), self.fit_line)})
        
        # self.delete()
        

        
    def delete(self):
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
        
        # TODO? esto no se si debería estar aquí
        self.ax.add_artist(self.fit_line)





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
        self.app.blit_manager.enable()
        self.line = Line(self.app, self.data)

    def disable(self, *args):
        self.line.delete()
        self.app.blit_manager.disable()
        self.app.figure.canvas.draw_idle()

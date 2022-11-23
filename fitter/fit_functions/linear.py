from matplotlib.backend_bases import MouseButton
from matplotlib.backend_tools import ToolToggleBase
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from ..data import DataSelection

class Line():
    def __init__(self, fig, ax, data: DataSelection) -> None:
        self.fig = fig
        self.ax = ax
        self.data = data
        self.p = np.zeros((2,2))
        self.fixed_p = np.zeros((2,2))
        self.clics = 0
        self.line, = self.ax.plot(self.p[0], self.p[1], '-', color='red')
        self.fit_line, = self.ax.plot(self.data.xdata, self.data.ydata, '--', color='r', alpha=0)
        self.MAX_CLICS = 2
        self._connect_motion()
        self._connect_clic()
    
    def get_args(self):
        p = self.p
        m = (p[0,1] - p[1,1])/(p[0,0] - p[1,0])
        return m, m*(-p[1,0])+p[1,1]
    
    @staticmethod
    def function(x,m,n):
        return x*m+n
        
    def _connect_motion(self):
        self.bind_id_motion = plt.connect('motion_notify_event', self.on_move)
        
    def _unbin_motion(self):
        plt.disconnect(self.bind_id_motion)
        self.bind_id_motion = None
        
    def _connect_clic(self):
        self.bind_id_clic = plt.connect('button_press_event', self.on_click) 
        
    def _unbin_clic(self):
        plt.disconnect(self.bind_id_clic) 
        self.bind_id_clic = None
        
    def __call__(self, x):
        p = self.p
        div = (p[0,0] - p[1,0])
        m = (p[0,1] - p[1,1]) / div if div!=0 else 0
        if self.clics==0:
            m=0
        
        return m*(x-p[1,0])+p[1,1]
    
    def draw(self, out=False):
        lims = self.ax.get_xlim() if not out else []
        points = self(lims) if not out else []
        self.line.set_xdata(lims)
        self.line.set_ydata(points)
        self.ax.figure.canvas.draw()
        
    def on_move(self, event):
        point = np.array([event.xdata, event.ydata])
        if event.inaxes:
            self.p[:] = self.fixed_p
            self.p[1-self.clics] = point
            self.draw()
        
    def on_click(self, event):
        
        if event.button is MouseButton.LEFT and self.clics <= self.MAX_CLICS:
            self.fixed_p[:] = self.p
            self.clics += 1
            if self.clics == self.MAX_CLICS:
                self._unbin_motion()
                m, n = self.get_args()
                xdata, ydata = self.data.get_selected()
                if np.sum(self.data.indexes_used)==0:
                    xdata, ydata = self.data.xdata.copy(), self.data.ydata.copy()
                self.fit = optimize.curve_fit(self.function, xdata, ydata, p0=self.get_args())
                print(self.fit)
                self.fit_line.set_alpha(1)
                self.fit_line.set_data(xdata, self.function(xdata, *self.fit[0]))
                # self.fit_line.set_ydata(self.function(xdata, *self.fit[0]))
                self.fit_line.set_label(f"m={self.fit[0][0]}\nn={self.fit[0][1]}")
                self.ax.legend()
                self.draw(out=True)
                # self.line.remove()
                return
                
            
        if event.button is MouseButton.RIGHT: 
            self.clics -= 1
            self.clics = max(0, self.clics)
            
            if self.clics < self.MAX_CLICS and not self.bind_id_motion:
                self._connect_motion()

        self.draw()
        
    def delete(self):
        #TODO: add a zoom plot?? 
        self._unbin_clic()
        self._unbin_motion()
        self.fit_line.remove()
        self.line.remove()
        del self.fit_line
        del self.line
        self.fig.canvas.draw_idle()





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
        self.line = Line(self.figure, self.figure.get_axes()[0], self.data)

    def disable(self, *args):
        self.line.delete()

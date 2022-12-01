from matplotlib.patches import Circle
from matplotlib.artist import Artist
import numpy as np

class DragPoint:
    def __init__(self, x, y, style, *args):
        self._x = x
        self._y = y
        self._style = style
        
        self.patch = Circle(np.array([x,y]), 10)
        
    def remove(self):
        self.patch.remove()


class DragPointManager:
    def __init__(self, dragpoint: DragPoint, blit_manager):
        """Manages a DragPoint's BlitManager connection, callbacks on matplotlib events and automatic drawing.

        Args:
            dragpoint (_type_): _description_
            blit_manager (BlitManager): used for automtic ploting.
        """
        self.dragpoint = dragpoint
        self.blit_manager = blit_manager
        
        self.ax = blit_manager.ax
        self.canvas = blit_manager.canvas
        
        self.dragpoint.patch.set_transform(None)
        self.blit_manager.ax.add_patch(self.dragpoint.patch)
        
        self.poly = self.dragpoint.patch

        self.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('button_release_event', self.on_button_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        
        self._ind = None # Used for enabling mouse motion.


    def update(self):
        pass


    def get_xy(self, x, y):
        """Aplies correct transformation from display to data coordinates"""
        return self.ax.transData.inverted().transform((x,y))
    
    def set_xy(self, x, y):
        """Aplies correct transformation from data coordinates to display"""
        return self.ax.transData.transform((x,y))

    def on_button_press(self, event):
        """Callback for mouse button presses."""
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        x, y = event.xdata, event.ydata
        x, y = self.set_xy(x, y)
        if np.hypot(*(self.poly.center - np.array([x,y]))) < 1.5*self.poly.get_radius():
            self._ind = 0

    
    def on_button_release(self, event):
        """Callback for mouse button releases."""
        if event.button != 1:
            return
        self._ind = None

    def on_key_press(self, event):
        """Callback for key presses."""
        #! This may be useful later.
        if not event.inaxes:
            return


    def on_mouse_move(self, event):
        """Callback for mouse movements."""
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata
        x, y = self.set_xy(x, y)

        prop = {'center': np.array([x,y])}
        Artist.update(self.poly, prop)
        
        self.blit_manager.draw()
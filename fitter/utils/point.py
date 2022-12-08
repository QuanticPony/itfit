from matplotlib.patches import Circle
from matplotlib.artist import Artist
import numpy as np

class DragPoint:
    def __init__(self, x, y, style, *args):
        self._style = style
        self.restriction_callback = lambda x,y: (x,y)
        self.patch = Circle(np.array([x,y]), 10)
        
    def get_center(self):
        return self.restriction_callback(*self.patch.get_center())
        
    def remove(self):
        self.patch.remove()

class DragPointManager:
    def __init__(self, dragpoint: DragPoint, blit_manager):
        """Manages a DragPoint's BlitManager connection, callbacks on matplotlib events and automatic drawing.

        Args:
            dragpoint (DragPoint): contains patch.
            blit_manager (BlitManager): used for automtic ploting.
        """
        self.dragpoint = dragpoint
        self.blit_manager = blit_manager
        
        self.ax = blit_manager.ax
        self.canvas = blit_manager.canvas
        
        self.dragpoint.patch.set_transform(None)
        self.blit_manager.ax.add_patch(self.dragpoint.patch)
        
        self.poly = self.dragpoint.patch
        self.connection_callbacks = {}
        self.restricction_callback = lambda x,y: (x,y)

        self.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('button_release_event', self.on_button_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        
        self._ind = None # Used for enabling mouse motion.

    def connect(self, function):
        """Connects a callback for change envents. Function must have signature `def f(event)`"""
        key = np.random.randint(1000000)
        self.connection_callbacks.update({key: function})
        return key
    
    def disconnect(self, cid):
        """Disconnects the callback with given `cid`"""
        if cid in self.connection_callbacks.keys():
            self.connection_callbacks.pop(cid)
            
    def add_restriction(self, function):
        """Adds a restriction to object movement. Function must have signature `def f(new_x,new_y): -> Tuple(float, float)`"""
        self.restricction_callback = function
        self.dragpoint.restriction_callback = self.restricction_callback
    
    def remove_restriction(self):
        """Removes the restriction to object movemet"""
        self.restricction_callback = lambda x,y:(x,y)
        self.dragpoint.restriction_callback = self.restricction_callback

    def get_xy(self, x, y):
        """Aplies correct transformation from display to data coordinates"""
        return self.ax.transData.inverted().transform((x,y))
    
    def set_xy(self, x, y):
        """Aplies correct transformation from data coordinates to display"""
        return self.ax.transData.transform((x,y))

    def on_button_press(self, event):
        """Callback for mouse button presses"""
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        x, y = event.xdata, event.ydata
        x, y = self.set_xy(x, y)
        if np.hypot(*(self.poly.center - np.array([x,y]))) < 1.5*self.poly.get_radius():
            self._ind = 0
    
    def on_button_release(self, event):
        """Callback for mouse button releases"""
        if event.button != 1:
            return
        self._ind = None

    def on_key_press(self, event):
        """Callback for key presses"""
        #! This may be useful later.
        if not event.inaxes:
            return

    def on_mouse_move(self, event):
        """Callback for mouse movements"""
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata
        x, y = self.restricction_callback(x, y)
        x, y = self.set_xy(x, y)

        prop = {'center': np.array([x,y])}
        Artist.update(self.poly, prop)
        for k,v in self.connection_callbacks.items():
            v(x,y)
        
        self.blit_manager.draw()
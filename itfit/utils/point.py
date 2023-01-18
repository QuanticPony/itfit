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

from matplotlib.patches import Circle
from matplotlib.artist import Artist
import numpy as np


class DragPoint:
    """Data containter for draggable points. In the future it may support form, size and colour change.
    """
    def __init__(self, x, y, style, *args):
        """Creates a patch in given display coordinates.

        Parameters:
            x (float):
                y position in display units (between 0 and 1).
            y (float):
                y position in display units (between 0 and 1).
            style : Any
                No used.
        """
        self._style = style
        self.restriction_callback = lambda x,y: (x,y)
        self.patch = Circle(np.array([x,y]), 10)
        
    def get_center(self):
        """Returns the center position in display coordinates.

        Returns:
            (Tuple[float,float]):
                Center in display coordinates.
        """
        return self.restriction_callback(*self.patch.get_center())
        
    def remove(self):
        """Removes the point from the figure."""
        self.patch.remove()
        
        

class DragPointManager:
    """Manages `DragPoints`: event connection, automatic replotting on change/update, blitting and restrictions.
    """
    def __init__(self, dragpoint: DragPoint, blit_manager):
        """Manages a DragPoint's BlitManager connection, callbacks on matplotlib events and automatic drawing.

        Parameters:
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
        
        self._ind_ = None # Used for enabling mouse motion.

    def connect(self, function):
        """Connects a callback for change envents. 
        
        Parameters:
            function (callable):
                Function to be executed when the DragPoint updates. Must have signature `def f(event)`.    
        Returns:
            (Int):
                Connection id. Can be used in `DragPointManager.disconnect`.
        """
        cin = np.random.randint(1000000)
        self.connection_callbacks.update({cin: function})
        return cin
    
    def disconnect(self, cid):
        """Disconnects the callback with given `cid`.
        
        Parameters:
            cid (Int):
                Connection id.
        """

        if cid in self.connection_callbacks.keys():
            self.connection_callbacks.pop(cid)
            
    def add_restriction(self, function):
        """Adds a restriction to point movement. 
        
        Parameters:
            function (callable):
                Must have signature `def f(new_x,new_y): -> Tuple[float, float]`
        """
        self.restricction_callback = function
        self.dragpoint.restriction_callback = self.restricction_callback
    
    def remove_restriction(self):
        """Removes the restriction to point movement"""
        self.restricction_callback = lambda x,y:(x,y)
        self.dragpoint.restriction_callback = self.restricction_callback

    def get_xy(self, x, y):
        """Applies correct transformation from display to data coordinates.
        
        Parameters:
            x (float):
                x in display coordinates.
            y (float):
                y in display coordinates.  
        Returns:
            (Tuple[float,float]):
                x and y in data coordinates.
        """
        return self.ax.transData.inverted().transform((x,y))
    
    def set_xy(self, x, y):
        """Applies correct transformation from data coordinates to display
        
        Parameters:
            x (float): 
                x in data coordinates.
            y (float):
                y in data coordinates.
        Returns:
            (Tuple[float,float]):
                x and y in display coordinates.
        """
        return self.ax.transData.transform((x,y))

    def on_button_press(self, event):
        """Callback for mouse button presses"""
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        if self.blit_manager.bind_motion != -1:
            return

        x, y = event.xdata, event.ydata
        x, y = self.set_xy(x, y)
        if np.hypot(*(self.poly.center - np.array([x,y]))) < 1.5*self.poly.get_radius():
            self._ind_ = hash(self)
        
            self.blit_manager.bind_motion = self._ind_
    
    def on_button_release(self, event):
        """Callback for mouse button releases"""
        if event.button != 1:
            return

        if self.blit_manager.bind_motion == self._ind_:
            self.blit_manager.bind_motion = None
        self._ind_ = 0

    def on_key_press(self, event):
        """Callback for key presses"""
        #! This may be useful later.
        if not event.inaxes:
            return

    def on_mouse_move(self, event):
        """Callback for mouse movements"""
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        if self._ind_ == 0:
            return
        if self.blit_manager.bind_motion != self._ind_:
            return
        
        x, y = event.xdata, event.ydata
        x, y = self.restricction_callback(x, y)
        x, y = self.set_xy(x, y)

        prop = {'center': np.array([x,y])}
        Artist.update(self.poly, prop)
        for k,v in self.connection_callbacks.items():
            v(x,y)
        
        self.blit_manager.draw()
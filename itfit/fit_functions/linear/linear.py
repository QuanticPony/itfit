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

import numpy as np

from .. import GenericFitter, GenericFitterTool, FunctionContainer
from ...data import DataSelection
from ...utils import DragPoint, DragPointManager, BlitManager, DragPointCollection


class DragLineManager(DragPointCollection):
    """Collection of DragPoints representing a straight line."""
    
    @staticmethod
    def function(x, m, n):
        """Straight line function.

        Parameters:
            x (float):
                independent variable.
            m (float):
                slope.
            n (float):
                value at `x=0`.

        Returns:
            (float):
                `f(x) = m*x+n`
        """
        return m*x + n
    
    @staticmethod
    def get_args_length():
        """Gets number of arguments of `function`.

        Returns:
            (int): Number of arguments of `function`.
        """
        return 2
    
    def __init__(self, dragpoints: list[DragPoint], blit_manager: BlitManager):
        """Line between multiple DragPoints. Updates with them.

        Parameters:
            dragpoints (list[DragPoint]): line vertices.
            blit_manager (BlitManager): used for automtic ploting.
        """
        super().__init__(dragpoints, blit_manager)
        self.update()
    
    def update(self, *args, **kargs):
        """Updates line data with DragObjects positions"""
        x0, x1 = self.get_xdata()
        m, n = self.get_args()
        
        if (m,n) == (0,0):
            self.poly.set_xdata(self.get_xdata_display())
            self.poly.set_ydata(self.get_ydata_display())

        # create x and y data
        dx = abs(x0-x1)*0.5
        x = np.linspace(min(x0,x1)-dx, max(x0,x1)+dx, 250)
        y = self.function(x, m, n)
        
        # from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1, 2)
        x_data, y_data = self.set_xy(xy).T
        
        # set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)
 
    def get_args(self):
        """Gives linear function parameters.

        Returns:
            (Tuple[float, float]):
                `m` and `n` of `f(x)=m*x + n`.
        """
        x0, x1 = self.get_xdata()
        y0, y1 = self.get_ydata()

        if (x1-x0)==0:
            return 0.,0.
        m:float = (y1 - y0)/(x1 - x0)
        n:float = m*(-x1)+y1
        return m, n

class LineFitter(GenericFitter):
    """Linear function fitter."""
    name = 'linear'
    
    def __init__(self, app, data: DataSelection):
        """Linear fitter following function `f(x)=m*x + n`.

        Parameters:
            app (Fitter): 
                Main application.
            data (DataSelection): 
                Data to fit.
        """
        super().__init__(app, data)
        
        ## Create DragPoints and DragLines needed
        
        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.2,0.3)), None), 
                            DragPoint(*self.ax.transAxes.transform((0.8,0.7)), None)]
        self.drag_points_managers = [DragPointManager(p, self.app.blit_manager) for p in self.drag_points]
        self.fitter_drag_collection = DragLineManager(self.drag_points, self.app.blit_manager)
        self.function = self.fitter_drag_collection.function
        
        ## Connect Line to Points change events
        self.drag_points_cids = [] # Connections ids for change events
        for dp in self.drag_points_managers:
            self.drag_points_cids.append(
                dp.connect(self.fitter_drag_collection.update)
            )
        
        ## Add created DragPoints and DragLines to BlitManager's artists
        self.app.blit_manager.artists.append(self.fitter_drag_collection)
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        
        self.fig.canvas.draw_idle()
    

class LineTool(GenericFitterTool):
    """Toggles Line Tool."""
    
    # default_keymap = ''
    description = 'Line me please'

    def enable(self, *args):
        """Triggered when LineTool is enabled.
        Uses BlitManager for faster rendering of DragObjects.
        """
        super().enable()
        self.fitter = LineFitter(self.app, self.data)

    def disable(self, *args):
        """Triggered when LineTool is disabled.
        Removes DragObjects and disables BlitManager.
        """
        super().disable()
        # If extra cleaning is needed
        
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

from .. import GenericFitter, GenericFitterTool
from ...data import DataSelection
from ...utils import DragPoint, DragPointManager, BlitManager, DragPointCollection


class DragQuadraticManager(DragPointCollection):
    """Collection of DragPoints representing a quadratic line."""
    
    @staticmethod
    def function(x, a, b, c):
        """Quadratic function.

        Parameters:
            x (float):
                independent variable.
            a (float):
                x^2 coefficient.
            b (float):
                x^1 coefficient.
            c (float):
                constant coefficient.

        Returns:
            (float):
                `f(x)=a*x^2 + b*x + c`
        """
        return a*x*x + b*x + c
    
    @staticmethod
    def get_args_length():
        """Gets number of arguments of `function`.

        Returns:
            (int): Number of arguments of `function`.
        """
        return 3
    
    def __init__(self, dragpoints: list[DragPoint], blit_manager: BlitManager):
        """Quadratic line between 2 DragPoints. Updates with them.

        Args:
            dragpoints (list[DragPoint]): line vertices.
            blit_manager (BlitManager): used for automtic ploting.
        """
        super().__init__(dragpoints, blit_manager)
        # name points based on use
        self.center_point = self.dragpoints[0]
        self.lateral_point = self.dragpoints[1]
        self.update()
    
    def update(self, *args, **kargs):
        """Updates line data with DragObjects positions"""
        cp_x, lp_x = self.get_xdata()
        a,b,c = self.get_args()

        # create x and y data of quadratic line centered in center_point
        dx = abs(lp_x-cp_x)*1.5
        x = np.linspace(cp_x-dx, cp_x+dx, 250)
        y = self.function(x, a, b, c)
        
        # from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1, 2)
        x_data, y_data = self.set_xy(xy).T
        
        # set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)
        
    def get_args(self):
        """Gives quadratic function parameters.

        Returns:
            (Tuple[float, float, float]):
                `a`, `b` and `c` of `f(x)=a*x^2 + b*x + c`.
        """
        cp_x, cp_y = self.get_xy(*self.center_point.patch.get_center())
        lp_x, lp_y = self.get_xy(*self.lateral_point.patch.get_center())
        a = (lp_y - cp_y)/np.square(lp_x-cp_x)
        b = -2*a*cp_x
        c = cp_y + a*cp_x*cp_x
        return a,b,c

class QuadraticFitter(GenericFitter):
    """Quadratic function fitter."""
    name = 'quadratic'
    
    def __init__(self, app, data: DataSelection):
        """Quadratic fitter following function `f(x)=a*x^2 + b*x + c`

        Parameters:
            app (Fitter): 
                Main application.
            data (DataSelection): 
                Data to fit.
        """
        super().__init__(app, data)
        
        ## Create DragPoints and DragLines needed
        
        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.5,0.2)), None), 
                            DragPoint(*self.ax.transAxes.transform((0.7,0.5)), None)]
        self.drag_points_managers = [DragPointManager(p, self.app.blit_manager) for p in self.drag_points]
        self.fitter_drag_collection = DragQuadraticManager(self.drag_points, self.app.blit_manager)
        self.function = self.fitter_drag_collection.function
        
        ## Connect Quadratic to Points change events
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
    

class QuadraticTool(GenericFitterTool):
    """Toggles Quadratic Tool."""
    
    # default_keymap = ''
    description = 'Quadratic me please'

    def enable(self, *args):
        """Triggered when QuadraticTool is enabled.
        Uses BlitManager for faster rendering of DragObjects.
        """
        super().enable()
        self.fitter = QuadraticFitter(self.app, self.data)

    def disable(self, *args):
        """Triggered when QuadraticTool is disabled.
        Removes DragObjects and disables BlitManager.
        """
        super().disable()
        # If extra cleaning is needed
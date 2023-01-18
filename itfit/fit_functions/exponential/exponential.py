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


class DragExponentialManager(DragPointCollection):
    """Collection of DragPoints representing a straight line."""
    
    @staticmethod 
    def function(x,a,b):
        """Exponential function.

        Parameters:
            x (float):
                independent variable.
            a (float):
                scales exponential function.
            b (float):
                scales x.

        Returns:
            (float):
                `f(x) = a*exp(b*x)`
        """
        return a*np.exp(b*x)
    
    @staticmethod
    def get_args_length():
        """Gets number of arguments of `function`.

        Returns:
            (int): Number of arguments of `function`.
        """
        return 2
    
    def __init__(self,dragpoints: list[DragPoint],blit_manager: BlitManager):
        """Exponential line between 2 DragPoints. Updates with them.

        Args:
            dragpoints (list[DragPoint]): line vertices.
            blit_manager (BlitManager): used for automatic ploting.
        """ 
        super().__init__(dragpoints,blit_manager)
        # name points based on use 
        self.point_1 = self.dragpoints[0]
        self.point_2 = self.dragpoints[1]
        self.update()

    def update(self,*args,**kargs):
        """Updates line data with DragObjects positions"""
        p1_x, p2_x = self.get_xdata()
        a,b = self.get_args()

        #create x and y data of an exponential that moves across two poitns
        dx = abs(p1_x-p2_x) * 1.5 
        x = np.linspace(min(p1_x,p2_x)-dx,max(p1_x,p2_x)+dx,250)
        y = self.function(x, a, b)

        # from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1,2)
        x_data, y_data = self.set_xy(xy).T 

        #set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)

    def get_args(self):
        """Gives exponential function parameters.

        Returns:
            (Tuple[float,float]):
                `a`, and `b` of `f(x) = a*exp(b*x)`
        """ 
        p1_x, p1_y = self.get_xy(*self.point_1.patch.get_center())
        p2_x, p2_y = self.get_xy(*self.point_2.patch.get_center())

        b = 1/(p1_x - p2_x) * np.log(p1_y/p2_y)

        a = p1_y / np.exp(b*p1_x)
        return a, b 

class ExponentialFitter(GenericFitter):
    """Exponential function fitter."""
    name = 'exponential'

    def __init__(self,app,data: DataSelection):
        """ Exponential fitter following function `f(x) = a*exp(b*x)`

        Parameters:
            app (Fitter): 
                Main application.
            data (DataSelection): 
                Data to fit.
        """

        super().__init__(app,data)

        ## Create DragPoints and DragLines needed

        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.4,0.2)), None),
                            DragPoint(*self.ax.transAxes.transform((0.3,0.5)), None)]
        self.drag_points_managers = [DragPointManager(p,self.app.blit_manager) for p in self.drag_points]
        self.fitter_drag_collection = DragExponentialManager(self.drag_points, self.app.blit_manager)
        self.function = self.fitter_drag_collection.function

        ## Connect Exponential to Points change events

        self.drag_points_cids = [] #Connection ids for change events
        for dp in self.drag_points_managers:
            self.drag_points_cids.append(
                dp.connect(self.fitter_drag_collection.update)
            )

        ## Add created DragPoints and DragLines to BlitManager's artists
        self.app.blit_manager.artists.append(self.fitter_drag_collection)
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        self.fig.canvas.draw_idle()

class ExponentialTool(GenericFitterTool):
    """ Toggles Exponential Tool."""

    # default_keymap = '' 
    description = 'Exponentiate me please'

    def enable(self,*args):
        """Triggered when ExponentialTool is enabled.
        Uses BLitManager for faster rendering of DragObjects.
        """ 
        super().enable()
        self.fitter = ExponentialFitter(self.app, self.data)

    def disable(self,*args):
        """ Triggered when ExponentialTool is disabled
        Removes DragObjects and disables BLitManager.
        """ 
        super().disable()
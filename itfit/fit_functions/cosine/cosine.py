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


class DragCosineManager(DragPointCollection):
    """Collection of DragPoints representing a cosine function."""
    
    @staticmethod
    def function(x, a, b, c, d):
        """Cosine function.

        Parameters:
            x (float):
                independent variable.
            a (float):
                Amplitude of the wave.
            b (float):
                frequency of the wave.
            c (float):
                centre of the cosine function.
            d (float):
                constant value around which the wave oscillates.

        Returns:
            (float):
                `f(x) = a*cos(b*x+c)+d`
        """
        return a*np.cos(b*x+c) + d 

    @staticmethod
    def get_args_length():
        """Gets number of arguments of `function`.

        Returns:
            (int): Number of arguments of `function`.
        """
        return 4
    
    def __init__(self, dragpoints: list[DragPoint], blit_manager: BlitManager):
        """Cosine function between multiple DragPoints. Updates with them.

        Parameters:
            dragpoints (list[DragPoint]): wave points.
            blit_manager (BlitManager): used for automtic ploting.
        """
        super().__init__(dragpoints, blit_manager)
        self.point_1 = self.dragpoints[0]
        self.point_2 = self.dragpoints[1]
        self.update()
    
    def update(self, *args, **kargs):
        """Updates function data with DragObjects positions"""
        p1_x, p2_x = self.get_xdata()
        a,b,c,d = self.get_args()

        #create x and y data of trigonometric function that moves across two points
        dx = abs(p1_x-p2_x) * 1.5 
        x = np.linspace(min(p1_x,p2_x)-dx,max(p1_x,p2_x)+dx,250)
        y = self.function(x, a, b, c,d)
        
        # from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1, 2)
        x_data, y_data = self.set_xy(xy).T
        
        # set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)
 
    def get_args(self):
        """Gives cosine function parameters.

        Returns:
            (Tuple[float, float]):
                `a`, `b`, `c` and `d` of `f(x)=a*cos(b*x +c)+d`.
        """
        x0, x1 = self.get_xdata()
        y0, y1 = self.get_ydata()

        a = abs(y0-y1)
        b = - np.pi/2 / (x0-x1)
        c = np.pi/2 -b *x1 
        d = y1

        return a, b, c, d

class CosineFitter(GenericFitter):
    """Cosine function fitter."""
    name = 'cosine'

    def __init__(self, app, data: DataSelection):
        """Cosine fitter following function 'f(x) = a*cos(b*x+b)'.
        
        Parameters:
            app (Fitter):
                Main application.
            data (DataSelection):
                Data to fit.
        """
        super().__init__(app,data)

        ##Create DragPoints and DragLines needed

        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.2,0.3)), None), 
                            DragPoint(*self.ax.transAxes.transform((0.8,0.7)), None)]
        self.drag_points_managers = [DragPointManager(p, self.app.blit_manager) for p in self.drag_points]
        self.fitter_drag_collection = DragCosineManager(self.drag_points, self.app.blit_manager)

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

class CosineTool(GenericFitterTool):
    """Toggles CosineTool."""

    # default_keymap = ''
    description = 'Cosine me please'

    def enable(self,*args):
        """Triggered when CosineTool is enabled.
        Uses BlitManager for faster rendering of DragObjects.
        """

        super().enable()
        self.fitter = CosineFitter(self.app,self.data)
    
    def disable(self, *args):
        """Triggered when CosineTool is disabled.
        Removes DragObjects and disables BlitManager.
        """

        super().disable()
        # If extra cleaning is needed
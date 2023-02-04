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


class DragSineManager(DragPointCollection):
    """Collection of DragPoints representing a sine function."""
    
    @staticmethod
    def function(x, a, b, c, d):
        """Sine function.

        Parameters:
            x (float):
                independent variable.
            a (float):
                Amplitude of the wave.
            b (float):
                frequency of the wave.
            c (float):
                centre of the sine function.
            d (float):
                constant value around which the wave oscillates.

        Returns:
            (float):
                `f(x) = a*sin(b*x+c)+d`
        """
        return a*np.sin(b*x+c) + d 

    @staticmethod
    def gradient(x, a, b, c, d):
        """Sine gradient function.

        Parameters:
            x (float):
                independent variable.
            a (float):
                Amplitude of the wave.
            b (float):
                frequency of the wave.
            c (float):
                centre of the sine function.
            d (float):
                constant value around which the wave oscillates.

        Returns:
            (np,array):
                ( sin(b*x + c), a*x*cos(b*x+c), a*cod(b*x+c), 1)
        """
        dfda = np.sin(b*x + c)
        dfdb = a * x* np.cos(b*x +c)
        dfdc = a * np.cos(b*x + c)
        dfdd = 1
        return np.array ([dfda], [dfdb], [dfdc], [dfdd])
    
    def __init__(self, dragpoints: list[DragPoint], blit_manager: BlitManager):
        """Sine function between multiple DragPoints. Updates with them.

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
        """Gives sine function parameters.

        Returns:
            (Tuple[float, float]):
                `a`, `b`, `c` and `d` of `f(x)=a*sin(b*x +c)+d`.
        """
        x0, x1 = self.get_xdata()
        y0, y1 = self.get_ydata()

        a = abs(y0-y1)
        b = np.pi/2 / (x0-x1)
        c = -b *x1 
        d = y1

        return a, b, c, d

class SineFitter(GenericFitter):
    """Sine function fitter."""
    name = 'sine'

    def __init__(self, app, data: DataSelection):
        """Sine fitter following function 'f(x) = a*sin(b*x+b)'.
        
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
        self.fitter_drag_collection = DragSineManager(self.drag_points, self.app.blit_manager)
        self.function = self.fitter_drag_collection.function
        self.gradient = self.fitter_drag_collection.gradient

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

class SineTool(GenericFitterTool):
    """Toggles SineTool."""

    # default_keymap = ''
    description = 'Sine me please'

    def enable(self,*args):
        """Triggered when SineTool is enabled.
        Uses BlitManager for faster rendering of DragObjects.
        """

        super().enable()
        self.fitter = SineFitter(self.app,self.data)
    
    def disable(self, *args):
        """Triggered when SineTool is disabled.
        Removes DragObjects and disables BlitManager.
        """

        super().disable()
        # If extra cleaning is needed
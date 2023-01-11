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

from . import BlitManager, DragPoint, DragPointCollection


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

        #create x and y data of exponential line of an exponential that moves across two poitns
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
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


class DragGaussianManager(DragPointCollection):
    """Collection of DragPoints representing a Gaussian function."""
    
    @staticmethod
    def function(x,A,m,s):
        """Gaussian function.

        Parameters:
            x (float):
                independent variable.
            A (float):
                value at `x=m`.
            m (float):
                central point.
            s (float):
                sigma.

        Returns:
            (float):
                `f(x) = A*exp(0.5*(x-m)^2 / s^2)`
        """
        return A*np.exp(- 0.5 * (x - m)**2 / s**2)
    
    def __init__(self,dragpoints: list[DragPoint],blit_manager: BlitManager):
        """Gaussian line between 2 DragPoints. Updates with them.

        Args:
            dragpoints (list[DragPoint]): line vertices.
            blit_manager (BlitManager): used for automatic ploting.
        """

        super().__init__(dragpoints,blit_manager)
        # name points based on use
        self.peak = self.dragpoints[0]
        self.side = self.dragpoints[1]
        self.update()

    def update(self,*args,**kargs):
        """Updates line data with DragObjects positions"""

        peak_x, side_x = self.get_xdata()
        A,m,s = self.get_args()

        #create x and y data of gaussian line of a gaussian that moves across two poitns
        dx = abs(peak_x-side_x) * 1.5
        x = np.linspace(min(peak_x,side_x)-dx,max(peak_x,side_x)+dx,250)
        y = self.function(x,A,m,s)

        #from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1,2)
        x_data, y_data = self.set_xy(xy).T

        #set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)

    def get_args(self):
        """Gives Gaussian function parameters.

        Returns:
            (Tuple[float, float, float]):
                `A`, `m`, and `s` of `f(x) = A*exp(0.5*(x-m)^2 / s^2)`
        """
        peak_x, peak_y = self.get_xy(*self.peak.patch.get_center())
        side_x, side_y = self.get_xy(*self.side.patch.get_center())

        if (peak_y < side_y and peak_y > 0) or \
           (peak_y >= side_y and peak_y < 0):
                peak_x, peak_y = self.get_xy(*self.side.patch.get_center())
                side_x, side_y = self.get_xy(*self.peak.patch.get_center())
        
        m = peak_x
        A = peak_y

        #create a case for negative peaks
        s =  abs(side_x-peak_x) * np.sqrt( 0.5 / np.log(abs(peak_y/side_y)) )
        
        return A,m,s
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

from . import DragPoint, DragPointCollection, BlitManager


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
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


class DragLorentzianManager(DragPointCollection):
    @staticmethod
    def function(x,A,x0,FWHM):
        """# TODO: make docstrings

        Args:
            x (float): _description_
            A (float): _description_
            x0 (float): _description_
            FWHM (float): _description_

        Returns:
            (float): _description_
        """
        
        return A/np.pi*(FWHM/2)/((x-x0)**2+(FWHM/2)**2)
    
    @staticmethod
    def get_args_length():
        """Gets number of arguments of `function`.

        Returns:
            (int): Number of arguments of `function`.
        """
        return 3
    
    def __init__(self,dragpoints: list[DragPoint],blit_manager: BlitManager):
        """Lorentzian line between 2 DragPoints. Updates with them.

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
        A,x0,FWHM = self.get_args()

        #create x and y data of Lorentzian line of a Lorentzian that moves across two points
        dx = abs(peak_x-side_x) * 1.5
        x = np.linspace(min(peak_x,side_x)-dx,max(peak_x,side_x)+dx,250)
        y = self.function(x,A,x0,FWHM)

        #from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1,2)
        x_data, y_data = self.set_xy(xy).T

        #set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)

    def get_args(self):
        """Gives Lorentzian function parameters.

        Returns:
            (tuple[float,float,float]): `A`, `x0`, and `FWHM` of `f(x) = A/pi*(FWHM/2)/((x-x0)^2+(FWHM/2)^2)`.
        """
        peak_x, peak_y = self.get_xy(*self.peak.patch.get_center())
        side_x, side_y = self.get_xy(*self.side.patch.get_center())

        if (peak_y < side_y and peak_y > 0) or \
           (peak_y >= side_y and peak_y < 0):
                peak_x, peak_y = self.get_xy(*self.side.patch.get_center())
                side_x, side_y = self.get_xy(*self.peak.patch.get_center())
        
        x0 = peak_x
        FWHM = 2*abs(peak_x-side_x)
        A = peak_y*FWHM/2*np.pi


        return A,x0,FWHM

class LorentzianFitter(GenericFitter):
    """Lorentzian function fitter."""
    name = 'lorentzian'

    def __init__(self,app,data: DataSelection):
        """ Lorentzian fitter following function `f(x) = A/pi*(FWHM/2)/((x-x0)^2+(FWHM/2)^2)`

        Parameters:
            app (Fitter):
                Main application.
            data (DataSelection):
                Data to fit.
        """

        super().__init__(app,data)

        ## Create DragPoints and DragLines needed

        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.5,0.7)), None),
                            DragPoint(*self.ax.transAxes.transform((0.7,0.3)), None)]
        self.drag_points_managers = [DragPointManager(p,self.app.blit_manager) for p in self.drag_points]
        self.fitter_drag_collection = DragLorentzianManager(self.drag_points, self.app.blit_manager)
        self.function = self.fitter_drag_collection.function

        ##Connect Lorentzian to Points change events
        self.drag_points_cids = [] #Connections ids for change events
        for dp in self.drag_points_managers:
            self.drag_points_cids.append(
                dp.connect(self.fitter_drag_collection.update)
            )
        self.drag_points_managers[1].add_restriction(self.res_fwhm)
        
        ## Add created DragPoints and DragLines to BlitManager's artists
        self.app.blit_manager.artists.append(self.fitter_drag_collection)
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        
        self.fig.canvas.draw_idle()

    def res_fwhm(self, x, y):
        return x, self.drag_points_managers[0].get_xy(*self.drag_points[0].patch.get_center())[1]/2


        
    
class LorentzianTool(GenericFitterTool):
    """Toggles Lorentzian Tool."""

    # default_keymap = ''
    description = 'Lorentz me please'

    def enable(self,*args):
        """Triggered when LorentzianTool is enabled,
        Uses BlitManager for faster rendering of DragObjects.
        """
        super().enable()
        self.fitter = LorentzianFitter(self.app,self.data)

    def disable(self,*args):
        """Triggered when LorentzianTool is disabled.
        Removes DragObjects and disables BlitManager.
        """
        super().disable()
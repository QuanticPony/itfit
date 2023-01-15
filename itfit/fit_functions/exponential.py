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

from . import GenericFitter, GenericFitterTool
from ..data import DataSelection
from ..utils import DragPoint, DragPointManager, DragExponentialManager

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
    default_toggled = False 
    radio_group = 'fitter'

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
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

import matplotlib.pyplot as plt
from matplotlib import path
from matplotlib.backend_tools import ToolToggleBase
from matplotlib.collections import RegularPolyCollection
from matplotlib.widgets import Lasso

from ..data import DataSelection


class LassoManager:
    """
    """
    def __init__(self, app, data: DataSelection):
        """Creates a lasso selector and applies the selection to the given data.

        Parameters:
            app (Fitter):
                Main application.
            data (DataSelection): 
                Data to apply selection.
        """
        self.app = app
        self.axes = app.ax
        self.canvas = self.axes.figure.canvas
        self.data = data

        self.Nxy = len(data.xdata)

        self.data.select_all()

        self.data.select_none()

        self.data_ploted = self.axes.plot(
            data.xdata, data.ydata, color=(0, 0, 0, 0))

        self.cid = self.canvas.mpl_connect('button_press_event', self.on_press)

        self.collection_facecolors = self.data.get_colors(
            (0, 1, 0, 1), (1, 0, 0, 1))
        self.collection = RegularPolyCollection(
            6, sizes=(40,),
            facecolors=self.collection_facecolors,
            offsets=self.data.get_data(),
            offset_transform=self.axes.transData)

        self.axes.add_collection(self.collection)

    def callback(self, verts):
        facecolors = self.collection.get_facecolors()
        # self.data_ploted.get_
        p = path.Path(verts)
        ind = p.contains_points(self.data.get_data())

        self.data.bool_selection(ind)
        facecolors = self.data.get_colors((0, 1, 0, 1), (1, 0, 0, 1))

        self.collection.set_facecolors(facecolors)
        self.delete()

    def delete(self):
        if hasattr(self, "lasso"):
            self.canvas.draw_idle()
            self.canvas.widgetlock.release(self.lasso)
            del self.lasso
        plt.disconnect(self.cid)
        self.cid = None

    def on_press(self, event):
        if self.canvas.widgetlock.locked():
            return
        if event.inaxes is None:
            return
        self.lasso = Lasso(event.inaxes,
                           (event.xdata, event.ydata),
                           self.callback)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)


class LassoTool(ToolToggleBase):
    """Toggles Lasso Tool."""
    # default_keymap = ''
    description = 'Lasso me please'

    def __init__(self, *args, app, data: DataSelection, **kwargs):
        """Creates a lasso tool.

        Parameters:
            app (Fitter): 
                Main application.
            data (DataSelection): 
                Data to apply selection.
        """
        self.app = app
        self.data = data
        super().__init__(*args, **kwargs)

    def enable(self, *args):
        """Enables the lasso tool. Interaction is locked until mouse button is released.
        """
        self.lasso_manager = LassoManager(self.app, self.data)

    def disable(self, *args):
        """Disables the lasso tool. After tool unselect or data selection applied.
        """
        self.lasso_manager.delete()
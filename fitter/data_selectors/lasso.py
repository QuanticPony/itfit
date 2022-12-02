import matplotlib.pyplot as plt
from matplotlib import path
from matplotlib.backend_tools import ToolToggleBase
from matplotlib.collections import RegularPolyCollection
from matplotlib.widgets import Lasso

from ..data import DataSelection


class LassoManager:
    def __init__(self, ax, data: DataSelection):
        self.axes = ax
        self.canvas = ax.figure.canvas
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
            offset_transform=ax.transData)

        ax.add_collection(self.collection)

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
    default_toggled = False
    radio_group = "fitter"

    def __init__(self, *args, app, data: DataSelection, **kwargs):
        self.app = app
        self.data = data
        super().__init__(*args, **kwargs)

    def enable(self, *args):
        self.lasso_manager = LassoManager(self.figure.get_axes()[0], self.data)

    def disable(self, *args):
        self.lasso_manager.delete()
from matplotlib.patches import CirclePolygon, Patch, Circle
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.artist import Artist
from matplotlib.path import Path
import numpy as np



class DragPoint:
    def __init__(self, x, y, style, *args):
        self._x = x
        self._y = y
        self._style = style
        
        self.patch = Circle(np.array([x,y]), 0.02)
        self.patch.set_animated = True


class DragPointManager:
    showverts = True
    epsilon = 5  # max pixel distance to count as a vertex hit

    def __init__(self, dragpoint, blink_manager):
        # if dragpoint.patch.figure is None:
        #     raise RuntimeError('You must first add the polygon to a figure '
        #                        'or canvas before defining the interactor')
        
        self.dragpoint = dragpoint
        self.blink_manager = blink_manager
        
        self.ax = blink_manager.ax
        self.canvas = blink_manager.canvas
        
        self.dragpoint.patch.set_transform(self.ax.transAxes)
        self.blink_manager.ax.add_patch(self.dragpoint.patch)
        
        self.poly = self.dragpoint.patch
        

        # x, y = zip(*self.poly.xy)
        x, y = self.poly.center
        # self.line = Line2D(x, y,
        #                    marker='o', markerfacecolor='r',
        #                    animated=True)
        # self.ax.add_line(self.line)

        self.cid = self.poly.add_callback(self.poly_changed)
        self._ind = None  # the active vert

        # canvas.mpl_connect('draw_event', self.on_draw)
        self.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('button_release_event', self.on_button_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def on_draw(self, event):...
        # self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        # self.ax.draw_artist(self.poly)
        # self.ax.draw_artist(self.line)
        # do not need to blit here, this will fire before the screen is
        # updated

    def poly_changed(self, poly):
        """This method is called whenever the pathpatch object is called."""
        # only copy the artist props to the line (except visibility)
        # vis = self.line.get_visible()
        # Artist.update_from(self.line, poly)
        # self.line.set_visible(vis)  # don't use the poly visibility state

    # def get_ind_under_point(self, event):
    #     """
    #     Return the index of the point closest to the event position or *None*
    #     if no point is within ``self.epsilon`` to the event position.
    #     """
    #     # display coords
    #     xy = np.asarray(self.poly.xy)
    #     xyt = self.poly.get_transform().transform(xy)
    #     xt, yt = xyt[:, 0], xyt[:, 1]
    #     d = np.hypot(xt - event.x, yt - event.y)
    #     indseq, = np.nonzero(d == d.min())
    #     ind = indseq[0]

    #     if d[ind] >= self.epsilon:
    #         ind = None

    #     return ind

    def on_button_press(self, event):
        """Callback for mouse button presses."""
        if not self.showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        # self._ind = self.get_ind_under_point(event)
        x, y = event.xdata, event.ydata
        if np.hypot(*(self.poly.center - np.array([x,y]))) < 1.5*self.poly.get_radius():
            self._ind = 0

    def on_button_release(self, event):
        """Callback for mouse button releases."""
        if not self.showverts:
            return
        if event.button != 1:
            return
        self._ind = None

    def on_key_press(self, event):
        """Callback for key presses."""
        if not event.inaxes:
            return
        # if event.key == 't':
        #     self.showverts = not self.showverts
        #     self.line.set_visible(self.showverts)
        #     if not self.showverts:
        #         self._ind = None
        # elif event.key == 'd':
        #     ind = self.get_ind_under_point(event)
        #     if ind is not None:
        #         self.poly.xy = np.delete(self.poly.xy,
        #                                  ind, axis=0)
        #         self.line.set_data(zip(*self.poly.xy))
        # elif event.key == 'i':
        #     xys = self.poly.get_transform().transform(self.poly.xy)
        #     p = event.x, event.y  # display coords
        #     for i in range(len(xys) - 1):
        #         s0 = xys[i]
        #         s1 = xys[i + 1]
        #         d = dist_point_to_segment(p, s0, s1)
        #         if d <= self.epsilon:
        #             self.poly.xy = np.insert(
        #                 self.poly.xy, i+1,
        #                 [event.xdata, event.ydata],
        #                 axis=0)
        #             self.line.set_data(zip(*self.poly.xy))
        #             break
        # if self.line.stale:
        #     self.canvas.draw_idle()

    def on_mouse_move(self, event):
        """Callback for mouse movements."""
        if not self.showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata

        prop = {'center': np.array([x,y])}
        Artist.update(self.poly, prop)
        
        self.blink_manager.draw()
        
        # self.poly.xy[self._ind] = x, y
        # if self._ind == 0:
        #     self.poly.xy[-1] = x, y
        # elif self._ind == len(self.poly.xy) - 1:
        #     self.poly.xy[0] = x, y
        # self.line.set_data(zip(*self.poly.xy))

        # self.canvas.restore_region(self.background)
        # self.ax.draw_artist(self.poly)
        # # self.ax.draw_artist(self.line)
        # self.canvas.blit(self.ax.bbox)
        
if __name__=='__main__':
    import matplotlib
    matplotlib.use('WXAgg')
    
    fig, ax = plt.subplots()
    a = DragPoint(0.5,0.5, 'o')
    a.patch.set_transform(ax.transAxes)
    ax.add_patch(a.patch)
    DragPointManager(ax, a)
    
    b = DragPoint(0.3,0.3, 'o')
    b.patch.set_transform(ax.transAxes)
    ax.add_patch(b.patch)
    DragPointManager(ax, b)
    
    plt.show()
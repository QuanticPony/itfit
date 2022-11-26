import numpy as np
import matplotlib.pyplot as plt
from matplotlib.artist import Artist

from . import DragPointManager, DragPoint

class BlitManager:

    def __init__(self, app):
        
        self.app = app
        
        self.artists = []
        
        self.ax = app.ax
        self.canvas = app.figure.canvas

        self.background = self.get_background()

        self.canvas.mpl_connect('draw_event', self.on_draw)
        # self.canvas.mpl_connect('button_press_event', self.on_button_press)
        # self.canvas.mpl_connect('key_press_event', self.on_key_press)
        # self.canvas.mpl_connect('button_release_event', self.on_button_release)
        # self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        

    def get_background(self):
        for a in self.artists:
            a.poly.set_visible(False)
            
        self.ax.clear()
        self.canvas.draw()
        return self.canvas.copy_from_bbox(self.ax.bbox)
    
    def draw(self):
        self.canvas.restore_region(self.background)
        
        for a in self.artists:
            a.poly.set_visible(True)
            a.update()
            self.ax.draw_artist(a.poly)
            
        self.canvas.blit(self.ax.bbox)
        
        
    def on_draw(self, event):
        self.draw()
        
if __name__=='__main__':
    import matplotlib
    matplotlib.use('WXAgg')
    
    class fi:
        def __init__(self):
            self.fig, self.ax = plt.subplots()
            
    f = fi()
    bm = BlitManager(f)
    
    a = DragPoint(0.5,0.5, '*')
    a.patch.set_transform(f.ax.transAxes)
    f.ax.add_patch(a.patch)
    am = DragPointManager(f.ax, a)
    
    b = DragPoint(0.3,0.3, 'o')
    b.patch.set_transform(f.ax.transAxes)
    f.ax.add_patch(b.patch)
    bm= DragPointManager(f.ax, b)
    
    bm.artists.append(am)
    bm.artists.append(bm)
    
    
    plt.show()
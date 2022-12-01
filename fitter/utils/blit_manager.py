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

        self.enabled = False
        self.background = None
        self.draw_event_connection_id = None
        

    def get_background(self):
        for a in self.artists:
            a.poly.set_visible(False)
        
        for a in self.ax.artists:
            self.ax.draw_artists(a)
            
        self.canvas.blit()

        return self.canvas.copy_from_bbox(self.ax.bbox)
    
    def update_background(self):
        self.background = self.get_background()
        

    def draw(self):
        self.canvas.restore_region(self.background)
        
        for a in self.artists:
            try: # if custom object
                a.poly.set_visible(True)
                a.update()
                self.ax.draw_artist(a.poly)
            except AttributeError: # if matplotlib artists
                a.set_visible(True)
                self.ax.draw_artist(a)
            
        self.canvas.blit(self.ax.bbox)
        
        
    def on_draw(self, event):
        self.draw()
        
    def enable(self):
        if not self.enabled:
            self.update_background()
            self.enabled = True
            self.draw_event_connection_id = self.canvas.mpl_connect('draw_event', self.on_draw)
            
    def disable(self):
        if self.enabled:
            self.enabled = False
            self.canvas.mpl_disconnect(self.draw_event_connection_id)
            self.draw_event_connection_id = None
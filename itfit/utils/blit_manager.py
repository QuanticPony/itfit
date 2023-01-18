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

class BlitManager:
    """**Do not use this class unless you know what blitting is and you are familiar with the rest of the code.**"""
    def __init__(self, app):
        """Class for managing blitting. DragObjects must be appended to `self.artists`.
        BlitManager must be manualy enabled and disabled.
        `with` statements can be used to enable or disable blitting temporaly.

        Parameters:
            app (Fitter):
                Aplication using BlitManager.
        """
        
        self.app = app
        self.ax = app.ax
        self.canvas = app.figure.canvas
        
        self.artists = []

        self._bind_motion_ : int = -1
        self._enabled_ = False
        self.background = None
        self.draw_event_connection_id = None
        
    def get_background(self):
        """"Gets current background and saves it, used in blitting process."""
        for a in self.artists:
            a.poly.set_visible(False)
        
        for a in self.ax.artists:
            self.ax.draw_artists(a)
            
        self.canvas.blit()

        return self.canvas.copy_from_bbox(self.ax.bbox)
    
    def update_background(self):
        """Updates saved background, used in blitting process."""
        self.background = self.get_background()

    def draw(self, artists_visible=True):
        """Draws the canvas using blitting."""
        if self.background is None:
            self.update_background()
        self.canvas.restore_region(self.background)
        
        for a in self.artists:
            try: # if custom object
                a.poly.set_visible(artists_visible)
                self.ax.draw_artist(a.poly)
            except AttributeError: # if matplotlib artists
                a.set_visible(artists_visible)
                self.ax.draw_artis(a)
            
        self.canvas.blit(self.ax.bbox)
        
    def on_draw(self, event):
        """Trigger for draw event."""
        self.draw()
              
    def enable(self):
        """Enables BlitManager."""
        if not self._enabled_:
            self.update_background()
            self._enabled_ = True
            self.draw_event_connection_id = self.canvas.mpl_connect('draw_event', self.on_draw)
            
    def disable(self):
        """Disables BlitManager."""
        if self._enabled_:
            self._enabled_ = False
            self.canvas.mpl_disconnect(self.draw_event_connection_id)
            self.draw_event_connection_id = None
      
    def enabled(self):
        """Enables Blit Manager and returns itself."""
        self.enable()
        return self     
     
    def disabled(self):
        """Disables BlitManager, redraws without DragObjects and returns itself."""
        self.disable()
        self.draw(artists_visible=False)
        return self
    
    @property
    def bind_motion(self):
        return self._bind_motion_
    
    @bind_motion.setter
    def bind_motion(self, new_id: int):
        # if (new_id is None) or (self._bind_motion_ is not None):
        if self._bind_motion_ == -1:
            self._bind_motion_ = new_id
        elif new_id is None:
            self._bind_motion_ = -1
            
        
    
    def __enter__(self, *_):
        pass
        
    def __exit__(self, *_):
        if not self._enabled_:
            self.enable()
        else:
            self.disable()
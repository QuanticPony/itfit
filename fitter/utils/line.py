from matplotlib.lines import Line2D

from . import DragPoint

class DragLineManager:
    def __init__(self, dragpoints: list[DragPoint], blit_manager):
        """Line between multiple DragPoints. Updates with them.

        Args:
            dragpoints (list[DragPoint]): line vertices.
            blit_manager (BlitManager): used for automtic ploting.
        """
        
        self.dragpoints = dragpoints
        self.blit_manager = blit_manager
        
        self.ax = blit_manager.ax
        self.canvas = blit_manager.canvas
        
        self.poly = Line2D(
            self.get_xdata_display(),
            self.get_ydata_display(),
            linestyle='-',
            color='red',
            transform=None
        )
        
        self.patch = self.blit_manager.ax.add_patch(self.poly)
        
        
    def update(self):
        """Updates the line information. Must be call prior to blit."""
        self.poly.set_xdata(self.get_xdata_display())
        self.poly.set_ydata(self.get_ydata_display())
        
    def get_xy(self, x, y):
        """Aplies correct transformation from display to data coordinates"""
        return self.ax.transData.inverted().transform((x,y))
    
    def set_xy(self, x, y):
        """Aplies correct transformation from data coordinates to display"""
        return self.ax.transData.transform((x,y))
        
    def get_xdata_display(self):
        return [p.patch.get_center()[0] for p in self.dragpoints]
    
    def get_ydata_display(self):
        return [p.patch.get_center()[1] for p in self.dragpoints]
    
    def get_xdata(self):
        return [self.get_xy(*p.patch.get_center())[0] for p in self.dragpoints]
    
    def get_ydata(self):
        return [self.get_xy(*p.patch.get_center())[1] for p in self.dragpoints]
    
    def remove(self):
        self.patch.remove()
        
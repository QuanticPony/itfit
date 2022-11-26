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
            [p.patch.get_center()[0] for p in self.dragpoints],
            [p.patch.get_center()[1] for p in self.dragpoints],
            linestyle='-',
            color='red',
            transform=self.ax.transAxes
        )
        
        self.blit_manager.ax.add_patch(self.poly)
        
        
    def update(self):
        """Updates the line information. Must be call prior to blit."""
        self.poly.set_xdata([p.patch.get_center()[0] for p in self.dragpoints])
        self.poly.set_ydata([p.patch.get_center()[1] for p in self.dragpoints])
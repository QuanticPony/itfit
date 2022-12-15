from matplotlib.lines import Line2D

from . import DragPoint, BlitManager

class DragPointCollection:
    """A collection of DragPoints used to implement complex interactive functions.
    All collections of DragPoints must inherit from DragPointCollection and implement the following methods:
    
    * function: `f(x, *args)` that returns a float.
    * update: updates `DragPointCollection.poly` with `DragPointCollection.dragpoints` positions.
    * get_args: returns arguments needed for function (`*args`). Must be derived from `DragPointCollection.dragpoints` positions.
    """

    @staticmethod
    def function(*args, **kargs): ... 
    def update(self, *args, **kargs):...
    def get_args(self):...
    
    # Common methods
    def __init__(self, dragpoints: list[DragPoint], blit_manager: BlitManager):
        """Collection of DragPoints. Used to implement more complicated DragObjects.
        
        Args:
            dragpoints (list[DragPoint]): collection vertices.
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
        
    def get_xy(self, *args):
        """Aplies and returns correct transformation from display to data coordinates.
        
        Parameters:
            *args (List[float,float] | List[List[float,float],...]):
                Coordinates from display.
        Returns:
            (Tuple[float,float] | Tuple[Tuple[float,float],...]):
                Coordinates from data.
        """

        args  = args if len(args)==2 else args[0]
        return self.ax.transData.inverted().transform(args)
    
    def set_xy(self, *args):
        """Aplies and returns correct transformation from data coordinates to display.
        
        Parameters:
            *args (List[float] | List[List[float,float]]):
                Coordinates from data.
        Returns:
            (Tuple[float] | Tuple[Tuple[float,float]]):
                Coordinates from display.
        """
        args  = args if len(args)==2 else args[0]
        return self.ax.transData.transform(args)
        
    def get_xdata_display(self):
        """Gets xdata from DragPoints in display coordinates.
        
        Returns:
            (Tuple[float]):
                x in display coordinates.
        """
        
        return [p.get_center()[0] for p in self.dragpoints]
    
    def get_ydata_display(self):
        """Gets ydata from DragPoints in display coordinates.
        
        Returns:
            (Tuple[float]):
                y in display coordinates.
        """
        return [p.get_center()[1] for p in self.dragpoints]
    
    def get_xdata(self):
        """Gets xdata from DragPoints in data coordinates.
        
        Returns:
            (Tuple[float]):
                x in data coordinates.
        """
        return [self.get_xy(*p.get_center())[0] for p in self.dragpoints]
    
    def get_ydata(self):
        """Gets ydata from DragPoints in data coordinates.
        
        Returns:
            (Tuple[float]):
                y in data coordinates.
        """
        return [self.get_xy(*p.get_center())[1] for p in self.dragpoints]
    
    def remove(self):
        """Removes the patch from the axes."""
        self.patch.remove()
        
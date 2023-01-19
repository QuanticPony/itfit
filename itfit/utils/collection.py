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
    @staticmethod
    def get_args_length():...
    def update(self, *args, **kargs):...
    def get_args(self):...
    
    # Common methods
    def __init__(self, dragpoints: list[DragPoint], blit_manager: BlitManager, *, linestyle='-', color='red'):
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
            linestyle=linestyle,
            color=color,
            transform=None
        )
        
        self.patch = self.blit_manager.ax.add_patch(self.poly)  
        
    def get_xy(self, *args):
        """Applies and returns correct transformation from display to data coordinates.
        
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
        """Applies and returns correct transformation from data coordinates to display.
        
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
        
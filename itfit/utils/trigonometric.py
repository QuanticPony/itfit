import numpy as np

from . import DragPoint, DragPointCollection, BlitManager


class DragTrigonometricManager(DragPointCollection):
    """Collection of DragPoints representing a trigonometric function."""
    
    @staticmethod
    def function(x, a, b, c, d):
        """Trigonometric function.

        Parameters:
            x (float):
                independent variable.
            a (float):
                Amplitude of the wave.
            b (float):
                frequency of the wave.
            c (float):
                centre of the trigonometric function.
            d (float):
                constant value around which the wave oscillates.

        Returns:
            (float):
                `f(x) = a*sin(b*x+c)+d`
        """
        return a*np.sin(b*x+c) + d 
    
    def __init__(self, dragpoints: list[DragPoint], blit_manager: BlitManager):
        """Trigonometric function between multiple DragPoints. Updates with them.

        Parameters:
            dragpoints (list[DragPoint]): wave points.
            blit_manager (BlitManager): used for automtic ploting.
        """
        super().__init__(dragpoints, blit_manager)
        self.point_1 = self.dragpoints[0]
        self.point_2 = self.dragpoints[1]
        self.update()
    
    def update(self, *args, **kargs):
        """Updates function data with DragObjects positions"""
        p1_x, p2_x = self.get_xdata()
        a,b,c,d = self.get_args()

        #create x and y data of trigonometric function that moves across two points
        dx = abs(p1_x-p2_x) * 1.5 
        x = np.linspace(min(p1_x,p2_x)-dx,max(p1_x,p2_x)+dx,250)
        y = self.function(x, a, b, c,d)
        
        # from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1, 2)
        x_data, y_data = self.set_xy(xy).T
        
        # set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)
 
    def get_args(self):
        """Gives trigonometrical function parameters.

        Returns:
            (Tuple[float, float]):
                `a`, `b`, `c` and `d` of `f(x)=a*sin(b*x +c)+d`.
        """
        x0, x1 = self.get_xdata()
        y0, y1 = self.get_ydata()

        a = abs(y0-y1)
        b = np.pi/2 / (x0-x1)
        c = -b *x1 
        d = y1

        return a, b, c, d
import numpy as np

from . import DragPointCollection, DragPoint, BlitManager


class DragQuadraticManager(DragPointCollection):
    @staticmethod
    def function(x, a, b, c):
        return a*x*x + b*x + c
    
    def __init__(self, dragpoints: list[DragPoint], blit_manager: BlitManager):
        """Quadratic line between 2 DragPoints. Updates with them.

        Args:
            dragpoints (list[DragPoint]): line vertices.
            blit_manager (BlitManager): used for automtic ploting.
        """
        super().__init__(dragpoints, blit_manager)
        # name points based on use
        self.center_point = self.dragpoints[0]
        self.lateral_point = self.dragpoints[1]
        self.update()
    
    def update(self, *args, **kargs):
        """Updates line data with DragObjects positions"""
        cp_x, lp_x = self.get_xdata()
        a,b,c = self.get_args()

        # create x and y data of quadratic line centered in center_point
        dx = abs(lp_x-cp_x)*1.5
        x = np.linspace(cp_x-dx, cp_x+dx, 250)
        y = self.function(x, a, b, c)
        
        # from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1, 2)
        x_data, y_data = self.set_xy(xy).T
        
        # set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)
        
    def get_args(self):
        """Gives quadratic function parameters.

        Returns
        -------
        Tuple(Float, Float, Float)
            `a`, `b` and `c` of `f(x)=a*x^2 + b*x + c`.
        """
        cp_x, cp_y = self.get_xy(*self.center_point.patch.get_center())
        lp_x, lp_y = self.get_xy(*self.lateral_point.patch.get_center())
        a = (lp_y - cp_y)/np.square(lp_x-cp_x)
        b = -2*a*cp_x
        c = cp_y + a*cp_x*cp_x
        return a,b,c
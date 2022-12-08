import numpy as np 
from . import BlitManager, DragPoint, DragPointCollection

class DragGaussianManager(DragPointCollection):
    @staticmethod
    def function(x,A,m,s):
        return A*np.exp(- 0.5 * (x - m)**2 / s**2)
    
    def __init__(self,dragpoints: list[DragPoint],blit_manager: BlitManager):
        """Gaussian line between 2 DragPoints. Updates with them.

        Args:
            dragpoints (list[DragPoint]): line vertices.
            blit_manager (BlitManager): used for automatic ploting.
        """

        super().__init__(dragpoints,blit_manager)
        # name points based on use
        self.peak = self.dragpoints[0]
        self.side = self.dragpoints[1]
        self.update()

    def update(self,*args,**kargs):
        """Updates line data with DragObjects positions"""

        peak_x, side_x = self.get_xdata()
        A,m,s = self.get_args()

        #create x and y data of gaussian line of a gaussian that moves across two poitns
        dx = abs(peak_x-side_x) * 1.5
        x = np.linspace(min(peak_x,side_x)-dx,max(peak_x,side_x)+dx,250)
        y = self.function(x,A,m,s)

        #from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1,2)
        x_data, y_data = self.set_xy(xy).T

        #set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)

    def get_args(self):
        """Gives Gaussian function parameters.

        Returns
        -------
        Tuple(Float,Float,Float)
            'A', 'm', and 's' of 'f(x) = A*exp(0.5*(x-m)^2 / s^2)'
        """
        peak_x, peak_y = self.get_xy(*self.peak.patch.get_center())
        side_x, side_y = self.get_xy(*self.side.patch.get_center())

        m = peak_x
        A = peak_y 

        s =  abs(side_x-peak_x) * np.sqrt( 0.5 / np.log(peak_y/side_y) )
        return A,m,s
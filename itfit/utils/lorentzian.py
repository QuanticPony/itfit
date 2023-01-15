import numpy as np

from . import BlitManager, DragPoint, DragPointCollection


class DragLorentzianManager(DragPointCollection):
    @staticmethod
    def function(x,A,x0,FWHM):
        """# TODO: make docstrings

        Args:
            x (_type_): _description_
            A (_type_): _description_
            x0 (_type_): _description_
            FWHM (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        return A/np.pi*(FWHM/2)/((x-x0)**2+(FWHM/2)**2)
    
    @staticmethod
    def get_args_length():
        """Gets number of arguments of `function`.

        Returns:
            (int): Number of arguments of `function`.
        """
        return 3
    
    def __init__(self,dragpoints: list[DragPoint],blit_manager: BlitManager):
        """Lorentzian line between 2 DragPoints. Updates with them.

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
        A,x0,FWHM = self.get_args()

        #create x and y data of Lorentzian line of a Lorentzian that moves across two points
        dx = abs(peak_x-side_x) * 1.5
        x = np.linspace(min(peak_x,side_x)-dx,max(peak_x,side_x)+dx,250)
        y = self.function(x,A,x0,FWHM)

        #from data coordinates to display coordinates
        xy = np.array((x,y)).T.reshape(-1,2)
        x_data, y_data = self.set_xy(xy).T

        #set new data
        self.poly.set_xdata(x_data)
        self.poly.set_ydata(y_data)

    def get_args(self):
        """Gives Lorentzian function parameters.

        Returns:
            (tuple[float,float,float]): `A`, `x0`, and `FWHM` of `f(x) = A/pi*(FWHM/2)/((x-x0)^2+(FWHM/2)^2)`.
        """
        peak_x, peak_y = self.get_xy(*self.peak.patch.get_center())
        side_x, side_y = self.get_xy(*self.side.patch.get_center())

        if (peak_y < side_y and peak_y > 0) or \
           (peak_y >= side_y and peak_y < 0):
                peak_x, peak_y = self.get_xy(*self.side.patch.get_center())
                side_x, side_y = self.get_xy(*self.peak.patch.get_center())
        
        x0 = peak_x
        FWHM = 2*abs(peak_x-side_x)
        A = peak_y*FWHM/2*np.pi


        return A,x0,FWHM
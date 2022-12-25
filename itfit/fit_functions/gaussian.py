from . import GenericFitter, GenericFitterTool
from ..data import DataSelection
from ..utils import DragPoint, DragPointManager, DragGaussianManager

class GaussianFitter(GenericFitter):
    """Gaussian function fitter."""
    name = 'gaussian'

    def __init__(self,app,data: DataSelection):
        """ Gaussian fitter following function `f(x) = A*exp(0.5*(x-m)^2/s^2)`

        Parameters:
            app (Fitter): 
                Main application.
            data (DataSelection): 
                Data to fit.
        """

        super().__init__(app,data)

        ## Create DragPoints and DragLines needed

        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.5,0.7)), None),
                            DragPoint(*self.ax.transAxes.transform((0.7,0.3)), None)]
        self.drag_points_managers = [DragPointManager(p,self.app.blit_manager) for p in self.drag_points]
        self.fitter_drag_collection = DragGaussianManager(self.drag_points, self.app.blit_manager)

        ##Connect Gaussian to Points change events
        self.drag_points_cids = [] #Connections ids for change events
        for dp in self.drag_points_managers:
            self.drag_points_cids.append(
                dp.connect(self.fitter_drag_collection.update)
            )
        
        ## Add created DragPoints and DragLines to BlitManager's artists
        self.app.blit_manager.artists.append(self.fitter_drag_collection)
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        
        self.fig.canvas.draw_idle()
    
class GaussianTool(GenericFitterTool):
    """Toggles Gaussian Tool."""

    # default_keymap = ''
    description = 'Gauss me please'
    default_toggled = False 
    radio_group = "fitter"

    def enable(self,*args):
        """Triggered when GaussianTool is enabled,
        Uses BlitManager for faster rendering of DragObjects.
        """

        super().enable()
        self.fitter = GaussianFitter(self.app,self.data)

    def disable(self,*args):
        """Triggered when GaussianTool is disabled.
        Removes DragObjects and disables BlitManager.
        """

        super().disable()

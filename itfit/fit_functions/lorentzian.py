from . import GenericFitter, GenericFitterTool
from ..data import DataSelection
from ..utils import DragPoint, DragPointManager, DragLorentzianManager

class LorentzianFitter(GenericFitter):
    """Lorentzian function fitter."""
    name = 'lorentzian'

    def __init__(self,app,data: DataSelection):
        """ Lorentzian fitter following function `f(x) = A/pi*(FWHM/2)/((x-x0)^2+(FWHM/2)^2)`

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
        self.fitter_drag_collection = DragLorentzianManager(self.drag_points, self.app.blit_manager)
        self.function = self.fitter_drag_collection.function

        ##Connect Lorentzian to Points change events
        self.drag_points_cids = [] #Connections ids for change events
        for dp in self.drag_points_managers:
            self.drag_points_cids.append(
                dp.connect(self.fitter_drag_collection.update)
            )
        self.drag_points_managers[1].add_restriction(self.res_fwhm)
        
        ## Add created DragPoints and DragLines to BlitManager's artists
        self.app.blit_manager.artists.append(self.fitter_drag_collection)
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        
        self.fig.canvas.draw_idle()

    def res_fwhm(self, x, y):
        return x, self.drag_points_managers[0].get_xy(*self.drag_points[0].patch.get_center())[1]/2


        
    
class LorentzianTool(GenericFitterTool):
    """Toggles Lorentzian Tool."""

    # default_keymap = ''
    description = 'Lorentz me please'
    default_toggled = False 
    radio_group = "fitter"

    def enable(self,*args):
        """Triggered when LorentzianTool is enabled,
        Uses BlitManager for faster rendering of DragObjects.
        """
        super().enable()
        self.fitter = LorentzianFitter(self.app,self.data)

    def disable(self,*args):
        """Triggered when LorentzianTool is disabled.
        Removes DragObjects and disables BlitManager.
        """
        super().disable()
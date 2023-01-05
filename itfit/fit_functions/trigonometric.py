from . import GenericFitter, GenericFitterTool
from ..data import DataSelection
from ..utils import DragPoint, DragPointManager, DragTrigonometricManager

class TrigonometricFitter(GenericFitter):
    """Trigonometric function fitter."""
    name = 'trigonometric'

    def __init__(self, app, data: DataSelection):
        """Trigonometric fitter following function 'f(x) = a*sin(b*x+b)'.
        
        Parameters:
            app (Fitter):
                Main application.
            data (DataSelection):
                Data to fit.
        """
        super().__init__(app,data)

        ##Create DragPoints and DragLines needed

        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.2,0.3)), None), 
                            DragPoint(*self.ax.transAxes.transform((0.8,0.7)), None)]
        self.drag_points_managers = [DragPointManager(p, self.app.blit_manager) for p in self.drag_points]
        self.fitter_drag_collection = DragTrigonometricManager(self.drag_points, self.app.blit_manager)

        ## Connect Line to Points change events
        self.drag_points_cids = [] # Connections ids for change events
        for dp in self.drag_points_managers:
            self.drag_points_cids.append(
                dp.connect(self.fitter_drag_collection.update)
            )

        ## Add created DragPoints and DragLines to BlitManager's artists
        self.app.blit_manager.artists.append(self.fitter_drag_collection)
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        
        self.fig.canvas.draw_idle()

class TrigonometricTool(GenericFitterTool):
    """Toggles Trigonometric Tool."""

    # default_keymap = ''
    description = 'Trig me please'
    default_toggled = False 
    radio_goup = "fitter"

    def enable(self,*args):
        """Triggered when TrigonometricTool is enabled.
        Uses BlitManager for faster rendering of DragObjects.
        """

        super().enable()
        self.fitter = TrigonometricFitter(self.app,self.data)
    
    def disable(self, *args):
        """Triggered when TrigonometricTool is disabled.
        Removes DragObjects and disables BlitManager.
        """

        super().disable()
        # If extra cleaning is needed
from . import GenericFitter, GenericFitterTool
from ..data import DataSelection
from ..utils import DragPoint, DragPointManager, DragExponentialManager

class ExponentialFitter(GenericFitter): #no me he atrevido a mirar generic fitter

    name = 'exponential'

    def __init__(self,app,data: DataSelection):
        """ Exponential fitter following function 'f(x) = a*exp(b*x)

        Parameters
        ----------
        app: Fitter
            Main application
        data : DataSelection
            Data to fit
        """

        super().__init__(app,data) #que hace super

        ##Create DragPOints and DragLines needed

        self.drag_points = [DragPoint(*self.ax.transAxes.transform((0.4,0.2)), None),
                            DragPoint(*self.ax.transAxes.transform((0.3,0.5)), None)] #las coordenadas inciales de los puntos
        self.drag_points_managers = [DragPointManager(p,self.app.blit_manager) for p in self.drag_points] # no entiendo esta
        self.fitter_drag_collection = DragExponentialManager(self.drag_points, self.app.blit_manager)

        ##Connect Exponential to Points change events

        self.drag_points_cids = [] #Connection ids for change events
        for dp in self.drag_points_managers:
            self.drag_points_cids.append(
                dp.connect(self.fitter_drag_collection.update)
            ) # lo mismo no acabo de entender la sintaxis, entiendo lo que ahce

        ## Add created DragPoints and DragLines to BlitManager's artists
        self.app.blit_manager.artists.append(self.fitter_drag_collection)
        for dpm in self.drag_points_managers:
            self.app.blit_manager.artists.append(dpm)
        self.fig.canvas.draw_idle()

class ExponentialTool(GenericFitterTool):
    """ Toggles Exponential Tool."""

    # default_keymap = '' 
    description = 'Exponentiate me please'
    default_toggled = False 
    radio_group = 'fitter'

    def enable(self,*args):
        """Triggered when ExponentialTool is enabled.
        Uses BLitManager for faster rendering of DragObjects.
        """ 
        super().enable()
        self.fitter = ExponentialFitter(self.app, self.data)

    def disable(self,*args):
        """ Triggered when ExponentialTool is disabled
        Removes DragObjects and disables BLitManager.
        """ 
        super().disable()
try:
    __FITTER_IMPORTED__
except NameError:
    __FITTER_IMPORTED__= False

if not __FITTER_IMPORTED__:
    from .point import DragPoint, DragPointManager
    from .line import DragLineManager
    from .blit_manager import BlitManager
    
    
__FITTER_IMPORTED__ = True
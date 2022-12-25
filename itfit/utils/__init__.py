"""TODO"""
try:
    __FITTER_UTILS_IMPORTED__
except NameError:
    __FITTER_UTILS_IMPORTED__= False

if not __FITTER_UTILS_IMPORTED__:
    from .blit_manager import BlitManager
    from .fit_container import FitResultContainer
    
    from .point import DragPoint, DragPointManager
    from .collection import DragPointCollection
    
    from .line import DragLineManager
    from .quadratic import DragQuadraticManager
    from .exponential import DragExponentialManager
    from .gaussian import DragGaussianManager
    
    LinearFunction = DragLineManager.function
    QuadraticFunction = DragQuadraticManager.function
    ExponentialFunction = DragExponentialManager.function
    GaussianFunction = DragGaussianManager.function
    
    
__FITTER_UTILS_IMPORTED__ = True
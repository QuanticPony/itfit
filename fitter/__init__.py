try:
    __FITTER_IMPORTED__
except NameError:
    __FITTER_IMPORTED__= False
    
__version__ = "0.0.3"

if not __FITTER_IMPORTED__:
    from . import data
    from . import fit_functions
    from . import data_selectors
    from .fitter_app import Fitter
    
    
__FITTER_IMPORTED__ = True
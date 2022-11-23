try:
    __FITTER_IMPORTED__
except NameError:
    __FITTER_IMPORTED__= False

if not __FITTER_IMPORTED__:
    from . import data
    from . import fit_functions
    from . import selectors
    from .fitter_app import Fitter
    
    
__FITTER_IMPORTED__ = True


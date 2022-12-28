"""TODO"""
try:
    __ITFIT_IMPORTED__
except NameError:
    __ITFIT_IMPORTED__= False
    
__version__ = "0.0.9"

if not __ITFIT_IMPORTED__:
    from . import data
    from . import fit_functions
    from . import data_selectors
    from .fitter_app import Fitter
    
    
__ITFIT_IMPORTED__ = True
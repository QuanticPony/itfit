try:
    __FITTER_FIT_FUNCTIONS_IMPORTED__
except NameError:
    __FITTER_FIT_FUNCTIONS_IMPORTED__= False

if not __FITTER_FIT_FUNCTIONS_IMPORTED__:
    from .linear import LineTool
    
__FITTER_FIT_FUNCTIONS_IMPORTED__ = True

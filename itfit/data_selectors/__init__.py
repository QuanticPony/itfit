"""TODO"""
try:
    __FITTER_SELECTORS_IMPORTED__
except NameError:
    __FITTER_SELECTORS_IMPORTED__= False

if not __FITTER_SELECTORS_IMPORTED__:
    from .lasso import LassoTool
    
__FITTER_SELECTORS_IMPORTED__ = True
"""TODO"""
try:
    __FITTER_PLOT_IMPORTED__
except NameError:
    __FITTER_PLOT_IMPORTED__= False

if not __FITTER_PLOT_IMPORTED__:
    from .builder import PlotBuilder
    
__FITTER_PLOT_IMPORTED__ = True
"""TODO"""
try:
    __FITTER_DATA_CLASSES_IMPORTED__
except NameError:
    __FITTER_DATA_CLASSES_IMPORTED__= False

if not __FITTER_DATA_CLASSES_IMPORTED__:
    from .data_classes import  DataContainer, DataSelection
    
__FITTER_DATA_CLASSES_IMPORTED__ = True

import matplotlib.pyplot as plt

from .data import DataSelection
from .selectors import LassoTool
from .fit_functions import LineTool

plt.rcParams['toolbar'] = 'toolmanager'

class Fitter:
    def __init__(self, xdata, ydata, *args, **kargs):
        self.data = DataSelection(xdata, ydata)
        self.figure = plt.figure()
        self.ax = self.figure.gca()
        self.fits = {}
        self.selections = {}
        
        
    def __call__(self):
        self.data_line = self.ax.plot(self.data.xdata, self.data.ydata)
        
        self.figure.canvas.manager.toolmanager.add_tool('Lasso', LassoTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Lasso', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Line', LineTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Line', 'fitter')

        plt.show()
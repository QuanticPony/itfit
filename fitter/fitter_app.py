# Copyright 2022 Unai Lería Fortea & Pablo Vizcaíno García

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import matplotlib.pyplot as plt

from .data import DataSelection
from .data_selectors import LassoTool
from .fit_functions import LineTool, QuadraticTool, ExponentialTool, GaussianTool
from .utils import BlitManager

plt.rcParams['toolbar'] = 'toolmanager'

class Fitter:
    def __init__(self, xdata, ydata, *args, **kargs):
        self.data = DataSelection(xdata, ydata)
        self.figure = plt.figure()
        self.ax = self.figure.gca()
        self.fits = {}
        self.selections = {}
        self.blit_manager = BlitManager(self)
        
        
    def __call__(self):
        self.data_line = self.ax.plot(self.data.xdata, self.data.ydata)
        
        self.figure.canvas.manager.toolmanager.add_tool('Lasso', LassoTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Lasso', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Line', LineTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Line', 'fitter')
        
        self.figure.canvas.manager.toolmanager.add_tool('Quadratic', QuadraticTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Quadratic', 'fitter')

        self.figure.canvas.manager.toolmanager.add_tool('Exponential', ExponentialTool, app=self, data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Exponential', 'fitter')

        self.figure.canvas.manager.toolmanager.add_tool('Gaussian', GaussianTool, app=self,data=self.data)
        self.figure.canvas.manager.toolbar.add_tool('Gaussian', 'fitter')

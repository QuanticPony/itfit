# Copyright 2023 Unai Lería Fortea & Pablo Vizcaíno García

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

def dataFunction(x, m, n):
    return m*x + n

noise = np.random.normal(size=200)

xdata = np.arange(200)
ydata = dataFunction(xdata, -2/200, 5) + noise

import matplotlib.pyplot as plt
import itfit

fitter = itfit.Fitter(xdata, ydata)
fitter()
plt.show()

plot = fitter.default_plot_last_fit("Time $[s^{-1}]$", "Value", "Title")
plt.show()

plot.save_fig("example.png")
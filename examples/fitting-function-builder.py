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

import matplotlib.pyplot as plt
import numpy as np
import itfit
from itfit.fit_functions import Gaussian, Line

def gauss(x, A, x0, sigma):
    return A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def dataFunction(x, m, n, A, x0, sigma):
    return m*x + n + gauss(x, A ,x0, sigma)

noise = np.random.normal(size=200)

xdata = np.arange(200)
ydata = dataFunction(xdata, -0.04, 5, np.random.random()
                     * 30, np.random.random()*200, 15) + noise



fitter = itfit.Fitter(xdata, ydata)
function_builder = itfit.FunctionBuilder(fitter)

function_builder.define(Gaussian + Line)

fitter()
fitter.add_custom_fit_function(function_builder)
plt.show()
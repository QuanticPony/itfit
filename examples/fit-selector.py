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
from itfit.fit_functions import Quadratic, Sine

def sine(x, A, phi):
    return A * np.sin(x/5+phi)

def quadratic(x, C, x0):
    return C*(x-x0)*(x-x0) + 1

def dataFunction(x, C, x0, A, phi):
    return sine(x, A, phi)/quadratic(x, C, x0)

noise = np.random.normal(size=200)

xdata = np.arange(200)
ydata = dataFunction(xdata, 0.005, 75, 50, 0.2) + noise



fitter = itfit.Fitter(xdata, ydata)
function_builder = itfit.FunctionBuilder(fitter)

function_builder.define(Sine / Quadratic)

fitter.add_custom_fit_function(function_builder)
fitter()



plot_builder = fitter.get_plot_builder()

plot_builder.plot_fit(color="pink").plot_fit_errors().with_data()


plt.show()
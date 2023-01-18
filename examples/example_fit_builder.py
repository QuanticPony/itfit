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

import itfit
import numpy as np
from tests import dataFunction
import matplotlib.pyplot as plt
import matplotlib 
matplotlib.use("Qt5Agg")

from itfit.fit_functions import *

noise = np.random.normal(size=200)

xdata = np.arange(200)
ydata = dataFunction(xdata, -0.04, 5, np.random.random()
                     * 30, np.random.random()*200, 15) + noise



fitter_app = itfit.Fitter(xdata, ydata)
function_builder = itfit.FunctionBuilder(fitter_app)

function_builder.define(Gaussian + Line * (Exponential))

fitter_app()
fitter_app.add_custom_fit_function(function_builder)
plt.show(block=True)

# fitter_app.default_plot_last_fit("$you^{up}$", "give", "Never gonna").save_fig("example.svg")
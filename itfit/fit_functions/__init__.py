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

"""TODO"""
try:
    __FITTER_FIT_FUNCTIONS_IMPORTED__
except NameError:
    __FITTER_FIT_FUNCTIONS_IMPORTED__= False

if not __FITTER_FIT_FUNCTIONS_IMPORTED__:
    from .generic.generic_fitter import GenericFitter, GenericFitterTool
    from .generic.function_container import FunctionContainer
    from .linear import LineTool
    from .quadratic import QuadraticTool
    from .exponential import ExponentialTool
    from .gaussian import GaussianTool
    from .lorentzian import LorentzianTool
    
    Line = FunctionContainer(linear.LineFitter, None)
    Quadratic = FunctionContainer(quadratic.QuadraticFitter, None)
    Exponential = FunctionContainer(exponential.ExponentialFitter, None)
    Gaussian = FunctionContainer(gaussian.GaussianFitter, None)
    Lorentzian = FunctionContainer(lorentzian.LorentzianFitter, None)
    
__FITTER_FIT_FUNCTIONS_IMPORTED__ = True
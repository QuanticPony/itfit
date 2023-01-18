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

"""#Fitting functions
All fitting functions inherit from GenericFitter and follow the same structure.
To create a new function you have 2 options:

* Use FunctionBuilder to create function from already created ones.
* Write a new fitter using GenericFitter.

Here we will

"""
try:
    __FITTER_FIT_FUNCTIONS_IMPORTED__
except NameError:
    __FITTER_FIT_FUNCTIONS_IMPORTED__= False

if not __FITTER_FIT_FUNCTIONS_IMPORTED__:
    from .common.generic_fitter import GenericFitter, GenericFitterTool
    from .common.function_container import FunctionContainer
    
    from .linear import Line
    from .gaussian import Gaussian
    from .exponential import Exponential
    from .quadratic import Quadratic
    from .lorentzian import Lorentzian
    from .cosine import Cosine
    from .sine import Sine
    
__FITTER_FIT_FUNCTIONS_IMPORTED__ = True
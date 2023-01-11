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
    __FITTER_UTILS_IMPORTED__
except NameError:
    __FITTER_UTILS_IMPORTED__= False

if not __FITTER_UTILS_IMPORTED__:
    from .blit_manager import BlitManager
    from .fit_container import FitResultContainer
    
    from .point import DragPoint, DragPointManager
    from .collection import DragPointCollection
    
    from .line import DragLineManager
    from .quadratic import DragQuadraticManager
    from .exponential import DragExponentialManager
    from .gaussian import DragGaussianManager
    
    LinearFunction = DragLineManager.function
    QuadraticFunction = DragQuadraticManager.function
    ExponentialFunction = DragExponentialManager.function
    GaussianFunction = DragGaussianManager.function
    
    
__FITTER_UTILS_IMPORTED__ = True
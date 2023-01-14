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
    __FITTER_SELECTORS_IMPORTED__
except NameError:
    __FITTER_SELECTORS_IMPORTED__= False

if not __FITTER_SELECTORS_IMPORTED__:
    from .lasso import LassoTool
    
__FITTER_SELECTORS_IMPORTED__ = True
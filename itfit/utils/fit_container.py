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


class FitResultContainer:
    def __init__(self, data, fit_manager, scipy_result):
        """_summary_

        Parameters:
            data (itfit.data.DataContainer):
                Data fitted.
            fit_manager (itfit.fit_functions.GenericFitter):
                Fit function used
            scipy_result (dict):
                Dictionary of `scipy.optimize.curve_fit` output.
        """
        self.data = data
        self.function = fit_manager.function
        self.gradient = fit_manager.gradient
        self.fit_manager = fit_manager
        self.scipy_output = {
            "popt" : scipy_result[0],
            "pcov" : scipy_result[1],
            "fvec" : scipy_result[2]["fvec"],
            "nfev" : scipy_result[2]["nfev"],
            "fjac" : scipy_result[2]["fjac"],
            "ipvt" : scipy_result[2]["ipvt"],
            "qtf"  : scipy_result[2]["qtf"],
            "mesg" : scipy_result[3],
            "ier"  : scipy_result[4] 
        }
        
    def get_parameters(self):
        """Gets the optimal fitting parameters found.

        Returns:
            (Tuple[float]):
                Tuple of parameters.
        """
        return self.scipy_output["popt"]
        
    def get_parameters_covariance(self):
        """Gets the parameters covariance matrix.

        Returns:
            (Ndarray(NxN)[float]):
                Parameters covariance matrix.
        """
        return self.scipy_output["pcov"]
        
    def get_parameters_errors(self):
        """Gets the square root of diagonal elements of the covariance matrix.

        Returns:
            (Tuple[float]):
                Optimal fitting parameters standard error.
        """
        return np.sqrt(np.diag(self.get_parameters_covariance()))

    def get_xdata(self):
        """Gets the x component of the data used.

        Returns:
            (Tuple[float]):
                X component of data used.
        """
        return self.data.xdata
        
    def get_ydata(self):
        """Gets the y component of the data used.

        Returns:
            (Tuple[float]):
                Y component of data used.
        """
        return self.data.ydata
    
    def get_data(self):
        """Gets the data used.

        Returns:
            (Tuple[Tuple[float], Tuple[float]]):
                Data used.
        """
        return self.data.get_data()

    def prop_errors(self):
        """ Return the error of the fit, given a gradient of a function.

        Returns:
            (Tuple[float]):
                errors of the fit
        """
        try:
            errors = [ np.sqrt( float(self.gradient (xi,*self.get_parameters()).T @ self.get_parameters_covariance() @ self.gradient (xi,*self.get_parameters()))) for xi in self.get_fit_xdata()     ]
        except AttributeError:
            return None
        return errors


    def get_fit_xdata(self):
        """Gets the x component of the fit curve. Equal to get_xdata output.

        Returns:
            (Tuple[float]):
                X component of fit curve. Equal to get_xdata output.
        """
        return self.get_xdata()
    
    def get_fit_ydata(self):
        """Gets the y coomponent of the fit curve.

        Returns:
            (Tuple[float]):
                Y component of fit curve.
        """
        return self.get_ydata() + self.scipy_output["fvec"]
    
    def get_fit_data(self):
        """Gets the fit curve data.

        Returns:
            (Tuple[Tuple[float], Tuple[float]]):
                Fit curve data.
        """
        return np.array((self.get_fit_xdata(), self.get_fit_ydata())).T
    
    def get_message(self):
        """Gets scipy output `mesg` output.

        Returns:
            (str):
                Scipy output message.
        """
        return self.scipy_output["mesg"]
    
    def evaluate(self, x):
        """Evaluates the given `x` in the fitting function with the optimal parameters.

        Parameters:
            x (float): 
                Independent variable.

        Returns:
            y (float): 
                Dependent variable.
        """
        return self.function(x, *self.get_parameters())
    
    def save(self, filename): # TODO:
        ...
    
    @classmethod    
    def load(cls, filename): # TODO:
        ...
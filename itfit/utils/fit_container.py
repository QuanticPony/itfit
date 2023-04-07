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

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..data import DataSelection
    from ..fit_functions.common import FunctionContainer, GenericFitter


import numpy as np


class FitResultContainer:
    def __init__(self, data: DataSelection, fit_manager: FunctionContainer|GenericFitter, scipy_result: dict):
        """_summary_

        Parameters:
            data (itfit.data.DataSelection):
                Data fitted.
            fit_manager (FunctionContainer|GenericFitter):
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
            (tuple[float]):
                tuple of parameters.
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
            (tuple[float]):
                Optimal fitting parameters standard error.
        """
        return np.sqrt(np.diag(self.get_parameters_covariance()))

    def get_xdata(self):
        """Gets the x component of all the data.

        Returns:
            (tuple[float]):
                X component of all the data.
        """
        return self.data.xdata
    
    def get_xdata_errors(self):
        """Gets the x component error in all the data.

        Returns:
            (tuple[float]):
                X component error of all the data.
        """
        return self.data.get_errors()[0]
        
    def get_ydata(self):
        """Gets the y component of all the data.

        Returns:
            (tuple[float]):
                Y component of all data.
        """
        return self.data.ydata
    
    def get_ydata_errors(self):
        """Gets the y component error in all the data.

        Returns:
            (tuple[float]):
                Y component error of all the data.
        """
        return self.data.get_errors()[1]
    
    def get_xdata_selected(self):
        """Gets the x component of the data used.

        Returns:
            (tuple[float]):
                X component of data used.
        """
        return self.data.get_selected()[0]
    
    def get_xdata_errors_selected(self):
        """Gets the x component error in data used.

        Returns:
            (tuple[float]):
                X component error of data used.
        """
        return self.data.get_selected_errors()[0]
    
    def get_ydata_selected(self):
        """Gets the y component of the data used.

        Returns:
            (tuple[float]):
                Y component of data used.
        """
        return self.data.get_selected()[1]
    
    def get_ydata_errors_selected(self):
        """Gets the y component error in data used.

        Returns:
            (tuple[float]):
                Y component error of data used.
        """
        return self.data.get_selected_errors()[1]
    
    def get_data(self):
        """Gets the all data.

        Returns:
            (tuple[tuple[float], tuple[float]]):
                All data.
        """
        return self.data.get_data()
    
    def get_data_selected(self):
        """Gets the data used.

        Returns:
            (tuple[tuple[float], tuple[float]]):
                Data used.
        """
        return np.array(self.data.get_selected()).T

    def prop_errors(self):
        """ Return the error of the fit, given a gradient of a function.

        Returns:
            (Tuple[float]):
                errors of the fit
        """
        try:
            x_array = self.get_fit_xdata()
            errors = np.zeros((len(x_array)))
            cov = self.get_parameters_covariance()

            for i,x in enumerate(x_array):
                grad = self.gradient(x, *self.get_parameters())
                errors[i] = np.sqrt( float(grad.T @ cov @ grad))
        except AttributeError:
            return None
        return errors


    def get_fit_xdata(self):
        """Gets the x component of the fit curve. Equal to get_xdata output.

        Returns:
            (tuple[float]):
                X component of fit curve. Equal to get_xdata output.
        """
        return self.get_xdata()
    
    def get_fit_ydata(self):
        """Gets the y coomponent of the fit curve.

        Returns:
            (tuple[float]):
                Y component of fit curve.
        """
        return self.function(self.get_xdata(), *self.get_parameters())
    
    def get_fit_xdata_selected(self):
        """Gets the x component of the fit curve for selected data interval. Equal to get_xdata_selected output.

        Returns:
            (tuple[float]):
                X component of fit curve. Equal to get_xdata output.
        """
        return self.get_xdata_selected()
    
    def get_fit_ydata_selected(self):
        """Gets the y coomponent of the fit curve for selected data interval.

        Returns:
            (tuple[float]):
                Y component of fit curve.
        """
        return self.function(self.get_xdata_selected(), *self.get_parameters())
    
    def get_fit_data(self):
        """Gets the fit curve data for all data.

        Returns:
            (tuple[tuple[float], tuple[float]]):
                Fit curve data.
        """
        return np.array((self.get_fit_xdata(), self.get_fit_ydata())).T
    
    def get_fit_data_selected(self):
        """Gets the fit curve data for selected data.

        Returns:
            (tuple[tuple[float], tuple[float]]):
                Fit curve data.
        """
        return np.array((self.get_fit_xdata_selected(), self.get_fit_ydata_selected())).T
    
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
    
    def error_verts(self, only_selected: bool=True):
        """Returns a tuple of two lists of points representing the error of the optimization. 
        Each lists size is Nx2 or None if errors in the function are not supported.

        Parameters:
            only_selected (bool):
                Only get errors points for selected data. Defaults to True.

        Returns:
            (tuple[list]|tuple[None]): Positive and negative error points.
        """
        xdata, _  = self.data.get_selected() if only_selected else self.data.get_data().T
        error_fit = self.prop_errors()
        if error_fit is not None:
            iy_pos = self.evaluate(xdata)+error_fit
            verts_positive = [(xdata[0],self.evaluate(xdata[0])), *zip(xdata,iy_pos), (xdata[len(xdata)-1],self.evaluate(xdata[len(xdata)-1]))]
            
            iy_neg = self.evaluate(xdata)-error_fit
            verts_negative = [(xdata[0],self.evaluate(xdata[0])), *zip(xdata,iy_neg), (xdata[len(xdata)-1],self.evaluate(xdata[len(xdata)-1]))]
            return verts_positive, verts_negative
        return (None, None)
                

    def __str__(self):
        TAB = "\t"
        NEX = "\n"

        return f"""ItFit FitResultContainer
Using fit function: {self.fit_manager.name}
Scipy result message: {self.get_message()}

Optimal parameters: 
{TAB}values: {self.get_parameters()}
{TAB}errors: {self.get_parameters_errors()}
{TAB}covariance:
{TAB}{TAB}[{(NEX + TAB*2 +" ").join([str(l) for l in self.get_parameters_covariance()])}]
"""
        
    def save(self, filename):
        """Creates a .txt with the fit results.
        Format of the text file:
        #Function: function
        #best fit parameter: parameters

        #xdata #xerror #ydata #yerror #function 

        """

        __, func_selected = self.get_fit_data_selected()
        x_selected, y_selected = self.get_xdata_selected(), self.get_ydata_selected()
        xerror, yerror=    self.get_xdata_errors_selected(), self.get_ydata_errors_selected()

        parameters, errors = self.get_parameters(), self.get_parameters_errors()

        with open(filename,'w') as f:
            f.write('#Best fit parameters:', parameters, errors, '\n')
            f.write('#xdata #xerror #ydata #yerror #function\n')
            for i in range(len(x_selected)):
                f.write(x_selected[i], xerror[i], y_selected[i], yerror[i], func_selected[i], '\n') 

    
    @classmethod    
    def load(cls, filename): # TODO:
        ...
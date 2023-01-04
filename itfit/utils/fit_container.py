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
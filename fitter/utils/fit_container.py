import numpy as np


class FitResultContainer:
    def __init__(self, data, fit_manager, scipy_result):
        """_summary_

        Parameters
        ----------
        data (DataContainer):
            Data fitted.
        fit_manager (GenericFitter):
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
        return self.scipy_output["popt"]
        
    def get_parameters_covariance(self):
        return self.scipy_output["pcov"]
        
    def get_parameters_errors(self):
        return np.sqrt(np.diag(self.get_parameters_covariance()))

    def get_xdata(self):
        return self.data.xdata
        
    def get_ydata(self):
        return self.data.ydata
    
    def get_data(self):
        return self.data.get_data()

    def get_fit_xdata(self):
        return self.get_data()
    
    def get_fit_ydata(self):
        return self.get_ydata() + self.scipy_output["fvec"]
    
    def get_fit_data(self):
        return np.array((self.get_fit_xdata(), self.get_fit_ydata())).T
    
    def get_message(self):
        return self.scipy_output["mesg"]
    
    def evaluate(self, x):
        return self.function(x, *self.get_parameters())
    
    def save(self, filename): # TODO:
        ...
    
    @classmethod    
    def load(cls, filename): # TODO:
        ...
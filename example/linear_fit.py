import matplotlib.pyplot as plt
import numpy as np

from fitter.data import DataSelection
from fitter.data_selectors import LassoTool
from fitter.fit_functions import LineTool
from fitter import Fitter



def main(filename):
    values =  np.random.normal(size=200)

    xdata = np.array(range(len(values))) - len(values)/2
    ydata = -(xdata*xdata/1000) + values
    
    f = Fitter(xdata, ydata)
    f()
    
if __name__=='__main__':
    main("data.txt")
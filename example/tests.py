import matplotlib.pyplot as plt
import numpy as np

from itfit import Fitter
import pylustrator

def gauss(x, A, x0, sigma):
    return A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def dataFunction(x, m,n, A, x0, sigma):
    return m*x + n + gauss(x, A ,x0, sigma)


def main():
    noise =  np.random.normal(size=200)

    xdata = np.arange(200)
    ydata = dataFunction(xdata, -0.04, 5, 20, 120,15) + noise
    
    fitter_app = Fitter(xdata, ydata)
    fitter_app()
    
    plt.show()
        
    for fit in fitter_app.fits.values():  
        fig, ax = plt.subplots()
        ax.plot(xdata, ydata)
        fit_line, = ax.plot(fit.get_xdata(), fit.get_fit_ydata(), '--', c='black')
        # fit_line, = ax.plot(fit.get_xdata(), fit.get_ydata() + fit.scipy_output["fvec"], '--', c='black')
        
        print(fit.get_parameters())
        print(fit.get_parameters_errors())

        ax.grid()
        
    plt.show()
    
    pylustrator.start()
    fit, = fitter_app.fits.values()
    plt.figure(5)
    plt.clf()
    plt.plot(xdata, ydata)
    plt.plot(fit.get_xdata(), fit.get_ydata() + fit.scipy_output["fvec"])
    plt.show()
    
if __name__=='__main__':
    main()
import matplotlib.pyplot as plt
import numpy as np

from fitter import Fitter

def gauss(x, A, x0, sigma):
    return A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

def dataFunction(x, m,n, A, x0, sigma):
    return m*x + n + gauss(x, A ,x0, sigma)


def main():
    noise =  np.random.normal(size=200)

    xdata = np.arange(200)
    ydata = dataFunction(xdata, -0.04, 5, 20, 120,15) + noise
    
    f = Fitter(xdata, ydata)
    f()
    
    plt.show()
    
if __name__=='__main__':
    main()
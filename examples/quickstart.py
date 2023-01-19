import numpy as np

def dataFunction(x, m, n):
    return m*x + n

noise = np.random.normal(size=200)

xdata = np.arange(200)
ydata = dataFunction(xdata, -2/200, 5) + noise

import matplotlib.pyplot as plt
import itfit

fitter = itfit.Fitter(xdata, ydata)
fitter()
plt.show()

plot = fitter.default_plot_last_fit("Time $[s^{-1}]$", "Value", "Title")
plt.show()

plot.save_fig("example.png")
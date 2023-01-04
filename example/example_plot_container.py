import itfit
import numpy as np
from tests import dataFunction, gauss
import matplotlib.pyplot as plt

noise = np.random.normal(size=200)

xdata = np.arange(200)
ydata = dataFunction(xdata, -0.04, 5, np.random.random()
                     * 30, np.random.random()*200, 15) + noise

fitter_app = itfit.Fitter(xdata, ydata)

fitter_app()
plt.show()

fit = fitter_app.get_plot_builder()\
    .plot_fit(':', 'red', 'test')\
    .with_data('.', 'black', 'data')\
    .grid()\
    .legend()\
    .set_xlim(-10, 220)\
    .set_ylim(-10, 30)\
    .xlabel("label_x").fontsize(8).color('red').end_xlabel()\
    .ylabel("y_label").fontsize(14).color('blue').end_ylabel()\
    .title("Duck").fontsize(21).color('green').end_title()

plt.show()



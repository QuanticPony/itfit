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
    .labels()\
        .start_x_label("label_x").fontsize(8).color('red').end_xlabel()\
        .start_y_label("y_label").fontsize(14).color('blue').end_ylabel()\
    .end_labels()\
    .title("Duck").fontsize(21).color('green').end_title()\
    .spines().start_top_spine().invisible().end_top_spine()\
             .start_right_spine().alpha(0.33).end_right_spine()\
             .start_bottom_spine().linestyle('--').color('purple').linewidth(3).end_bottom_spine()\
    .end_spines()

plt.show()



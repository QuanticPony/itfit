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
    .style("science")\
    .plot_fit(':', 'red', 'test')\
    .with_data('.', 'black', 'data')\
    .xlabel("time [s]")\
    .ylabel("current [mA]")\
    .title("Experiment")\
    .grid()\
    .legend()\
    .set_xlim(-10, 220)\
    .set_ylim(-10, 30)\
    .spines().start_top_spine().invisible().end_top_spine()\
             .start_right_spine().alpha(0.33).color("white").end_right_spine()\
             .start_bottom_spine().linestyle('--').color('purple').linewidth(3).end_bottom_spine()\
    .end_spines()\
    .set_size((12,9))\
    .tight_layout()

plt.show()
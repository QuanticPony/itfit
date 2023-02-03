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
    from matplotlib.lines import Line2D
    
    from .. import Fitter
    from ..plot import PlotBuilder
    
import asyncio
import matplotlib.pyplot as plt



class FitSelector:
    def __init__(self, app: Fitter):
        self.app = app
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Click on legend line to toggle line on/off')
        x_data, y_data = self.app.data.get_selected()
        line_data, = self.ax.plot(x_data, y_data, '.', c='black', label="data")
        if self.app.data.yerr:
            line_data_errs = self.ax.errorbar(x_data, y_data, yerr=self.app.data.get_selected_errors()[1], fmt=None, ecolor='black')
        
        self.fit_lines: list[Line2D] = [line_data]
        self.legend_to_lines_map: dict[Line2D, Line2D] = {}
        self.lines_to_hash: dict[Line2D, int] = {}
        
        for key, fit in self.app.fits.items():
            line, = self.ax.plot(fit.get_fit_xdata(), fit.get_fit_ydata(), label=f"{fit.fit_manager.name}:{key}")
            self.fit_lines.append(line)
            self.lines_to_hash.update({line : key})
            

    def set_multiple_selection_mode(self):
        legend = self.ax.legend()
        
        for legend_line, original_line in zip(legend.get_lines(), self.fit_lines):
            legend_line.set_picker(True)
            self.legend_to_lines_map[legend_line] = original_line
            
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
    
    def set_single_selection_mode(self):
        for line in self.fit_lines:
            line.set_picker(True)
            
        self.fig.canvas.mpl_connect('pick_event', self.on_pick_single)
        self.fig.show()
        
        
    def on_pick(self, event):
        legline = event.artist
        origline = self.legend_to_lines_map[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        
        legline.set_alpha(1.0 if visible else 0.2)
        self.fig.canvas.draw()

    def on_pick_single(self, event):
        self._key = self.lines_to_hash.get(event.artist)
        self.fig.canvas.stop_event_loop()
        return 
        
    def get_selected_single(self):
        plt.close(self.fig)
        return self._key
            
    def get_selected(self):
        result: list[int] = []
        for line in self.fit_lines:
            if line.get_visible():
                if val := self.lines_to_hash.get(line):
                    result.append(val) 
        return result
    
    def connect_select_one(self, plotBuilder: PlotBuilder):
        self._key = False
        self.plotBuilder = plotBuilder
        self.set_single_selection_mode()
        self.fig.show()
        self.fig.canvas.start_event_loop()
        return self
        
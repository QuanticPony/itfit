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

import matplotlib.pyplot as plt


class FitSelector:
    def __init__(self, app: Fitter):
        """Allows to select fits inside a figure, via click.

        Args:
            app (Fitter): Fitter aplication source of fits and data.
        """
        self.app = app
        
        self.fig, self.ax = plt.subplots()
        x_data, y_data = self.app.data.get_data().T
        line_data, = self.ax.plot(x_data, y_data, '.', c='black', label="data")
        
        self._key : int|list[int]
        self._mode_: str
        self.fit_lines: list[Line2D] = [line_data]
        self.legend_to_lines_map: dict[Line2D, Line2D] = {}
        self.lines_to_hash: dict[Line2D, int] = {}
        
        for key, fit in self.app.fits.items():
            line, = self.ax.plot(fit.get_fit_xdata(), fit.get_fit_ydata(), label=f"{fit.fit_manager.name}:{key}")
            self.fit_lines.append(line)
            self.lines_to_hash.update({line : key})
            

    def set_multiple_selection_mode(self):
        """Starts multiple selection mode picker and sets title.
        """
        self.ax.set_title('Click on legend line to toggle line on/off')
        self._mode_ = 'm'
        legend = self.ax.legend()
        
        for legend_line, original_line in zip(legend.get_lines(), self.fit_lines):
            legend_line.set_picker(True)
            self.legend_to_lines_map[legend_line] = original_line
            
        self.fig.canvas.mpl_connect('pick_event', self.on_pick_multiple)
        self.fig.show()
    
    def set_single_selection_mode(self):
        """Starts single selection mode picker and sets title.
        """
        self.ax.set_title('Click line to select it')
        self._mode_ = 's'
        for line in self.fit_lines:
            line.set_picker(True)
            
        self.fig.canvas.mpl_connect('pick_event', self.on_pick_single)
        self.fig.show()
        
        
    def on_pick_multiple(self, event):
        """Pick event for multiple selection mode.
        """
        legline = event.artist
        origline = self.legend_to_lines_map[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        
        legline.set_alpha(1.0 if visible else 0.2)
        self.fig.canvas.draw()

    def on_pick_single(self, event):
        """Pick event for single selection mode.
        """
        k = self.lines_to_hash.get(event.artist)
        if isinstance(k, int):
            self._key = k
        self.fig.canvas.stop_event_loop()
        return 
        
    def get_selected_from_figure(self):
        """Gets the lines selected on multiple selection mode based on visibility.
        """
        result: list[int] = []
        for line in self.fit_lines:
            if line.get_visible():
                if val := self.lines_to_hash.get(line):
                    result.append(val) 
        self.fig.canvas.stop_event_loop()
        self._key = result

    def get_selected(self):
        """Returns the selected fit/s.

        Returns:
            (int, list[int]): Keys of fits selected.
        """
        if self._mode_ == 'm':
            self.get_selected_from_figure()
        plt.close(self.fig)
        return self._key
    
    def connect_select_one(self):
        """Starts fit selection figure and waits for it to finish.

        Returns:
            (itFit.FitSelector): returns itself.
        """
        self._key = False
        self.set_single_selection_mode()
        self.fig.show()
        self.fig.canvas.start_event_loop()
        return self

            
    def connect_select_multiple(self):
        """Starts fit selection figure and waits for it to finish.

        Returns:
            (itFit.FitSelector): returns itself.
        """
        self._key = False
        self.set_multiple_selection_mode()
        self.fig.show()
        self.fig.canvas.start_event_loop()
        return self
        
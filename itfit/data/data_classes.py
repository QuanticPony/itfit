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

import numpy as np

class DataContainer:
    """Container for data.
    """
    def __init__(self, xdata: list, ydata: list, yerr: list|None=None, xerr: list|None=None):
        """Creates a DataContainer.

        Parameters:
            xdata (list[float]):
                x data.
            ydata (list[float]):
                y data.
            yerr (list | None, optional): 
                Error en y data. Defaults to None.
            xerr (list | None, optional): 
                Error in x data. Defaults to None.
        """
        self.xdata = np.array(xdata).copy()
        self.ydata = np.array(ydata).copy()
        self.xerr  = np.array(xerr).copy() if xerr is not None else None
        self.yerr  = np.array(yerr).copy() if yerr is not None else None
        
    def length(self):
        """Returns lenght of data.

        Returns:
            (int):
                lenght of data.
        """
        return self.xdata.size
    
    def get_data(self):
        """Returns data. As list of tuples: `lenght x 2`.

        Returns:
            (tuple[tuple[float, float]]):
                Data stored.
        """
        return np.array((self.xdata, self.ydata)).T
    
    def get_errors(self):
        """Returns data errors. A list of tuples: `lenght x2`.

        Returns:
            (tuple[tuple[float,float]]): 
                Errors in data stored.
        """
        return np.array((self.xerr, self.yerr), dtype=object).T

        
class DataSelection(DataContainer):
    def __init__(self, xdata, ydata, yerr: list|None=None, xerr: list|None=None):
        super().__init__(xdata, ydata, yerr=yerr, xerr=xerr)
        self.indexes_used = np.ones(len(self.xdata), dtype=bool)  
        
    def select_all(self):
        """Selects all data.
        """
        self.indexes_used[:] = True
        
    def select_none(self):
        """Unselect all data.
        """
        self.indexes_used[:] = False

    def add_selection(self, indexes: list):
        """Adds `indexes` to `indexes_used`.

        Parameters:
            indexes (list): 
                list of index.
        """
        self.indexes_used[np.array(indexes)] = True
        
    def selection(self, indexes):
        """Erase previous selected indexes. Adds `indexes` to `indexes_used`.

        Parameters:
            indexes (list):
                list of index.
        """
        self.indexes_used[:] = False
        self.add_selection(indexes)
        
    def bool_selection(self, indexes_used):
        """Erase previous selected indexes. Sets new `indexes_used`.

        Parameters:
            indexes_used (list):
                list of booleans. True if index used, False otherwise.
        """
        self.indexes_used[:] = indexes_used[:]
        
    def get_selected(self):
        """Returns the selected data.

        Returns:
            (tuple[tuple[float], tuple[float]]):
                tuple containing x and y selected data in arrays.
        """
        return self.xdata[self.indexes_used], self.ydata[self.indexes_used]
    
    def get_selected_errors(self):
        """Returns the selected data errors.

        Returns:
            (tuple[tuple[float], tuple[float]]):
                tuple containing x and y selected data errors in arrays.
        """
        return self.xerr[self.indexes_used] if self.xerr is not None else None, self.yerr[self.indexes_used] if self.yerr is not None else None
    
    def get_not_selected(self):
        """Returns the not selected data.

        Returns:
            (tuple[tuple[float], tuple[float]]):
                tuple containing x and y not selected data in arrays.
        """
        return self.xdata[~self.indexes_used], self.ydata[~self.indexes_used]
    
    def get_not_selected_errors(self):
        """Returns the not selected data errors.

        Returns:
            (tuple[tuple[float], tuple[float]]):
                tuple containing x and y not selected data errors in arrays.
        """
        return self.xdata[~self.indexes_used] if self.xerr is not None else None, self.ydata[~self.indexes_used] if self.yerr is not None else None

    def get_colors(self, color_in, color_out):
        """Returns a list of colours depending if same index data is selected or not.

        Parameters:
            color_in (tuple[float,float,float,float]):
                Colour for selected data.
            color_out (tuple[float,float,float,float]):
                Colour for unselected data.

        Returns:
            (tuple[tuple[float,float,float,float]]):
                A list of colours.
        """
        colors = np.zeros((self.length(),4))
        colors[self.indexes_used,:] = color_in[:]
        colors[~self.indexes_used,:] = color_out[:]
        return colors
    
    def copy(self):
        """Creates a copy of the data selection object.

        Returns:
            (DataSelection): A copy of the data selection object.
        """
        instance = DataSelection(self.xdata.copy(), 
                                 self.ydata.copy(), 
                                 self.yerr.copy() if self.yerr is not None else None, 
                                 self.xerr.copy() if self.xerr is not None else None)
        instance.indexes_used = self.indexes_used.copy()
        return instance
        
if __name__=='__main__':
    d = DataSelection(xdata=[0,1,2], ydata=[3,4,5])
    
    assert (d.xdata == np.array([0,1,2])).all()         , "x input error"
    assert (d.ydata == np.array([3,4,5])).all()         , "y input error"
    assert (d.length() == 3)                            , "data length error"
    assert (d.get_data() == np.array([[0,3],
                                      [1,4],
                                      [2,5]])).all()    , "get_data error"
    
    d.selection([0,1])
    c = d.get_colors((0,0,0,1), (1,0,0,0))
    assert (c == [[0.,0.,0.,1.],
                  [0.,0.,0.,1.],
                  [1.,0.,0.,0.]]).all()                 , "get_colors error"
    print("All tests OK")
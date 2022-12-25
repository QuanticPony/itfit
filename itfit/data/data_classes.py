import numpy as np

class DataContainer:
    """Container for data.
    """
    def __init__(self, xdata: list, ydata: list):
        """Creates a DataContainer.

        Parameters:
            xdata (List[float]):
                x data.
            ydata (List[float]):
                y data.
        """
        self.xdata = np.array(xdata).copy()
        self.ydata = np.array(ydata).copy()
        
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
            (Tuple[Tuple[float, float]]):
                Data stored.
        """
        return np.array((self.xdata, self.ydata)).T

        
class DataSelection(DataContainer):
    def __init__(self, xdata, ydata):
        super().__init__(xdata, ydata)
        self.indexes_used = np.ones(len(self.xdata), dtype=bool)
        
    # def __init__(self, data: DataContainer):
    #     self = DataContainer
    #     self.indexes_used = np.ones(len(self.xdata), dtype=bool)
        
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
            indexes (List): 
                List of index.
        """
        self.indexes_used[np.array(indexes)] = True
        
    def selection(self, indexes):
        """Erase previous selected indexes. Adds `indexes` to `indexes_used`.

        Parameters:
            indexes (List):
                List of index.
        """
        self.indexes_used[:] = False
        self.add_selection(indexes)
        
    def bool_selection(self, indexes_used):
        """Erase previous selected indexes. Sets new `indexes_used`.

        Parameters:
            indexes_used (List):
                List of booleans. True if index used, False otherwise.
        """
        self.indexes_used[:] = indexes_used[:]
        
    def get_selected(self):
        """Returns the selected data.

        Returns:
            (Tuple[Tuple[float], Tuple[float]]):
                Tuple containing x and y selected data in arrays.
        """
        return self.xdata[self.indexes_used], self.ydata[self.indexes_used]
    
    def get_not_selected(self):
        """Returns the not selected data.

        Returns:
            (Tuple[Tuple[float], Tuple[float]]):
                Tuple containing x and y not selected data in arrays.
        """
        return self.xdata[~self.indexes_used], self.ydata[~self.indexes_used]

    def get_colors(self, color_in, color_out):
        """Returns a list of colours depending if same index data is selected or not.

        Parameters:
            color_in (Tuple[float,float,float,float]):
                Colour for selected data.
            color_out (Tuple[float,float,float,float]):
                Colour for unselected data.

        Returns:
            (Tuple[Tuple[float,float,float,float]]):
                A list of colours.
        """
        colors = np.zeros((self.length(),4))
        colors[self.indexes_used,:] = color_in[:]
        colors[~self.indexes_used,:] = color_out[:]
        return colors
        
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
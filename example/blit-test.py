import matplotlib
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
import numpy as np
from fitter.utils import DragPointManager, DragPoint, BlitManager, DragLineManager

class fi:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        
f = fi()
BM = BlitManager(f)

a = DragPoint(0.5,0.5, '*')
am = DragPointManager(a, BM)

b = DragPoint(0.3,0.3, 'o')
bm = DragPointManager(b, BM)

c = DragLineManager([a,b], BM)

BM.artists.append(c)
BM.artists.append(am)
BM.artists.append(bm)

plt.show()
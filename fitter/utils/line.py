from matplotlib.patches import CirclePolygon

class DragLine:
    def __init__(self, x, y, *args) -> None:
        self.x = x
        self.y = y
        
        CirclePolygon((self.x, self.y), *args)
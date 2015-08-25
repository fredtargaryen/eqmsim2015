from PyQt4.QtGui import QPainter

class Plotter(QPainter):
    def __init__(self, area, graphof):
        super(Plotter, self).__init__()
        self._GraphArea = area
        self._ShowLabels = False
        if graphof == "Concentration":
            self._finalY = 10
        elif graphof == "Rate":
            self._finalY = 0

    # GETTERS AND SETTERS
    def GetFinalY(self):
        return self._finalY
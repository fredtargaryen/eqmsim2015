from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPainter

class Plotter(QPainter):
    def __init__(self, area):
        super(Plotter, self).__init__()
        self._GraphArea = area
        self._ReactantColour = Qt.red
        self._ProductColour = Qt.blue
        self._ShowLabels = False

    # GETTERS AND SETTERS
    def GetReactantColour(self):
        return self._ReactantColour

    def SetReactantColour(self, color):
        self._ReactantColour = color

    def GetProductColour(self):
        return self._ProductColour

    def SetProductColour(self, color):
        self._ProductColour = color
from PyQt4.QtGui import QWidget, QPen, QPushButton, QPainterPath
from PyQt4.QtCore import Qt, QPointF
from gui.Plotter import Plotter

class GraphWindow(QWidget):
    def __init__(self, reaction):
        super(GraphWindow, self).__init__()
        self.setWindowTitle("Reaction Graph")
        self.setGeometry(600, 400, 240, 300)
        self._graph = QWidget()
        self._plotter = Plotter(self._graph)
        self._reaction = reaction
        self.closebtn = QPushButton("Close", self)
        self.closebtn.setGeometry(80, 270, 80, 30)
        self.closebtn.clicked.connect(self.close)
        self.show()

    def paintEvent(self, e):
        self._plotter.begin(self)
        self.drawGraph(self._plotter, 0.75)
        self._plotter.end()

    def drawGraph(self, plotter, change):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        plotter.setPen(pen)
        plotter.drawLine(20, 20, 20, 220)
        plotter.drawLine(20, 220, 220, 220)
        reactants = self._reaction.GetReactants()
        AverageReactantConc = 0
        for x in range(self._reaction.REACTING_SPECIES_LIMIT):
            AverageReactantConc += reactants[x].GetInitialMoles()
        AverageReactantConc /= (len(reactants) * self._reaction.GetVolume())
        plotter.setPen(QPen(plotter.GetReactantColour(), 2, Qt.SolidLine))
        reactionpath = QPainterPath()
        reactionpath.moveTo(QPointF(20, 20))
        reactionpath.arcTo(20, -70, 300 * change, 180, 180, 90)
        reactionpath.lineTo(220, 110)
        plotter.drawPath(reactionpath)
        plotter.setPen(QPen(plotter.GetProductColour(), 2, Qt.SolidLine))
        productpath = QPainterPath()
        productpath.moveTo(QPointF(20, 220))
        productpath.arcTo(20, 130, 300 * change, 180, 180, -90)
        productpath.lineTo(220, 130)
        plotter.drawPath(productpath)
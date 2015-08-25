from PyQt4.QtGui import QWidget, QPen, QPainterPath, QColor
from PyQt4.QtCore import Qt, QPointF
from gui.Plotter import Plotter


class GraphWindow(QWidget):
    def __init__(self, reaction, graphof, parentwidget, forprinting):
        super(GraphWindow, self).__init__()
        self._graphof = graphof
        self.setWindowTitle(self._graphof + " Graph")
        self._graph = QWidget()
        self._plotter = Plotter(self._graph, graphof)
        self._reaction = reaction
        self.setParent(parentwidget)
        self._forprinting = forprinting
        self._progress = 0

    # Draws the graph. This is not drawn iteratively because all rate
    # and concentration graphs have a very similar shape
    # A rectangle is drawn over the graph, the same colour as the background,
    # and moved away when the animation starts as if the graph is being drawn
    # as the animation plays!
    def paintEvent(self, e):
        self._plotter.begin(self)
        if self._reaction.GetCatalyst().GetUsed():
            change = self._reaction.GetCatalyst().GetEfficacy()
        else:
            change = 1
        eqmpoint = 150/change
        if change > 1:
            eqmpoint -= 0.1 * self._reaction.GetCatalyst().GetInitialMoles()
        elif change < 1:
            eqmpoint += 0.1 * self._reaction.GetCatalyst().GetInitialMoles()
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        self._plotter.setPen(pen)
        self._plotter.drawLine(80, 20, 80, 220)
        self._plotter.drawLine(80, 220, 400, 220)
        self._plotter.setPen(QPen(self._reaction.GetReactantColour()))
        reactionpath = QPainterPath()
        reactionpath.moveTo(QPointF(80, 20))
        reactionpath.arcTo(80, -80 + self._plotter.GetFinalY(), eqmpoint * 2, 200 - (2 * self._plotter.GetFinalY()), 180, 90)
        reactionpath.lineTo(400, 120 - self._plotter.GetFinalY())
        self._plotter.drawPath(reactionpath)
        self._plotter.setPen(QPen(self._reaction.GetProductColour()))
        productpath = QPainterPath()
        productpath.moveTo(QPointF(80, 220))
        productpath.arcTo(80, 120 + self._plotter.GetFinalY(), eqmpoint * 2, 200 - (2 * self._plotter.GetFinalY()), 180, -90)
        productpath.lineTo(400, 120 + self._plotter.GetFinalY())
        self._plotter.drawPath(productpath)
        if not self._forprinting:
            white = QColor(240, 240, 240)
            self._plotter.setPen(QPen(white))
            self._plotter.setBrush(white)
            self._plotter.drawRect(82 + self.parent().GetAnimUpdates() * 0.23, 20, 320, 198)
        self._plotter.setPen(QColor(0, 0, 0))
        self._plotter.drawText(180, 235, "Time")
        self._plotter.drawText(0, 120, self._graphof)
        self._plotter.end()

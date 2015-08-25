from PyQt4.QtCore import Qt, QRectF
from PyQt4.QtGui import QWidget, QPainter, QPushButton, QPen, QPixmap, QFont
from gui.GraphWindow import GraphWindow


class ReactionProfile(QWidget):
    def __init__(self, reaction):
        super(ReactionProfile, self).__init__()
        self._CurrentReaction = reaction
        self.simbtn = QPushButton("Show/hide graph window", self)
        self.simbtn.setGeometry(10, 100, 140, 30)
        self.simbtn.clicked.connect(self.MakeGraph)
        self._GraphWindow = None

    def paintEvent(self, e):
        painter = QPainter()
        reactantside = ""
        productside = ""
        reactantside += self._CurrentReaction.GetReactants()[0].GetFormula()
        for x in range(1, len(self._CurrentReaction.GetReactants())):
            reactant = self._CurrentReaction.GetReactants()[x]
            formula = reactant.GetFormula()
            moles = reactant.GetInitialMoles()
            if moles > 0:
                reactantside += " + "+formula
        productside += self._CurrentReaction.GetProducts()[0].GetFormula()
        for x in range(1, len(self._CurrentReaction.GetProducts())):
            product = self._CurrentReaction.GetProducts()[x]
            formula = product.GetFormula()
            moles = product.GetInitialMoles()
            if moles > 0:
                productside += " + "+formula
        painter.begin(self)
        painter.setFont(QFont("Arial", 20, 50, False))
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawText(376 - (len(reactantside) * 15), 40, reactantside)
        target = QRectF(378, 20, 44, 32)
        arrows = QPixmap("assets/double arrow.png")
        portion = QRectF(10, 0, 44, 32)
        painter.drawPixmap(target, arrows, portion)
        painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        painter.drawText(425, 40, productside)
        painter.end()

    def GetReaction(self):
        return self._CurrentReaction

    def MakeGraph(self):
        self._GraphWindow = GraphWindow(self._CurrentReaction)
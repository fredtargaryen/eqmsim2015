from PyQt4.QtGui import QGridLayout, QPixmap, QLabel, QSpinBox, QDialog, QPushButton
from chem.Reaction import Reaction


class BalanceWindow(QDialog):
    def __init__(self, reaction, window):
        super(BalanceWindow, self).__init__()
        self.setWindowTitle("Balance Equation")
        self._grid = QGridLayout()
        self._numbermenus = []
        self._reactants = []
        self._products = []
        self._boxes = []
        self._formulae = []
        self._symbols = []
        self._themainwindow = window
        # Ensures only valid reactants and products are used
        for x in range(Reaction.REACTING_SPECIES_LIMIT):
            species = reaction.GetReactants()[x]
            if species.GetUsed():
                self._reactants.append(species)
            species = reaction.GetProducts()[x]
            if species.GetUsed():
                self._products.append(species)
        for x in range(len(self._reactants)):
            box = QSpinBox()
            box.setRange(1, 9)
            box.valueChanged.connect(self.update)
            self._boxes.append(box)
            formula = ""
            if self._reactants[x].GetSRatio() > 1:
                formula = self._reactants[x].GetFormulaForLabels()[1:]
            else:
                formula = self._reactants[x].GetFormulaForLabels()
            self._formulae.append(formula)
            self._symbols.append(QLabel())
        for x in range(len(self._products)):
            box = QSpinBox()
            box.setRange(1, 9)
            box.valueChanged.connect(self.update)
            self._boxes.append(box)
            formula = ""
            if self._products[x].GetSRatio() > 1:
                formula = self._products[x].GetFormulaForLabels()[1:]
            else:
                formula = self._products[x].GetFormulaForLabels()
            self._formulae.append(formula)
            self._symbols.append(QLabel())
        for x in range(len(self._reactants)):
            self._grid.addWidget(self._boxes[x], x, 0)
            self._grid.addWidget(QLabel(self._formulae[x]), x, 1)
            self._grid.addWidget(self._symbols[x], x, 2)
        arrows = QLabel()
        arrows.setPixmap(QPixmap("assets/double arrow v.png"))
        self._grid.addWidget(arrows, len(self._reactants), 1)
        for x in range(len(self._products)):
            self._grid.addWidget(self._boxes[x + len(self._reactants)], x + 1 + len(self._reactants), 0)
            self._grid.addWidget(QLabel(self._formulae[x + len(self._reactants)]), x + 1 + len(self._reactants), 1)
            self._grid.addWidget(self._symbols[x + len(self._reactants)], x + 1 + len(self._reactants), 2)
        self._okbtn = QPushButton("OK")
        self._okbtn.clicked.connect(self.close)
        self._grid.addWidget(self._okbtn, len(self._reactants)+len(self._products)+2, 1)
        self.setLayout(self._grid)

    def paintEvent(self, QPaintEvent):
        for x in range(len(self._reactants)):
            if self._boxes[x].value() == self._reactants[x].GetSRatio():
                self._symbols[x].setPixmap(QPixmap("assets/jamie's tick.png"))
            else:
                self._symbols[x].setPixmap(QPixmap("assets/jamie's cross.png"))
        for x in range(len(self._products)):
            if self._boxes[x + len(self._reactants)].value() == self._products[x].GetSRatio():
                self._symbols[x + len(self._reactants)].setPixmap(QPixmap("assets/jamie's tick.png"))
            else:
                self._symbols[x + len(self._reactants)].setPixmap(QPixmap("assets/jamie's cross.png"))

    def close(self):
        self._themainwindow.show()
        super(BalanceWindow, self).close()
from PyQt4.QtGui import QDialog, QGroupBox, QFormLayout, QLineEdit, QLabel, QRadioButton, \
    QGridLayout, QVBoxLayout, QPushButton
from chem.Reaction import Reaction

class ConditionsDialog(QDialog):
    def __init__(self, reaction):
        super(ConditionsDialog, self).__init__()
        self.setGeometry (300 , 300 , 700 , 350)
        self.setWindowTitle ('Edit Conditions')
        if reaction is None:
            self._reaction = Reaction()
        else:
            self._reaction = reaction
        self._CanReturnReaction = False

        # Sets up GUI widgets. Formula boxes will need to support super and subscript somehow
        # Will also need validation later

        # Reactants section
        self._reactantbox = QGroupBox("Reactants", self)
        self._reactantform = QFormLayout()
        self._reactantinfoboxes = []
        self._productinfoboxes = []
        self._catalystinfoboxes = []
        for x in range(Reaction.REACTING_SPECIES_LIMIT):
            self._reactantinfoboxes.append(QLineEdit())
            self._reactantinfoboxes[x*2].setText(self._reaction.GetReactants()[x].GetFormula())
            self._reactantinfoboxes.append(QLineEdit())
            self._reactantinfoboxes[x*2+1].setText(str(self._reaction.GetReactants()[x].GetInitialMoles()))
            self._reactantform.addRow(QLabel(str(x + 1)+".\tFormula:"), self._reactantinfoboxes[x*2])
            self._reactantform.addRow(QLabel("\tInitial Moles:"), self._reactantinfoboxes[x*2+1])
        self._reactantbox.setLayout(self._reactantform)
        # Products section
        self._productbox = QGroupBox("Products", self)
        self._productform = QFormLayout()
        for x in range(Reaction.REACTING_SPECIES_LIMIT):
            self._productinfoboxes.append(QLineEdit())
            self._productinfoboxes[x*2].setText(self._reaction.GetProducts()[x].GetFormula())
            self._productinfoboxes.append(QLineEdit())
            self._productinfoboxes[x*2+1].setText(str(self._reaction.GetProducts()[x].GetInitialMoles()))
            self._productform.addRow(QLabel(str(x + 1)+".\tFormula:"), self._productinfoboxes[x*2])
            self._productform.addRow(QLabel("\tInitial Moles:"), self._productinfoboxes[x*2+1])
        self._productbox.setLayout(self._productform)
        # Catalyst section
        self._catalystbox = QGroupBox("Catalyst", self)
        self._catalystform = QFormLayout()
        self._catalystinfoboxes.append(QLineEdit())
        self._catalystinfoboxes.append(QLineEdit())
        self._catalystinfoboxes.append(QLineEdit())
        self._catalystinfoboxes[0].setText(self._reaction.GetCatalyst().GetFormula())
        self._catalystinfoboxes[1].setText(str(self._reaction.GetCatalyst().GetInitialMoles()))
        self._catalystinfoboxes[2].setText(str(self._reaction.GetCatalyst().GetEaChangePerMole()))
        self._catalystform.addRow(QLabel("Formula:"), self._catalystinfoboxes[0])
        self._catalystform.addRow(QLabel("Moles:"), self._catalystinfoboxes[1])
        self._catalystform.addRow(QLabel("Ea change (per mole):"), self._catalystinfoboxes[2])
        self._catalystbox.setLayout(self._catalystform)
        # Forward heat transfer
        self._heatbox = QGroupBox("Forward heat transfer", self)
        self._heatform = QFormLayout()
        self._endo = QRadioButton("Endothermic")
        self._exo = QRadioButton("Exothermic")
        if self._reaction.GetEndothermic():
            self._endo.setChecked(True)
        else:
            self._exo.setChecked(True)
        self._heatform.addRow(self._endo)
        self._heatform.addRow(self._exo)
        self._heatbox.setLayout(self._heatform)
        # Other conditions section. Includes Vessel volume; Temperature.
        self._otherbox = QGroupBox("Other conditions")
        self._otherform = QFormLayout()
        self._tempbox = QLineEdit()
        self._volbox = QLineEdit()
        self._tempbox.setText(str(self._reaction.GetTemperature()))
        self._volbox.setText(str(self._reaction.GetVolume()))
        self._otherform.addRow(QLabel("Vessel volume:"), self._volbox)
        self._otherform.addRow(QLabel("Temperature:"), self._tempbox)
        self._otherbox.setLayout(self._otherform)
        # OK and Cancel buttons
        self._okbtn = QPushButton("OK")
        self._okbtn.clicked.connect(self.ApplyChanges)
        self._cancelbtn = QPushButton("Cancel")

        self._rightbox = QGroupBox()
        self._rightbox.setFlat(False)
        self._rightform = QVBoxLayout()
        self._rightform.addWidget(self._catalystbox)
        self._rightform.addWidget(self._heatbox)
        self._rightform.addWidget(self._otherbox)
        self._rightbox.setLayout(self._rightform)

        # Layout of all those group boxes
        self._grid = QGridLayout()
        self._grid.addWidget(self._reactantbox, 0, 0)
        self._grid.addWidget(self._productbox, 0, 1)
        self._grid.addWidget(self._rightbox, 0, 2)
        self._grid.addWidget(self._okbtn, 1, 1)
        self._grid.addWidget(self._cancelbtn, 1, 2)
        self.setLayout(self._grid)

        if reaction is None:
            self._reaction = Reaction()
        else:
            self._reaction = reaction

        self._okbtn.clicked.connect(self.close)
        self._cancelbtn.clicked.connect(self.close)
        self.exec_()

    def ApplyChanges(self):
        errorlist = []
        # Validation goes here later
        if len(errorlist) == 0:
            for x in range(Reaction.REACTING_SPECIES_LIMIT):
                self._reaction.GetReactants()[x].SetFormula(self._reactantinfoboxes[x*2].text())
                self._reaction.GetReactants()[x].SetInitialMoles(float(str(self._reactantinfoboxes[x*2+1].text())))
                self._reaction.GetProducts()[x].SetFormula(self._productinfoboxes[x*2].text())
                self._reaction.GetProducts()[x].SetInitialMoles(float(str(self._productinfoboxes[x*2+1].text())))
            self._reaction.GetCatalyst().SetFormula(self._catalystinfoboxes[0].text())
            self._reaction.GetCatalyst().SetInitialMoles(float(str(self._catalystinfoboxes[1].text())))
            self._reaction.GetCatalyst().SetEaChangePerMole(int(str(self._catalystinfoboxes[2].text())))
            self._reaction.SetTemperature(int(self._tempbox.text()))
            self._reaction.SetVolume(float(self._volbox.text()))

    def GetReaction(self):
        if self._CanReturnReaction:
            return self._reaction

    def close(self):
        self._CanReturnReaction = True
        super(ConditionsDialog, self).close()